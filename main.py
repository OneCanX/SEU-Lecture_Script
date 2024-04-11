import sys
import time
import threading
import copy

from login import login_seu
from lecture import *
from fetch_lecture import *
import config


def wait_begin(lecture):
    current_time = int(time.time())
    begin_time = int(lecture.get_begin_time_stramp())
    end_time = int(lecture.get_end_time_stramp())
    if current_time > end_time:
        print("抢课时间已结束，大侠请重新来过")
        sys.exit(0)
    print("请输入提前几秒开始抢（请保证本地时间准确）：")
    advance_time = int(input())
    while current_time < begin_time - advance_time:
        current_time = int(time.time())
        print('等待{}秒'.format(begin_time - advance_time - current_time))
        time.sleep(1)


if __name__ == '__main__':
    ss = login_seu()

    lecture_list = get_lecture_list(ss)
    if len(lecture_list) == 0:
        print("当前无讲座")
        sys.exit(0)
    print_lecture_list(lecture_list)
    lecture_info = None
    lecture_key = None
    while not lecture_info:
        print("请输入序号：")
        lecture_key = int(input())
        try:
            lecture_info = lecture_list[lecture_key]
        except Exception:
            print("非法输入")
    lecture = Lecture(lecture_info)
    wid = lecture.wid
    print("已选择：" + lecture.wid)

    wait_begin(lecture)

    print('开始抢课')
    threading.Thread(target=get_vcode_loop, args=(wid, copy.deepcopy(ss))).start()
    thread_list = list()
    for i in range(config.thread_num):
        thread_list.append(threading.Thread(target=fetch_lecture_loop,
                                            args=('t{}'.format(i), wid, copy.deepcopy(ss))))
    start_interval = config.interval / config.thread_num
    for thread in thread_list:
        thread.start()
        time.sleep(start_interval)
