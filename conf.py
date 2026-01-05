import dacite
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class SHERLOCK_Table:
    grist_base: str | None
    grist_doc_id: str | None
    grist_table_id: str


@dataclass
class GristDefaults:
    api_key: str
    base: str
    doc_id: str


@dataclass
class SHERLOCK_Tables:
    E35_E55: SHERLOCK_Table
    E41_E55: SHERLOCK_Table
    E42_E55: SHERLOCK_Table
    P3_E55: SHERLOCK_Table
    P177_E55: SHERLOCK_Table
    RDF_PROPERTIES: SHERLOCK_Table
    PROJECTS: SHERLOCK_Table


@dataclass
class Conf:
    cache_file: str
    output_ttl_root: str
    grist_defaults: GristDefaults
    sherlock_data: SHERLOCK_Tables


def make_conf(yaml_conf_file: Path) -> Conf:
    with yaml_conf_file.open("r") as f:
        conf: Conf = dacite.from_dict(Conf, yaml.safe_load(f))
        return conf
