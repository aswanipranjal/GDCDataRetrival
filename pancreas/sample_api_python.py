import os
import json
import requests
import gzip
import pandas

from os import listdir
from os.path import isfile, join

headers = {'content-type': 'application/json'}

url = "https://gdc-api.nci.nih.gov/files"

payload = {
"filters":
        {
            "op":"and",
            "content":
                    [
                        { 
                            "op":"in",
                            "content":
                                        { 
                                            "field":"cases.project.project_id", 
                                            "value":["TCGA-PAAD"]
                                        } 
                        },

                        {   "op":"in",
                            "content":
                                        {
                                            "field":"files.access",
                                            "value":["open"]
                                        }
                        },

                        {   "op":"in",
                            "content":
                                        {
                                            "field":"files.data_category",
                                            "value":["Transcriptome Profiling"]
                                        }
                        },

                        {   "op":"in",
                            "content":
                                        {
                                            "field":"files.data_type",
                                            "value":["Gene Expression Quantification"]
                                        }
                        },

                        {   "op":"in",
                            "content":
                                        {
                                            "field":"files.analysis.workflow_type",
                                            "value":["HTSeq - FPKM"]
                                        }
                        }
                    ]
        }, 
            "format":"txt",
            "size":"10",
            "facetTab":"files"
}

r = requests.post(url, json=payload, headers=headers)

data = json.loads(r.text)


file_names = []

for i in range(len(data["data"]["hits"])):
    os.system("curl --remote-name --remote-header-name 'https://gdc-api.nci.nih.gov/data/{0}'".format(data["data"]["hits"][i]["file_id"]))
    file_names.append(data["data"]["hits"][i]["file_name"])

cwd = os.getcwd()

with gzip.open('f144de50-6126-4912-9c94-824d1eb0fac5.FPKM.txt.gz', 'rb') as f:
    file_content1 = pandas.read_table(f, names = ["Gene", "f144de50-6126-4912-9c94-824d1eb0fac5.FPKM"])

with gzip.open('caf9cab4-f98f-46bd-a75d-0eb1e9c6c9ea.FPKM.txt.gz', 'rb') as f:
    file_content2 = pandas.read_table(f, names = ["Gene", "caf9cab4-f98f-46bd-a75d-0eb1e9c6c9ea.FPKM"])

print(pandas.merge(file_content1, file_content2, on="Gene", how="outer"))

