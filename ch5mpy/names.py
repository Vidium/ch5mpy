# coding: utf-8
# Created on 16/01/2023 11:09
# Author : matteo

# ====================================================
# imports
from __future__ import annotations

from enum import Enum


# ====================================================
# code
class H5Mode(str, Enum):
    READ = "r"  # Readonly, file must exist
    READ_WRITE = "r+"  # Read/write, file must exist
    WRITE_TRUNCATE = "w"  # Create file, truncate if exists
    WRITE = "w-"  # Create file, fail if exists
    READ_WRITE_CREATE = "a"  # Read/write if exists, create otherwise
