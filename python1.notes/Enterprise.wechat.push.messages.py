#!/usr/bin/python
#! -*- coding: utf-8 -*-
"""
Author: ZhenYuSha
Create type_time: 2020-2-24
Info: 定期向企业微信推送消息
"""
import requests, json
import datetime
import time

########################################################################
#获取天气
import requests
from bs4 import BeautifulSoup


def getHTMLText(url, timeout=30):
    try:
        r = requests.get(url, timeout=30)  # 用requests抓取网页信息
        r.raise_for_status()  # 可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'


def get_data(html):
    final_list = []
    soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup库解析网页
    body = soup.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    lis = ul.find_all('li')

    for day in lis:
        temp_list = []

        date = day.find('h1').string  # 找到日期
        temp_list.append(date)

        info = day.find_all('p')  # 找到所有的p标签
        temp_list.append(info[0].string)

        if info[1].find('span') is None:  # 找到p标签中的第二个值'span'标签——最高温度
            temperature_highest = ' '  # 用一个判断是否有最高温度
        else:
            temperature_highest = info[1].find('span').string
            temperature_highest = temperature_highest.replace('℃', ' ')

        if info[1].find('i') is None:  # 找到p标签中的第二个值'i'标签——最高温度
            temperature_lowest = ' '  # 用一个判断是否有最低温度
        else:
            temperature_lowest = info[1].find('i').string
            temperature_lowest = temperature_lowest.replace('℃', ' ')

        temp_list.append(temperature_highest)  # 将最高气温添加到temp_list中
        temp_list.append(temperature_lowest)  # 将最低气温添加到temp_list中

        wind_scale = info[2].find('i').string  # 找到p标签的第三个值'i'标签——风级，添加到temp_list中
        temp_list.append(wind_scale)

        final_list.append(temp_list)  # 将temp_list列表添加到final_list列表中
    return final_list


# 用format()将结果打印输出
def print_data(final_list,num):
    data = "广州未来7日的天气情况如下:\n\n" + "{:^10} {:^8} {:^6} {:^6}  {:^8}\n".format('日期', '天气', '最高温度℃', '最低温度℃', '风级')
    #print("广州未来7日的天气情况如下:")
    #print("{:^10} {:^8} {:^6} {:^6}  {:^8}".format('日期', '天气', '最高温度℃', '最低温度℃', '风级'))
    for i in range(num):
        final = final_list[i]
        #print("{:^10} {:^10} {:^10} {:^10} {:^14}".format(final[0], final[1], final[2], final[3], final[4]))
        data = data + "{:^10} {:^8} {:^6} {:^6} {:^8}\n\n".format(final[0], final[1], final[2], final[3], final[4])
    return data


# 用main()主函数将模块连接
def main():
    url = 'http://www.weather.com.cn/weather/101280101.shtml'
    html = getHTMLText(url)
    final_list = get_data(html)
    return print_data(final_list, 7)

#main()


##################################################################################
#获取企业微信机器人的webhook
wx_url = "省略"

#爬取天气的结果，打印出来
send_message = main()


def get_current_time():
  """获取当前时间，当前时分秒"""
  now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  hour = datetime.datetime.now().strftime("%H")
  mm = datetime.datetime.now().strftime("%M")
  ss = datetime.datetime.now().strftime("%S")
  return now_time, hour, mm, ss


def sleep_time(hour, m, sec):
  """返回总共秒数"""
  return hour * 3600 + m * 60 + sec


def send_msg(content):
  """艾特全部，并发送指定信息"""
  data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
  r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
  print(r.json)


def every_time_send_msg(interval_h=0, interval_m=5, interval_s=0, special_h="00", special_m="00", mode="special"):
  """每天指定时间发送指定消息"""

  # 设置自动执行间隔时间
  second = sleep_time(interval_h, interval_m, interval_s)
  # 死循环
  while 1 == 1:
    # 获取当前时间和当前时分秒
    c_now, c_h, c_m, c_s = get_current_time()
    print("当前时间：", c_now, c_h, c_m, c_s)
    if mode == "special":
      if c_h == special_h and c_m == special_m:
        # 执行
        print("正在发送...")
        send_msg(send_message)
    else:
      send_msg(send_message)
    print("每隔" + str(interval_h) + "小时" + str(interval_m) + "分" + str(interval_s) + "秒执行一次")
    # 延时
    time.sleep(second)


if __name__ == '__main__':
  every_time_send_msg(mode="no")
