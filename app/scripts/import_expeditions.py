import os

import fire
from dotenv import load_dotenv

from db import execute_query

load_dotenv(".env", verbose=True)

FILE_PATH = os.environ.get("RAW_DATA_PATH")


class Expeditions(object):
    def expeditions_from_crosswalk(self):
        file = f"{FILE_PATH}/get_expeditions_from_crosswalk/expeditions.csv"
        sql = f"""
        COPY expeditions(name,workbook_tab_name,data_source_notes)
        FROM '{file}' DELIMITER ',' CSV HEADER;
        """

        execute_query(sql)


if __name__ == "__main__":
    fire.Fire(Expeditions)
