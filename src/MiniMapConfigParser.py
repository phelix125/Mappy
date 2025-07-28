import logging
import json
from typing import Any, Callable
from src.Constants import MINIMAP_CONFIG_FILE_PATH
class MiniMapConfigParser:
    X = 'X'
    Y = 'Y'
    WIDTH = 'WIDTH'
    HEIGHT = 'HEIGHT'

    def __init__(self, data: dict):
        self.data = data

        self.X: str = self._parse_config(
            key=self.X,
            cast=int,
            required=True,
            validate=lambda val: val >= 0,
            error_msg="Value must be greated then 0",
        )
        self.Y: str = self._parse_config(
            key=self.Y,
            cast=int,
            required=True,
            validate=lambda val: val >= 0,
            error_msg="Value must be greated then 0",
        )
        self.WIDTH: str = self._parse_config(
            key=self.WIDTH,
            cast=int,
            required=True,
            validate=lambda val: val >= 0,
            error_msg="Value must be greated then 0",
        )
        self.HEIGHT: str = self._parse_config(
            key=self.HEIGHT,
            cast=int,
            required=True,
            validate=lambda val: val >= 0,
            error_msg="Value must be greated then 0",
        )
    def overide_data(self, data):
        self.data = data
        self._save_dict_to_json()

    def _save_dict_to_json(self) -> None:
        with open(MINIMAP_CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
            
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