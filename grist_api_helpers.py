import requests
from typing import Any
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

urllib3.disable_warnings()
session = requests.Session()
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)


def get(base: str, api_key: str, path: str) -> Any:
    print("📡", path)
    return session.get(
        f"{base}{path}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        verify=False
    ).json()


# def orgs(base: str, api_key: str):
#     return get(base, api_key, "/orgs")


# def orgs_iremus(base: str, api_key: str):
#     return get(base, api_key, "/orgs/iremus")


# def workspace(base: str, api_key: str, id: str):
#     return get(base, api_key, f"/workspaces/{id}")


# def records(base: str, api_key: str, doc_id: str, table_id: str) -> Any:
#     time.sleep(0.5)
#     return get(base, api_key, f"/docs/{doc_id}/tables/{table_id}/records")


# def encode_filter(parameter: str, value: str):
#     return f"%7B%22{parameter}%22%3A%20%5B%22{value}%22%5D%7D"


# def records_by_column(base: str, api_key: str, doc_id: str, table_id: str, column: str, value: str):
#     u = f"/docs/{doc_id}/tables/{table_id}/records?filter={encode_filter(column, value)}"
#     return get(base, api_key, u)


# def put_record(base: str, api_key: str, doc_id: str, table_id: str, data: str):
#     return session.put(
#         f"{base}/docs/{doc_id}/tables/{table_id}/records",
#         headers={
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         },
#         json=data,
#         verify=False
#     ).json()


# def columns(base: str, api_key: str, doc_id: str, table_id: str):
#     return get(base, api_key, f"/docs/{doc_id}/tables/{table_id}/columns")


# def patch_record(base: str, api_key: str, doc_id: str, table_id: str, data: Any):
#     return session.put(
#         f"{base}/docs/{doc_id}/tables/{table_id}/records",
#         headers={
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         },
#         json=data,
#         verify=False
#     ).json()


# def post_attachment(base: str, api_key: str, doc_id: str, f):
#     return session.post(
#         f"{base}/docs/{doc_id}/attachments",
#         headers={"Authorization": f"Bearer {api_key}"},
#         files={"upload": f}
#     ).json()


# def tables(base: str, api_key: str, doc_id: str):
#     return get(base, api_key, f"/docs/{doc_id}/tables")
