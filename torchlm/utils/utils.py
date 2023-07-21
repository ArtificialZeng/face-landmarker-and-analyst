import cv2
import numpy as np
from typing import Tuple, Optional

__all__ = [
    "draw_bboxes",
    "draw_landmarks"
]


def draw_bboxes(img: np.ndarray, bboxes: np.ndarray) -> np.ndarray:
    im = img[:, :, :].copy()  # 创建输入图像的副本
    bboxes = bboxes[:, :4]  # 获取bboxes的前四个值，通常分别对应于左上角和右下角的坐标
    bboxes = bboxes.reshape(-1, 4)  # 重新调整bboxes的形状，每个边界框有四个值
    for box in bboxes:  # 遍历每个边界框
        im = cv2.rectangle(im, (int(box[0]), int(box[1])),
                           (int(box[2]), int(box[3])), (0, 255, 0), 2)  # 使用cv2.rectangle在图像上绘制矩形，颜色是绿色，线条宽度为2
    return im.astype(np.uint8)  # 将图像的数据类型转换为uint8并返回
'''
for box in bboxes: 这一行遍历输入的边界框数组 bboxes。这个数组的每个元素都是一个边界框，通常表示为一个四元素的数组，包括边界框的左上角和右下角的 (x, y) 坐标。

im = cv2.rectangle(im, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2) 这一行使用 cv2.rectangle 函数在图像 im 上绘制一个矩形，这个矩形就是边界框。这个函数的参数包括：

im：输入图像，我们在这个图像上绘制矩形。

(int(box[0]), int(box[1]))：矩形左上角的 (x, y) 坐标。

(int(box[2]), int(box[3]))：矩形右下角的 (x, y) 坐标。

(0, 255, 0)：矩形的颜色，这里是绿色。在 OpenCV 中，颜色通常表示为 (B, G, R) 的三元组，每个元素的范围是 0 到 255。这里，绿色的三元组是 (0, 255, 0)。

2：矩形的线宽，这里是 2 像素。

return im.astype(np.uint8) 这一行返回绘制了矩形的图像。.astype(np.uint8) 是把图像的数据类型转换为无符号 8 位整型，这是最常用的图像数据类型。'''

def draw_landmarks(
        img: np.ndarray,  #这是输入的图像，它应该是一个numpy数组。
        landmarks: np.ndarray,  #是需要绘制的关键点的坐标，它也是一个numpy数组。通常每一个关键点包含两个坐标（x, y）。
        font: float = 0.25,   #这是绘制关键点标号时使用的字体大小，它的默认值是0.25。
        circle: int = 2,  #用来绘制关键点的圆的半径，它的默认值是2。
        text: bool = False,  #这个参数决定是否在每个关键点旁边绘制对应的编号。默认情况下，这个参数是False，也就是说不绘制关键点的编号。
        color: Optional[Tuple[int, int, int]] = (0, 255, 0),  #这是用来绘制关键点和关键点编号的颜色，它是一个包含三个元素的元组，分别表示RGB颜色的红、绿、蓝三个通道。默认情况下，这个颜色是绿色。
        offset: int = 5,  #这是关键点编号相对于关键点的偏移量，它的默认值是5。
        thickness: int = 1  #这是绘制关键点编号时使用的线的粗细，它的默认值是1。
) -> np.ndarray:
    im = img.astype(np.uint8).copy()  # 创建输入图像的副本，并将其数据类型转换为uint8
    if landmarks.ndim == 2:  # 如果landmarks的维度是2
        landmarks = np.expand_dims(landmarks, axis=0)  # 在axis=0的位置增加一个维度
    for i in range(landmarks.shape[0]):  # 遍历landmarks的第一维度，这个循环是对landmarks中的每一个关键点组进行循环。landmarks的shape[0]返回关键点组的数量，每一组关键点可以理解为对应一张图像的所有关键点。
        for j in range(landmarks[i].shape[0]):  # 遍历landmarks的第二维度，这个内部循环是对给定关键点组内的每一个关键点进行循环。
            x, y = landmarks[i, j, :].astype(int).tolist()  # 获取关键点的坐标，并转换为列表，从当前的关键点组中获取单个关键点的坐标，并转换为整数类型。
            cv2.circle(im, (x, y), circle, color, -1)  # 使用cv2.circle在图像上绘制圆形，表示关键点
            #在图像上以给定的坐标(x, y)为中心，以给定的半径(circle)绘制一个颜色为color的实心圆（因为最后一个参数是-1，表示实心）。
            if text:  # 如果需要在关键点旁边绘制文本，这是一个条件语句，当text为True时，才会执行下面的代码，也就是在每个关键点旁边添加标签。
                b = np.random.randint(0, 255)  # 生成随机颜色 这三行代码生成了一个随机的RGB颜色，这个颜色将用于绘制关键点的编号。
                g = np.random.randint(0, 255)
                r = np.random.randint(0, 255)
                cv2.putText(im, '{}'.format(i), (x, y - offset), cv2.FONT_ITALIC, font, (b, g, r), thickness)  # 使用cv2.putText在图像上绘制文本
    return im.astype(np.uint8)  # 将图像的数据类型转换为uint8并返回

'''
im：在这里输入的图像，我们希望在这个图像上添加文本。

'{}'.format(i)：这是我们要添加的文本。在这里，我们添加的文本是变量 i 的字符串形式。

(x, y - offset)：这是我们要添加文本的位置。在这里，我们把文本放在由变量 x 和 y - offset 给出的位置。这里的 offset 用于调整文本相对于关键点的位置。

cv2.FONT_ITALIC：这是我们要使用的字体。在这里，我们选择的是斜体字。

font：这是我们要使用的字体大小。

(b, g, r)：这是我们要使用的字体颜色。在这里，我们使用的颜色是由随机生成的变量 b, g 和 r 给出的。

thickness：这是我们要使用的线条粗细。在这里，我们使用的是变量 thickness 定义的粗细。

总的来说，这行代码在图像 im 的 (x, y - offset) 位置添加一个颜色为 (b, g, r)、大小为 font、粗细为 thickness 的 i 文本。'''

