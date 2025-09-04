import requests
from requests.adapters import HTTPAdapter
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util.retry import Retry

urllib3.disable_warnings(InsecureRequestWarning)

session = requests.Session()
session.verify = False
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def get(base, api_key, path):
    return session.get(
        f"{base}{path}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        verify=False
    ).json()


def orgs(base, api_key):
    return get(base, api_key, "/orgs")


def orgs_iremus(base, api_key):
    return get(base, api_key, "/orgs/iremus")


def workspace(base, api_key, id):
    return get(base, api_key, f"/workspaces/{id}")


def records(base, api_key, doc_id, table_id):
    time.sleep(1)
    return get(base, api_key, f"/docs/{doc_id}/tables/{table_id}/records")


def encode_filter(parameter, value):
    return f"%7B%22{parameter}%22%3A%20%5B%22{value}%22%5D%7D"


def records_by_column(base, api_key, doc_id, table_id, column, value):
    u = f"/docs/{doc_id}/tables/{table_id}/records?filter={encode_filter(column, value)}"
    return get(base, api_key, u)


def put_record(base, api_key, doc_id, table_id, data):
    return session.put(
        f"{base}/docs/{doc_id}/tables/{table_id}/records",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data,
        verify=False
    ).json()


def columns(base, api_key, doc_id, table_id):
    return get(base, api_key, f"/docs/{doc_id}/tables/{table_id}/columns")


def patch_record(base, api_key, doc_id, table_id, data):
    return session.put(
        f"{base}/docs/{doc_id}/tables/{table_id}/records",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data,
        verify=False
    ).json()


def post_attachment(base, api_key, doc_id, f):
    return session.post(
        f"{base}/docs/{doc_id}/attachments",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"upload": f}
    ).json()


def tables(base, api_key, doc_id):
    return get(base, api_key, f"/docs/{doc_id}/tables")
