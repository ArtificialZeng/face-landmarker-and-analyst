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
'''
torchlm.runtime.bind: 这是一个方法用于将模型绑定到一个运行时环境。根据名称推测，torchlm可能是一个库或者模块，runtime可能是关于运行时的一个模块，bind可能是一个将模型绑定到运行时的函数。

pipnet_ort: 这个应该是一个模型类的实例，可能表示一个采用ONNX格式的预训练模型。

onnx_path="/home/ailab/Downloads/pipnet_resnet18.onnx": 这个参数表示ONNX模型文件的路径。

num_nb=10: 这个参数可能表示邻接点的数量。在关键点检测任务中，可能表示每个关键点周围的邻接点的数量。

num_lms=98: 这个参数可能表示模型需要检测的关键点的数量。在此模型中，它需要检测98个关键点。

net_stride=32: 这个参数可能表示模型在进行卷积操作时的步长。步长决定了卷积窗口在输入矩阵上移动的速度。

input_size=256: 这个参数表示模型输入图像的大小。在这里，输入图像的大小是256x256。

meanface_type="wflw": 这个参数可能表示预处理输入图像时使用的平均脸的类型。"wflw"可能是一个具体的平均脸类型。'''

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
