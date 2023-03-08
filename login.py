url_test = "http://10.1.17.140/opra-api/sys/login"
url_dev = "https://10.1.17.141/opra-api/sys/login"
uat_mu = "https://10.1.19.222/opra-api/sys/login"
uat_cz = "https://10.1.19.205/opra-api/sys/login"
opra_ca = "https://10.1.101.13/opra-api/sys/login"
opra_mu = "https://10.1.102.13/opra-api/sys/login"
opra_cz = "https://10.1.103.13/opra-api/sys/login"
pt = "https://10.1.18.186/opra-api/sys/login"

import requests
class login(object):
    def __init__(self, hj="TEST"):
        self.id = "upl"
        self.pwd = "Abc@123"
        if hj == "TEST":
            self.url = url_test
        elif hj == "DEV":
            self.url = url_dev
        elif hj == "UATMU":
            self.url = uat_mu
        elif hj == "UATCZ":
            self.url = uat_cz
        elif hj == "OPRACA":
            self.url = opra_ca
            self.id = "JS00913"
            self.pwd = "Abc@369369"
        elif hj == "OPRAMU":
            self.url = opra_mu
        elif hj == "OPRACZ":
            self.url = opra_cz
        elif hj == "PT":
            self.url = pt

    def login(self):
        data = {
            "password": self.pwd,
            "userId": self.id
        }
        requests.packages.urllib3.disable_warnings()
        r= requests.post(url=self.url, json=data,verify=False)
        return r.json()['accessToken']