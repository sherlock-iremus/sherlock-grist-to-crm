SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SCRIPT_DIR/../ENV
ROOT="$(dirname "$SCRIPT_DIR")"

rm -rf $ROOT/out/ttl/grist/sherlock
mkdir -p $ROOT/out/ttl/grist/sherlock

source ./venv/bin/activate

common_args="
--grist_api_key $GRIST_API_KEY
--grist_base $GRIST_BASE
--grist_doc_id $GRIST_DOC_ID
--e35_e55_grist_table_id $E35_E55_GRIST_TABLE_ID
--e41_e55_grist_table_id $E41_E55_GRIST_TABLE_ID
--e42_e55_grist_table_id $E42_E55_GRIST_TABLE_ID
--p3_e55_grist_table_id $P3_E55_GRIST_TABLE_ID
--p177_e55_grist_table_id $P177_E55_GRIST_TABLE_ID
--rdf_properties_grist_table_id $RDF_PROPERTIES_GRIST_TABLE_ID
--projects_grist_table_id $PROJECTS_GRIST_TABLE_ID
"

# E21 Personnes
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_PERSONNES \
    --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-PERSONNES.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \

# # Projets
# python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
#     --grist_table_id SHERLOCK_PROJETS \
#     --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-PROJECTS.ttl \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E7_Activity \
#     --p2_has_type http://data-iremus.huma-num.fr/id/58c38fd3-ca35-476a-aa39-9cc815ee2dab \

# # Collections
# python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
#     --grist_table_id SHERLOCK_COLLECTIONS \
#     --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-COLLECTIONS.ttl \
#     --rdf_type http://data-iremus.huma-num.fr/ns/sherlock#Collection \

# # Fichiers des projets
# python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
#     --grist_table_id SHERLOCK_PROJETS_FICHIERS \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E31_Document \
#     --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-PROJECTS-FILES.ttl \

# # E35 E55
# python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
#     --grist_table_id SHERLOCK_E35 \
#     --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E35-E55.ttl \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    
# # E41 E55
# python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
#     --grist_table_id SHERLOCK_E41 \
#     --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E41-E55.ttl \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    
# # E42 E55
# python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
#     --grist_table_id SHERLOCK_E42 \
#     --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E42-E55.ttl \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    
# # P3 E55
# python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
#     --grist_table_id SHERLOCK_P3 \
#     --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-P3-E55.ttl \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    
# # P177 E55
# python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
#     --grist_table_id SHERLOCK_E13 \
#     --e32_uuid 3abbb495-7105-4066-89fe-9d4b0474e492 \
#     --output_ttl $ROOT/out/ttl/grist/sherlock/SHERLOCK-E13-E55.ttl \
#     --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \