import sqlite3
import csv


def load_csv_data_to_sqlite(file_path, table_name):
    conn = sqlite3.connect("store_monitoring.db")
    cursor = conn.cursor()

    with open(file_path, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
        column_names = ", ".join(headers)
        placeholders = ", ".join(["?"] * len(headers))
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

        for row in csvreader:
            cursor.execute(query, row)

    conn.commit()
    conn.close()


load_csv_data_to_sqlite("E:\Loop Startup Task\store.csv", "stores")
