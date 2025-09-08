SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
source $SCRIPT_DIR/../ENV
ROOT="$(dirname "$SCRIPT_DIR")"
source ./venv/bin/activate

BASE_OUTPUT=$OUTPUT_TTL_ROOT/grist/projects
mkdir -p $BASE_OUTPUT

common_args="
--grist_api_key $GRIST_API_KEY
--grist_base $GRIST_BASE
--grist_doc_id $GRIST_DOC_ID
"

case "$1" in
    "aam")
        python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
            --grist_table_id AAM \
            --project_id aam \
            --sherlock_collection c583a908-30da-4d05-b0b1-dec8d3401a1e \
            --output_ttl $BASE_OUTPUT/aam.ttl \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E73_Information_Object \
            --e13_authors 447b85ae-53c6-4787-8f63-4c9118023c92,4b310d11-24e4-41b6-b8e3-4fa223ff8fae \
            --makerdfslabelfrom aam::nom,aam::prenom,aam::qualite \
        ;;
    "euterpe-oeuvres")
        python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
            --grist_table_id EUTERPE_OEUVRES \
            --project_id euterpe \
            --sherlock_collection b77c7bb2-25e7-4003-8d6d-8b12a722c30b \
            --output_ttl $BASE_OUTPUT/euterpe-oeuvres.ttl \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E36_Visual_Item \
            --e13_authors e6584d49-a83a-4a18-aab7-02ecaa80732b,5d3e1e80-8f04-4a21-a085-f0fd2e1c40aa \
        ;;
    "euterpe-personnes")
        python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
            --grist_table_id EUTERPE_PERSONNES \
            --project_id euterpe \
            --sherlock_collection 48e1830b-f181-4cc6-8ab2-55cbf621e210 \
            --output_ttl $BASE_OUTPUT/euterpe-personnes.ttl \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \
        ;;
    "mg-livraisons")
        python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
            --grist_table_id MG_LIVRAISONS \
            --project_id mg-tei \
            --sherlock_collection f252113e-7480-43dd-a48f-0f4d07176eab \
            --output_ttl $BASE_OUTPUT/mg-livraisons.ttl \
            --rdf_type http://iflastandards.info/ns/lrm/lrmoo/F2_Expression \
            --e13_authors e6584d49-a83a-4a18-aab7-02ecaa80732b,5d3e1e80-8f04-4a21-a085-f0fd2e1c40aa \
        ;;
    "refar-personnes")
        python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
            --grist_table_id REFAR_PERSONNES \
            --project_id refar-personnes \
            --output_ttl $BASE_OUTPUT/refar-personnes.ttl \
            --e32_uuid 81366968-0fc8-43f6-9a32-9609c19a33c0 \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \
        ;;
    *)
        echo "Unknown project code: \"$1\""
        ;;
esac