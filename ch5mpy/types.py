from __future__ import annotations

from typing import runtime_checkable, Protocol, Any, TYPE_CHECKING
from typing_extensions import Self

if TYPE_CHECKING:
    from ch5mpy.dict import H5Dict


@runtime_checkable
class SupportsH5ReadWrite(Protocol):
    def __h5_write__(self, values: H5Dict[Any]) -> None:
        ...

    @classmethod
    def __h5_read__(cls, values: H5Dict[Any]) -> Self:
        ...
