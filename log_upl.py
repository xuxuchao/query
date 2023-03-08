# -*- coding:utf-8 -*-

import os
import logging
import datetime
import colorlog


logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(logs):  # 判断logs目录是否存在
    os.mkdir(logs)




class MyLog(object):

    now_time = datetime.datetime.now().strftime('%Y-%m-%d')

    report_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

    log_path_all = os.path.join(report_root, "upl_all_" + now_time + ".log")  # log存放路径-all
    log_path_error = os.path.join(report_root, "upl_error_" + now_time + ".log")  # log存放路径-error

    # 设置控制台打印的颜色
    log_colors_config = {
        'DEBUG': 'black',
        'INFO': 'cyan',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    }

    def __init__(self, details=None):
        # 设置输出格式-控制台
        self.ch_formatter = colorlog.ColoredFormatter(
            '%(log_color) s%(asctime)s | %(filename)s-%(lineno)d | [%(levelname)s] : %(message)s',
            log_colors=self.log_colors_config)
        # 设置输出格式-文件
        self.fh_formatter = logging.Formatter(
            '%(asctime)s | %(filename)s-%(lineno)d | [%(levelname)s] : %(message)s')
        # 定义一个日志收集器
        self.my_logger = logging.getLogger(details)
        # 设定级别-默认级别
        self.my_logger.setLevel(logging.INFO)
        # 设置输出到文件的位置
        self.all_log = logging.FileHandler(filename=self.log_path_all, encoding='utf-8')
        self.all_log.setLevel(logging.INFO)
        self.error_log = logging.FileHandler(filename=self.log_path_error, encoding='utf-8')
        self.error_log.setLevel(logging.ERROR)

        # 创建一个handler，用于输出到控制台
        self.console = logging.StreamHandler()
        # 设置输出到控制台级别
        self.console.setLevel(level=logging.INFO)

        # 输出渠道对接输出格式
        self.console.setFormatter(self.ch_formatter)
        self.all_log.setFormatter(self.fh_formatter)
        self.error_log.setFormatter(self.fh_formatter)

        # 日志收集器对接输出渠道
        self.my_logger.addHandler(self.console)
        self.my_logger.addHandler(self.all_log)
        self.my_logger.addHandler(self.error_log)

    def get_log(self):
        return self.my_logger


log = MyLog().get_log()

if __name__ == '__main__':

    log.info('111')