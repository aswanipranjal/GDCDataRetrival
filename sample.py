import os
import json
import requests
import gzip
import pandas
import api

PROGRAM_NAME = "TCGA"
PROJECT_ID = "TCGA-BRCA"

def main():

    cwd_path = [os.getcwd()]
    cwd_path.append("Data")
    api.create_dir("/".join(cwd_path))

    query_object = api.GDCQuery(endpoint = "files")
    query_object.add_in_filter("file.access", "open")
    query_object.add_in_filter("cases.project.program.name", PROGRAM_NAME)
    query_object.add_in_filter("cases.project.project_id", PROJECT_ID)

    for dt in query_object.DATA_TYPES:
        cwd_path.append(dt)
        api.create_dir("/".join(cwd_path))
        query_object.add_in_filter("files.data_type", dt)

        for wft in query_object.WORKFLOW_TYPES:
            query_object.add_in_filter("files.analysis.workflow_type", wft)
            query_object.get()

            if query_object.hits:
                cwd_path.append(wft)
                print(cwd_path) 
                api.create_dir("/".join(cwd_path))
                for item in query_object.hits[:10]:
                    filename = "/".join(cwd_path) + "/" + item["file_name"]
                    print(filename)
                    api.py_download_file(item["file_id"], filename)

                
                cwd_path.pop()
            query_object._filters.pop()
        query_object._filters.pop()
        cwd_path.pop()

if __name__ == "__main__":
    main()


