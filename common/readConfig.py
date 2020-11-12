import os
import codecs
import configparser

proDir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# print(proDir)
configPath = os.path.join(proDir, "conf/config.ini")


class ReadConfig:
    def __init__(self):
        # fd = open(configPath, "r")
        # data = fd.read()
        # print(data)
        # #  remove BOM
        # if data[:3] == codecs.BOM_UTF8:
        #     data = data[3:]
        #     file = codecs.open(configPath, "w")
        #     file.write(data)
        #     file.close()
        # fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_account(self, name):
        value = self.cf.get("ACCOUNT", name)
        return value

    def set_account(self, name, value):
        self.cf.set("ACCOUNT", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_redis(self, name):
        value = self.cf.get("REDIS", name)
        return value


localReadConfig = ReadConfig()
# print(        localReadConfig.get_headers("client_identity"))
