import re
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
def get_re_en():

    while True:
        try:
            dicts = {}
            dicts_en = {}
            dicts_re = {}
            line = q.get(block=False)
            name = line[1]
            dicts_en[f'{line[0]}'] = f'{name}'
            # 加密
            url_en = f'https://10.1.18.186/opra-api/upl-file/test/decry?data={name}&type=NAME'
            resp_en = requests.get(url_en,headers=headers,verify=False)
            dicts[f'{line[0]}'] = f'{name}'
            dicts_en[f'{line[0]}'] = f'{resp_en.text}'
            # 解密
            url_re = f'https://10.1.18.186/opra-api/upl-file/test/encry?data={resp_en.text}&type=NAME'
            resp_re = requests.get(url_re,headers=headers,verify=False)
            dicts_re[f'{line[0]}'] = f'{resp_re.text}'
            print("加密", dicts_en, "原始数据", dicts, "解密", dicts_re)
            for key, value in dicts.items():
                if dicts_re[key] == value:
                    pass
                else:
                    print("加密前：" + value + '----------' +"加密后：" + dicts_en[key] + '----------' "解密后：" + dicts_re[key], "不一致")
                if dicts_en[key] == value:
                    print("加密后：" + dicts_en[key] + '\n' "解密后：" + dicts_re[key], "相等，不一致")

        except queue.Empty:
            break


if __name__ == '__main__':
    f = open(r'E:\文件\data\FaradayFile\FAB\FAB_USED2019-05-11TRAVELSKY.txt', encoding='utf-8')
    lines = f.readlines()
    q = queue.Queue()

    for i in lines:
        lst = []
        rg_str_lst = i.split(',')
        for i in rg_str_lst:
            lst.append(i)
        q.put(lst)

    # 进程数
    process_num = len(lines)
    ts = []
    for i in range(100):
        t = threading.Thread(target=get_re_en())
        ts.append(t)
        t.start()

    for i in ts:
        t.join()
