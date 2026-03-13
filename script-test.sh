uv run grist-table-to-json.py \
    --conf ./conf.iremus.yaml \
    --grist_table_id Test \
    --rdf_type http://www.cidoc-crm.org/cidoc-crm/E36_Visual_Item \

echo ''
echo '🌴'
echo ''

sh ~/repositories/sherlock-scripts-prod/graph-replace-sherlock-test.sh