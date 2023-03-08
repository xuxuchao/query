# encoding=utf-8

import os
cmd = "sqlldr userid=opraupl/acca1234@10.1.26.182:1521/uplpt control='E:\PycharmProjects\query\sqlldr\cpd.ctl' streamsize=10485760 date_cache=5000 readsize=10485760"
os.system(cmd)

