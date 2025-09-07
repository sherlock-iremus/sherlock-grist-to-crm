from dataclasses import dataclass, field
from enum import Enum


class MappingDataType(Enum):
    E35_E55 = 'e35_e55_grist_table_id'
    E41_E55 = 'e41_e55_grist_table_id'
    E42_E55 = 'e42_e55_grist_table_id'
    P3_E55 = 'p3_e55_grist_table_id'
    P177_E55 = 'p177_e55_grist_table_id'
    PROJECTS = 'projects_grist_table_id'
    RDF_PROPERTIES = 'rdf_properties_grist_table_id'


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
