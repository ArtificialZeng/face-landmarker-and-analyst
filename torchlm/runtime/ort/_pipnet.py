import os
import cv2
import warnings
import numpy as np
import onnxruntime as ort
from typing import Optional, List

from .._runtime import LandmarksDetBase
from .._runtime import get_meanface, DEFAULT_MEANFACE_STRINGS

__all__ = ["pipnet_ort"]


def _normalize(
        img: np.ndarray
) -> np.ndarray:
    """
    :param img: source image, RGB with HWC and range [0,255]
    :return: normalized image CHW Tensor for PIPNet
    """
    img = img.astype(np.float32)
    img /= 255.
    img[:, :, 0] -= 0.485
    img[:, :, 1] -= 0.456
    img[:, :, 2] -= 0.406
    img[:, :, 0] /= 0.229
    img[:, :, 1] /= 0.224
    img[:, :, 2] /= 0.225
    img = img.transpose((2, 0, 1))  # HWC->CHW
    return img.astype(np.float32)


class _PIPNetORT(LandmarksDetBase):
    # 定义了一个名为"_PIPNetORT"的类，该类继承了"LandmarksDetBase"基类。

    def __init__(
            self,
            onnx_path: str,
            num_nb: int = 10,
            num_lms: int = 68,
            input_size: Optional[int] = 256,
            net_stride: Optional[int] = 32,
            meanface_type: Optional[str] = None
    ):
    # 这是"_PIPNetORT"类的构造函数，定义了类的一些属性和默认值。

        super(_PIPNetORT, self).__init__()
        # 调用父类的构造函数。

        assert os.path.exists(onnx_path)
        # 确保onnx模型的文件路径存在。

        self.onnx_path = onnx_path
        self.num_nb = num_nb
        self.num_lms = num_lms
        self.input_size = input_size
        self.net_stride = net_stride
        # 设置类的属性。

        # setup default meanface
        self.meanface_status = False
        self.meanface_type = meanface_type
        self.meanface_indices: List[List[int]] = [[]]
        self.reverse_index1: List[int] = []
        self.reverse_index2: List[int] = []
        self.max_len: int = -1
        # 设置默认的平均面部关键点。

        self._set_default_meanface()
        # 调用方法设置默认的平均面部关键点。

        # ORT settings
        self.providers = ort.get_available_providers()
        self.device = ort.get_device()
        self.session = ort.InferenceSession(
            self.onnx_path,
            providers=self.providers
        )
        # 设置ORT的设定，获取可用的设备和设置推断会话。

        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape
        self.output_names = [x.name for x in self.session.get_outputs()]
        self.output_shapes = [x.shape for x in self.session.get_outputs()]
        # 获取输入和输出的名字和形状。

        print(f"PIPNetORT Running Device: {self.device},"
              f" Available Providers: {self.providers}\n"
              f"Model Loaded From: {self.onnx_path}\n"
              f"Input Name: {self.input_name},"
              f" Input Shape: {self.input_shape}"
              f" Output Names: {self.output_names},"
              f" Output Shapes: {self.output_shapes}")
              # 打印有关设备、提供者、模型路径、输入输出名字和形状的信息。


    def set_custom_meanface(
    def set_custom_meanface(
            self,
            custom_meanface_file_or_string: str
    ) -> bool:
    # 定义一个函数"set_custom_meanface"，这个函数接收一个参数custom_meanface_file_or_string，它可能是一个文件路径或者一个字符串。

        """
        :param custom_meanface_file_or_string: a long string or a file contains normalized
        or un-normalized meanface coords, the format is "x0,y0,x1,y1,x2,y2,...,xn-1,yn-1".
        :return: status, True if successful.
        """
        # 这部分是函数的文档字符串，对函数的参数和返回值进行了解释。

        try:
            custom_meanface_type = "custom"
            # 设置自定义面部关键点的类型为"custom"。

            if os.path.isfile(custom_meanface_file_or_string):
                with open(custom_meanface_file_or_string) as f:
                    custom_meanface_string = f.readlines()[0]
            else:
                custom_meanface_string = custom_meanface_file_or_string
            # 检查参数custom_meanface_file_or_string是否为文件，如果是文件，就读取文件的第一行，否则直接使用输入的字符串。

            custom_meanface_indices, custom_reverse_index1, \
            custom_reverse_index2, custom_max_len, custom_meanface_lms = get_meanface(
                meanface_string=custom_meanface_string, num_nb=self.num_nb)
            # 调用get_meanface函数，获取面部关键点的信息。

            # check landmarks number
            if custom_meanface_lms != self.num_lms:
                warnings.warn(
                    f"custom_meanface_lms != self.num_lms, "
                    f"{custom_meanface_lms} != {self.num_lms}"
                    f"So, we will skip this setup for PIPNet meanface."
                    f"Please check and setup meanface carefully before"
                    f"running PIPNet ..."
                )
                # 如果自定义的面部关键点数量与预期不符，发出警告。

                self.meanface_type = custom_meanface_type
                self.meanface_indices = custom_meanface_indices
                self.reverse_index1 = custom_reverse_index1
                self.reverse_index2 = custom_reverse_index2
                self.max_len = custom_max_len
                # 更新 num_lms
                self.num_lms = custom_meanface_lms
                self.meanface_status = True
            else:
                # 如果自定义的面部关键点数量与预期相符，进行下列操作。

                # replace if successful
                self.meanface_type = custom_meanface_type
                self.meanface_indices = custom_meanface_indices
                self.reverse_index1 = custom_reverse_index1
                self.reverse_index2 = custom_reverse_index2
                self.max_len = custom_max_len
                self.meanface_status = True
            # 在不抛出异常的情况下，更新类的属性。

        except:
            self.meanface_status = False
            # 如果在尝试执行以上代码时发生任何错误，把meanface_status设置为False。

        return self.meanface_status
        # 返回meanface_status的值，如果设置自定义面部关键点成功，返回True，否则返回False。


    def _set_default_meanface(self):
        if self.meanface_type is not None:
            if self.meanface_type.upper() not in DEFAULT_MEANFACE_STRINGS:
                warnings.warn(
                    f"Can not found default dataset: {self.meanface_type.upper()}!"
                    f"So, we will skip this setup for PIPNet meanface."
                    f"Please check and setup meanface carefully before"
                    f"running PIPNet ..."
                )
                self.meanface_status = False
            else:
                meanface_string = DEFAULT_MEANFACE_STRINGS[self.meanface_type.upper()]
                meanface_indices, reverse_index1, reverse_index2, max_len, meanface_lms = \
                    get_meanface(meanface_string=meanface_string, num_nb=self.num_nb)
                # check landmarks number
                if meanface_lms != self.num_lms:
                    warnings.warn(
                        f"meanface_lms != self.num_lms, {meanface_lms} != {self.num_lms}"
                        f"So, we will skip this setup for PIPNet meanface."
                        f"Please check and setup meanface carefully before"
                        f"running PIPNet ..."
                    )
                    self.meanface_status = False
                else:
                    self.meanface_indices = meanface_indices
                    self.reverse_index1 = reverse_index1
                    self.reverse_index2 = reverse_index2
                    self.max_len = max_len

                    self.meanface_status = True

    def apply_detecting(self, image: np.ndarray) -> np.ndarray:
        height, width, _ = image.shape
        image = cv2.resize(image, (self.input_size, self.input_size))  # 256, 256
        image = np.expand_dims(_normalize(image), axis=0)  # 1xCHW
        # (1,68,8,8) (1,68,8,8) (1,68,8,8) (1,68*10,8,8) (1,68*10,8,8)
        outputs_cls, outputs_x, outputs_y, outputs_nb_x, outputs_nb_y = self.session.run(
            output_names=self.output_names,
            input_feed={self.input_name: image}
        )
        batch = outputs_cls.shape[0]
        grid_h, grid_w = outputs_cls.shape[2:]  # 8, 8
        assert batch == 1

        outputs_cls = np.reshape(outputs_cls, (self.num_lms, -1))  # (68,64)
        max_ids = np.argmax(outputs_cls, axis=1)  # (68,)
        max_ids_nb = np.tile(max_ids.reshape(-1, 1), reps=[1, self.num_nb]).flatten()  # (68*10,)

        outputs_x = np.reshape(outputs_x, (self.num_lms, -1))  # (68,64)
        outputs_x_select = outputs_x[np.arange(self.num_lms), max_ids]  # (68,)
        outputs_y = np.reshape(outputs_y, (self.num_lms, -1))  # (68,64)
        outputs_y_select = outputs_y[np.arange(self.num_lms), max_ids]  # (68,)

        outputs_nb_x = np.reshape(outputs_nb_x, (self.num_lms * self.num_nb, -1))  # (68*10,64)
        outputs_nb_x_select = outputs_nb_x[np.arange(self.num_lms * self.num_nb), max_ids_nb]  # (68*10,)
        outputs_nb_x_select = np.reshape(outputs_nb_x_select, (-1, self.num_nb))  # (68,10)
        outputs_nb_y = np.reshape(outputs_nb_y, (self.num_lms * self.num_nb, -1))  # (68*10,64)
        outputs_nb_y_select = outputs_nb_y[np.arange(self.num_lms * self.num_nb), max_ids_nb]  # (68*10,)
        outputs_nb_y_select = np.reshape(outputs_nb_y_select, (-1, self.num_nb))  # (68,10)

        # grid_w=grid_h=8 max_ids->[0,63] calculate grid center (cx,cy) in 8x8 map
        lms_pred_x = max_ids % grid_w + outputs_x_select  # x=cx+offset_x (68,)
        lms_pred_y = max_ids // grid_w + outputs_y_select  # y=cy+offset_y (68,)
        lms_pred_x /= 1.0 * self.input_size / self.net_stride  # normalize coord (x*32)/256
        lms_pred_y /= 1.0 * self.input_size / self.net_stride  # normalize coord (y*32)/256

        lms_pred_nb_x = np.reshape((max_ids % grid_w), (-1, 1)) + outputs_nb_x_select  # (68,10)
        lms_pred_nb_y = np.reshape((max_ids // grid_w), (-1, 1)) + outputs_nb_y_select  # (68,10)
        lms_pred_nb_x /= 1.0 * self.input_size / self.net_stride  # normalize coord (nx*32)/256
        lms_pred_nb_y /= 1.0 * self.input_size / self.net_stride  # normalize coord (ny*32)/256

        # merge predictions
        tmp_nb_x = lms_pred_nb_x[self.reverse_index1, self.reverse_index2].reshape(self.num_lms, self.max_len)
        tmp_nb_y = lms_pred_nb_y[self.reverse_index1, self.reverse_index2].reshape(self.num_lms, self.max_len)
        tmp_x = np.mean(np.concatenate([lms_pred_x.reshape(-1, 1), tmp_nb_x], axis=1), axis=1, keepdims=True)  # (68,1)
        tmp_y = np.mean(np.concatenate([lms_pred_y.reshape(-1, 1), tmp_nb_y], axis=1), axis=1, keepdims=True)  # (68,1)
        lms_pred_merge = np.concatenate([tmp_x, tmp_y], axis=1)  # (68,2)

        # de-normalize
        lms_pred_merge[:, 0] *= float(width)  # e.g 256
        lms_pred_merge[:, 1] *= float(height)  # e.g 256

        return lms_pred_merge


# Export Alias
pipnet_ort = _PIPNetORT
