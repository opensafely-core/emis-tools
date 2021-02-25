import os

import prestodb
import urllib3
from requests import Session
from requests_pkcs12 import Pkcs12Adapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def get_conn():
    conn = prestodb.dbapi.connect(
        host="directoraccess-cert.emishealthinsights.co.uk",
        port=443,
        user=os.environ["USER"],
        catalog="hive",
        schema="extract_oxford_datalabs",
        http_scheme="https",
    )

    with open(os.environ["PFX_PASSWORD_PATH"], "rb") as f:
        pkcs12_password = f.read().strip()

    session = Session()
    session.mount(
        "https://directoraccess-cert.emishealthinsights.co.uk:443",
        Pkcs12Adapter(
            pkcs12_filename=os.environ["PFX_PATH"],
            pkcs12_password=pkcs12_password,
        ),
    )
    session.verify = False
    conn._http_session = session
    return ConnectionProxy(conn)



class ConnectionProxy:
    """Proxy for prestodb.dbapi.Connection, with a more useful cursor."""

    def __init__(self, connection):
        self.connection = connection

    def __getattr__(self, attr):
        """Pass any unhandled attribute lookups to proxied connection."""

        return getattr(self.connection, attr)

    def cursor(self):
        """Return a proxied cursor."""

        return CursorProxy(self.connection.cursor())


class CursorProxy:
    """Proxy for prestodb.dbapi.Cursor.

    Unlike prestodb.dbapi.Cursor:

    * any exceptions caused by an invalid query are raised by .execute() (and
      not later when you fetch the results)
    * the .description attribute is set immediately after calling .execute()
    * you can iterate over it to yield rows
    * .fetchone()/.fetchmany()/.fetchall() are disabled (they are not currently
      used by EMISBackend, although they could be implemented if required)
    """

    _rows = None

    def __init__(self, cursor, batch_size=10 ** 6):
        """Initialise proxy.

        cursor: the presto.dbapi.Cursor to be proxied
        batch_size: the number of records to fetch at a time (this will need to
            be tuned)
        """

        self.cursor = cursor
        self.batch_size = batch_size

    def __getattr__(self, attr):
        """Pass any unhandled attribute lookups to proxied cursor."""

        return getattr(self.cursor, attr)

    def execute(self, sql, *args, **kwargs):
        """Execute a query/statement and fetch first batch of results.

        This:

        * triggers any exceptions caused by the query/statement
        * populates the .description attribute of the cursor
        """

        self.cursor.execute(sql, *args, **kwargs)
        self._rows = self.cursor.fetchmany()
        return self

    def __iter__(self):
        """Iterate over results."""

        while self._rows:
            yield from iter(self._rows)
            self._rows = self.cursor.fetchmany(self.batch_size)

    def fetchone(self):
        raise RuntimeError("Iterate over cursor to get results")

    def fetchmany(self, size=None):
        raise RuntimeError("Iterate over cursor to get results")

    def fetchall(self):
        raise RuntimeError("Iterate over cursor to get results")
