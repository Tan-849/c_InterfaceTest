import yaml


class YmlUtil:

    def read_yml(self, yaml_path, key=None):
        with open(yaml_path, 'r', encoding="utf-8") as f:
            value = yaml.safe_load(f)
            if key != None:
                return value[key]
            else:
                return value

    def white_yml(self, yaml_path, data):

        with open(yaml_path, 'a+', encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)

    def clean_yml(self, yaml_path):
        with open(yaml_path, 'w', encoding="utf-8") as f:
            pass
