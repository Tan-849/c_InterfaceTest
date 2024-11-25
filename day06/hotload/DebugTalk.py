import time

import yaml



class DebugTalk:

    def read_yml(self, key=None):
        with open("./testcases/phpwind/temp.yml", 'r', encoding="utf-8") as f:
            value = yaml.safe_load(f)
            if key != None:
                return value[key]
            else:
                return value

    def add(self,a,b):
        return int(a)+int(b)

    def md5(self):
        pass

    def get_number(self):
        pass

    def get_random_number(self):
        return str(int(time.time()))
