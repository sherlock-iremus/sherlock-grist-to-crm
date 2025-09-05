import argparse
from typing import Dict
from grist_api_helpers import records
from pprint import pprint
from .GristMappingData import MappingDataType, GristMappingData, GristMappingDataCodeToUuid

parser = argparse.ArgumentParser()

parser.add_argument('--grist_api_key')
parser.add_argument('--grist_base')
parser.add_argument('--grist_doc_id')
for x in list(MappingDataType):
    parser.add_argument(f"--{x.value}")

parser.add_argument('--e13_authors')
parser.add_argument('--e32_uuid')
parser.add_argument('--grist_table_id')
parser.add_argument('--makerdfslabelfrom')
parser.add_argument('--output_ttl')
parser.add_argument('--p2_has_type')
parser.add_argument('--project_id')
parser.add_argument('--rdf_type')
parser.add_argument('--sherlock_collection')

args = parser.parse_args()

################################################################################
# FETCH GRIST MAPPING DATA
################################################################################

print('🌲🌲🌲🌲🌲 📡 🌲🌲🌲🌲🌲')
GRIST_MAPPING_DATA: GristMappingData = GristMappingData()
for x in list(MappingDataType):
    grist_table_id = getattr(args, x.value)
    grist_table_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, grist_table_id)['records']
    GRIST_MAPPING_DATA[x] = GristMappingDataCodeToUuid()
    match x:
        case MappingDataType.PROJECTS:
            for row in grist_table_data:
                GRIST_MAPPING_DATA[x][row['fields']['E42_business_id'].strip()] = row['fields']['UUID'].strip()
        case MappingDataType.P177_E55:
            for row in grist_table_data:
                GRIST_MAPPING_DATA[x][row['fields']['project_annotation_id'].strip()] = row['fields']['UUID'].strip()
        case MappingDataType.RDF_PROPERTIES:
            for row in grist_table_data:
                GRIST_MAPPING_DATA[x][row['fields']['Prefix'] + ':' + row['fields']['Local_name']] = row['fields']['URI']
        case _:
            for row in grist_table_data:
                GRIST_MAPPING_DATA[x][row['fields']['Grist_column_code'].strip()] = row['fields']['UUID'].strip()

if args.project_id:
    project_uuid = GRIST_MAPPING_DATA[MappingDataType.PROJECTS][args.project_id]
else:
    project_uuid = None

