
class BaseData(object):
    def __init__(self):

        self._base_match_url = f"http://10.1.17.141/opra-api/upl-common/UplPassengerCount/diff/other/match"
        self._base_match_url2 = f"https://ly/opra-api/upl-common/UplPassengerCount/diff/other/match"
        self._process_url = f"http://10.1.17.141/opra-api/upl-common/uplCalAveragePax/createEstimateSap/MU/202105"
        self._process_url2 = f"https://ly/opra-api/upl-common/uplCalAveragePax/createEstimateSap/MU/202105"
        self._process_url_m = f"http://10.1.17.141/opra-api/upl-common/uplCalAveragePax/createEstimateMap/MU/202105"
        self._process_url2_m = f"https://ly/opra-api/upl-common/uplCalAveragePax/createEstimateMap/MU/202105"
        self._huanjing_list = {0: "开发", 1: "测试", 2: "东航UAT", 3: "南航UAT", 4: "国航生产", 5: "南航生产", 6: "东航生产", 7: "性能测试"}
        self._jiormon_list = {0:"季平均票价", 1:"月平均票价"}
        self._url_list = {0: "DEV", 1: "TEST", 2: "UATMU", 3: "UATCZ", 4: "OPRACA", 5: "OPRACZ", 6: "OPRAMU", 7: "PT"}
        self._url_host_list = {0: "10.1.17.141", 1: "10.1.17.140", 2: "10.1.19.222", 3: "10.1.19.205", 4: "10.1.101.13",
                               5: "10.1.103.13", 6: "10.1.102.13", 7: "10.1.18.186"}
        self._oracle_list = {0: "OPRA_UPL_DEV", 1: "OPRA_UPL_TEST", 2: "OPRA_UPL_UAT_MU", 3: "OPRA_UPL_UAT_CZ",
                             4: "OPRA_UPL_CA", 5: "OPRA_UPL_CZ", 6: "OPRA_UPL_MU", 7: "OPRA_UPL_PT"}