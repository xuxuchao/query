import os
import time,requests
from tkinter import *
from tkinter import ttk
from toolTio import createToolTip
from tkinter import messagebox
from connect_Orcale import OracleConnect
from login import login
from api_key import get_apikeys
from base_page import BaseData
from read_file import ReadCsv,DoExcel


detail_sql = ''

class start(BaseData):
    def __init__(self,root):
        self.parent = root
        super().__init__()
        self.notebook()
        self.page_one_frame_one()
        self.page_one_frame_two()
        self.page_one_frame_three()
        self.page_one_button()
        self.page_one_response()
        self.page_two_one()
        self.page_three_one()
        self.page_four()

    def notebook(self):
        self.notebook = ttk.Notebook()
        self.frame1 = Frame(self.parent)
        self.frame2 = Frame(self.parent)
        self.frame3 = Frame(self.parent)
        self.frame4 = Frame(self.parent)


        self.notebook.add(self.frame1, text='配比还原')
        self.notebook.add(self.frame2, text='查询票号')
        self.notebook.add(self.frame3, text='生成平均票价')
        self.notebook.add(self.frame4, text='TPS/响应时间统计')


        self.notebook.pack(padx=5, pady=5, fill=BOTH, expand=TRUE)

    def page_one_frame_one(self):
        self.__var = IntVar()
        self.__var.set(1)
        # 选择环境
        frame_one = LabelFrame(self.frame1, text="选择需要操作的环境")
        huanjing = {0: "开发环境", 1: "测试环境", 2: "东航UAT", 3: "南航UAT", 4: "国航生产", 5: "南航生产", 6: "东航生产", 7: "性能环境"}
        for val,name in huanjing.items():
            Radiobutton(frame_one, text=name, indicatoron=0, width=27,variable=self.__var, value=val, command=self.pthuanjing).pack(anchor=W)

        frame_one.pack(padx=10,pady=10,ipadx=5,ipady=5,anchor=W)

    def page_one_frame_two(self):
        self.carrier_e1 = StringVar()    # 承运人
        self.flight_no_e1 = StringVar()   # 航班号
        self.flight_departure_date_e1 = StringVar()   # 飞行日期
        self.origin_airport_city_code_e1 = StringVar()     # 始发站

        # 输入参数
        frame = LabelFrame(self.frame1, text="参数")
        carrier = Label(frame, text="*承运人")
        carrier.grid(row=0, column=0)
        flight_no = Label(frame, text="*航班号")
        flight_no.grid(row=1, column=0)
        flight_departure_date = Label(frame, text="*飞行日期")
        flight_departure_date.grid(row=2, column=0)
        origin_airport_city_code = Label(frame, text="始发站")
        origin_airport_city_code.grid(row=3, column=0)

        carrier_e = Entry(frame, textvariable=self.carrier_e1)
        carrier_e.grid(row=0, column=1, pady=5, padx=5)
        flight_no_e = Entry(frame, textvariable=self.flight_no_e1)
        flight_no_e.grid(row=1, column=1, pady=5, padx=5)
        flight_departure_date_e = Entry(frame, textvariable=self.flight_departure_date_e1)
        flight_departure_date_e.grid(row=2, column=1, pady=5, padx=5)
        origin_airport_city_code_e = Entry(frame, textvariable=self.origin_airport_city_code_e1)
        origin_airport_city_code_e.grid(row=3, column=1, pady=5, padx=5)
        frame.place(x=250, y=10)
        createToolTip(origin_airport_city_code_e, '还原和删除数据，始发站支持录入多个，逗号分割')

    def page_one_frame_three(self):
        self.campartmente_e1 = StringVar()
        self.pax_count_uplift_e1 = StringVar()
        self.pax_count_uplift_departure_e1 = StringVar()
        self.passenger_count_variance_e1 = StringVar()
        self.ticket_no_variance_e1 = StringVar()
        self.ticket_no_variance_processing_count_e1 = StringVar()
        self.accounting_pax_count_variance_e1 = StringVar()
        self.not_revenue_passenger_count_e1 = StringVar()
        self.revenue_passenger_count_e1 = StringVar()
        self.ticket_no_variance_processing_status_e1 = StringVar()

        # 配比执行结果
        frame3 = LabelFrame(self.frame1, text="汇总表数据")
        campartment = Label(frame3, text="主舱位")
        campartment.grid(row=0, column=0)
        pax_count_uplift = Label(frame3, text="运输旅客人数")
        pax_count_uplift.grid(row=1, column=0)
        pax_count_uplift_departure = Label(frame3, text="离港旅客人数")
        pax_count_uplift_departure.grid(row=2, column=0)
        passenger_count_variance = Label(frame3, text="旅客人数差异数")
        passenger_count_variance.grid(row=3, column=0)
        ticket_no_variance = Label(frame3, text="票号不匹配人数")
        ticket_no_variance.grid(row=4, column=0)
        ticket_no_variance_processing_count = Label(frame3, text="票号不匹配处理数")
        ticket_no_variance_processing_count.grid(row=5, column=0)
        accounting_pax_count_variance = Label(frame3, text="记账旅客人数差异数")
        accounting_pax_count_variance.grid(row=6, column=0)
        not_revenue_passenger_count = Label(frame3, text="不估算收入人数")
        not_revenue_passenger_count.grid(row=7, column=0)
        revenue_passenger_count = Label(frame3, text="估算收入人数")
        revenue_passenger_count.grid(row=8, column=0)
        ticket_no_variance_processing_status = Label(frame3, text="票号不匹配处理状态")
        ticket_no_variance_processing_status.grid(row=9, column=0)

        campartmente_e = Entry(frame3, textvariable=self.campartmente_e1, state=DISABLED, justify='center')
        campartmente_e.grid(row=0, column=1, pady=0, padx=5)
        pax_count_uplift_e = Entry(frame3, textvariable=self.pax_count_uplift_e1, state=DISABLED, justify='center')
        pax_count_uplift_e.grid(row=1, column=1, pady=0, padx=5)
        pax_count_uplift_departure_e = Entry(frame3, textvariable=self.pax_count_uplift_departure_e1, state=DISABLED,
                                             justify='center')
        pax_count_uplift_departure_e.grid(row=2, column=1, pady=0, padx=5)
        passenger_count_variance_e = Entry(frame3, textvariable=self.passenger_count_variance_e1, state=DISABLED,
                                           justify='center')
        passenger_count_variance_e.grid(row=3, column=1, pady=0, padx=5)
        ticket_no_variance_e = Entry(frame3, textvariable=self.ticket_no_variance_e1, state=DISABLED,
                                     justify='center')
        ticket_no_variance_e.grid(row=4, column=1, pady=0, padx=5)
        ticket_no_variance_processing_count_e = Entry(frame3,
                                                      textvariable=self.ticket_no_variance_processing_count_e1,
                                                      state=DISABLED,
                                                      justify='center')
        ticket_no_variance_processing_count_e.grid(row=5, column=1, pady=0, padx=5)
        accounting_pax_count_variance_e = Entry(frame3, textvariable=self.accounting_pax_count_variance_e1,
                                                state=DISABLED, justify='center')
        accounting_pax_count_variance_e.grid(row=6, column=1, pady=0, padx=5)
        not_revenue_passenger_count_e = Entry(frame3, textvariable=self.not_revenue_passenger_count_e1,
                                              state=DISABLED, justify='center')
        not_revenue_passenger_count_e.grid(row=7, column=1, pady=0, padx=5)
        revenue_passenger_count_e = Entry(frame3, textvariable=self.revenue_passenger_count_e1, state=DISABLED,
                                          justify='center')
        revenue_passenger_count_e.grid(row=8, column=1, pady=0, padx=5)
        ticket_no_variance_processing_status_e = Entry(frame3,
                                                       textvariable=self.ticket_no_variance_processing_status_e1,
                                                       state=DISABLED, justify='center')
        ticket_no_variance_processing_status_e.grid(row=9, column=1, pady=0, padx=5)

        frame3.place(x=600, y=10)

    def page_one_button(self):
        btn1 = Button(self.frame1, text="执行配比", width=20, command=self.match, bg="gray")
        btn1.place(x=250, y=160)

        btn2 = Button(self.frame1, text="还原数据", width=20, command=self.reduction, bg="gray")

        btn2.place(x=250, y=195)

        btn3 = Button(self.frame1, text="删除汇总数据", width=20, command=self.delete, bg="gray", fg='red')

        btn3.place(x=250, y=230)

        btn4 = Button(self.frame1, text="重置", width=8, command=self.clear, bg="#bdbebd")
        btn4.place(x=500, y=230)

        btn5 = Button(self.frame1, text="查询", width=8, command=self.query, bg="#bdbebd")
        btn5.place(x=420, y=230)

        # Add Tooltip
        createToolTip(btn1, '调用配比接口实现单航班配比')
        createToolTip(btn2, '还原输入参数的CPD/LK/EMDLK/FIM字段:TICKET_VARIANCE_IND=N/TICKET_MATCH_FLAG=null')
        createToolTip(btn3, '删除输入参数的SUMMARY/DETAIL/REASON表的数据')
        createToolTip(btn4, '清空执行结果和输入参数内容')

    def page_one_response(self):
        page1_frame2 = LabelFrame(self.frame1, text="执行结果")
        scrollbar = Scrollbar(page1_frame2)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.sql_deteil_e = Listbox(page1_frame2, width=500, height=100, yscrollcommand=scrollbar.set)
        self.sql_deteil_e.insert(END, "当前默认环境为测试环境")
        self.sql_deteil_e.pack()
        page1_frame2.pack(padx=10, pady=5, ipadx=5, ipady=5, side=LEFT)

    def page_two_one(self):
        # 页面二
        btn1 = Button(self.frame2, text="查询", width=10, command=self.query_ticket_no, bg="#bdbebd")

        # 输入参数
        page2_frame01 = LabelFrame(self.frame2, text="参数")
        file_path = Label(page2_frame01, text="文件路径")
        file_path.grid(row=0, column=0)
        ticket_no = Label(page2_frame01, text="复制txt文件内容")
        ticket_no.grid(row=1, column=0)

        self.file_path_e1 = StringVar()
        file_path_e = Entry(page2_frame01, textvariable=self.file_path_e1, width=50)
        file_path_e.grid(row=0, column=1, pady=5, padx=5)

        self.ticket_no_e1 = StringVar()
        ticket_no_e = Entry(page2_frame01, textvariable=self.ticket_no_e1, width=50)
        ticket_no_e.grid(row=1, column=1, pady=5, padx=5)

        page2_frame03 = LabelFrame(self.frame2, text="结果")

        scrollbar = Scrollbar(page2_frame03)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.text = Text(page2_frame03,width=120,height=25 ,yscrollcommand=scrollbar.set)
        self.text.insert(END, "只支持查询txt格式的文件")
        self.text.pack()
        page2_frame03.grid(row=4, column=0,padx=10,columnspan=5,pady=10)

        btn1.grid(row=2,column=3, padx=10, pady=20)
        page2_frame01.grid(row=1, column=0,rowspan=2,columnspan=5,sticky=W,padx=10)


    def page_three_one(self):
        # 页面三
        btn3_1 = Button(self.frame3, text="执行", width=10, command=self.pricessing_month_do, bg="#bdbebd")
        btn3_1.grid(row=2,column=3, padx=10, pady=5)


        # 输入参数
        page2_frame01 = LabelFrame(self.frame3, text="参数")
        carrier_3 = Label(page2_frame01, text="CARRIER")
        carrier_3.grid(row=0, column=0)
        processing_month_3 = Label(page2_frame01, text="PROCESSING_MONTH")
        processing_month_3.grid(row=1, column=0)
        page2_frame01.grid(row=1, column=0,rowspan=2,columnspan=5,sticky=W,padx=10)

        self.carriere_3 = StringVar()
        carrier_e = Entry(page2_frame01, textvariable=self.carriere_3, width=50)
        carrier_e.insert(0,"CA")
        carrier_e.grid(row=0, column=1, pady=5, padx=5)

        self.processing_monthe_3 = StringVar()
        pro_month_e = Entry(page2_frame01, textvariable=self.processing_monthe_3, width=50)
        pro_month_e.insert(0,"202205")
        pro_month_e.grid(row=1, column=1, pady=5, padx=5)

        self.text3 = Text(self.frame3,width=120)
        self.text3.grid(row=5, column=0,columnspan=5,padx=10)

        self.__var2 = IntVar()
        self.__var2.set(1)
        self.text3.insert(END, "当前默认环境为测试环境\n")

        self.__var3 = IntVar()
        self.__var3.set(0)


        # 选择环境
        frame_one = LabelFrame(self.frame3, text="选择需要生成平均票价的环境")
        huanjing = {0: "开发环境", 1: "测试环境", 2: "东航UAT", 3: "南航UAT",4: "国航生产", 5: "南航生产", 6: "东航生产", 7: "性能环境"}

        # 选择
        frame_two = LabelFrame(self.frame3, text="季平均/月平均")
        ji_or_mon = {0: "季平均", 1: "月平均"}

        for val,name in huanjing.items():
            Radiobutton(frame_one, text=name, indicatoron=0,width=9,variable=self.__var2, value=val, command=self.pthuanjing2,
                        compound="right").pack(anchor=E,side=LEFT,pady=5, padx=2)
        frame_one.grid(row=3,column=0,sticky=W,padx=10, pady=10,columnspan=4)

        for val, name in ji_or_mon.items():
            Radiobutton(frame_two, text=name, indicatoron=1, width=9, variable=self.__var3, value=val, command=self.ptjiormon,
                        compound="right").pack(anchor=E, side=LEFT, pady=5, padx=2)
        frame_two.grid(row=3, column=1, sticky=E, padx=10, pady=10, columnspan=4)

    def page_four(self):
        # 页面四
        btn4_1 = Button(self.frame4, text="获取", width=10, command=self.parse_file, bg="#bdbebd")
        btn4_1.grid(row=2, column=4, padx=10, pady=5)

        # 输入参数
        page4_frame01 = LabelFrame(self.frame4, text="-")
        report_s = Label(page4_frame01, text="测试报告路径")
        report_s.grid(row=0, column=0)
        save_s = Label(page4_frame01, text="保存文件路径")
        save_s.grid(row=1, column=0)
        start_row_s = Label(page4_frame01, text="起始行")
        start_row_s.grid(row=2, column=0)
        start_col_s = Label(page4_frame01, text="起始列")
        start_col_s.grid(row=2, column=3)
        page4_frame01.grid(row=1, column=0, rowspan=2, columnspan=5, sticky=W, padx=10)

        self.report_v = StringVar()
        report_b = Entry(page4_frame01, textvariable=self.report_v, width=50)
        report_b.insert(0, "E://")
        report_b.grid(row=0, column=1, columnspan=4, pady=5, padx=5)

        self.save_v = StringVar()
        save_b = Entry(page4_frame01, textvariable=self.save_v, width=50)
        save_b.insert(0, "D://result.xlsx")
        save_b.grid(row=1, column=1, pady=5, columnspan=4,padx=5)

        self.start_row = StringVar()
        save_b = Entry(page4_frame01, textvariable=self.start_row, width=10)
        save_b.insert(0, "1")
        save_b.grid(row=2, column=2, pady=5, padx=5)

        self.start_col = StringVar()
        save_b = Entry(page4_frame01, textvariable=self.start_col, width=10)
        save_b.insert(0, "1")
        save_b.grid(row=2, column=4, pady=5, padx=5)

        self.text4 = Text(self.frame4, width=120)
        self.text4.grid(row=4, column=0, columnspan=7, padx=10,pady=20)



# --------------------------------------------------------------------------------------------------------------------------------------------

    def pricessing_month_do(self):
        token = login(f"{self._url_list[self.__var2.get()]}").login()

        carrier = self.carriere_3.get().upper().strip()
        processing_month = self.processing_monthe_3.get().strip()
        if not carrier:
            self.text3.insert(END, "承运人不能为空\n")
        elif carrier == 'TEST':
            self.text3.insert(END,
                '''select *  from UPL_TICKET_PAX WHERE flight_no='6381' AND FLOWN_DEPARTURE_DATE=date '2022-07-06' AND ORIGIN_AIRPORT_CITY_CODE='KWE';\nselect *  from UPL_DCS_CPD WHERE OPERATING_FLIGHT_NO='6381' AND FLIGHT_FIRST_LEG_DEPARTURE_DATE=date '2022-07-06' AND ORIGIN_AIRPORT_CITY_CODE='KWE';\nselect *  from UPL_DCS_CfD where ORIGINAL_FLIGHT_NO='6381' AND FLIGHT_1ST_LEG_DEPARTURE_DATE=date '2022-07-06' AND ORIGIN_AIRPORT_CITY_CODE='KWE';\nselect * from upl_load_pax_variance_detail where FLIGHT_NO='6381' and FIRST_LEG_FLIGHT_DEPARTURE_DATE=date '2022-07-06';\nselect * from upl_load_pax_variance_summary where FLIGHT_NO='6381' and FLIGHT_DEPARTURE_DATE=date '2022-07-06';\nselect * from upl_load_pax_variance_reason where FLIGHT_NO='6381' and FLIGHT_DEPARTURE_DATE=date '2022-07-06';\n'''
            )
        elif not processing_month:
            self.text3.insert(END, "处理月不能为空\n")
        else:
            self.page3_btn3_1Click()
            if self.__var2.get() < 1:
                if self.__var3.get() == 0:
                    url = self._process_url.replace("MU", carrier).replace("202105", processing_month)
                else:
                    url = self._process_url_m.replace("MU", carrier).replace("202105", processing_month)
            else:
                if self.__var3.get() == 0:
                    url = self._process_url2.replace('ly', f'{self._url_host_list[self.__var2.get()]}').replace("MU",carrier).replace("202105", processing_month)
                else:
                    url = self._process_url2_m.replace('ly', f'{self._url_host_list[self.__var2.get()]}').replace("MU",carrier).replace("202105", processing_month)

            self.text3.insert(END, f'{url}\n')
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "Accept-Language": "zh-CN"
            }
            if self.__var3.get() ==0:
                headers["ApiKeys"] = get_apikeys(headers=headers,
                                                 url="/upl-common/uplCalAveragePax/createEstimateSap/MU/202105".replace(
                                                     "MU", carrier).replace("202105", processing_month), method="get",
                                                 params=None)
            else:
                headers["ApiKeys"] = get_apikeys(headers=headers,
                                                 url="/upl-common/uplCalAveragePax/createEstimateMap/MU/202105".replace(
                                                     "MU",carrier).replace("202105", processing_month), method="get",
                                                 params=None)

            attempts = 0
            success = False
            while attempts < 5 and not success:
                try:
                    requests.packages.urllib3.disable_warnings()
                    r = requests.get(url=url, params=None, headers=headers, verify=False)
                    success = True
                    self.text3.insert(END, f"执行结果为：{r.status_code}\n")

                except Exception as e:
                    self.text3.insert(END, f"执行结果为：{e},\n重试中\n")
                    attempts += 1
                    time.sleep(2)
                    if attempts == 5:
                        return
    def match(self):
        token = login(f"{self._url_list[self.__var.get()]}").login()
        if self.__var.get() < 1:
            url = self._base_match_url
        else:
            url = self._base_match_url2.replace('ly', f'{self._url_host_list[self.__var.get()]}')
        carrier = self.carrier_e1.get().upper().strip()
        flight_no = self.flight_no_e1.get().strip()
        flight_date = self.flight_departure_date_e1.get().strip()
        if "-" in flight_date:
            flight_departure_date = flight_date
        else:
            flight_departure_date = flight_date[0:4] + "-" + flight_date[4:6] + "-" + flight_date[6:8]
        origin_airport_city_code = self.origin_airport_city_code_e1.get().upper().strip()
        if not carrier:
            self.sql_deteil_e.insert(END, "承运人不能为空")
        elif not flight_no:
            self.sql_deteil_e.insert(END, "航班号不能为空")
        elif not flight_departure_date:
            self.sql_deteil_e.insert(END, "飞行日期不能为空")
        elif not origin_airport_city_code:
            self.sql_deteil_e.insert(END, "始发站不能为空")
        elif len(origin_airport_city_code) > 3:
            self.sql_deteil_e.insert(END, "执行配比,始发站长度不能超过3位")
        else:
            self.sql_deteil_e.insert(END, "开始执行配比操作")
            data = {
                "operatingCarrier": f"{carrier}",
                "operatingFlightNo": f"{flight_no}",
                "origin_airport_city_code": f"{origin_airport_city_code}",
                "segmentScheduleDepartureDate": f"{flight_departure_date}"
            }
            self.sql_deteil_e.insert(END, f"URL:{url}")
            self.sql_deteil_e.insert(END, f"DATA:{data}")
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "Accept-Language": "zh-CN"
            }
            headers["ApiKeys"] = get_apikeys(headers=headers, url="/upl-common/UplPassengerCount/diff/other/match",
                                             method="put", params=None)

            attempts = 0
            success = False
            while attempts < 5 and not success:
                try:
                    requests.packages.urllib3.disable_warnings()
                    r = requests.put(url=url, json=data, headers=headers, verify=False)
                    success = True
                    self.sql_deteil_e.insert(END, f"执行配比结果为：{r.json()}")
                except Exception as e:
                    self.sql_deteil_e.insert(END, f"执行配比结果为：{e},重试中")
                    attempts += 1
                    time.sleep(2)
                    if attempts == 5:
                        return
            self.query()

    def pthuanjing(self):
        hj_l = self._huanjing_list[self.__var.get()]
        self.sql_deteil_e.insert(END, f"当前选择环境为{hj_l}环境")


    def pthuanjing2(self):
        hj_l = self._huanjing_list[self.__var2.get()]
        self.text3.insert(END,f"当前选择环境为{hj_l}环境\n")

    def ptjiormon(self):
        jm_l = self._jiormon_list[self.__var3.get()]
        self.text3.insert(END,f"选择需要生成{jm_l}\n")

    def clear(self):
        self.sql_deteil_e.delete(0, END)
        self.carrier_e1.set("")
        self.flight_no_e1.set("")
        self.flight_departure_date_e1.set("")
        self.origin_airport_city_code_e1.set("")
        self.__var.set(1)
        self.sql_deteil_e.insert(END, "当前默认环境为测试环境")

    def query_ticket_no(self):
        base_path = self.file_path_e1.get()
        file_list = os.listdir(path=base_path)
        for f in file_list:
            file_path = base_path + '\\' + f
            if file_path.endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8') as file:
                    s = file.read()
                    b = os.path.basename(file_path)
                    if self.ticket_no_e1.get() in s:
                        a = f'{self.ticket_no_e1.get()}在文件{b}里---！'
                        self.text.insert(END, a)
                        self.text.insert(END, '\n')
                    else:
                        self.text.insert(END, f'{b}文件里面没有')
                        self.text.insert(END, '\n')
                    file.close()
            else:
                continue

    def query(self):
        self.campartmente_e1.set('')
        self.pax_count_uplift_e1.set('')
        self.pax_count_uplift_departure_e1.set('')
        self.passenger_count_variance_e1.set('')
        self.ticket_no_variance_e1.set('')
        self.ticket_no_variance_processing_count_e1.set('')
        self.accounting_pax_count_variance_e1.set('')
        self.not_revenue_passenger_count_e1.set('')
        self.revenue_passenger_count_e1.set('')
        self.ticket_no_variance_processing_status_e1.set('')

        huanjing = self._oracle_list[self.__var.get()]
        carrier = self.carrier_e1.get().upper().strip()
        flight_no = self.flight_no_e1.get().strip()
        flight_date = self.flight_departure_date_e1.get().strip()
        if "-" in flight_date:
            flight_departure_date = flight_date
        else:
            flight_departure_date = flight_date[0:4] + "-" + flight_date[4:6] + "-" + flight_date[6:8]
        origin_airport_city_code = self.origin_airport_city_code_e1.get().upper().strip()

        if not carrier:
            self.sql_deteil_e.insert(END, "承运人不能为空")
        elif not flight_no:
            self.sql_deteil_e.insert(END, "航班号不能为空")
        elif not flight_departure_date:
            self.sql_deteil_e.insert(END, "飞行日期不能为空")
        elif not origin_airport_city_code:
            self.sql_deteil_e.insert(END, "始发站不能为空")
        elif len(origin_airport_city_code) > 3:
            self.sql_deteil_e.insert(END, "始发站长度不能超过3位")
        else:
            sql = f'''
                SELECT COMPARTMENT,
                PAX_COUNT_FROM_UPLIFT_DATA,
                PAX_COUNT_FROM_DEPARTURE_DATA,
                PASSENGER_COUNT_VARIANCE,
                TICKET_NO_VARIANCE,
                TICKET_NO_VARIANCE_PROCESSING_COUNT,
                ACCOUNTING_PAX_COUNT_VARIANCE,
                NOT_REVENUE_PASSENGER_COUNT,
                REVENUE_PASSENGER_COUNT,
                TICKET_NO_VARIANCE_PROCESSING_STATUS
                FROM OPRAUPL.UPL_LOAD_PAX_VARIANCE_SUMMARY WHERE CARRIER='{carrier}' AND FLIGHT_DEPARTURE_DATE=DATE '{flight_departure_date}' AND ORIGIN_AIRPORT_CITY_CODE='{origin_airport_city_code}' AND FLIGHT_NO='{flight_no}'
            '''
            res = OracleConnect(db_name=f"{huanjing}").sql_select(sql)
            if res:
                campartmente_f1, pax_count_uplift_f1, pax_count_uplift_departure_f1, passenger_count_variance_f1, ticket_no_variance_f1 = [], [], [], [], []
                ticket_no_variance_f1, ticket_no_variance_processing_count_f1, accounting_pax_count_variance_f1, not_revenue_passenger_count_f1, revenue_passenger_count_f1, ticket_no_variance_processing_status_f1 = [], [], [], [], [], []

                for i in res:
                    campartmente_f1.append(i[0])
                    pax_count_uplift_f1.append(i[1])
                    pax_count_uplift_departure_f1.append(i[2])
                    passenger_count_variance_f1.append(i[3])
                    ticket_no_variance_f1.append(i[4])
                    ticket_no_variance_processing_count_f1.append(i[5])
                    accounting_pax_count_variance_f1.append(i[6])
                    not_revenue_passenger_count_f1.append(i[7])
                    revenue_passenger_count_f1.append(i[8])
                    ticket_no_variance_processing_status_f1.append(i[9])
                self.campartmente_e1.set(campartmente_f1)
                self.pax_count_uplift_e1.set(pax_count_uplift_f1)
                self.pax_count_uplift_departure_e1.set(pax_count_uplift_departure_f1)
                self.passenger_count_variance_e1.set(passenger_count_variance_f1)
                self.ticket_no_variance_e1.set(ticket_no_variance_f1)
                self.ticket_no_variance_processing_count_e1.set(ticket_no_variance_processing_count_f1)
                self.accounting_pax_count_variance_e1.set(accounting_pax_count_variance_f1)
                self.not_revenue_passenger_count_e1.set(not_revenue_passenger_count_f1)
                self.revenue_passenger_count_e1.set(revenue_passenger_count_f1)
                self.ticket_no_variance_processing_status_e1.set(ticket_no_variance_processing_status_f1)
            else:
                self.sql_deteil_e.insert(END, "汇总表无数据")

    def reduction(self):
        huanjing = self._oracle_list[self.__var.get()]
        carrier = self.carrier_e1.get().upper().strip()
        flight_no = self.flight_no_e1.get().strip()
        flight_date = self.flight_departure_date_e1.get().strip()
        if "-" in flight_date:
            flight_departure_date = flight_date
        else:
            flight_departure_date = flight_date[0:4] + "-" + flight_date[4:6] + "-" + flight_date[6:8]
        origin_airport_city_code = self.origin_airport_city_code_e1.get().upper().strip()

        if not carrier:
            self.sql_deteil_e.insert(END, "承运人不能为空")
        elif not flight_no:
            self.sql_deteil_e.insert(END, "航班号不能为空")
        elif not flight_departure_date:
            self.sql_deteil_e.insert(END, "飞行日期不能为空")
        elif self.btn2Click() == "no":
            self.sql_deteil_e.insert(END, "取消还原数据操作")
        else:
            self.sql_deteil_e.insert(END, "开始执行还原数据操作")
            if not origin_airport_city_code:
                end_sql = ''
            else:
                end_sql = f" AND ORIGIN_AIRPORT_CITY_CODE IN ('{origin_airport_city_code}')".replace(",","','").replace("，","','")
                fim_end_sql = f" AND RECEIVING_ORIGIN1 IN ('{origin_airport_city_code}')".replace(",", "','").replace("，", "','")

            update_sql = [
                f"UPDATE OPRAUPL.UPL_DCS_CPD SET TICKET_VARIANCE_IND='N',UPLIFT_DATA_SEQUENCE='',UPLIFT_DATA_SOURCE='',TICKET_MATCH_FLAG=null WHERE OPERATING_CARRIER='{carrier}' AND OPERATING_FLIGHT_NO='{flight_no}' AND  FLIGHT_FIRST_LEG_DEPARTURE_DATE=DATE '{flight_departure_date}' AND TICKET_VARIANCE_IND IN ('Y','N') {end_sql}",
                f"UPDATE OPRAUPL.UPL_DCS_CPD SET  REMARK='',VERIFIED_FIM_NO='',VERIFIED_TICKET_NO='' WHERE OPERATING_CARRIER='{carrier}' AND OPERATING_FLIGHT_NO='{flight_no}' AND  FLIGHT_FIRST_LEG_DEPARTURE_DATE=DATE '{flight_departure_date}' AND TICKET_VARIANCE_IND IN ('Y','N') {end_sql}",
                f"UPDATE OPRAUPL.UPL_TICKET_PAX SET TICKET_VARIANCE_IND='N',TICKET_MATCH_FLAG=null WHERE CARRIER='{carrier}' AND FLIGHT_NO='{flight_no}' AND  FLOWN_DEPARTURE_DATE=DATE '{flight_departure_date}' AND TICKET_VARIANCE_IND IN ('Y','N') {end_sql}",
                # "update upl_dcs_cpd set ticket_no='',PREFIX='' where sequence in ('1037653740095991810','1037653740095991811','1037653740104380416','1037653739605258242','1037653740024750082')",
                f"UPDATE OPRAUPL.UPL_DCS_ETCD SET TICKET_VARIANCE_IND='N',TICKET_MATCH_FLAG=null WHERE OPERATING_CARRIER='{carrier}' AND OPERATING_FLIGHT_NO='{flight_no}' AND  SEGMENT_SCHEDULE_DEPARTURE_DATE=DATE '{flight_departure_date}' AND TICKET_VARIANCE_IND IN ('Y','N') {end_sql}",
                f"UPDATE OPRAUPL.UPL_TICKET_FIM_TO_DETAIL SET TICKET_MATCH_FLAG=null,TICKET_VARIANCE_IND='N' WHERE TICKET_VARIANCE_IND='Y' AND RELATED_TICKET_NO IN (SELECT PREFIX || TICKET_NO FROM OPRAUPL.UPL_TICKET_FIM_TO WHERE RECEIVING_FLIGHT_NO1 = '{flight_no}' AND RECEIVING_FLIGHT_DEPARTURE_DATE1 = DATE '{flight_departure_date}' {fim_end_sql})"
            ]
            do_sql = []
            for sql in update_sql:
                OracleConnect(db_name=f"{huanjing}").sql_iud(sql)
                do_sql.append(sql)
            for detail in do_sql:
                time.sleep(0.5)
                self.sql_deteil_e.insert(END, detail)
            self.sql_deteil_e.insert(END, "还原数据成功")


    def delete(self):
        huanjing = self._oracle_list[self.__var.get()]

        carrier = self.carrier_e1.get().upper().strip()
        flight_no = self.flight_no_e1.get().strip()
        flight_date = self.flight_departure_date_e1.get().strip()
        if "-" in flight_date:
            flight_departure_date = flight_date
        else:
            flight_departure_date = flight_date[0:4] + "-" + flight_date[4:6] + "-" + flight_date[6:8]
        origin_airport_city_code = self.origin_airport_city_code_e1.get().upper().strip()

        if not carrier:
            self.sql_deteil_e.insert(END, "承运人不能为空")
        elif not flight_no:
            self.sql_deteil_e.insert(END, "航班号不能为空")
        elif not flight_departure_date:
            self.sql_deteil_e.insert(END, "飞行日期不能为空")
        elif self.btn3Click() == "no":
            self.sql_deteil_e.insert(END, "取消删除数据操作")
        else:
            self.sql_deteil_e.insert(END, "开始执行删除数据操作")
            if not origin_airport_city_code:
                end_sql = ''
            else:
                end_sql = f" AND ORIGIN_AIRPORT_CITY_CODE IN ('{origin_airport_city_code}')".replace(",","','").replace("，","','")

            delete_sql = [
                f"DELETE FROM OPRAUPL.UPL_LOAD_PAX_VARIANCE_SUMMARY WHERE CARRIER='{carrier}' AND FLIGHT_NO='{flight_no}' AND FLIGHT_DEPARTURE_DATE=DATE '{flight_departure_date}' {end_sql}",
                f"DELETE FROM OPRAUPL.UPL_LOAD_PAX_VARIANCE_DETAIL WHERE OPERATING_CARRIER='{carrier}' AND FLIGHT_NO='{flight_no}' AND FIRST_LEG_FLIGHT_DEPARTURE_DATE=DATE '{flight_departure_date}' {end_sql}",
                f"DELETE FROM OPRAUPL.UPL_LOAD_PAX_VARIANCE_REASON WHERE CARRIER='{carrier}' AND FLIGHT_NO='{flight_no}' AND FLIGHT_DEPARTURE_DATE=DATE '{flight_departure_date}' {end_sql}"
            ]
            do_sql2 = []
            for sql in delete_sql:
                OracleConnect(db_name=f"{huanjing}").sql_iud2(sql)
                do_sql2.append(sql)
            for detail in do_sql2:
                time.sleep(0.5)
                self.sql_deteil_e.insert(END, detail)
            self.sql_deteil_e.insert(END, "删除数据成功")

    def parse_file(self):
        result = ReadCsv(self.report_v.get() + '\\_stats.csv').read_csv()
        j = 1
        for i in result:
            k = str(j)+ '-' +i[0]+'-' +i[1]+'-' +i[2]
            self.text4.insert(END, k)
            self.text4.insert(END, '\n')
            print(i)
            DoExcel(self.save_v.get()).write_sheet_data(i)
            j+=1


    @staticmethod
    def btn3Click():
        res = messagebox.askquestion(
            "操作提示", "将删除汇总表、明细表、原因表"
        )
        return res

    @staticmethod
    def page3_btn3_1Click():
        res = messagebox.showinfo(
            "操作提示","开始执行"
        )

    @staticmethod
    def btn2Click():
        res = messagebox.askquestion(
            "操作提示", "将还原配比数据,不会删除汇总明细"
        )
        return res

def main():
    root = Tk()
    root.title("测试工具")
    root.geometry("900x500")
    start(root)
    root.mainloop()

if __name__ == '__main__':
    main()