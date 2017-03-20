import requests
import json

file_endpt = 'https://gdc-api.nci.nih.gov/data/'
file_uuid = '0004d251-3f70-4395-b175-c94c2f5b1b81'
response = requests.get(file_endpt + file_uuid)
print(json.dumps(response.json(), indent=2))
''' Response
{
  "data": {
    "data_type": "Aligned Reads",
    "updated_datetime": "2016-05-26T17:06:40.003624-05:00",
    "created_datetime": "2016-05-26T17:06:40.003624-05:00",
    "file_name": "0017ba4c33a07ba807b29140b0662cb1_gdc_realn.bam",
    "md5sum": "a08304b120c5df76b6532da0e9a35ced",
    "data_format": "BAM",
    "acl": [
      "phs000178"
    ],
    "access": "controlled",
    "platform": "Illumina",
    "state": "submitted",
    "file_id": "d853e541-f16a-4345-9f00-88e03c2dc0bc",
    "data_category": "Raw Sequencing Data",
    "file_size": 23650901931,
    "submitter_id": "c30188d7-be1a-4b43-9a17-e19ccd71792e",
    "type": "aligned_reads",
    "file_state": "processed",
    "experimental_strategy": "WXS"
  },
  "warnings": {}
}'''