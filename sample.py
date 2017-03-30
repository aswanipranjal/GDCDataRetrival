import os
import json
import requests
import gzip
import pandas
import api
import time
import sys

from functools import reduce

PROGRAM_NAME = "TCGA"

DATA_TYPE = "Gene Expression Quantification"

WORKFLOW_TYPES = ["HTSeq - FPKM", "HTSeq - FPKM-UQ"]

PROJECT_ID = ["TCGA-BRCA",
"TCGA-UCEC",
"TCGA-KIRC",
"TCGA-LUAD",
"TCGA-LGG",
"TCGA-THCA",
"TCGA-HNSC",
"TCGA-LUSC",
"TCGA-PRAD",
"TCGA-SKCM",
"TCGA-COAD",
"TCGA-BLCA",
"TCGA-STAD",
"TCGA-OV",
"TCGA-LIHC",
"TCGA-CESC",
"TCGA-KIRP",
"TCGA-SARC",
"TCGA-PCPG",
"TCGA-PAAD",
"TCGA-READ",
"TCGA-GBM",
"TCGA-ESCA",
"TCGA-LAML",
"TCGA-TGCT",
"TCGA-THYM",
"TCGA-MESO",
"TCGA-UVM",
"TCGA-ACC",
"TCGA-KICH",
"TCGA-UCS",
"TCGA-DLBC",
"TCGA-CHOL"]

def create_dir(dir):
    if not os.path.exists(dir):
        print("creating directory: " + dir)
        os.makedirs(dir)
    else:
        print(dir + " already exists")


def main():

    cwd_path = [os.getcwd()]
    cwd_path.append("Data")
    create_dir("/".join(cwd_path))

    query_object = api.GDCQuery(endpoint = "files")
    query_object.add_in_filter("file.access", "open")
    query_object.add_in_filter("cases.project.program.name", PROGRAM_NAME)
    query_object.add_in_filter("files.data_type", DATA_TYPE)

    for PI in PROJECT_ID:
        cwd_path.append(PI)
        create_dir("/".join(cwd_path))
        query_object.add_in_filter("cases.project.project_id", PI)

        for WFT in WORKFLOW_TYPES:
            query_object.add_in_filter("files.analysis.workflow_type", WFT)
            query_object.get(page_size=500)

            if query_object.hits:
                cwd_path.append(WFT)
                create_dir("/".join(cwd_path))
                dataframe_files = []

                for item in query_object.hits[:10]:
                    filename = "/".join(cwd_path) + "/" + item["file_name"]
                    print("Downloading file: "+filename)
                    api.py_download_file(item["file_id"], filename)

                    with gzip.open(filename, 'rb') as f:
                        dataframe_files.append(pandas.read_table(f, names=["Gene", item["file_id"] ]))
                
                df_final = reduce(lambda left,right: pandas.merge(left,right,on='Gene'), dataframe_files)
                df_final.to_csv("/".join(cwd_path)+".txt", sep = " ", index = False)
                cwd_path.pop()
            query_object._filters.pop()

        query_object._filters.pop()
        cwd_path.pop()

if __name__ == "__main__":
    main()
