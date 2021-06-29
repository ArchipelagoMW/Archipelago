import io, re, json
from Utils import local_path

def data_path(*args): 
    return local_path('data', 'oot', *args)

def read_json(file_path):
    json_string = ""
    with io.open(file_path, 'r') as file:
        for line in file.readlines():
            json_string += line.split('#')[0].replace('\n', ' ')
    json_string = re.sub(' +', ' ', json_string)
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as error:
        raise Exception("JSON parse error around text:\n" + \
                        json_string[error.pos-35:error.pos+35] + "\n" + \
                        "                                   ^^\n")
