# -*- coding:utf-8 -*-
"""
说明：对ORACLE数据库的操作方法
"""
import os
import cx_Oracle

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

do_sql2 = []
class OracleConnect(object):
    def __init__(self, db_name="OPRA_UPL_TEST"):  # db_name: 对应数据库配置项名
        if db_name == "OPRA_UPL_TEST":
            connect_str = "OPRAUPL/acca1234@10.1.18.249:1521/OPRAUPL"
        elif db_name == "OPRA_UPL_DEV":
            connect_str = "OPRAUPL/acca1234@10.1.17.236:1521/OPRAUPL"
        elif db_name == "OPRA_UPL_UAT_CZ":
            connect_str = "OPRAUPL/acca1234@10.1.19.235:1521/OPRAUPL"
        elif db_name == "OPRA_UPL_UAT_MU":
            connect_str = "OPRAUPL/acca1234@10.1.19.196:1521/OPRAUPL"
        elif db_name == "OPRA_UPL_CZ":
            connect_str = "OPRAUPL/m6e9_x8j3@10.1.108.26:1521/CZUPLP"
        elif db_name == "OPRA_UPL_CA":
            connect_str = "RLSTMP/OpraCA_2022@@10.1.106.26:1521/cauplp"
        elif db_name == "OPRA_UPL_MU":
            connect_str = "OPRAUPL/Upl_2112@10.1.107.26:1521/muuplp"
        elif db_name == "OPRA_UPL_PT":
            connect_str = "OPRAUPL/acca1234@10.1.26.182:1521/uplpt"
        self.db = cx_Oracle.connect(connect_str)
        self.cr = self.db.cursor()

    def sql_iud(self, sql):
        print("执行sql",sql)
        self.cr.execute(sql)
        self.db.commit()
    def sql_iud2(self, sql):
        print("执行sql",sql)
        self.cr.execute(sql)
        self.db.commit()
    def sql_select(self,sql):
        self.cr.execute(sql)
        r = self.cr.fetchall()
        return r

import random,string
def digits_number(num):
    """
    返回纯数字编号，最大长度未20位
    :param num: 数字长度
    :return:
    """
    return ''.join(random.sample(string.digits * 2, num))

if __name__ == '__main__':
    # list_a =[
    #     ["999","1","6707538231","1037653739596869632"],
    #     ["999","1","4870341814","1037653739575832576"]
    # ]

    for a in range(200):
        sequence = random.randint(10000000000000,99900000000000)
        sql = f"insert into upl_rev_discount (SEQUENCE, OFF_SEASON, OFF_SEASON_DISCOUNT, SHOULDER_SEASON, SHOULDER_SEASON_DISCOUNT, PEAK_SEASON, PEAK_SEASON_DISCOUNT, EFFECTIVE_DATE_FROM, EFFECTIVE_DATE_TO, CREATED_BY, CREATED_DATE, LAST_MODIFIED_BY, LAST_MODIFIED_DATE, RULE_CODE) values ('{sequence}', '1,7,8,9', 11, '2,5,11', 22, '3,4,6,10,12', 33, to_date('01-03-2023', 'dd-mm-yyyy'), to_date('31-03-2023', 'dd-mm-yyyy'), 'upl', to_date('29-03-2023 13:13:00', 'dd-mm-yyyy hh24:mi:ss'), 'upl', to_date('29-03-2023 17:28:21', 'dd-mm-yyyy hh24:mi:ss'), 'UYI')"
        OracleConnect("OPRA_UPL_TEST").sql_iud(sql)