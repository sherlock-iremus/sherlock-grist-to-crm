import argparse
from typing import Dict
from grist_api_helpers import records
from pprint import pprint
from .GristMappingData import MappingDataType, GristMappingData, GristMappingDataCodeToUuid
from .GristDataParser import GristDataParser

print('🌲' * 33)
print('🌲' * 13 + '      📡      ' + '🌲' * 13)
print('🌲' * 33)

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

grist_mapping_data: GristMappingData = GristMappingData()
for x in list(MappingDataType):
    grist_table_id = getattr(args, x.value)
    grist_table_data = records(args.grist_base, args.grist_api_key, args.grist_doc_id, grist_table_id)['records']
    grist_mapping_data[x] = GristMappingDataCodeToUuid()
    match x:
        case MappingDataType.PROJECTS:
            for row in grist_table_data:
                grist_mapping_data[x][row['fields']['E42_business_id'].strip()] = row['fields']['UUID'].strip()
        case MappingDataType.P177_E55:
            for row in grist_table_data:
                grist_mapping_data[x][row['fields']['project_annotation_id'].strip()] = row['fields']['UUID'].strip()
        case MappingDataType.RDF_PROPERTIES:
            for row in grist_table_data:
                grist_mapping_data[x][row['fields']['Prefix'] + ':' + row['fields']['Local_name']] = row['fields']['URI']
        case _:
            for row in grist_table_data:
                grist_mapping_data[x][row['fields']['Grist_column_code'].strip()] = row['fields']['UUID'].strip()

if args.project_id:
    project_uuid = grist_mapping_data[MappingDataType.PROJECTS][args.project_id]
else:
    project_uuid = None

################################################################################
# PARSE DATA
################################################################################

gdp = GristDataParser(
    grist_mapping_data=grist_mapping_data,
    project_id=args.project_id,
    project_uuid=project_uuid,
    output_ttl=args.output_ttl,
    e13_authors=args.e13_authors.split(',') if args.e13_authors else [],
    makerdfslabelfrom=args.makerdfslabelfrom.split(',') if args.makerdfslabelfrom else [],

)
