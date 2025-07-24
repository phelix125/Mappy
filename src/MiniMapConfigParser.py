import logging
from typing import Any, Callable

class MiniMapConfigParser:
    SHAPE = 'shape'
    QUADRANT = 'quadrant'
    MIN_SIZE = 'min_size'
    MAX_SIZE = 'max_size'

    def __init__(self, data: dict):
        self.data = data

        self.shape: str = self._parse_config(
            key=self.SHAPE,
            cast=str,
            required=True,
            validate=lambda val: val.lower() in {'circle', 'square'},
            error_msg="shape must be 'circle' or 'square'",
        ).lower()

        self.quadrant: int = self._parse_config(
            key=self.QUADRANT,
            cast=int,
            required=False,
            default=0,
            validate=lambda val: val in {0, 1, 2, 3, 4},
            error_msg="quadrant must be 1–4 or blank",
        )

        self.min_size: int = self._parse_config(
            key=self.MIN_SIZE,
            cast=int,
            required=True,
            validate=lambda val: val >= 0,
            error_msg="min_size must be a positive integer",
        )

        self.max_size: int = self._parse_config(
            key=self.MAX_SIZE,
            cast=int,
            required=True,
            validate=[lambda val: val >= 0 , lambda val: val > self.min_size],
            error_msg=["max_size must be a positive integer",
                       "max_size must be larger then min_size"]
            
        )

    def _parse_config(
        self,
        key: str,
        cast: Callable[[Any], Any],
        required: bool = True,
        default: Any = None,
        validate: Callable[[Any], bool] | list[Callable[[Any], bool]] = lambda x: True,
        error_msg: str | list[str] = "Invalid value" 
    ) -> Any:
        raw_value = self.data.get(key, default)

        if (raw_value is None or raw_value == "") and required:
            raise KeyError(f"Missing required config key: {key}")
        elif raw_value == "" or raw_value is None:
            raw_value = default

        try:
            value = cast(raw_value)
        except (ValueError, TypeError):
            raise ValueError(f"{key}: expected {cast.__name__}, got '{raw_value}'")

        validators = validate if isinstance(validate, (list, tuple)) else [validate]

        for idx,fn in enumerate(validators):
            if not fn(value):
                raise ValueError(f"{key}: {error_msg[idx]}")

        return value

    def get(self, key: str):
        return self.data.get(key)