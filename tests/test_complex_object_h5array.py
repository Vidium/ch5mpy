# coding: utf-8

# ====================================================
# imports
import pytest
from pathlib import Path

from ch5mpy import File
from ch5mpy import H5Mode
from ch5mpy import H5Array
from ch5mpy import write_object


# ====================================================
# code
class ComplexObject:
    def __init__(self, value: int):
        self.value = value


@pytest.fixture
def co_array() -> H5Array:
    data = [1, 2, 3, 4, 5]

    with File("h5_str_array", H5Mode.WRITE_TRUNCATE) as h5_file:
        write_object(h5_file, "data", data)

    yield H5Array(File("h5_str_array", H5Mode.READ_WRITE)["data"]).maptype(ComplexObject)

    Path("h5_str_array").unlink()


def test_co_array_dtype(co_array):
    assert co_array.dtype == object


def test_co_array_equals(co_array):
    first_element = co_array[0]
    assert isinstance(first_element, ComplexObject) and first_element.value == 1
