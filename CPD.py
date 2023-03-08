import re,time
from log_upl import log
import requests
import threading,queue
from login import login
name = ''
token = login(hj='PT').login()
headers = {
    "Authorization": token,
    "Content-Type": "application/json",
    "Accept-Language": "zh-CN"
}
en_url = "https://10.1.18.186/opra-api/upl-file/test/decry?data={0}&type={1}"
de_url = "https://10.1.18.186/opra-api/upl-file/test/encry?data={0}&type={1}"

def get_re_en():

    while True:
        try:
            dicts = {}
            dicts_en = {}
            dicts_re = {}
            line = q.get(block=False)

            first_name = line[0].strip()
            full_name = line[1].strip()
            frequent_flyer_no_of_passenger = line[2].strip()
            credential_no = line[3].strip()
            passport_no = line[4].strip()
            ticket_no= line[5].strip()

            dicts['ticket_no'] = ticket_no
            dicts_en['ticket_no'] = ticket_no
            dicts_re['ticket_no'] = ticket_no

            dicts_en['first_name'] = f'{first_name}'
            dicts_en['full_name'] = f'{full_name}'
            dicts_en['frequent_flyer_no_of_passenger'] = f'{frequent_flyer_no_of_passenger}'
            dicts_en['credential_no'] = f'{credential_no}'
            dicts_en['passport_no'] = f'{passport_no}'

            # 名字加密
            name_url_en = en_url.format(f'{first_name}','NAME')
            name_resp_en = requests.get(name_url_en,headers=headers,verify=False)
            dicts['first_name'] = f'{first_name}'
            dicts_en['first_name'] = f'{name_resp_en.text}'
            # 名字解密
            name_url_re = de_url.format(f'{name_resp_en.text}','NAME')
            name_resp_re = requests.get(name_url_re,headers=headers,verify=False)
            dicts_re['first_name'] = f'{name_resp_re.text}'
            # full名字加密
            full_name_url_en = en_url.format(f'{full_name}','NAME')
            full_name_resp_en = requests.get(full_name_url_en,headers=headers,verify=False)
            dicts['full_name'] = f'{full_name}'
            dicts_en['full_name'] = f'{full_name_resp_en.text}'
            # full名字解密
            full_name_url_re = de_url.format(f'{full_name_resp_en.text}','NAME')
            full_name_resp_re = requests.get(full_name_url_re,headers=headers,verify=False)
            dicts_re['full_name'] = f'{full_name_resp_re.text}'
            # 常旅客卡号加密
            frequent_flyer_no_url_en = en_url.format(f'{frequent_flyer_no_of_passenger}','FFP')
            frequent_flyer_no_resp_en = requests.get(frequent_flyer_no_url_en,headers=headers,verify=False)
            dicts['frequent_flyer_no_of_passenger'] = f'{frequent_flyer_no_of_passenger}'
            dicts_en['frequent_flyer_no_of_passenger'] = f'{frequent_flyer_no_resp_en.text}'
            # 常旅客卡号解密
            frequent_flyer_no_url_re = de_url.format(f'{frequent_flyer_no_resp_en.text}','FFP')
            frequent_flyer_no_resp_re = requests.get(frequent_flyer_no_url_re,headers=headers,verify=False)
            dicts_re['frequent_flyer_no_of_passenger'] = f'{frequent_flyer_no_resp_re.text}'
            # 证件号加密
            credential_no_url_en = en_url.format(f'{credential_no}','IDENTITYCARD')
            credential_no_resp_en = requests.get(credential_no_url_en,headers=headers,verify=False)
            dicts['credential_no'] = f'{credential_no}'
            dicts_en['credential_no'] = f'{credential_no_resp_en.text}'
            # 证件号解密
            credential_no_url_re = de_url.format(f'{credential_no_resp_en.text}','IDENTITYCARD')
            credential_no_resp_re = requests.get(credential_no_url_re,headers=headers,verify=False)
            dicts_re['credential_no'] = f'{credential_no_resp_re.text}'
            # 护照号加密
            passport_no_url_en = en_url.format(f'{passport_no}','IDENTITYCARD')
            passport_no_resp_en = requests.get(passport_no_url_en,headers=headers,verify=False)
            dicts['passport_no'] = f'{passport_no}'
            dicts_en['passport_no'] = f'{passport_no_resp_en.text}'
            # 护照号解密
            passport_no_url_re = de_url.format(f'{passport_no_resp_en.text}','IDENTITYCARD')
            passport_no_resp_re = requests.get(passport_no_url_re,headers=headers,verify=False)
            dicts_re['passport_no'] = f'{passport_no_resp_re.text}'

            print("加密", dicts_en,'\n', "原始数据", dicts,'\n', "解密", dicts_re)
            for key, value in dicts.items():
                if dicts_re[key] == value:
                    pass
                else:
                    log.info("加密前：" + value + '----------' +"加密后：" + dicts_en[key] + '----------' "解密后：" + dicts_re[key], f"{key}不一致")
                if dicts_en[key] == value and value !='' and key !='ticket_no':
                    log.info("加密后：" + f'{dicts_en[key]}' + ' ' + "解密后：" + f'{dicts_re[key]}' + ' ' + f"{key}相等，不一致")

            with open('logs/x.txt',mode='a+') as note:
                if dicts_en['ticket_no'] !='':
                    note.writelines('\'' + f"{dicts_en['ticket_no']}" + '\'' + ':')
                    note.writelines(f"{dicts_en}\n")
            with open('sqlldr/cpd.txt',mode='a+') as note2:
                if dicts_en['ticket_no'] != '':
                    note2.writelines(f"{dicts_en['ticket_no']}" + ',' + f"{dicts_en['first_name']}" +',' +  f"{dicts_en['full_name']}" +','
                                     +  f"{dicts_en['frequent_flyer_no_of_passenger']}"+',' +  f"{dicts_en['credential_no']}" +','
                                     +  f"{dicts_en['passport_no']}" + '\n')

        except queue.Empty:
            break



if __name__ == '__main__':
    with open('logs/x.txt', mode='w') as note:
        note.writelines('CPD文件解析\n')
    with open('sqlldr/cpd.txt', mode='w') as note:
        note.writelines('CPD文件解析\n')

    file_name = 'CA_CPD_20220614.txt'

    f = open(r'E:\文件\data\{0}'.format(file_name), encoding='gb2312',errors='ignore')
    lines = f.readlines()[1:-1]
    q = queue.Queue()

    for i in lines:
        lst = [i.encode('gbk')[55:94].decode('utf-8'),i[95:126],i.encode('gbk')[201:220].decode('utf-8'),i.encode('gbk')[320:339].decode('utf-8'),i.encode('gbk')[340:359].decode('utf-8'),i.encode('gbk')[176:186].decode('utf-8')]
        q.put(lst)

    # 线程数
    process_num = len(lines)
    ts = []
    for i in range(100):
        t = threading.Thread(target=get_re_en())
        ts.append(t)
        t.start()

    for i in ts:
        t.join()

