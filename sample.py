import os
import json
import requests
import gzip
import pandas
import api

from functools import reduce

PROGRAM_NAME = "TCGA" # Right now we are focusing on TCGA. GDC provides us with TCGA and TARGER

DATA_TYPE = "Gene Expression Quantification" # Data type to be downloaded 

WORKFLOW_TYPES = ["HTSeq - FPKM", "HTSeq - FPKM-UQ"] # Work-flow type to be downloaded

# We shall download the data according to the project id.
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

NUM_FILES = 10

def create_dir(dir_name):
    if type(dir_name) == type([]):
        dir_name = "/".join(dir_name)
    if not os.path.exists(dir_name):
        print("creating directory: " + dir_name)
        os.makedirs(dir_name)
    else:
        print(dir_name + " already exists.")

def main():

    cwd_path = [os.getcwd()]
    cwd_path.append("Data")
    create_dir(cwd_path)

    # using gdctools' api.py file:

    # adding appropriate filters:
    query_object = api.GDCQuery(endpoint = "files")
    query_object.add_in_filter("file.access", "open")
    query_object.add_in_filter("cases.project.program.name", PROGRAM_NAME)
    query_object.add_in_filter("files.data_type", DATA_TYPE)

    for PI in PROJECT_ID:
        cwd_path.append(PI)
        #create a folder for the current Project ID
        create_dir(cwd_path)
        query_object.add_in_filter("cases.project.project_id", PI)

        for WFT in WORKFLOW_TYPES:
            query_object.add_in_filter("files.analysis.workflow_type", WFT)
            query_object.get(page_size=500)

            if query_object.hits:
                cwd_path.append(WFT)
                #create a folder for the current work-flow type
                create_dir(cwd_path)
                dataframe_files = []

                for item in query_object.hits[:NUM_FILES]:
                    filename = "/".join(cwd_path) + "/" + item["file_name"]
                    print("Downloading file: "+filename)
                    api.py_download_file(item["file_id"], filename)

                    with gzip.open(filename, 'rb') as f:
                        dataframe_files.append(pandas.read_table(f, names=["Gene", item["submitter_id"] ]))
                
                df_final = reduce(lambda left,right: pandas.merge(left,right,on='Gene'), dataframe_files)
                #create a condensed TSV file having all the downloaded samples
                df_final.to_csv("/".join(cwd_path)+".txt", sep = " ", index = False)
                cwd_path.pop()
            query_object._filters.pop()

        query_object._filters.pop()
        cwd_path.pop()

if __name__ == "__main__":
    main()
