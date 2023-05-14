import json
import re
import typing
from datetime import datetime
from pathlib import Path

import colorama         # pip install colorama
import httpx            # pip install httpx
from lxml import etree  # pip install lxml

from .rsa import RSA    # 外部文件


class ZWYT(object):
    def __init__(self, name, username, password):
        self.resvDev = None                 # 座位编号
        self.roomId = None
        self.cookies = {'ic-cookie': ''}    # 保存登录用的 cookie
        self.name = name                    # 名字
        self.username = str(username)       # 学号
        self.password = str(password)       # 密码
        colorama.init(autoreset=True)       # 控制打印输出的颜色

        # url接口
        self.urls = {
            'login_url': '',                # 登录
            'reserve': 'http://libbooking.gzhu.edu.cn/ic-web/reserve',          # 预约
            'seatmenu': 'http://libbooking.gzhu.edu.cn/ic-web/seatMenu',        # 获取 roomId
            'findaddress': 'http://libbooking.gzhu.edu.cn/ic-web/auth/address',
            'get_location': 'http://libbooking.gzhu.edu.cn/authcenter/toLoginPage',
            'userinfo': 'http://libbooking.gzhu.edu.cn/ic-web/auth/userInfo'    # 获取用户信息
        }

        # xpath 匹配规则
        self.xpath_rules = {
            'lt': '//input[@id="lt"]/@value',
            'execution': '//input[@name="execution"]/@value'
        }

        # 请求头
        self.headers = {
            "Host": "libbooking.gzhu.edu.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42",
            "token": "a50b1863a0394feab1e4de8d3f370c97",
            "Origin": "http://libbooking.gzhu.edu.cn",
            "Referer": "http://libbooking.gzhu.edu.cn/",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"
        }

        # 初始化请求连接对象
        self.rr = httpx.Client()

    def get_response(self, url, method, params, headers, data):
        """
        发起请求, 获取响应
        url:
        method:
        params:
        headers:
        data:
        返回数据:
        """
        ...

    # TODO: 请求方式获取 roomId
    def get_roomId(self):
        """
        获取 roomId
        :return:
        """
        res = self.rr.get(url=self.urls['roomId'], headers=self.headers)
        res = res.json()

    # TODO: 请求方式获取 devId
    def get_devId(self):
        params = {
            "roomIds": "100647013",
            "resvDates": "20230514",
            "sysKind": "8"
        }

        res = self.rr.get(url=self.urls['reserve'], params=params, headers=self.headers)
        json_data = res.json()

    # 取对应座位的 resvDev、devId
    def get_seat_resvDev(self, devName: str):
        """
        devName: 座位编号. 比如 101-011、202-030、3c-011、3c-212、M301-1
        """
        resvDev = None
        filename = devName.strip().split('-')[0]  # 移除传入的座位名头尾的空格后再分割传入的座位名称
       
        # 预约的是琴房
        if filename[0] == 'M':
            json_path = Path().cwd() / 'json/琴房.json'         # 准备打开的 json 文件的路径
        else:
            json_path = Path().cwd() / f'json/{filename}.json'  # 准备打开的 json 文件的路径

        # 打开对应的 json 文件
        with open(json_path, mode='r', encoding='utf-8') as f:
            json_data = json.load(f)

        # 遍历获取对应座位的 devId
        for i in json_data.get('data'):
            if i.get('devName') == devName:
                resvDev = i.get('devId')
        return resvDev

    # 获取用户 appAccNo
    def get_person_appAccNo(self):
        """
        获取用户的 appAccNo
        """
        # 请求接口
        res = self.rr.get(url=self.urls['userinfo'], cookies=self.cookies)
        return res.json().get('data').get('accNo')

    # 登录
    def login(self):
        """
        登录
        """
        res = self.rr.get(url=self.urls['login_url'])  # 请求登录url获取一些参数
        html = etree.HTML(res.text)

        lt = html.xpath(self.xpath_rules['lt'])[0]
        execution = html.xpath(self.xpath_rules['execution'])[0]
        rsa = RSA().strEnc(self.username + self.password + lt)  # 把密码和那些参数用RSA加密

        data = {
            'rsa': rsa,
            'ul': len(self.username),
            'pl': len(self.password),
            'lt': lt,
            'execution': execution,
            '_eventId': 'submit',
        }
        url = self.urls['login_url']
        res = self.rr.post(url=url, data=data, timeout=60)

        location = str(res.headers.get('Location'))
        ticket = re.findall('ticket=(.*)', location)[0]  # 获取ticket

        url = f"""{re.findall('service=(.*)', url)[0]}?ticket={ticket}"""
        location = self.rr.get(url=url).headers.get('Location')

        unitoken = re.findall('uniToken=(.*)', str(location))[0]  # 获取unitoken
        uuid = re.findall('uuid=(.*?)&', str(location))[0]  # 获取 uuid
        params = {
            "manager": "false",
            "uuid": uuid,
            "consoleType": "16",
            "uniToken": unitoken
        }

        # 获取 ic-cookie
        get_cookie_res = self.rr.get(
            url="http://libbooking.gzhu.edu.cn/ic-web//auth/token",
            params=params,
            headers=self.headers
        )

        icc = get_cookie_res.headers.get('Set-Cookie')
        self.cookies['ic-cookie'] = re.findall('ic-cookie=(.*?);', icc)[0]

    #  获取登录url
    def get_login_url(self):
        """
        获取登录带参数的 登录 url
        """
        params = {
            "finalAddress": "http://libbooking.gzhu.edu.cn",
            "errPageUrl": "http://libbooking.gzhu.edu.cn/#/error",
            "manager": "false",
            "consoleType": "16"
        }

        # 从data里面获取一个url
        url = self.urls['findaddress']
        address = self.rr.get(url=url, params=params).json().get('data')

        # 将上面获取到的url 作为请求参数
        url = url = f"{self.urls['get_location']}?redirectUrl={address}"
        res = self.rr.get(url=url)

        self.urls['login_url'] = res.headers.get('Location')

    # 获取预约日期
    def get_reverse_date(self) -> typing.List:
        """
        功能: 返回预约的日期和时间
        return: 返回一个列表, 列表里面每个元素是一个字典, 字典里面有start(开始时间)和end(结束时间)
        """
        # 预约时间段
        hours = (
            ('8:30:00', '12:30:00'), ('12:30:00', '16:30:00'), ('16:30:00', '20:30:00'), ('20:30:00', '21:45:00')
        )

        # 获取当前的 年份、月份、天
        year, month, day = int(datetime.now().year), int(datetime.now().month), int(datetime.now().day)

        # 要返回的数据
        reverse_days = []

        # 保存每个字典
        date_list = []

        # 有31天的月份
        if month in (1, 3, 5, 7, 8, 10):
            if day == 31:
                date_list.append({'year': year, 'month': month, 'day': 31})
                date_list.append({'year': year, 'month': month + 1, 'day': 1})
            else:
                date_list.append({'year': year, 'month': month, 'day': day})
                date_list.append({'year': year, 'month': month, 'day': day + 1})

        # 2月份
        elif month == 2:
            # 闰年 == 能被 4 整除, 但不能被 100 整除的年份
            if year % 4 == 0 and year % 100 != 0:
                if day == 29:
                    date_list.append({'year': year, 'month': month, 'day': 29})
                    date_list.append({'year': year, 'month': month + 1, 'day': 1})
                else:
                    date_list.append({'year': year, 'month': month, 'day': day})
                    date_list.append({'year': year, 'month': month, 'day': day + 1})
            # 平年
            else:
                if day == 28:
                    date_list.append({'year': year, 'month': month, 'day': 28})
                    date_list.append({'year': year, 'month': month + 1, 'day': 1})
                else:
                    date_list.append({'year': year, 'month': month, 'day': day})
                    date_list.append({'year': year, 'month': month, 'day': day + 1})

        # 12月份
        elif month == 12:
            if day == 31:
                date_list.append({'year': year, 'month': month, 'day': 31})
                date_list.append({'year': year + 1, 'month': 1, 'day': 1})  # 新的一年 1 月份
            else:
                date_list.append({'year': year, 'month': month, 'day': day})
                date_list.append({'year': year, 'month': month, 'day': day + 1})

        # 其它的就是每个月 30天的月份
        else:
            if day == 30:
                date_list.append({'year': year, 'month': month, 'day': 30})
                date_list.append({'year': year, 'month': month + 1, 'day': 1})
            else:
                date_list.append({'year': year, 'month': month, 'day': day})
                date_list.append({'year': year, 'month': month, 'day': day + 1})

        # 添加起始和结束时间
        for i in date_list:
            for hour in hours:
                reverse_days.append({
                    # 起始时间
                    'start': f"{i.get('year')}-{i.get('month')}-{i.get('day')} {hour[0]}",
                    # 结束时间
                    'end': f"{i.get('year')}-{i.get('month')}-{i.get('day')} {hour[-1]}"
                })
        return reverse_days

    # 预约
    def reserve(self, devName):
        """
        预约
        """
        # 获取所预约的座位编号
        self.resvDev = self.get_seat_resvDev(devName)

        # 登录
        self.get_login_url()
        self.login()

        # 获取用户的 appAccNo
        appAccNo = self.get_person_appAccNo()

        print('\n')  # 换行

        # 遍历所有日期, 进行预约
        for date in self.get_reverse_date():
            json_data = {
                "sysKind": 8,
                "appAccNo": appAccNo,
                "memberKind": 1,
                "resvMember": [appAccNo],  # 读者个人编号
                "resvBeginTime": date.get('start'),  # 预约起始时间
                "resvEndTime": date.get('end'),  # 预约结束时间
                "testName": "",
                "captcha": "",
                "resvProperty": 0,
                "resvDev": [self.resvDev],  # 座位编号
                "memo": ""
            }

            # 发起预约请求
            res = self.rr.post(url=self.urls['reserve'], headers=self.headers, json=json_data, cookies=self.cookies)

            # 将服务器返回数据解析为 json
            res_json = res.json()
            message = res_json.get('message')

            # 预约成功
            if message == '新增成功':
                print(
                    colorama.Style.BRIGHT + colorama.Fore.GREEN + f"""\n预约成功: {self.name} 预约了 {devName}: {json_data['resvBeginTime']} ~ {json_data['resvEndTime']}""")

            # 该时间段有预约了
            elif re.findall('当前时段有预约', message):
                print(
                    colorama.Style.BRIGHT + colorama.Fore.YELLOW + f"""{self.name} 在该时段内已经有预约了 {devName}: 起始时间:{json_data['resvBeginTime']}, 结束时间:{json_data['resvEndTime']}""")

            elif re.findall('预约时间要大于当前时间', message):
                print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + '预约时间要大于当前时间')

            # 预约失败---可选择向微信推送预约失败的信息, 比如可以使用 pushplus 平台
            else:
                print(
                    colorama.Style.BRIGHT + colorama.Fore.RED + f"""\n{self.name}, 时间段: {json_data['resvBeginTime']} 预约失败, {message}""")

    # 签到
    def sign(self, devName):
        """
        签到
        """
        self.get_login_url()
        self.login()

        lurl = "http://libbooking.gzhu.edu.cn/ic-web/phoneSeatReserve/login"
        url = "http://libbooking.gzhu.edu.cn/ic-web/phoneSeatReserve/sign"

        # 获取签到用的 devSn
        devSn = self.get_seat_resvDev(devName)

        # 登录
        res1 = self.rr.post(url=lurl,
                            json={"devSn": devSn, "type": "1", "bind": 0, "loginType": 2},
                            cookies=self.cookies)

        # 返回的json数据
        res1_data = res1.json()

        # 预约座位的编号不对
        if res1_data.get('data') is None:
            print(
                colorama.Style.BRIGHT + colorama.Fore.YELLOW +
                f"{res1_data.get('message')}"
            )
            return

        # 暂无预约
        if res1_data.get('data').get('reserveInfo') is None:
            return

        # 获取预约编号
        resvId = res1_data.get('data').get('reserveInfo').get('resvId')

        # 签到接口
        res2 = self.rr.post(
            url=url, json={"resvId": resvId}, cookies=self.cookies)

        # 获取返回的信息
        message = res2.json().get('message')

        # 签到成功
        if message == '操作成功':
            print(
                colorama.Style.BRIGHT + colorama.Fore.GREEN +
                f"\n{self.name} 签到成功--{message}\n"
            )

        # 已经签到过
        elif message == '用户已签到，请勿重复签到':
            print(
                colorama.Style.BRIGHT + colorama.Fore.YELLOW +
                f'\n {self.name} 用户已签到, 请勿重复签到\n'
            )

        # 签到失败
        else:
            print(
                colorama.Style.BRIGHT + colorama.Fore.RED +
                f"\n{self.name}--签到失败--{message}\n"
            )
