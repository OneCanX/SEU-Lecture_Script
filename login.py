import config
import requests
import json
from utils.ids_encrypt import encryptAES
from bs4 import BeautifulSoup


# 登录信息门户，返回登录后的session
def login(cardnum, password):
    ss = requests.Session()
    form = {"username": cardnum}

    #  获取登录页面表单，解析隐藏值
    url = "https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal"
    res = ss.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    attrs = soup.select('[tabid="01"] input[type="hidden"]')
    for k in attrs:
        if k.has_attr('name'):
            form[k['name']] = k['value']
        elif k.has_attr('id'):
            form[k['id']] = k['value']
    form['password'] = encryptAES(password, form['pwdDefaultEncryptSalt'])
    # 登录认证
    res = ss.post(url, data=form, allow_redirects=False)
    # 登录ehall
    ss.get('http://ehall.seu.edu.cn/login?service=http://ehall.seu.edu.cn/new/index.html')

    res = ss.get('http://ehall.seu.edu.cn/jsonp/userDesktopInfo.json')
    json_res = json.loads(res.text)
    try:
        name = json_res["userName"]
        print(name[0], "** 登陆成功！")
    except Exception:
        print("认证失败！")
        return False

    return ss


def login_seu():
    user_name = config.username
    print("帐号:" + user_name)
    password = config.password
    print("密码:" + '*' * len(password))
    print("开始登陆")
    ss = login(user_name, password)
    while ss is False or ss is None:
        print("请重新登陆")
        print("请输入帐号:")
        user_name = input()
        print("请输入密码:")
        password = input()
        print("开始登陆")
        ss = login(user_name, password)
    print("登陆成功")
    return ss