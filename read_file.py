"""
description：对csv文件进行操作
author：马烈勇
"""

import openpyxl
import os
import csv

result = [['POST', 'ImportFileCFD', '1', '0', '1563.0000000819564', '1563.0000000819564', '1563.0000000819564', '1563.0000000819564', '718.0', '0.0011116172934978368', '0.0', '1600', '1600', '1600', '1600', '1600', '1600', '1600', '1600', '1600', '1600', '1600'], ['POST', 'ImportFileCPD', '1', '0', '6750.0', '6750.0', '6750.0', '6750.0', '720.0', '0.0011116172934978368', '0.0', '6800', '6800', '6800', '6800', '6800', '6800', '6800', '6800', '6800', '6800', '6800'], ['POST', 'ImportFileEMDLK', '1', '0', '2031.000000424683', '2031.000000424683', '2031.000000424683', '2031.000000424683', '720.0', '0.0011116172934978368', '0.0', '2000', '2000', '2000', '2000', '2000', '2000', '2000', '2000', '2000', '2000', '2000'], ['POST', 'ImportFileLK', '1', '0', '7859.000000171363', '7859.000000171363', '7859.000000171363', '7859.000000171363', '715.0', '0.0011116172934978368', '0.0', '7900', '7900', '7900', '7900', '7900', '7900', '7900', '7900', '7900', '7900', '7900'], ['GET', 'QueryErrorDataEmdlk', '4309', '0', '62', '121.06938964915742', '30.99999949336052', '1405.9999994933605', '70661.65212346253', '4.789958917682179', '0.0', '62', '78', '140', '190', '300', '380', '560', '670', '920', '1400', '1400'], ['GET', 'QueryErrorDatalk', '4383', '0', '78', '141.8578599171873', '46.00000008940697', '1234.0000001713634', '96064.30435774583', '4.872218597401019', '0.0', '78', '110', '170', '220', '330', '420', '580', '690', '980', '1200', '1200']]

class ReadCsv:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_csv(self):
        result = []
        with open(self.file_name, encoding='utf-8-sig') as f:
            for row in csv.reader(f, skipinitialspace=True):
                if row:
                    result.append(row)
        return result[1:-1]


class DoExcel:

    def __init__(self, filename):
        """
        1、初始化对象，打开相应文件
        2、打开配置文件获取test模块中upload_url
        :param filename:
        """
        self.filename = filename


    def write_sheet_data(self,value):
        """
        # 获取指定文件内指定sheet内容
        1、根据sheet行数进行判断，把每一行读取出来的数据转为字典，并且把字典拼接为列表
        :param sheet_name:需要打开的sheet
        :return:
        """

        # load_workbook() 一个参数,加载xlsl文件的路径,续写.
        wb = openpyxl.load_workbook(self.filename)
        # 对xlsx文件操作之前,要 active.
        wa = wb.active
        # append() 一个参数,列表,写入的一行.
        wa.append([value[1],value[2],round(float(value[4]), 2),value[16],value[18],value[21],round(float(value[5]), 2)])
        # save() 一个参数,保存路径
        wb.save(self.filename)
        wb.close()



if __name__ == '__main__':
    # DoExcel('result.xlsx').write_sheet_data(2)
    value =ReadCsv('E:\PycharmProjects\Performance\\result\\2023-04-13_151342\_stats.csv').read_csv()[0]
    print(value)
