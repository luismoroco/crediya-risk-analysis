import json
from dataclasses import fields, is_dataclass
from decimal import Decimal
from typing import Any, Type, TypeVar, get_args, get_origin

T = TypeVar("T", bound="BaseModel")


class BaseModel:

    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
        kwargs = {}
        for f in fields(cls):
            if f.name not in data:
                continue
            value = data[f.name]
            f_type = f.type

            if f_type is Decimal and value is not None:
                value = Decimal(str(value))

            elif is_dataclass(f_type) and isinstance(value, dict):
                value = f_type.from_dict(value)

            elif get_origin(f_type) is list and isinstance(value, list):
                inner_type = get_args(f_type)[0]
                if is_dataclass(inner_type):
                    value = [inner_type.from_dict(v) for v in value]
                else:
                    value = [inner_type(v) for v in value]

            kwargs[f.name] = value

        return cls(**kwargs)

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        return cls.from_dict(json.loads(json_str))
