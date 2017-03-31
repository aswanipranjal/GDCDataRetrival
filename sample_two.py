import os
import json
import requests
import gzip
import pandas
import api

NUM_FILES = 10 # number of files to be downloaded

PROGRAM_NAME = "TCGA" # Right now we are focusing on TCGA. GDC provides us with TCGA and TARGET project data

DATA_TYPE = "Gene Expression Quantification" # Data type to be downloaded 

WORKFLOW_TYPES = ["HTSeq - FPKM", "HTSeq - FPKM-UQ"] # Work-flow type to be downloaded

# We shall download the data according to the project id.
with open("project_ids.json") as df:
    project_ids = json.load(df)

PROJECT_ID = project_ids["PROJECT_ID"]

def main():

    cwd_path = [os.getcwd()]
    cwd_path.append("CaseData")
    api.create_dir(cwd_path)

    cases_query = api.GDCQuery("cases")
    cases_query.add_in_filter("cases.project.program.name", PROGRAM_NAME)
    cases_query.add_in_filter("files.data_type", DATA_TYPE)

    print("\ngoing inside project id loop")
    for PI in PROJECT_ID:
        list_of_cases = []
        cwd_path.append(PI)
        # create a folder for the current Project ID
        api.create_dir(cwd_path)
        # add the project id into the list of filters we are using
        cases_query.add_in_filter("cases.project.project_id", PI)

        print("\ngetting cases hits")
        cases_query.get()
        case_hits = cases_query.hits()[0:NUM_FILES]
        for hit in case_hits:
            val["submitter_id"] = hit["submitter_id"]
            val["case_id"] = hit["case_id"]
            list_of_cases.append(val)
        print("\nlist of cases created")
        print("\nfile wuery created")
        file_query = api.GDCQuery("files")
        file_query._filters = api.transfer_filters(cases_query)

        print("\ngoing inside WFT loop")
        for WFT in WORKFLOW_TYPES:
            # add the workflow type into the list of filters we are using
            file_query.add_in_filter("files.analysis.workflow_type", WFT)

            cwd_path.append(WFT)
            #create a folder for the current work-flow type
            api.create_dir(cwd_path)
                
            #this is the list containing pandas.dataframe objects for each of the file that we have downloaded
            dataframe_files = []

            print("\n going inside list of cases loop")
            for item in list_of_cases:
                file_query.add_in_filter("cases.case_id", item["case_id"])
                file_query.get()
                hit = file_query.hits()[0]
                filename = "/".join(cwd_path) + "/" + hit["file_name"]

                print("Downloading file: "+filename)

                api.py_download_file(hit["file_id"], filename)

                dataframe_files.append(api.gzip_to_dataframe(filename, column_names=["Gene", item["submitter_id"]]))

                file_query._filters.pop()
                    
                # if the file already exists, retrieve the data from it and add it to the dataframe list
            if os.path.exists("/".join(cwd_path)+".txt"):
                print("Appending to existing file")
                dataframe_files.append(pandas.read_csv("/".join(cwd_path)+".txt", sep = " "))   
                # merge all the downloaded files 
            df_final = api.merge_dataframes(dataframe_files, 'Gene')
            # create a condensed TSV file having all the downloaded samples
            df_final.to_csv("/".join(cwd_path)+".txt", sep = " ", index = False)
            file_query._filter.pop()
            cwd_path.pop()

        file_query._filters.pop()
        cwd_path.pop()

if __name__ == "__main__":
    main()
