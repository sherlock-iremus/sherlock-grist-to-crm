import dacite
from dataclasses import dataclass, field, fields, asdict
import json
from pathlib import Path
from typing import Dict

from conf import Conf
import grist_api_helpers


@dataclass
class Cache:
    E35_E55: Dict[str, str] = field(default_factory=dict[str, str])
    E41_E55: Dict[str, str] = field(default_factory=dict[str, str])
    E42_E55: Dict[str, str] = field(default_factory=dict[str, str])
    P3_E55: Dict[str, str] = field(default_factory=dict[str, str])
    P177_E55: Dict[str, str] = field(default_factory=dict[str, str])
    RDF_PROPERTIES: Dict[str, str] = field(default_factory=dict[str, str])
    PROJECTS: Dict[str, str] = field(default_factory=dict[str, str])

    def is_empty(self) -> bool:
        l = 0
        for f in fields(self):
            l += len(self.__getattribute__(f.name))
        return l == 0


class CacheManager:
    def __init__(self, file_path: Path, conf: Conf):
        self.conf = conf
        self.file_path = file_path
        self.cache: Cache = Cache()
        self._load()

    def _load(self) -> None:
        if self.file_path.exists():
            with self.file_path.open("r", encoding="utf-8") as f:
                d = json.load(f)
                self.cache = dacite.from_dict(Cache, d)

        if self.cache.is_empty():
            self.build_cache()

    def save(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(asdict(self.cache), f, indent=4, ensure_ascii=False)

    def build_cache(self) -> None:
        for table_id in [field.name for field in fields(Cache)]:
            grist_data = grist_api_helpers.get(
                self.conf.grist_defaults.base,
                self.conf.grist_defaults.api_key,
                f"/docs/{self.conf.sherlock_data.__getattribute__(table_id).grist_doc_id or self.conf.grist_defaults.doc_id}/tables/{self.conf.sherlock_data.__getattribute__(table_id).grist_table_id}/records"
            )
            for record in grist_data['records']:
                if "Grist_column_code" in record["fields"]:
                    k = record["fields"]["Grist_column_code"].strip()
                    v = record['fields']['UUID'].strip()
                    if k and v:
                        self.cache.__getattribute__(table_id)[k] = v
                elif table_id == "P177_E55":
                    k = record['fields']['project_annotation_id'].strip()
                    v = record['fields']['UUID'].strip()
                    if k and v:
                        self.cache.P177_E55[k] = v
                elif table_id == "RDF_PROPERTIES":
                    k = record['fields']['Prefix'].strip() + ':' + record['fields']['Local_name'].strip()
                    v = record['fields']['URI'].strip()
                    if k and v:
                        self.cache.RDF_PROPERTIES[k] = v
                elif table_id == "PROJECTS":
                    k = record['fields']['E42_business_id'].strip()
                    v = record['fields']['UUID'].strip()
                    if k and v:
                        self.cache.PROJECTS[k] = v
        self.save()