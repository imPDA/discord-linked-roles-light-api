from __future__ import annotations

import re
from enum import Enum, auto
from typing import Optional

from pydantic import BaseModel, Field, validator


class MetadataType(Enum):
    INTEGER_LESS_THAN_OR_EQUAL = 1
    INTEGER_GREATER_THAN_OR_EQUAL = 2
    INTEGER_EQUAL = 3
    INTEGER_NOT_EQUAL = 4
    DATETIME_LESS_THAN_OR_EQUAL = 5
    DATETIME_GREATER_THAN_OR_EQUAL = 6
    BOOLEAN_EQUAL = 7
    BOOLEAN_NOT_EQUAL = 8

    def __repr__(self):
        return str(self.value)


KEY_PATTERN = re.compile(r'[a-z0-9_]*')


class Metadata(BaseModel):
    platform_name: str = Field(max_length=50)
    platform_username: Optional[str] = Field(max_length=100)

    def __init__(self, **data):
        for field_name, field in data.items():
            if type(field) != self.__fields__[field_name].type_ and field_name not in ['platform_name', 'platform_username']:
                data[field_name] = self.__fields__[field_name].type_(key=data[field_name])
        super().__init__(**data)

    def to_payload(self) -> dict:
        return self.json(exclude_none=True)

    @classmethod
    def to_schema(cls) -> list[dict]:
        fields = []
        for field_name, field in cls.__fields__.items():
            if field_name not in ['platform_name', 'platform_username']:
                fields.append({k: v.default for k, v in field.type_.__fields__.items() if v.default is not None})
        return fields

    def __setattr__(self, key, value):
        if not (field := self.__fields__.get(key)):
            raise KeyError(f"No such a field ({key})")

        if field.type_ != type(value) and key not in ['platform_name', 'platform_username']:
            print(field.type_, type(value))
            super().__setattr__(key, field.type_(key=value))
        else:
            super().__setattr__(key, value)


class MetadataField(BaseModel):
    type: MetadataType
    key: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    name_localizations: Optional[dict]
    description: str = Field(min_length=1, max_length=200)
    description_localization: Optional[dict]

    @validator('key')
    def must_contain_only_these_symbols(cls, v):  # noqa
        if not KEY_PATTERN.fullmatch(v):
            raise ValueError("must be a-z, 0-9, or _ characters")
        return v

    @property
    def to_tuple(self) -> tuple[str, str]:
        return self.name, self.key

    def dict(self, **kwargs):
        return self.key
