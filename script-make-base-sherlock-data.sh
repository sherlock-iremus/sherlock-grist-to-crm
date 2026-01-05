# E21 Personnes
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_PERSONS \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \

# Projects
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_PROJECTS \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E7_Activity \
    --p2_has_type http://data-iremus.huma-num.fr/id/58c38fd3-ca35-476a-aa39-9cc815ee2dab \

# Projects Files
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_PROJECTS_FILES \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E31_Document \
    --p2_has_type 66ee2b5c-7d83-43d2-9d6e-d3a4d8443570 \


# Collections
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_COLLECTIONS \
    --rdf_type http://data-iremus.huma-num.fr/ns/sherlock#Collection \

# E55
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_E55 \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \

# E35 E55
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_E35_E55 \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \

# E41 E55
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_E41_E55 \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \

# E42 E55
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_E42_E55 \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \

# P3 E55
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id SHERLOCK_P3_E55 \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \

# P177 E55
uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --e32_uuid 3abbb495-7105-4066-89fe-9d4b0474e492 \
    --grist_table_id SHERLOCK_P177_E55 \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E55_Type \