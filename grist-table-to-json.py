import argparse
from pathlib import Path
from typing import Optional

from cache import CacheManager
from conf import Conf, make_conf
import grist_api_helpers
import DataParser

parser = argparse.ArgumentParser()

parser.add_argument("--conf")

parser.add_argument("--grist_doc_id")
parser.add_argument("--grist_table_id")

parser.add_argument('--e13_authors')
parser.add_argument('--e32_uuid')
parser.add_argument('--makerdfslabelfrom')
parser.add_argument('--p2_has_type')
parser.add_argument('--project_business_id')
parser.add_argument('--rdf_type')
parser.add_argument('--collection_uuid')

args = parser.parse_args()

conf: Conf = make_conf(Path(args.conf))
cache_manager: CacheManager = CacheManager(Path(conf.cache_file), conf)

print('🌲' * 69)
print('🌲', args.grist_table_id)
print('🌲' * 69)

grist_records = grist_api_helpers.get(
    conf.grist_defaults.base,
    conf.grist_defaults.api_key,
    f"/docs/{args.grist_doc_id or conf.grist_defaults.doc_id}/tables/{args.grist_table_id}/records"
)

project_uuid: Optional[str] = None
if args.project_business_id:
    project_uuid = cache_manager.cache.PROJECTS[args.project_business_id]

gdp = DataParser.DataParser(
    cache=cache_manager.cache,
    collection_uuid=args.collection_uuid,
    e13_authors=args.e13_authors.split(',') if args.e13_authors else [],
    e32_uuid=args.e32_uuid,
    records=grist_records["records"],
    makerdfslabelfrom=args.makerdfslabelfrom.split(',') if args.makerdfslabelfrom else [],
    output_ttl=Path(conf.output_ttl_root, args.grist_table_id + '.ttl'),
    p2_has_type=args.p2_has_type,
    project_business_id=args.project_business_id,
    project_uuid=project_uuid,
    rdf_type=args.rdf_type
)

del gdp
