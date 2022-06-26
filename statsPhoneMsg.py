import requests
import re
import json
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook
wb = Workbook()
destFilename = 'postBlogAuthor.xlsx'
ws1 = wb.active
ws1.title = "post-blog"

FIRST_PAGE_URL = 'https://www.cnblogs.com/'
CRAWLING_URL = 'http://kgmedit.kugou.com/sms/v4/message/show?department_id=0&caller_id=3&dispatcher_id=0&channel_id=0&deliver_status=-1&receipt_status=1&content_type=0&lAddtime=2022-06-01&rAddtime=2022-06-07&mobile=18575685239&userid=0'


def dateTimestamp(dateTime, formatStr = '%Y-%m-%d'):
    return time.mktime(
        time.strptime(dateTime, formatStr))

def groupByAuthor(parameter_list):
    pass

def crawlData(page, mobile = '18575685239'):
    """获取页面内容"""
    url = CRAWLING_URL
    headers = {
        'Content-Type': 'text/html',
        'Cookie': 'kg_dfid=3Mo1bh2BXxPW3wreLP2B2NES; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1647665966; opd_login_info=opd_username=7C95F564863673F8&opd_chinesename=735C6149B7FE6BF0FDE3008B4B328324&kg_login_ticket=FD08007304E2BC9A03837C38B8DA60DD192E12241C10C0B9103929191C434F9C4D4024B68181516A8A7977843E35E1E3; passport_login_info=user_slug=7C95F564863673F8&nickname=735C6149B7FE6BF0FDE3008B4B328324&token=FD08007304E2BC9A03837C38B8DA60DD192E12241C10C0B9103929191C434F9C4D4024B68181516A8A7977843E35E1E3&user_type=6257706DC11D87E6&appid=F1B5BA770B401A1E; KugouBack=IDCard=8F8F1B480A57F104A37FB1A2FE6A184EBFED48B6006BD10EF0495951B47E781F6490C33A1E35A84C19693C962D8689C40211D9E7A27DBB69&opdName=7C95F564863673F8&UserRole=A00AEEB8C19B0733C49F6D14B1331F1E0FBEC438A8FFD4B957BA8159B4C8D62B&AllRole=303778088A5D3A10648E90C0607897756DC251BEBBC0E579873E62D49780B1786E89755340011DC67BA1458C1EAE05A381387DD4087C010B&isAdmin=F1B5BA770B401A1E&version=A54C28C5CAE1DA00'
    }
    params = json.dumps({
        'department_id': '0',
        'caller_id': '3',
        'dispatcher_id': '0',
        'channel_id': '0',
        'deliver_status': '-1',
        'receipt_status': '1',
        'content_type': '0',
        'lAddtime': '2022-06-01',
        'rAddtime': '2022-06-07',
        'mobile': mobile,
        'userid': '0'
    })
    res = requests.get(url, params, headers=headers, verify=False).text
    
    html = BeautifulSoup(res, 'lxml')

    total = html.find('button', class_='btn-link').get_text()
    totals = re.findall(r"\d+", total)
    totalNum = int(totals[0])

    return totalNum
    postList = html.find_all('tr')
    # print(postList)
    # allMsg = []
    # for info in postList:
    #     msg = []
    #     td = info.find_all('td')
    #     for texts in td:
    #         text = texts.text.strip()
    #         msg.append(text)
    #     allMsg.append(msg)
    

def main():
    # 获取告警人手机号
    # 查询手机号告警数量及告警内容
    data = crawlData(1)
    print('-------------SUCCESS--------------')

if __name__ == '__main__':
    main()