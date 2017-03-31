import os
import json
import requests
import gzip
import pandas
import api

from functools import reduce

PROGRAM_NAME = "TCGA" # Right now we are focusing on TCGA. GDC provides us with TCGA and TARGET project data

DATA_TYPE = "Gene Expression Quantification" # Data type to be downloaded 

WORKFLOW_TYPES = ["HTSeq - FPKM", "HTSeq - FPKM-UQ"] # Work-flow type to be downloaded

# We shall download the data according to the project id.
with open("project_ids.json") as df:
    project_ids = json.load(df)
PROJECT_ID = project_ids["PROJECT_ID"]

NUM_FILES = 10 # number of files to be downloaded

def main():

    cwd_path = [os.getcwd()]
    cwd_path.append("Data")
    api.create_dir(cwd_path)

    # we will be searching GDC using the files end point as we can then specify the access criteria
    query_object = api.GDCQuery(endpoint = "files")
    # adding the open filter so as to download files that are freely available
    query_object.add_in_filter("file.access", "open")
    query_object.add_in_filter("cases.project.program.name", PROGRAM_NAME)
    query_object.add_in_filter("files.data_type", DATA_TYPE)

    for PI in PROJECT_ID:
        cwd_path.append(PI)
        # create a folder for the current Project ID
        api.create_dir(cwd_path)
        # add the project id into the list of filters we are using
        query_object.add_in_filter("cases.project.project_id", PI)

        for WFT in WORKFLOW_TYPES:
            # add the workflow type into the list of filters we are using
            query_object.add_in_filter("files.analysis.workflow_type", WFT)
            query_object.get(page_size=500)

            if query_object.hits:
                cwd_path.append(WFT)
                #create a folder for the current work-flow type
                api.create_dir(cwd_path)
                
                #this is the list containing pandas.dataframe objects for each of the file that we have downloaded
                dataframe_files = []

                for item in query_object.hits[:NUM_FILES]:
                    filename = "/".join(cwd_path) + "/" + item["file_name"]
                    print("Downloading file: "+filename)
                    api.py_download_file(item["file_id"], filename)
                    dataframe_files.append(api.gzip_to_dataframe(filename, column_names=["Gene", item["submitter_id"]]))
                    
                # merge all the downloaded files 
                df_final = api.merge_dataframes(dataframe_files, 'Gene')
                # create a condensed TSV file having all the downloaded samples
                df_final.to_csv("/".join(cwd_path)+".txt", sep = " ", index = False)
                cwd_path.pop()
            query_object._filters.pop()

        query_object._filters.pop()
        cwd_path.pop()

if __name__ == "__main__":
    main()
