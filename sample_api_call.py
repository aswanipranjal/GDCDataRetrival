import requests
import json

file_endpt = 'https://gdc-api.nci.nih.gov/files/'

payload = {
    "filters":{
        "op":"and",
        "content":[
            {
                "op":"in",
                "content":{
                    "field":"cases.submitter_id",
                    "value":[
                        "TCGA-CK-4948",
                        "TCGA-D1-A17N",
                        "TCGA-4V-A9QX",
                        "TCGA-4V-A9QM"
                    ]
                }
            },
            {
                "op":"=",
                "content":{
                    "field":"files.data_type",
                    "value":"Gene Expression Quantification"
                }
            }
        ]
    },
    "format":"tsv",
    "fields":"file_id,file_name,cases.submitter_id,cases.case_id,data_category,data_type,cases.samples.tumor_descriptor,cases.samples.tissue_type,cases.samples.sample_type,cases.samples.submitter_id,cases.samples.sample_id,analysis.workflow_type,cases.project.project_id,cases.samples.portions.analytes.aliquots.aliquot_id,cases.samples.portions.analytes.aliquots.submitter_id",
    "size":"1000"
}

headers = {"Content-Type" : "application/json"}
r = requests.post(url=file_endpt, headers=headers, json=payload)

response_data = r.text

print(type(response_data))






