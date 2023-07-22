import os
from _typeshed import BytesPath, FileDescriptorOrPath, StrPath, SupportsRichComparisonT
from collections.abc import Sequence
from typing import overload
from typing_extensions import Literal, LiteralString

__all__ = [
    "commonprefix",
    "exists",
    "getatime",
    "getctime",
    "getmtime",
    "getsize",
    "isdir",
    "isfile",
    "samefile",
    "sameopenfile",
    "samestat",
]

# All overloads can return empty string. Ideally, Literal[""] would be a valid
# Iterable[T], so that list[T] | Literal[""] could be used as a return
# type. But because this only works when T is str, we need Sequence[T] instead.
@overload
def commonprefix(m: Sequence[LiteralString]) -> LiteralString: ...
@overload
def commonprefix(m: Sequence[StrPath]) -> str: ...
@overload
def commonprefix(m: Sequence[BytesPath]) -> bytes | Literal[""]: ...
@overload  #一个装饰器，用于表示以下的函数或方法具有多个方法来处理不同类型或数量的输入参数。
def commonprefix(m: Sequence[list[SupportsRichComparisonT]]) -> Sequence[SupportsRichComparisonT]: ...
@overload  # Decorator indicating the function below can handle different types/number of arguments.
def commonprefix(m: Sequence[tuple[SupportsRichComparisonT, ...]]) -> Sequence[SupportsRichComparisonT]: ...  # Function declaration of 'commonprefix', which takes a sequence of tuples (with elements of type 'SupportsRichComparisonT') as input, and returns a sequence of 'SupportsRichComparisonT'.
#函数声明，函数名为commonprefix，它接收一个名为m的参数，参数类型为一个元组的序列（元组中的元素类型为SupportsRichComparisonT，这可能是一个占位符或者自定义的类型，表示支持丰富的比较操作，如等于、大于、小于等），并返回一个SupportsRichComparisonT元素组成的序列。
def exists(path: FileDescriptorOrPath) -> bool: ...  # Function declaration of 'exists', which takes a 'FileDescriptorOrPath' as input and returns a boolean indicating whether the path exists.
#函数声明，函数名为exists，它接收一个名为path的参数，参数类型为FileDescriptorOrPath（这可能是一个占位符或者自定义的类型，表示文件描述符或路径），并返回一个布尔值。
def getsize(filename: FileDescriptorOrPath) -> int: ...  # Function declaration of 'getsize', which takes a 'FileDescriptorOrPath' as input and returns an integer representing the size of the file.
#一个函数声明，函数名为getsize，它接收一个名为filename的参数，参数类型为FileDescriptorOrPath，并返回一个整数。
def isfile(path: FileDescriptorOrPath) -> bool: ...  # Function declaration of 'isfile', which takes a 'FileDescriptorOrPath' as input and returns a boolean indicating whether the path is a file.
#一个函数声明，函数名为isfile，它接收一个名为path的参数，参数类型为FileDescriptorOrPath，并返回一个布尔值。
def isdir(s: FileDescriptorOrPath) -> bool: ...  # Function declaration of 'isdir', which takes a 'FileDescriptorOrPath' as input and returns a boolean indicating whether the path is a directory.
#这是一个函数声明，函数名为isdir，它接收一个名为s的参数，参数类型为FileDescriptorOrPath，并返回一个布尔值。

# These return float if os.stat_float_times() == True,
# but int is a subclass of float.
def getatime(filename: FileDescriptorOrPath) -> float: ...
def getmtime(filename: FileDescriptorOrPath) -> float: ...
def getctime(filename: FileDescriptorOrPath) -> float: ...
def samefile(f1: FileDescriptorOrPath, f2: FileDescriptorOrPath) -> bool: ...
def sameopenfile(fp1: int, fp2: int) -> bool: ...
def samestat(s1: os.stat_result, s2: os.stat_result) -> bool: ...
