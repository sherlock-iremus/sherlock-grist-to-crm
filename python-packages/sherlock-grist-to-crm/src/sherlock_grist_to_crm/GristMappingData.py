from dataclasses import dataclass, field
from enum import Enum


class MappingDataType(Enum):
    E35_E55 = 'E35_E55'
    E41_E55 = 'E41_E55'
    E42_E55 = 'E42_E55'
    P3_E55 = 'P3_E55'
    P177_E55 = 'P177_E55'
    PROJECTS = 'PROJECTS'
    RDF_PROPERTIES = 'RDF_PROPERTIES'


class GristMappingDataCodeToUuid(dict[str, str]):
    def __setitem__(self, key: str, value: str):
        if not isinstance(key, str):
            raise TypeError(f"Key must be str, got {type(key).__name__}")
        if not isinstance(value, str):
            raise TypeError(f"Value must be str, got {type(value).__name__}")
        super().__setitem__(key, value)


class GristMappingData(dict[MappingDataType, GristMappingDataCodeToUuid]):
    def __setitem__(self, key: MappingDataType, value: GristMappingDataCodeToUuid):
        if not isinstance(key, MappingDataType):
            raise TypeError(f"Key must be {MappingDataType.__name__}, got {type(key).__name__}")
        if not isinstance(value, GristMappingDataCodeToUuid):
            raise TypeError(f"Value must be {GristMappingDataCodeToUuid.__name__}, got {type(value).__name__}")
        super().__setitem__(key, value)
