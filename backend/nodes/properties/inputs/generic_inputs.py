from typing import Dict, List

from .base_input import BaseInput


def DropDownInput(
    input_type: str, label: str, options: List[Dict], optional: bool = False
) -> Dict:
    """Input for a dropdown"""
    return {
        "type": f"dropdown::{input_type}",
        "label": label,
        "options": options,
        "optional": optional,
    }


def TextInput(label: str, has_handle=True, max_length=None, optional=False) -> Dict:
    """Input for arbitrary text"""
    return {
        "type": "text::any",
        "label": label,
        "hasHandle": has_handle,
        "maxLength": max_length,
        "optional": optional,
    }


class NumberInput(BaseInput):
    """Input a number"""

    def __init__(
        self,
        label: str,
        default=0.0,
        minimum=0,
        maximum=None,
        step=1,
        optional=False,
        number_type="any",
    ):
        super().__init__(f"number::{number_type}", label)
        self.default = default
        self.minimum = minimum
        self.maximum = maximum
        self.step = step
        self.optional = optional

    def toDict(self):
        return {
            "type": self.input_type,
            "label": self.label,
            "min": self.minimum,
            "max": self.maximum,
            "def": self.default,
            "step": self.step,
            "hasHandle": True,
            "optional": self.optional,
        }

    def enforce(self, value):
        assert value is not None, "Number does not exist"
        return max(float(self.minimum), float(value))


class IntegerInput(NumberInput):
    """Input an integer number"""

    def __init__(self, label: str):
        super().__init__(label, default=0, minimum=0, maximum=None, step=None)

    def enforce(self, value):
        assert value is not None, "Number does not exist"
        return max(int(self.minimum), int(value))


class BoundedNumberInput(NumberInput):
    """Input for a bounded float number range"""

    def __init__(
        self,
        label: str,
        minimum: float = 0.0,
        maximum: float = 1.0,
        default: float = 0.5,
        step: float = 0.25,
    ):
        super().__init__(
            label, default=default, minimum=minimum, maximum=maximum, step=step
        )

    def enforce(self, value):
        assert value is not None, "Number does not exist"
        return min(max(float(self.minimum), float(value)), float(self.maximum))


class OddIntegerInput(NumberInput):
    """Input for an odd integer number"""

    def __init__(self, label: str, default: int = 1, minimum: int = 1):
        super().__init__(label, default=default, minimum=minimum, maximum=None, step=2)

    def enforce(self, value):
        assert value is not None, "Number does not exist"
        odd = int(value) - (int(value) % 2)
        capped = max(int(self.minimum), odd)
        return capped


class BoundedIntegerInput(NumberInput):
    """Input for a bounded integer number range"""

    def __init__(
        self,
        label: str,
        minimum: int = 0,
        maximum: int = 100,
        default: int = 50,
        optional: bool = False,
    ):
        super().__init__(
            label,
            default=default,
            minimum=minimum,
            maximum=maximum,
            optional=optional,
        )

    def enforce(self, value):
        assert value is not None, "Number does not exist"
        return min(max(int(self.minimum), int(value)), int(self.maximum))


class BoundlessIntegerInput(NumberInput):
    """Input for a boundless integer number"""

    def __init__(
        self,
        label: str,
    ):
        super().__init__(
            label,
            default=0,
            minimum=None,
            maximum=None,
        )

    def enforce(self, value):
        assert value is not None, "Number does not exist"
        return int(value)


class SliderInput(NumberInput):
    """Input for integer number via slider"""

    def __init__(
        self,
        label: str,
        min_val: int,
        max_val: int,
        default: int,
        optional: bool = False,
    ):
        super().__init__(
            label,
            default=default,
            minimum=min_val,
            maximum=max_val,
            step=1,
            optional=optional,
            number_type="slider",
        )

    def enforce(self, value):
        assert value is not None, "Number does not exist"
        return min(max(int(self.minimum), int(value)), int(self.maximum))


def NoteTextAreaInput() -> Dict:
    """Input for note text"""
    return {
        "type": "textarea::note",
        "label": "Note Text",
        "resizable": True,
        "hasHandle": False,
        "optional": True,
    }


def MathOpsDropdown() -> Dict:
    """Input for selecting math operation type from dropdown"""
    return DropDownInput(
        "math-operations",
        "Math Operation",
        [
            {
                "option": "Add (+)",
                "value": "add",
            },
            {
                "option": "Subtract (-)",
                "value": "sub",
            },
            {
                "option": "Multiply (×)",
                "value": "mul",
            },
            {
                "option": "Divide (÷)",
                "value": "div",
            },
            {
                "option": "Exponent/Power (^)",
                "value": "pow",
            },
        ],
    )


def StackOrientationDropdown() -> Dict:
    """Input for selecting stack orientation from dropdown"""
    return DropDownInput(
        "generic",
        "Orientation",
        [
            {
                "option": "Horizontal",
                "value": "horizontal",
            },
            {
                "option": "Vertical",
                "value": "vertical",
            },
        ],
        optional=True,
    )


def IteratorInput() -> Dict:
    """Input for showing that an iterator automatically handles the input"""
    return {
        "type": "iterator::auto",
        "label": "Auto (Iterator)",
        "hasHandle": False,
        "optional": True,
    }


class AlphaFillMethod:
    EXTEND_TEXTURE = 1
    EXTEND_COLOR = 2


def AlphaFillMethodInput() -> Dict:
    """Alpha Fill method option dropdown"""
    return DropDownInput(
        "generic",
        "Fill method",
        [
            {
                "option": "Extend texture",
                "value": AlphaFillMethod.EXTEND_TEXTURE,
            },
            {
                "option": "Extend color",
                "value": AlphaFillMethod.EXTEND_COLOR,
            },
        ],
    )


def VideoTypeDropdown() -> Dict:
    """Video Type option dropdown"""
    return DropDownInput(
        "generic",
        "Video Type",
        [
            {
                "option": "MP4",
                "value": "mp4",
            },
            {
                "option": "AVI",
                "value": "avi",
            },
            {
                "option": "None",
                "value": "none",
            },
        ],
    )
