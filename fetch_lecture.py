import json
import sys
import threading
import time
import base64
import ddddocr

import config

vcode_value = ""
vcode_value_available = False
ocr = ddddocr.DdddOcr(show_ad=False)


def get_vcode(hd_wid: str, ss):
    global vcode_value, vcode_value_available, ocr
    url = "http://ehall.seu.edu.cn/gsapp/sys/jzxxtjapp/hdyy/vcode.do?=" + hd_wid
    vcode_value_available = False
    r = ss.post(url)
    result = r.json()['result']
    data = result.split('64,')[1]
    image_data = base64.b64decode(data)
    vcode_value = ocr.classification(image_data)
    vcode_value.replace("o", "0")
    vcode_value.replace("O", "0")
    for char in vcode_value:
        if char < "0" or char > "9":
            get_vcode(hd_wid, ss)
            break
    vcode_value_available = True


def get_vcode_loop(hd_wid: str, ss):
    i = 1
    while True:
        get_vcode(hd_wid, ss)
        time.sleep(config.vcode_interval)


def check_vcode_value_available():
    return vcode_value_available


def fetch_lecture(hd_wid: str, ss):
    global vcode_value, vcode_value_available
    while not vcode_value_available:
        time.sleep(0.005)

    url = "http://ehall.seu.edu.cn/gsapp/sys/jzxxtjapp/hdyy/queryActivityList.do"
    r = ss.post(url)
    response = r.json()
    datas = response['datas']
    info = None
    for item in datas:
        if item["WID"] == hd_wid:
            info = item
            break
    if info is None:
        print("抢课时间已结束，大侠请重新来过")
        sys.exit(0)

    url = "http://ehall.seu.edu.cn/gsapp/sys/jzxxtjapp/hdyy/yySave.do"
    data_json = {'HD_WID': hd_wid, "vcode": vcode_value}
    form = {"paramJson": json.dumps(data_json)}
    r = ss.post(url, data=form)
    result = r.json()
    if result['success'] is True or result['msg'] == '已经预约过该活动，无需重新预约！':
        print(result['msg'])
        sys.exit(0)
    get_vcode(hd_wid, ss)
    return result['code'], result['msg'], result['success']


last_msg = None


def fetch_lecture_loop(threads_id, hd_wid: str, ss):
    i = 0
    global last_msg
    lock = threading.Lock()
    while True:
        code, msg, success = fetch_lecture(hd_wid, ss)

        lock.acquire()
        i += 1
        print("\r", end='')
        print('线程{},第{}次请求,code：{},msg：{},success:{}'.format(
            threads_id, i, code, msg, success), end='', flush=(last_msg == msg))
        last_msg = msg
        lock.release()

        time.sleep(config.interval)
