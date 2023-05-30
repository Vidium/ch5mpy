from __future__ import annotations

from typing import Any, Collection, Iterator

import numpy.typing as npt

from ..h5g import GroupID
from .attrs import AttributeManager
from .base import HLObject, MutableMappingHDF5
from .dataset import Dataset
from .datatype import Datatype

class Group(HLObject, MutableMappingHDF5[str, "Group" | Dataset | Datatype]):
    def __init__(self, bind: GroupID): ...
    def __delitem__(self, name: str) -> None: ...
    def require_group(self, name: str) -> Group: ...
    def __getitem__(self, name: str | slice | tuple[()]) -> Group | Dataset | Datatype: ...
    def __setitem__(self, name: str, obj: Any) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    @property
    def attrs(self) -> AttributeManager: ...
    def create_group(self, name: str, track_order: bool | None = None) -> Group: ...
    def create_dataset(
        self,
        name: str | None,
        shape: int | tuple[()] | tuple[int | None, ...] | None = None,
        dtype: npt.DTypeLike | None = None,
        data: Collection[Any] | None = None,
        **kwds: Any,
    ) -> Dataset: ...
    @property
    def id(self) -> GroupID: ...
    def move(self, source: str, dest: str) -> None: ...
