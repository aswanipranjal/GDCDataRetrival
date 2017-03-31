import os
import json
import requests
import gzip
import pandas
import api
import sample

from functools import reduce

#PROGRAM_NAME = "TCGA"
#DATA_TYPE = "Gene Expression Quantification" 
#
#cases_query = api.GDCQuery("cases")
#cases_query.add_in_filter("cases.project.program.name", "TCGA")
#cases_query.add_in_filter("cases.project.project_id", "TCGA-BRCA")
#
#cases_query.get()
#
#response = cases_query.hits
##print(response[56])
#
##print("\n")
#
##print(response[332])
#
#file_query = api.GDCQuery("files")
#file_query.add_in_filter("cases.case_id", response[332]["case_id"])
#file_query.add_in_filter("cases.project.program.name", "TCGA")
#file_query.add_in_filter("files.data_type", "Gene Expression Quantification")
#file_query.add_in_filter("cases.project.project_id", "TCGA-BRCA")
#file_query.add_in_filter("files.analysis.workflow_type", "HTSeq - FPKM")
#
#print(file_query.get())
#if file_query.hits:
#    api.py_download_file(file_query.hits[0]["file_id"], file_query.hits[0]["file_name"])
print(sample.gzip_to_dataframe("1f853089-c40d-4bee-9833-837f327b275a.FPKM.txt.gz", column_names = ["Gene", "EX1"]).size)
    
