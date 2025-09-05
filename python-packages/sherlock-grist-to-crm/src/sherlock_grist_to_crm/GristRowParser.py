from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef, XSD
import re
import uuid

################################################################################
# CRM MAPPING CONSTANTS
################################################################################

ENTITIES_CODE_TO_CLASS_URI = {
    'E65': CRM.E65_Creation
}

DIRECT_PROPERTIES = {
    'P9_consists_of': 'P9i_forms_part_of',
    'P70_documents': 'P70i_is_documented_in',
    'P94_has_created': 'P94i_was_created_by',
}

INVERSE_PROPERTIES = {
    'P9i_forms_part_of': 'P9_consists_of',
    'P70i_is_documented_in': 'P70_Documents',
    'P94i_was_created_by': 'P94_has_created',
}

################################################################################
# RDF SERIALIZATION CONSTANTS
################################################################################

SHERLOCK_DATA = Namespace("http://data-iremus.huma-num.fr/id/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SHERLOCK = Namespace("http://data-iremus.huma-num.fr/ns/sherlock#")

################################################################################
# HELPERS
################################################################################


def hash_string_to_uuid(string):
    namespace = uuid.NAMESPACE_DNS
    return uuid.uuid5(namespace, string)


def remove_trailing_integers(s):
    return re.sub(r'\d+$', '', s)


def make_graph():
    g = Graph(base=str(SHERLOCK_DATA))
    g.bind("crm", CRM)
    g.bind("sherlock", SHERLOCK)
    return g


def get_entity_uri_by_code(code):
    if code not in ENTITIES_CODE_TO_CLASS_URI:
        raise ValueError(f'Unknown entity code: "{code}"')
    return ENTITIES_CODE_TO_CLASS_URI[code]


def format_crm_property(p):
    if p.startswith('crm:'):
        p = p.replace('crm:', '')
    if not p.startswith(str(CRM)):
        p = CRM[p]
    return p
