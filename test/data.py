from torchlm.data import LandmarksWFLWConverter
from torchlm.data import Landmarks300WConverter
from torchlm.data import LandmarksCOFWConverter
from torchlm.data import LandmarksAFLWConverter

def test_wflw_converter():  # 定义函数test_wflw_converter，可能用于测试LandmarksWFLWConverter类的功能
    converter = LandmarksWFLWConverter(  # 创建LandmarksWFLWConverter类的实例，命名为converter
        data_dir="../data/WFLW",  # 设定原始数据所在的文件夹
        save_dir="../data/WFLW/converted",  # 设定转换后的数据要保存的文件夹
        extend=0.2,  # 可能设定扩展标记区域的比例
        rebuild=True,  # 如果已经存在转换后的数据，也重新生成
        target_size=256,  # 设定转换后的图像的期望大小
        keep_aspect=False,  # 在转换过程中不保留原始图像的长宽比
        force_normalize=True,  # 在转换过程中进行数据归一化
        force_absolute_path=True  # 在处理文件路径时，转为绝对路径
    )  # 结束类实例的创建
    converter.convert()  # 调用converter的convert方法，根据前面设置的参数来对数据进行转换
    converter.show(count=30)  # 调用converter的show方法，并设置参数count为30，显示前30个转换后的数据
    
#这些注释是基于函数名和参数名的推断，可能并不完全准确，因为我们没有LandmarksWFLWConverter类的具体实现。

def test_300w_converter():
    converter = Landmarks300WConverter(
        data_dir="../data/300W",
        save_dir="../data/300W/converted",
        extend=0.2,
        rebuild=True,
        target_size=256,
        keep_aspect=False,
        force_normalize=True,
        force_absolute_path=True
    )
    converter.convert()

    converter.show(count=30)


def test_cofw_converter():
    converter = LandmarksCOFWConverter(
        data_dir="../data/COFW",
        save_dir="../data/COFW/converted",
        extend=0.2,
        rebuild=True,
        target_size=256,
        keep_aspect=False,
        force_normalize=True,
        force_absolute_path=True
    )
    converter.convert()

    converter.show(count=30)

def test_aflw_converter():
    converter = LandmarksAFLWConverter(
        data_dir="../data/AFLW",
        save_dir="../data/AFLW/converted",
        extend=0.2,
        rebuild=True,
        target_size=256,
        keep_aspect=False,
        force_normalize=True,
        force_absolute_path=True
    )
    converter.convert()

    converter.show(count=10)

if __name__ == "__main__":
    test_wflw_converter()
    test_300w_converter()
    test_cofw_converter()
    test_aflw_converter()
    """
    python3 ./data.py
    """
