import csv
import os

import prestodb
from tabulate import tabulate


def get_conn():
    return prestodb.dbapi.connect(
        host="directoraccess.emishealthinsights.co.uk",
        port=443,
        user=os.environ["USER"],
        catalog="hive",
        schema="extract_oxford_datalabs",
        http_scheme="https",
        auth=prestodb.auth.BasicAuthentication(os.environ["USER"], os.environ["TOKEN"]),
    )


def fetchsome(cursor, arraysize=1000):
    """ A generator that simplifies the use of fetchmany """
    # yield [[col[0] for col in cur.description]]
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result


def get_data(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    return fetchsome(cur)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            sql = f.read()
    else:
        with open("acceptance-test-study.sql") as f:
            sql = f.read()
            sql = sql.replace("TABLE_PREFIX", os.environ["TABLE_PREFIX"])
            sql = sql.replace("patient_view", "patient_500_slice")
            sql = sql.replace("observation_view", "observation_500_slice")
            sql = sql.replace("medication_view", "medication_500_slice")
    conn = get_conn()
    cur = conn.cursor()
    import re

    sql_without_comments = re.sub(
        r"^ *--.*", "", sql, count=0, flags=re.MULTILINE
    ).strip()
    sql_without_blank_lines = "".join(
        [x for x in sql_without_comments.split("\n") if x.strip()]
    )
    statements = sql_without_blank_lines.split(";")[:-1]
    for statement in statements[:-1]:
        print("-" * 80)
        for i, line in enumerate(statement.split("\n"), start=1):
            print("{:>3}: {}".format(i, line))
        cur.execute(statement)
        cur.fetchone()

    print("-" * 80)
    statement = statements[-1]
    for i, line in enumerate(statement.split("\n"), start=1):
        print("{:>3}: {}".format(i, line))
    print("-" * 60)
    data = get_data(conn, statement)
    # print(len(data))
    with open("/tmp/data.csv", "w") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)
    # XXX delete the temporary tables if necessary

    # print(tabulate(data))
