import os
import json
import requests

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
