import setuptools
from pathlib import Path
from torchlm import __version__

PATH_ROOT = Path(__file__).parent.resolve()


def get_long_description():
    description = (PATH_ROOT / "README.md").read_text(encoding="utf-8")
    # replace relative repository path to absolute link to the release
    static_url = f"https://github.com/DefTruth/torchlm/blob/main"
    description = description.replace("docs/res/", f"{static_url}/docs/res/")
    return description


setuptools.setup(
    name="torchlm",
    version=__version__,
    author="DefTruth",
    author_email="qyjdef@163.com",
    description="A PyTorch landmarks-only library with 100+ data augmentations, "
                "training and inference, can easily install with pip and compatible "
                "with albumentations and torchvision.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/DefTruth/torchlm",
    packages=setuptools.find_packages(),
    install_requires=[
        "opencv-python>=4.3.0",
        "numpy>=1.14.4",
        "torch>=1.6.0",
        "torchvision>=0.8.0",
        "onnx>=1.8.0",
        "onnxruntime>=1.7.0",
        "tqdm>=4.10.0",
        "hdf5storage>=0.1.18",
        "pandas>=1.2.1",
        "scipy>=1.6.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    include_package_data=True
)
