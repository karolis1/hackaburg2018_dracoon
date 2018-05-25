import json
import os
import shutil

import requests
import yaml
import pickle
import tqdm

path = '/api/v4'

conf_file = 'conf/dracoon.yml'
has_conf_file = os.path.isfile(conf_file)
if has_conf_file:
    with open(conf_file, 'r') as stream:
        try:
            conf = yaml.load(stream)
        except yaml.YAMLError as err:
            print(f"ERROR: can't read {conf_file}")
else:
    print(f"ERROR: file {conf_file} doesn't exist")


def login():
    api = '/auth/login'
    url = f"{conf['url']}{path}{api}"
    data = json.dumps({
        'login': conf['user'],
        'password': conf['pass'],
        'authType': 'sql'
    })
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json;charset=UTF-8'
    }
    res = requests.post(url, data=data, headers=headers)
    data = json.loads(res.text)
    return data['token']


token = ''
if 'token' in conf.keys():
    token = conf['token']
else:
    token = login()


def get_sub_nodes(id):
    api = "/nodes"
    query = f"?parent_id={id}"
    url = f"{conf['url']}{path}{api}{query}"
    headers = {'X-Sds-Auth-Token': token}
    res = requests.get(url, headers=headers)
    data = json.loads(res.text)
    return data['items']


def listify_tags(tag_string):
    tags = list(map(lambda x: x.strip(), filter(lambda x: x != '', tag_string.split(';'))))
    return tags


def download_node(node_id, local, storage_folder='data/'):
    api = f"/nodes/files/{node_id}/downloads"
    url = f"{conf['url']}{path}{api}"
    headers = {'X-Sds-Auth-Token': token}
    res = requests.get(url, headers=headers, stream=True)
    res.raw.decode_content = True
    with open(storage_folder + local, 'wb') as f:
        shutil.copyfileobj(res.raw, f)


def find_nodes(root):
    id = 0

    nodes = get_sub_nodes(id)
    id = None
    for node in nodes:
        if node['name'] == root:
            id = node['id']

    if id is None:
        raise Exception("Root does not exist")

    folder_nodes = get_sub_nodes(id)
    file_list = []

    for node in folder_nodes:
        id = node['id']
        file_nodes = get_sub_nodes(id)

        for fnode in file_nodes:
            file_list.append((fnode['id'], fnode['name'], listify_tags(fnode.get('notes'))))

    return file_list


def download_all():
    root = 'Tagged Documents'
    nodes_filenames_tags = find_nodes(root)

    pickle.dump(nodes_filenames_tags, open('download_meta.pickle', 'wb'))

    for node, filename, _ in tqdm.tqdm(nodes_filenames_tags):
        download_node(node, filename)


download_all()
