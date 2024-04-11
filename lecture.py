import time


class Lecture:
    def __init__(self, lecture_info):
        self.name = lecture_info['JZMC']
        self.wid = lecture_info['WID']
        self.begin_time = lecture_info['YYKSSJ']
        self.end_time = lecture_info['YYJSSJ']

    @staticmethod
    def __get_time_stramp(time_str):
        return time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))

    def get_begin_time_stramp(self):
        return self.__get_time_stramp(self.begin_time)

    def get_end_time_stramp(self):
        return self.__get_time_stramp(self.end_time)


def get_lecture_list(ss):
    url = "http://ehall.seu.edu.cn/gsapp/sys/jzxxtjapp/hdyy/queryActivityList.do"
    r = ss.post(url)
    response = r.json()
    datas = response['datas']
    return datas


def print_lecture_list(lecture_list):
    print("----------------讲座列表----------------")
    for key, lecture in enumerate(lecture_list):
        print("序号：", end=" ")
        print(key, end="  |")
        print("讲座名称：", end=" ")
        print(lecture['JZMC'], end="  |")
        print("预约开始时间：", end=" ")
        print(lecture['YYKSSJ'], end="  |")
        print("预约结束时间：", end=" ")
        print(lecture['YYJSSJ'], end="  |")
        print("活动时间：")
        print(lecture['JZSJ'])
    print("----------------讲座列表end----------------")
