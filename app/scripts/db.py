import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)


def execute_query(sql):
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
