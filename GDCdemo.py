import os
import json
import requests
import gzip
import pandas

from functools import reduce

# headers for the request
headers = {'content-type': 'application/json'}

# url to search the data
search_url = "https://gdc-api.nci.nih.gov/files"

# url to download the data
download_url = "https://gdc-api.nci.nih.gov/data"

def load_payload(file_name):
    print("Loading payload file..\n")
    with open(file_name) as payload_file:    
        payload = json.load(payload_file)
    return payload

def make_requests(url, payload = None, headers = None):
    print("making requests to " + url + "\n")
    r = requests.post(search_url, json=payload, headers=headers)
    response_data = json.loads(r.text)
    return response_data

# downloads the file based on the given UUID
def download_data(download_url, UUID, local_filename):
    print("dowloading file: " + local_filename + "\n")
    req = requests.get(download_url + "/" + UUID, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

def get_value(dictionary, value):
    return dictctionary[value]

# opens the zip files and converts the data into a pandas.DataFrame object
def zip_to_dataframe(file_name, column_names):
    with gzip.open(os.getcwd() + "/" + file_name, 'rb') as f:
        df = pandas.read_table(f, names = column_names)
    return df

def merge_dataframes(df_list, merge_column):
    return reduce(lambda left, right: pandas.merge(left, right, on=merge_column), df_list)

def df_to_csv(df, filename, sep = ",", index = False):
    df.to_csv(filename, sep = sep, index = index)

if __name__ == '__main__':

    payload = load_payload("payload.json")

    response = make_requests(search_url, payload, headers)

    file_names = [get_value(response["data"]["hits"][i], "file_name") for i in range(len(response["data"]["hits"]))]
    
    file_ids = [get_value(response["data"]["hits"][i], "file_id") for i in range(len(response["data"]["hits"]))]
    
    for i in range(len(response["data"]["hits"])):
        download_data(download_url, file_ids[i], file_names[i])
    
    dataframe_files = [zip_to_dataframe(file_names[i], ["Gene", file_ids[i]]) for i in range(len(file_names))]
    
    df_to_csv(merge_dataframes(dataframe_files, "Gene"), "response.tsv", sep = " ")
    
    df = pandas.read_csv("response.tsv", sep=" ")
    
    print(df)