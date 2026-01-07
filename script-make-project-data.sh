case "$1" in
    "aam")
        uv run grist-table-to-json.py \
            --collection_uuid c583a908-30da-4d05-b0b1-dec8d3401a1e \
            --conf ./conf.iremus.yaml \
            --e13_authors 447b85ae-53c6-4787-8f63-4c9118023c92,4b310d11-24e4-41b6-b8e3-4fa223ff8fae \
            --grist_table_id AAM \
            --makerdfslabelfrom aam::nom,aam::prenom,aam::qualite,aam::residence \
            --project_business_id aam \
            --rdf_type http://www.cidoc-crm.org/cidoc-crm/E73_Information_Object \
        ;;
    # "euterpe-oeuvres")
    #     python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    #         --grist_table_id EUTERPE_OEUVRES \
    #         --project_id euterpe \
    #         --sherlock_collection b77c7bb2-25e7-4003-8d6d-8b12a722c30b \
    #         --output_ttl $OUTPUT_TTL_ROOT/euterpe-oeuvres.ttl \
    #         --rdf_type http://www.cidoc-crm.org/cidoc-crm/E36_Visual_Item \
    #         --e13_authors e6584d49-a83a-4a18-aab7-02ecaa80732b,5d3e1e80-8f04-4a21-a085-f0fd2e1c40aa \
    #     ;;
    # "euterpe-personnes")
    #     python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    #         --grist_table_id EUTERPE_PERSONNES \
    #         --project_id euterpe \
    #         --sherlock_collection 48e1830b-f181-4cc6-8ab2-55cbf621e210 \
    #         --output_ttl $OUTPUT_TTL_ROOT/euterpe-personnes.ttl \
    #         --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \
    #     ;;
    "mg-livraisons")
        uv run grist-table-to-json.py \
            --collection_uuid f252113e-7480-43dd-a48f-0f4d07176eab \
            --conf ./conf.iremus.yaml \
            --e13_authors e6584d49-a83a-4a18-aab7-02ecaa80732b,5d3e1e80-8f04-4a21-a085-f0fd2e1c40aa \
            --grist_table_id MG_LIVRAISONS \
            --project_business_id mercure-galant-tei \
            --p2_has_type http://data-iremus.huma-num.fr/id/901c2bb5-549d-47e9-bd91-7a21d7cbe49f \
            --rdf_type http://iflastandards.info/ns/lrm/lrmoo/F2_Expression \
        ;;
    "mg-articles")
        uv run grist-table-to-json.py \
            --collection_uuid eae9b2e2-5087-43ca-bff0-6b8127a41a60 \
            --conf ./conf.iremus.yaml \
            --e13_authors e6584d49-a83a-4a18-aab7-02ecaa80732b,5d3e1e80-8f04-4a21-a085-f0fd2e1c40aa \
            --grist_table_id MG_ARTICLES \
            --project_business_id mercure-galant-tei \
            --p2_has_type http://data-iremus.huma-num.fr/id/13f43e00-680a-4a6d-a223-48e8d9bbeaae \
            --rdf_type http://iflastandards.info/ns/lrm/lrmoo/F2_Expression \
        ;;
    # "refar-personnes")
    #     python3 -m sherlock_grist_to_crm.grist-to-crm $common_args \
    #         --grist_table_id REFAR_PERSONNES \
    #         --project_id refar-personnes \
    #         --sherlock_collection bb8b4c24-4d9f-4790-a710-511e49e5c6b7 \
    #         --output_ttl $OUTPUT_TTL_ROOT/refar-personnes.ttl \
    #         --e32_uuid 81366968-0fc8-43f6-9a32-9609c19a33c0 \
    #         --rdf_type http://www.cidoc-crm.org/cidoc-crm/E21_Person \
    #     ;;
    *)
        echo "Unknown project code: \"$1\""
        ;;
esac