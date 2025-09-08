SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SCRIPT_DIR/../ENV
ROOT="$(dirname "$SCRIPT_DIR")"
source ./venv/bin/activate

BASE_OUTPUT=$OUTPUT_TTL_ROOT/grist/sherlock
rm -rf $BASE_OUTPUT
mkdir -p $BASE_OUTPUT

common_args="
--grist_api_key $GRIST_API_KEY
--grist_base $GRIST_BASE
--grist_doc_id $GRIST_DOC_ID
"

# E21 Personnes
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_PERSONS \
    --output_ttl $BASE_OUTPUT/SHERLOCK-PERSONS.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \

# Projets
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_PROJECTS \
    --output_ttl $BASE_OUTPUT/SHERLOCK-PROJECTS.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E7_Activity \
    --p2_has_type http://data-iremus.huma-num.fr/id/58c38fd3-ca35-476a-aa39-9cc815ee2dab \

# Collections
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_COLLECTIONS \
    --output_ttl $BASE_OUTPUT/SHERLOCK-COLLECTIONS.ttl \
    --rdf_type http://data-iremus.huma-num.fr/ns/sherlock#Collection \

# Fichiers des projets
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_PROJECTS_FILES \
    --output_ttl $BASE_OUTPUT/SHERLOCK-PROJECTS-FILES.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E31_Document \

# E35 E55
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_E35_E55 \
    --output_ttl $BASE_OUTPUT/SHERLOCK-E35-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    
# E41 E55
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_E41_E55 \
    --output_ttl $BASE_OUTPUT/SHERLOCK-E41-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    
# E42 E55
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_E42_E55 \
    --output_ttl $BASE_OUTPUT/SHERLOCK-E42-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    
# P3 E55
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --grist_table_id SHERLOCK_P3_E55 \
    --output_ttl $BASE_OUTPUT/SHERLOCK-P3-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \
    
# P177 E55
python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    --e32_uuid 3abbb495-7105-4066-89fe-9d4b0474e492 \
    --grist_table_id SHERLOCK_P177_E55 \
    --output_ttl $BASE_OUTPUT/SHERLOCK-E13-E55.ttl \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \