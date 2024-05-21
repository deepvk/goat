# type: ignore
from enum import Enum


class Precision(Enum):
    float16 = "float16"
    bfloat16 = "bfloat16"
    qt_8bit = "8bit"
    qt_4bit = "4bit"
    Unknown = "?"

    def from_str(precision):
        if precision in ["torch.float16", "float16"]:
            return Precision.float16
        if precision in ["torch.bfloat16", "bfloat16"]:
            return Precision.bfloat16
        if precision in ["8bit"]:
            return Precision.qt_8bit
        if precision in ["4bit"]:
            return Precision.qt_4bit
        return Precision.Unknown
