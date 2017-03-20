import os
import json
import requests


payload = {
    "filters" : {
        "op" : "and",
        "content":[
            {
                "op" : "in",
                "content" : {
                    "field" : "cases.project.project_id",
                    "value":[
                        "TCGA-PAAD"
                    ]
                }
            },
            {
                "op":"in",
                "content":{
                    "field":"files.access",
                    "value":"open"
                }
            }
        ]
    }, 
    "format":"txt",
    "size":"10"
}

headers = {'content-type': 'application/json'}
url = "https://gdc-api.nci.nih.gov/files"
r = requests.post(url, json=payload, headers=headers)

data = json.loads(r.text)

os.system("curl --remote-name --remote-header-name 'https://gdc-api.nci.nih.gov/data/{0}'".format(data["data"]["hits"][0]["file_id"]))

