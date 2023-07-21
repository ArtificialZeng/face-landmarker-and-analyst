import argparse  # 导入argparse模块，用于处理命令行参数
import cv2  # 导入cv2模块，用于读取和处理图像
import torchlm  # 导入torchlm库，可能是一个自定义库或者模型
from torchlm.runtime import faceboxesv2_ort, pipnet_ort  # 从torchlm.runtime模块导入了两个名为faceboxesv2_ort和pipnet_ort的类或函数

# 创建一个argparse.ArgumentParser对象
parser = argparse.ArgumentParser(description='Process some integers.')
# 添加一个命令行参数
parser.add_argument('--img', type=str, help='Path of the image to be processed')
# 解析命令行参数
args = parser.parse_args()

# 加载并绑定了人脸检测模型faceboxesv2_ort
torchlm.runtime.bind(faceboxesv2_ort())
# 加载并绑定了人脸关键点检测模型pipnet_ort
torchlm.runtime.bind(
  pipnet_ort(onnx_path="/home/ailab/Downloads/pipnet_resnet18.onnx", num_nb=10,
             num_lms=98, net_stride=32, input_size=256, meanface_type="wflw")
)

# 使用OpenCV的imread函数读取命令行参数指定的图像文件
image = cv2.imread(args.img)
# 将图像数据输入到先前绑定的模型进行前向传播计算，得到检测的面部特征点和边界框
landmarks, bboxes = torchlm.runtime.forward(image)
# 在图像上绘制检测的边界框
image = torchlm.utils.draw_bboxes(image, bboxes=bboxes)
# 在图像上绘制检测的面部特征点
image = torchlm.utils.draw_landmarks(image, landmarks=landmarks)

# 使用OpenCV的imshow函数在一个窗口中显示处理后的图像
cv2.imshow('image', image)
# OpenCV的waitKey函数，参数为0表示无限等待用户键盘输入
cv2.waitKey(0)
# 调用OpenCV的destroyAllWindows函数关闭所有imshow打开的窗口
cv2.destroyAllWindows()
