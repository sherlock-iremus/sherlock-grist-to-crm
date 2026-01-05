import dacite
from dataclasses import dataclass, field, fields, asdict
from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef, XSD
import re
from typing import Any, List, Optional
import uuid

from cache import Cache

SEP = ' ❄️  '

################################################################################
# RDF SERIALIZATION CONSTANTS
################################################################################

SHERLOCK_DATA = Namespace("http://data-iremus.huma-num.fr/id/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
LRMOO = Namespace('http://iflastandards.info/ns/lrm/lrmoo/')
SHERLOCK = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

################################################################################
# CRM MAPPING CONSTANTS
################################################################################

DIRECT_PROPERTIES = {
    'P9_consists_of': 'P9i_forms_part_of',
    'P70_documents': 'P70i_is_documented_in',
    'P94_has_created': 'P94i_was_created_by',
}

INVERSE_PROPERTIES = {v: k for k, v in DIRECT_PROPERTIES.items()}

ENTITIES_CODE_TO_CLASS_URI = {
    'E65': CRM.E65_Creation
}

################################################################################
# HELPERS
################################################################################


def hash_string_to_uuid(string: str):
    namespace = uuid.NAMESPACE_DNS
    return uuid.uuid5(namespace, string)


def remove_trailing_integers(s: str):
    return re.sub(r'\d+$', '', s)


def make_graph():
    g = Graph(base=str(SHERLOCK_DATA))
    g.bind("crm", CRM)
    g.bind("lrmoo", LRMOO)
    g.bind("sherlock", SHERLOCK)
    return g


def get_entity_uri_by_code(code: str):
    if code not in ENTITIES_CODE_TO_CLASS_URI:
        raise ValueError(f'Unknown entity code: "{code}"')
    return ENTITIES_CODE_TO_CLASS_URI[code]


def format_crm_property(p: str) -> URIRef:
    if p.startswith('crm:'):
        p = p.replace('crm:', '')
    if not p.startswith(str(CRM)):
        p = CRM[p]
    return URIRef(p)


@dataclass
class Record:
    id: int | str
    fields: dict[str, Any]

################################################################################
# CLASS
################################################################################


class DataParser:

    def __init__(
        self,
        cache: Cache,
        collection_uuid: Optional[str],
        e13_authors: Optional[List[str]],
        e32_uuid: Optional[str],
        records: list[Record],
        makerdfslabelfrom: Optional[List[str]],
        output_ttl: Path,
        p2_has_type: Optional[str],
        project_business_id: Optional[str],
        project_uuid: Optional[str],
        rdf_type: str,
    ):

        if e13_authors:
            self.e13_authors = [URIRef(x) for x in e13_authors]
        self.e32_uuid = e32_uuid
        self.cache = cache
        self.makerdfslabelfrom = makerdfslabelfrom
        self.output_ttl = output_ttl
        self.p2_has_type = p2_has_type
        self.project_business_id = project_business_id
        self.project_uuid = project_uuid
        self.rdf_type = rdf_type
        self.collection_uuid = collection_uuid

        self.rdf_properties_prefixes: set[str] = set()
        for x in cache.RDF_PROPERTIES.keys():
            self.rdf_properties_prefixes.add(x.split(':')[0])
        self.graph = make_graph()
        self.unknown_E35_id: set[str] = set()
        self.unknown_E41_id: set[str] = set()
        self.unknown_E42_id: set[str] = set()
        self.processed_column_names: set[str] = set()
        self.unprocessed_column_names: set[str] = set()

        self.records = [dacite.from_dict(Record, r) for r in records]
        print(f"📦 {len(self.records)} records fetched.")
        self.process_records()

    def __del__(self):
        self.log()
        self.graph.serialize(destination=self.output_ttl, encoding='utf-8')

    def log(self):
        print('💾 MAKING TTL DATA IN      :', self.output_ttl)
        print('👾 UNKNOWN E35 ID          :', SEP.join((self.unknown_E35_id)))
        print('👾 UNKNOWN E41 ID          :', SEP.join((self.unknown_E41_id)))
        print('👾 UNKNOWN E42 ID          :', SEP.join((self.unknown_E42_id)))
        print('🔴 UNPROCESSED COLUMN NAMES:', SEP.join(sorted(self.unprocessed_column_names)))
        print('🟢 PROCESSED COLUMN NAMES  :', SEP.join(sorted(self.processed_column_names)))
        print('')

    def process_records(self):
        for record in self.records:
            if 'UUID' in record.fields.keys() and record.fields['UUID']:
                subject = SHERLOCK_DATA[record.fields['UUID']]
            else:
                continue

            if self.rdf_type:
                self.graph.add((subject, RDF.type, URIRef(self.rdf_type)))

            if self.p2_has_type:
                types = self.p2_has_type.split(',')
                for x in types:
                    self.graph.add((subject, CRM.P2_has_type, URIRef(x)))

            if self.collection_uuid:
                self.graph.add((URIRef(self.collection_uuid), SHERLOCK.has_member, subject))

            if self.e32_uuid:
                self.graph.add((SHERLOCK_DATA[self.e32_uuid], CRM.P71_lists, subject))

            if self.project_uuid:
                self.graph.add((subject, SHERLOCK['has_context_project'], SHERLOCK_DATA[self.project_uuid]))

            for column_name, column_value in record.fields.items():
                self.process_cell(subject, column_name, column_value)

    def process_cell(self, subject: URIRef, column_name: str, column_value: str):
        if not column_value:
            column_value = ''
        else:
            column_value = str(column_value).strip()
        column_name = column_name.strip()
        if column_value:
            column_value = column_value.strip()
        if not column_value:
            return False

        # How many parts?
        column_names_parts = column_name.split('___')

        matched = False

        # We have a predicate! (or a predicate that points to a lesser CRM entity)
        if len(column_names_parts) == 1:
            # First we check if it's a RDF property
            rdf_property_uri = self.get_rdf_property_uri(column_name)
            if rdf_property_uri:
                self.graph.add((subject, URIRef(rdf_property_uri), Literal(column_value)))
                matched = True
            else:
                if re.match('P1_', column_name):
                    self.graph.add((subject, CRM.P1_is_identified_by, Literal(column_value)))
                    matched = True
                elif re.match('P102_', column_name):
                    self.graph.add((subject, CRM.P102_has_title, Literal(column_value)))
                    matched = True
                elif re.match('P82aP82b', column_name):
                    self.make_E52(subject, column_value)
                    matched = True
                elif re.match('P3_.*', column_name):
                    self.make_P3(subject, column_value, self.cache.P3_E55[remove_trailing_integers(column_name.replace('P3_', ''))])
                    matched = True
                elif re.match('E42_.*', column_name):
                    E42_type = remove_trailing_integers(column_name.replace('E42_', ''))
                    if E42_type in self.cache.E42_E55:
                        self.make_E42(subject, column_value, self.cache.E42_E55[E42_type])
                        matched = True
                    else:
                        self.unknown_E42_id.add(E42_type)
                elif re.match('E35_.*', column_name):
                    E35_type = remove_trailing_integers(column_name.replace('E35_', ''))
                    if E35_type in self.cache.E35_E55:
                        self.make_E35(subject, column_value, self.cache.E35_E55[E35_type])
                        matched = True
                    else:
                        self.unknown_E35_id.add(E35_type)
                elif re.match('E41_.*', column_name):
                    E41_type = remove_trailing_integers(column_name.replace('E41_', ''))
                    if E41_type in self.cache.E41_E55:
                        self.make_E41(subject, column_value, self.cache.E41_E55[E41_type])
                        matched = True
                    else:
                        self.unknown_E41_id.add(E41_type)
                elif column_name == 'sherlock__has_context_project':
                    self.graph.add((subject, SHERLOCK.has_context_project, SHERLOCK_DATA[column_value]))
                    matched = True
                elif column_name.startswith('E13_'):
                    x = column_name.replace('E13_', '')
                    annotation_type_uuid = self.cache.P177_E55[x.replace('__', '::')]
                    self.make_E13_with_literal_P141(subject, annotation_type_uuid, column_value)
                    # rdfs:label
                    if self.makerdfslabelfrom and x.replace('__', '::') in self.makerdfslabelfrom:
                        current_rdfs_label_value = self.graph.value(subject=subject, predicate=RDFS.label)
                        if current_rdfs_label_value:
                            self.graph.remove((subject, RDFS.label, Literal(current_rdfs_label_value)))
                        else:
                            current_rdfs_label_value = ''
                        new_rdfs_label: str = SEP.join(filter(lambda x: x, [current_rdfs_label_value, column_value]))
                        self.graph.add((subject, RDFS.label, Literal(new_rdfs_label)))
                    matched = True
                elif column_name == 'R5i_is_component_of':
                    self.graph.add((subject, LRMOO.R5i_is_component_of, URIRef(column_value)))
                    self.graph.add((URIRef(column_value), LRMOO.R5_has_component, subject))
                    matched = True
                elif column_value != '0':
                    if column_name in DIRECT_PROPERTIES.keys():
                        self.graph.add((subject, format_crm_property(column_name), URIRef(column_value)))
                        self.graph.add((URIRef(column_value), format_crm_property(DIRECT_PROPERTIES[column_name]), subject))
                        matched = True
                    elif column_name in INVERSE_PROPERTIES.keys():
                        self.graph.add((subject, format_crm_property(column_name), URIRef(column_value)))
                        self.graph.add((URIRef(column_value), format_crm_property(INVERSE_PROPERTIES[column_name]), subject))
                        matched = True
        if len(column_names_parts) == 3:
            # Properties creation
            p1 = column_names_parts[0]
            p1i = ''
            p2 = column_names_parts[2]
            p2i = ''
            if p1 in DIRECT_PROPERTIES:
                p1i = DIRECT_PROPERTIES[p1]
            elif p1 in INVERSE_PROPERTIES:
                p1i = INVERSE_PROPERTIES[p1]
            if p2 in DIRECT_PROPERTIES:
                p2i = DIRECT_PROPERTIES[p2]
            elif p2 in INVERSE_PROPERTIES:
                p2i = INVERSE_PROPERTIES[p2]
            # Medium entity creation
            medium_entity_class_resource = get_entity_uri_by_code(column_names_parts[1])
            medium_entity_resource = URIRef(str(uuid.uuid4()))
            self.graph.add((medium_entity_resource, RDF.type, medium_entity_class_resource))
            # Weaving
            self.graph.add((subject, format_crm_property(p1), medium_entity_resource))
            self.graph.add((medium_entity_resource, format_crm_property(p1i), subject))
            self.graph.add((medium_entity_resource, format_crm_property(p2), URIRef(column_value)))
            self.graph.add((URIRef(column_value), format_crm_property(p2i), medium_entity_resource))
            matched = True
        if matched == False and column_name != 'UUID':
            self.unprocessed_column_names.add(column_name)
        else:
            self.processed_column_names.add(column_name)

    def make_E52(self, subject: URIRef, P82aP82b_column_value: str):
        E52 = URIRef(str(uuid.uuid4()))
        self.graph.add((subject, CRM['P4_has_time-span'], E52))
        self.graph.add((E52, CRM.P82a_begin_of_the_begin, Literal(P82aP82b_column_value, datatype=XSD.dateTime)))
        self.graph.add((E52, CRM.P82b_end_of_the_end, Literal(P82aP82b_column_value, datatype=XSD.dateTime)))

    def make_P3(self, subject: URIRef, column_value: str, P3_type: str):
        pc = URIRef(str(uuid.uuid4()))
        self.graph.add((pc, RDF.type, CRM.PC3_has_note))
        self.graph.add((pc, CRM.P01_has_domain, subject))
        self.graph.add((pc, CRM.P03_has_range_literal, Literal(column_value)))
        self.graph.add((pc, CRM['P3.1_has_type'], SHERLOCK_DATA[P3_type]))

    def make_E42(self, subject: URIRef, column_value: URIRef | str, E42_type: str):
        if not column_value:
            return
        E42 = URIRef(str(uuid.uuid4()))
        self.graph.add((subject, CRM.P1_is_identified_by, E42))
        self.graph.add((E42, RDF.type, CRM.E42_Identifier))
        self.graph.add((E42, CRM.P2_has_type, SHERLOCK_DATA[E42_type]))
        if column_value.startswith('http'):
            self.graph.add((E42, CRM.P190_has_symbolic_content, URIRef(column_value)))
        else:
            self.graph.add((E42, CRM.P190_has_symbolic_content, Literal(column_value)))

    def make_E35(self, subject: URIRef, column_value: str, E35_type: str):
        E35 = URIRef(str(uuid.uuid4()))
        self.graph.add((subject, CRM.P102_has_title, E35))
        self.graph.add((E35, RDF.type, CRM.E35_Title))
        self.graph.add((E35, CRM.P2_has_type, SHERLOCK_DATA[E35_type]))
        if column_value.startswith('http'):
            self.graph.add((E35, CRM.P190_has_symbolic_content, URIRef(column_value)))
        else:
            self.graph.add((E35, CRM.P190_has_symbolic_content, Literal(column_value)))

    def make_E41(self, subject: URIRef, column_value: URIRef | str, E41_type: str):
        E41 = URIRef(str(uuid.uuid4()))
        self.graph.add((subject, CRM.P1_is_identified_by, E41))
        self.graph.add((E41, RDF.type, CRM.E41_Appellation))
        self.graph.add((E41, CRM.P2_has_type, SHERLOCK_DATA[E41_type]))
        if column_value.startswith('http'):
            self.graph.add((E41, CRM.P190_has_symbolic_content, URIRef(column_value)))
        else:
            self.graph.add((E41, CRM.P190_has_symbolic_content, Literal(column_value)))

    def make_E13_with_literal_P141(self, P140: URIRef, P177: str, P141: str):
        E13 = URIRef(str(uuid.uuid4()))
        self.graph.add((E13, RDF.type, CRM.E13_Attribute_Assignment))
        self.graph.add((E13, CRM.P140_assigned_attribute_to, P140))
        self.graph.add((E13, CRM.P177_assigned_property_of_type, URIRef(P177)))
        self.graph.add((E13, CRM.P141_assigned, Literal(P141)))
        for e13_author in self.e13_authors:
            self.graph.add((E13, CRM.P14_carried_out_by, e13_author))
        if self.project_uuid:
            self.graph.add((E13, SHERLOCK.has_context_project, SHERLOCK_DATA[self.project_uuid]))

    def get_rdf_property_uri(self, column_name: str) -> Optional[str]:
        if column_name.startswith('E13_'):
            column_name = column_name.replace('E13_', '')
        match = re.search(r"(.+)__(.+?)(?=(_[0-9]+)?$)", column_name)
        if match:
            prefix = match.group(1)
            if prefix == 'sherlock':
                return None
            localName = match.group(2)
            qualified_name = prefix + ':' + localName
            return self.cache.RDF_PROPERTIES[qualified_name] if qualified_name in self.cache.RDF_PROPERTIES else None
        return None
