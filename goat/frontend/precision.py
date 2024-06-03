# type: ignore
from enum import Enum


class Precision(Enum):
    float16 = "float16"
    bfloat16 = "bfloat16"
    float32 = "float32"
    Unknown = "?"

    def from_str(precision):
        if precision in ["torch.float16", "float16"]:
            return Precision.float16
        if precision in ["torch.float32", "float32"]:
            return Precision.float32
        if precision in ["torch.bfloat16", "bfloat16"]:
            return Precision.bfloat16
        return Precision.Unknown
