# coding: utf-8

# ====================================================
# imports
from __future__ import annotations

import pickle
from numbers import Number
from typing import TYPE_CHECKING, Any, Mapping

import numpy as np
import numpy.typing as npt
from h5py import string_dtype

import ch5mpy
from ch5mpy.h5array.array import get_size
from ch5mpy.objects.dataset import Dataset
from ch5mpy.objects.group import File, Group
from ch5mpy.utils import is_sequence

if TYPE_CHECKING:
    from ch5mpy import H5Array


# ====================================================
# code
def _store_dataset(
    loc: Group | File,
    name: str,
    array: npt.NDArray[Any] | H5Array[Any] | None = None,
    shape: tuple[int, ...] | None = None,
    dtype: npt.DTypeLike | None = None,
    chunks: bool | tuple[int, ...] | None = None,
    maxshape: int | tuple[int | None, ...] | None = None,
    fill_value: Any = None,
) -> Dataset[Any]:
    """Store a dataset."""
    if dtype is None:
        if array is not None:
            dtype = array.dtype

    if isinstance(dtype, type):
        str_dtype = str(dtype().dtype)
    else:
        str_dtype = str(dtype)

    if np.issubdtype(dtype, np.str_):
        array = None if array is None else array.astype(object)
        dtype = string_dtype()

    if array is not None:
        if shape is None:
            shape = array.shape

        elif shape != array.shape:
            raise ValueError("array's shape does not match the shape parameter.")

    elif shape is None:
        raise ValueError("At least one of `array` or `shape` must be provided.")

    if chunks:
        if chunks is True:  # literally `True`, not a tuple
            chunks = (get_size(ch5mpy.H5Array.MAX_MEM_USAGE),) + (1,) * (len(shape) - 1)

        if maxshape is None:
            maxshape = (None,) * len(shape)

    dset = loc.create_dataset(
        name,
        data=array,
        shape=shape,
        dtype=dtype,
        chunks=chunks,
        maxshape=maxshape,
        fillvalue=fill_value,
    )
    dset.attrs["dtype"] = str_dtype

    return dset


def write_dataset(
    loc: Group | File,
    name: str,
    obj: Any,
    *,
    chunks: bool | tuple[int, ...] | None = None,
    maxshape: tuple[int, ...] | None = None,
) -> None:
    """Write an array-like object to a H5 dataset."""
    if isinstance(obj, Mapping):
        group = loc.create_group(name)
        write_datasets(group, **obj)
        return

    # cast to np.array if needed (to get shape and dtype)
    array = np.array(obj) if not hasattr(obj, "shape") else obj

    if name in loc.keys():
        if loc[name] is array:
            # this exact dataset is already stored > do nothing
            return

        if loc[name].shape == array.shape and loc[name].dtype == array.dtype:
            # a similar array already exists > simply copy the data
            loc[name][()] = array
            return

        # a different array was stored, delete it before storing the new array
        del loc[name]

    _store_dataset(loc, name, array, chunks=chunks, maxshape=maxshape)


def write_datasets(
    loc: Group | File,
    *,
    chunks: bool | tuple[int, ...] | None = None,
    maxshape: tuple[int, ...] | None = None,
    **kwargs: Any,
) -> None:
    """Write multiple array-like objects to H5 datasets."""
    for name, obj in kwargs.items():
        write_dataset(loc, name, obj, chunks=chunks, maxshape=maxshape)


def write_object(
    loc: Group | File,
    name: str,
    obj: Any,
    *,
    chunks: bool | tuple[int, ...] | None = None,
    maxshape: tuple[int, ...] | None = None,
    overwrite: bool = False,
) -> None:
    """Write any object to a H5 file."""
    if hasattr(obj, "__h5_write__"):
        group = loc.create_group(name, overwrite=overwrite)
        obj.__h5_write__(group=group)
        group.attrs["__h5_type__"] = "object"
        group.attrs["__h5_class__"] = np.void(pickle.dumps(type(obj), protocol=pickle.HIGHEST_PROTOCOL))

    elif isinstance(obj, Mapping):
        group = loc.create_group(name, overwrite=overwrite)
        write_objects(group, **obj, chunks=chunks, maxshape=maxshape)

    elif is_sequence(obj):
        write_dataset(loc, name, obj, chunks=chunks, maxshape=maxshape)

    elif isinstance(obj, (Number, str)):
        if name in loc and overwrite:
            del loc[name]

        loc[name] = obj

    else:
        loc[name] = np.void(pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL))
        loc[name].attrs["__h5_type__"] = "pickle"


def write_objects(
    loc: Group | File,
    *,
    chunks: bool | tuple[int, ...] | None = None,
    maxshape: tuple[int, ...] | None = None,
    overwrite: bool = False,
    **kwargs: Any,
) -> None:
    """Write multiple objects of any type to a H5 file."""
    for name, obj in kwargs.items():
        write_object(loc, name, obj, chunks=chunks, maxshape=maxshape, overwrite=overwrite)
