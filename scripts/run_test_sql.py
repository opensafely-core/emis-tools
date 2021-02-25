import os
from getpass import getpass
import prestodb
from requests import Session
from requests_pkcs12 import Pkcs12Adapter

conn = prestodb.dbapi.connect(
    host="providerplus.emishealthinsights.co.uk",
    port=443,
    user=os.environ["USER"],
    catalog="hive",
    schema="extract_oxford_datalabs",
    http_scheme="https",
)

if "CERTIFICATE_PASSWORD_PATH" in os.environ:
    with open(os.environ["CERTIFICATE_PASSWORD_PATH"], "rb") as f:
        pkcs12_password = f.read().strip()
else:
    pkcs12_password = getpass()

session = Session()
session.mount(
    "https://providerplus.emishealthinsights.co.uk:443",
    Pkcs12Adapter(
        pkcs12_filename=os.environ["CERTIFICATE_PATH"],
        pkcs12_password=pkcs12_password
    ),
)
session.verify = False
conn._http_session = session
cursor = conn.cursor()
cursor.execute("select 123")
print(cursor.fetchall())
