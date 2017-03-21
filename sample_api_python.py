import os
import json
import requests
import gzip
import pandas

from functools import reduce

#headers for the request
headers = {'content-type': 'application/json'}

#url to search the data
search_url = "https://gdc-api.nci.nih.gov/files"

#url to download the data
download_url = "https://gdc-api.nci.nih.gov/data"


with open('payload.json') as payload_file:    
    payload = json.load(payload_file)

#making the request
r = requests.post(search_url, json=payload, headers=headers)
response_data = json.loads(r.text)

file_names = []
file_ids = []

#this loop, downloads the data ans saves the file names and file ids into the lists initialized above
for i in range(len(response_data["data"]["hits"])):
    os.system("curl --remote-name --remote-header-name '{0}/{1}'".format(download_url, response_data["data"]["hits"][i]["file_id"]))
    file_ids.append(response_data["data"]["hits"][i]["file_id"])
    file_names.append(response_data["data"]["hits"][i]["file_name"])

#get the current working directory
cwd = os.getcwd()
dataframe_files = []

#this loop opens the zip files and converts the data into a pandas.DataFrame object
for i in range(len(file_names)):
    with gzip.open(cwd+"/"+file_names[i], 'rb') as f:
        dataframe_files.append(pandas.read_table(f, names=["Gene", file_ids[i] ]))


#merging the dataframes together to form one single data frame
df_final = reduce(lambda left,right: pandas.merge(left,right,on='Gene'), dataframe_files)

#save the data frame as a TSV file
df_final.to_csv("response.tsv", sep = " ", index = False)

df = pandas.read_csv("response.tsv", sep=" ")

#print the accumulated data
print(df)