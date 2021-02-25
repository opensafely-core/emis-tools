import csv

from connection import get_conn


def run(input_path, output_path):
    with open(output_path, "w") as f:
        # Check whether we can write to output_path before doing any work.
        pass

    with open(input_path) as f:
        sql = f.read()

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)

    with open(output_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow([col[0] for col in cursor.description])
        writer.writerows(cursor)


if __name__ == "__main__":
    import sys

    run(sys.argv[1], sys.argv[2])
