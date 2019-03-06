import json 
import sys
from pprint import pprint

projects_directories = [
    'auth', 
    'common', 
    'composite-controls', 
    'cron', 
    'external-proxy', 
    'history', 
    'i18n', 
    'mappings', 
    'model-data',
    'model-structure', 
    'services', 
    'validators'
]

base_path = '/app'
playground_path = '/app/playground'
satis_path = playground_path + '/satis/build/satis.json'

def read_composer(path):
    file_path = path + 'composer.json'
    with open(file_path) as f:
        data = json.load(f)
    return data

def extract_required(data):
    return {
        'required': data['require'],
        'dev': data['require-dev']
    }

def gather_data(dictionary, data):
    for key in data.keys():
        if key in dictionary:
            dictionary[key].append(data[key])
        else:
            dictionary[key] = [data[key]]    

def remove_duplicates(dictionary):
    for key in dictionary.keys():
        dictionary[key] = set(dictionary[key])

def join_versions(dictionary):
    result = {}
    for key in dictionary:
        result[key] = ' || '.join(dictionary[key])
    return result

def update_satis_conf(required, dev):
    with open(satis_path) as f:
        data = json.load(f)
    data['require'] = required
    # data['require-dev'] = dev
    pprint(data)

    with open(satis_path, 'w') as outfile:
        json.dump(data, outfile)

def main():
    required_data = {}
    dev_data = {}
    for dir in projects_directories:
        element_path = base_path + '/' + dir + '/'
        packages = extract_required(read_composer(element_path))
        gather_data(required_data, packages['required'])
        gather_data(dev_data, packages['dev'])
       
    # usuwanie duplikatow
    remove_duplicates(required_data)
    remove_duplicates(dev_data)    

    required = join_versions(required_data)
    dev = join_versions(dev_data)

    update_satis_conf(required, dev)


if __name__ == '__main__':
    sys.exit(main() or 0)