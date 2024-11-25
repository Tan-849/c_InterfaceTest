import yaml


def read_yaml(yaml_path):
    with open(yaml_path, 'r',encoding="utf-8") as f:
        value = yaml.safe_load(f)
        return value

def white_yaml(yaml_path,data):
    with open(yaml_path, 'w',encoding="utf-8") as f:
        yaml.dump(data,f,allow_unicode=True)

def clean_yaml(yaml_path):
    with open(yaml_path, 'w',encoding="utf-8") as f:
        pass