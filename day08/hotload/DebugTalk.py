import base64
import hashlib
import time

import rsa
import yaml

from day08.config import setting


class DebugTalk:

    def read_yml(self, key=None):
        with open(setting.extract_yml, 'r', encoding="utf-8") as f:
            value = yaml.safe_load(f)
            if key != None:
                return value[key]
            else:
                return value

    def add(self,a,b):
        return int(a)+int(b)

    def get_number(self):
        pass

    def get_random_number(self):
        return str(int(time.time()))

    def md5_encode(self,data):
        # 把 data 转化成 utf-8 的编码格式
        data = str(data).encode('utf-8')
        # md5加密，哈希算法
        md5_value = hashlib.md5(data).hexdigest()
        return md5_value

    def base64_encode(self,data):
        data = str(data).encode('utf-8')
        base64_value = base64.b64encode(data).decode('utf-8')
        return base64_value

    def create_rsa_key(self):
        (public_key,private_key)=rsa.newkeys(1024)
        with open("./public_key.pem", 'w+', encoding="utf-8") as f:
            f.write(public_key.save_pkcs1().decode())
        with open("./private_key.pem", 'w+', encoding="utf-8") as f:
            f.write(private_key.save_pkcs1().decode())

    def rsa_encode(self,data):
        # 加载公钥
        with open("./public_key.pem", 'r', encoding="utf-8") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read().encode('utf-8'))
        # 把data转化成utf-8模式
        data = str(data).encode('utf-8')
        # 字符串加密后是 byte 类型
        byte_value = rsa.encrypt(data, public_key)
        # 把字节转化成字符串类型
        rsa_value = base64.b64encode(byte_value).decode('utf-8')
        return rsa_value

    def rsa_decode(self,data):
        # 加载私钥
        with open("./private_key.pem", 'r', encoding="utf-8") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read().encode('utf-8'))
        # 把data转化成utf-8模式
        data = base64.b64decode(str(data).encode('utf-8'))
        # 字符串解密后是 byte 类型
        byte_value = rsa.decrypt(data, private_key)
        # 把字节转化成字符串类型
        rsa_value = byte_value.decode('utf-8')
        return rsa_value



if __name__ == '__main__':
    DebugTalk = DebugTalk()
    DebugTalk.create_rsa_key()
    rsa_encode = DebugTalk.rsa_encode("admin")
    print(f"rsa_encode:{rsa_encode}")
    rsa_decode = DebugTalk.rsa_decode(rsa_encode)
    print(f"rsa_decode:{rsa_decode}")



