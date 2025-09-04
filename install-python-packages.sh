python3 -m venv my-venv
./my-venv/bin/pip install lxml rdflib requests pyaml
source ./my-venv/bin/activate
pip3 install --upgrade pip
cd python-packages/sherlock-grist-to-crm && pip3 install -e . && cd ../..
cd python-packages/grist-api-helpers && pip3 install -e . && cd ../..