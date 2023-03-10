# coding: utf-8

# ====================================================
# imports
from __future__ import annotations

import numpy as np
from numbers import Number
from functools import partial
from numpy import _NoValue as NoValue                                                       # type: ignore[attr-defined]

import numpy.typing as npt
from typing import Any
from typing import Iterable
from typing import TYPE_CHECKING

from ch5mpy._typing import NP_FUNC
from ch5mpy.h5array.functions.implement import register
from ch5mpy.h5array.functions.implement import implements
from ch5mpy.h5array.functions.apply import apply

if TYPE_CHECKING:
    from ch5mpy import H5Array


# ====================================================
# code
# ufuncs ----------------------------------------------------------------------
class H5_ufunc:
    def __init__(self,
                 np_ufunc: NP_FUNC):
        self._ufunc = np_ufunc

    def __call__(self,
                 a: H5Array[Any],
                 out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None,
                 *,
                 where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue,
                 dtype: npt.DTypeLike | None = None) -> Any:
        return apply(partial(self._ufunc, dtype=dtype),
                     '__set__',
                     a,
                     out=None if out is None else out[0],
                     dtype=dtype,
                     initial=NoValue,
                     where=where,
                     default_0D_output=False)


_IMPLEMENTED_UFUNCS: tuple[NP_FUNC, ...] = (
    np.sin, np.cos, np.tan,
    np.arcsin, np.arccos, np.arctan,
    np.sinh, np.cosh, np.tanh,
    np.arcsinh, np.arccosh, np.arctanh,
    np.floor, np.ceil, np.trunc,
    np.exp, np.expm1, np.exp2,
    np.log, np.log10, np.log2, np.log1p,
    np.positive, np.negative,
    np.sqrt, np.cbrt,
    np.square,
    np.absolute, np.fabs,
    np.sign
)

for ufunc in _IMPLEMENTED_UFUNCS:
    register(H5_ufunc(ufunc), ufunc)


@implements(np.isfinite)
def isfinite(a: H5Array[Any],
             out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None,
             *,
             where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) -> Any:
    return apply(partial(np.isfinite),
                 '__set__',
                 a,
                 out=None if out is None else out[0],
                 dtype=bool,
                 initial=NoValue,
                 where=where,
                 default_0D_output=False)


@implements(np.isinf)
def isinf(a: H5Array[Any],
          out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None,
          *,
          where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) -> Any:
    return apply(partial(np.isinf),
                 '__set__',
                 a,
                 out=None if out is None else out[0],
                 dtype=bool,
                 initial=NoValue,
                 where=where,
                 default_0D_output=False)


@implements(np.isnan)
def isnan(a: H5Array[Any],
          out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None,
          *,
          where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) -> Any:
    return apply(partial(np.isnan),
                 '__set__',
                 a,
                 out=None if out is None else out[0],
                 dtype=bool,
                 initial=NoValue,
                 where=where,
                 default_0D_output=False)


@implements(np.isneginf)
def isneginf(a: H5Array[Any],
             out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None) -> Any:
    return apply(partial(np.isneginf),
                 '__set__',
                 a,
                 out=None if out is None else out[0],
                 dtype=bool,
                 initial=NoValue,
                 where=NoValue,
                 default_0D_output=False)


@implements(np.isposinf)
def isposinf(a: H5Array[Any],
             out: tuple[H5Array[Any] | npt.NDArray[Any]] | None = None) -> Any:
    return apply(partial(np.isposinf),
                 '__set__',
                 a,
                 out=None if out is None else out[0],
                 dtype=bool,
                 initial=NoValue,
                 where=NoValue,
                 default_0D_output=False)


# numpy functions -------------------------------------------------------------
@implements(np.prod)
def prod(a: H5Array[Any],
         axis: int | Iterable[int] | tuple[int] | None = None,
         dtype: npt.DTypeLike | None = None,
         out: H5Array[Any] | npt.NDArray[Any] | None = None,
         keepdims: bool = False,
         initial: int | float | complex | NoValue = NoValue,
         where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) -> Any:
    initial = 1 if initial is NoValue else initial

    return apply(partial(np.prod, keepdims=keepdims, dtype=dtype, axis=axis), '__imul__', a, out,
                 dtype=dtype, initial=initial, where=where)


@implements(np.sum)
def sum_(a: H5Array[Any],
         axis: int | Iterable[int] | tuple[int] | None = None,
         dtype: npt.DTypeLike | None = None,
         out: H5Array[Any] | npt.NDArray[Any] | None = None,
         keepdims: bool = False,
         initial: int | float | complex | NoValue = NoValue,
         where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) -> Any:
    initial = 0 if initial is NoValue else initial

    return apply(partial(np.sum, keepdims=keepdims, dtype=dtype, axis=axis), '__iadd__', a, out,
                 dtype=dtype, initial=initial, where=where)


@implements(np.amax)
def amax(a: H5Array[Any],
         axis: int | Iterable[Any] | tuple[int] | None = None,
         out: H5Array[Any] | npt.NDArray[Any] | None = None,
         keepdims: bool = False,
         initial: Number | NoValue = NoValue,
         where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) \
        -> npt.NDArray[np.number[Any]] | np.number[Any]:
    return apply(partial(np.amax, keepdims=keepdims, axis=axis), '__set__', a, out,  # type: ignore[no-any-return]
                 dtype=None, initial=initial, where=where)


@implements(np.amin)
def amin(a: H5Array[Any],
         axis: int | Iterable[Any] | tuple[int] | None = None,
         out: H5Array[Any] | npt.NDArray[Any] | None = None,
         keepdims: bool = False,
         initial: Number | NoValue = NoValue,
         where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) \
        -> npt.NDArray[np.number[Any]] | np.number[Any]:
    return apply(partial(np.amin, keepdims=keepdims, axis=axis), '__set__', a, out,  # type: ignore[no-any-return]
                 dtype=None, initial=initial, where=where)


@implements(np.all)
def all_(a: H5Array[Any],
         axis: int | Iterable[Any] | tuple[int] | None = None,
         out: H5Array[Any] | npt.NDArray[Any] | None = None,
         keepdims: bool = False,
         *,
         where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) -> npt.NDArray[Any] | bool:
    return apply(partial(np.all, keepdims=keepdims, axis=axis), '__iand__', a, out,  # type: ignore[no-any-return]
                 dtype=bool, initial=True, where=where)


@implements(np.any)
def any_(a: H5Array[Any],
         axis: int | Iterable[Any] | tuple[int] | None = None,
         out: H5Array[Any] | npt.NDArray[Any] | None = None,
         keepdims: bool = False,
         *,
         where: npt.NDArray[np.bool_] | Iterable[np.bool_] | int | bool | NoValue = NoValue) -> npt.NDArray[Any] | bool:
    return apply(partial(np.any, keepdims=keepdims, axis=axis), '__ior__', a, out,  # type: ignore[no-any-return]
                 dtype=bool, initial=False, where=where)
