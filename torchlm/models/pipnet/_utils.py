import numpy as np
from typing import Tuple, List


def _get_meanface(
        meanface_string: str,
        num_nb: int = 10
) -> Tuple[List[int], List[int], List[int], int, int]:
    # 这行定义了一个名为"_get_meanface"的函数，它接收一个名为"meanface_string"的字符串和一个名为"num_nb"的整数作为输入，返回一个包含五个元素的元组。

    """
    :param meanface_string: a long string contains normalized or un-normalized
     meanface coords, the format is "x0,y0,x1,y1,x2,y2,...,xn-1,yn-1".
    :param num_nb: the number of Nearest-neighbor landmarks for NRM, default 10
    :return: meanface_indices, reverse_index1, reverse_index2, max_len
    """

    meanface = meanface_string.strip("\n").strip(" ").split(" ")
    # 这行首先移除了"meanface_string"中的换行符和空格，然后用空格分隔符把字符串分割成多个字符串，然后把这些字符串保存在"meanface"列表中。

    meanface = [float(x) for x in meanface]  # 这行把"meanface"列表中的每个字符串都转换成浮点数。

    meanface = np.array(meanface).reshape(-1, 2) # 这行把"meanface"列表转换成一个numpy数组，然后把这个数组重塑成一个二维数组，其中每行包含两个元素（一个关键点的x和y坐标）。

    meanface_lms = meanface.shape[0] # 这行获取了"meanface"数组的行数，也就是关键点的数量。

    # each landmark predicts num_nb neighbors
    meanface_indices = []
    # 创建一个空列表"meanface_indices"。

    for i in range(meanface.shape[0]):
        pt = meanface[i, :]
        dists = np.sum(np.power(pt - meanface, 2), axis=1)
        indices = np.argsort(dists)
        meanface_indices.append(indices[1:1 + num_nb])
        # 遍历"meanface"数组中的每一行（即每一个关键点），计算这个关键点与所有关键点的距离，然后把这些距离的索引按照从小到大的顺序进行排序，取出前"num_nb"个最近的关键点的索引，然后把这些索引添加到"meanface_indices"列表中。

    # each landmark predicted by X neighbors, X varies
    meanface_indices_reversed = {}
    # 创建一个空字典"meanface_indices_reversed"。

    for i in range(meanface.shape[0]):
        meanface_indices_reversed[i] = [[], []]
    # 为字典中的每个关键点创建两个空列表。

    for i in range(meanface.shape[0]):
        for j in range(num_nb):
            # meanface_indices[i][0,1,2,...,9] -> [[i,i,...,i],[0,1,2,...,9]]
            meanface_indices_reversed[meanface_indices[i][j]][0].append(i)
            meanface_indices_reversed[meanface_indices[i][j]][1].append(j)
            # 遍历"meanface"数组中的每一行（即每一个关键点），对于每一个关键点，遍历它的每一个最近邻关键点，然后把这个关键点的索引和最近邻关键点的索引分别添加到"meanface_indices_reversed"字典中对应的列表中。

    max_len = 0
    # 这行初始化了一个变量"max_len"，并设定其初始值为0。

    for i in range(meanface.shape[0]):
        tmp_len = len(meanface_indices_reversed[i][0])
        if tmp_len > max_len:
            max_len = tmp_len
    # 这几行遍历字典"meanface_indices_reversed"中每个关键点的第一个列表的长度，如果这个长度大于"max_len"，那么就更新"max_len"。

    # tricks, make them have equal length for efficient computation
    for i in range(meanface.shape[0]):
        meanface_indices_reversed[i][0] += meanface_indices_reversed[i][0] * 10
        meanface_indices_reversed[i][1] += meanface_indices_reversed[i][1] * 10
        meanface_indices_reversed[i][0] = meanface_indices_reversed[i][0][:max_len]
        meanface_indices_reversed[i][1] = meanface_indices_reversed[i][1][:max_len]
    # 这几行通过复制和截取的方式，使得字典"meanface_indices_reversed"中的每个列表都有"max_len"个元素。

    # make the indices 1-dim
    # [...,max_len,...,max_len*2,...]
    reverse_index1 = []
    reverse_index2 = []
    # 这几行初始化了两个空列表"reverse_index1"和"reverse_index2"。

    for i in range(meanface.shape[0]):
        reverse_index1 += meanface_indices_reversed[i][0]
        reverse_index2 += meanface_indices_reversed[i][1]
    # 这几行遍历字典"meanface_indices_reversed"中的每个关键点，然后把这个关键点对应的两个列表的元素添加到"reverse_index1"和"reverse_index2"。

    return meanface_indices, reverse_index1, reverse_index2, max_len, meanface_lms
    # 这行返回五个变量："meanface_indices"（每个关键点的最近邻关键点的索引），"reverse_index1"（每个关键点被哪些关键点预测的索引），"reverse_index2"（每个关键点被其他关键点预测时的相对位置），"max_len"（最大的邻近关键点数量），"meanface_lms"（关键点的总数）。



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

