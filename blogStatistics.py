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
CRAWLING_URL = 'https://www.cnblogs.com/mvc/AggSite/PostList.aspx'


def dateTimestamp(dateTime, formatStr = '%Y-%m-%d'):
    return time.mktime(
        time.strptime(dateTime, formatStr))

def groupByAuthor(parameter_list):
    pass

def crawlData(page, data, startDate = '', endDate = '', groupBy = 'hour'):
    """获取页面内容"""
    url = CRAWLING_URL
    headers = {
        'Content-Type': 'application/json',
    }
    params = json.dumps({
        'CategoryId': 808,
        'CategoryType': "SiteHome",
        'ItemListActionName': "PostList",
        'PageIndex': page,
        'ParentCategoryId': 0,
        'TotalPostCount': 4000,
    })
    res = requests.post(url, data=params, headers=headers, verify=False).text
    
    html = BeautifulSoup(res, 'lxml')

    postList = html.find_all(class_='post_item_foot')
    for postInfo in postList:
        content = postInfo.contents
        author = content[1].contents[0]
        # 发布时间字符串
        timeStr = content[2][11:27]

        localTime = time.localtime(time.mktime(
            time.strptime(timeStr, '%Y-%m-%d %H:%M')))
        
        postTimestamp = time.mktime(localTime)
        if (startDate != '' and postTimestamp < startDate) or (endDate != '' and postTimestamp > endDate):
            continue
        # 以时间 作为 key
        if groupBy == 'week':
            timeIndex = time.strftime("%Y-%m-%d week %w", localTime)
        elif groupBy == 'hour':
            timeIndex = time.strftime("%Y-%m-%d %H", localTime)
        elif groupBy == 'day':
            timeIndex = time.strftime("%Y-%m-%d", localTime)
        elif groupBy == 'author':
            timeIndex = author

        viewStr = content[4].contents[0].contents[0]
        commontStr = content[3].contents[0].contents[0]

        # 浏览量
        view = int(re.findall("\d+", viewStr)[0])
        # 评论量
        commont = int(re.findall("\d+", commontStr)[0])

        if timeIndex in data:
            data[timeIndex]['view'] += view
            data[timeIndex]['commont'] += commont
            data[timeIndex]['postCount'] += 1
        else:
            data[timeIndex] = {
                'view': view,
                'commont': commont,
                'postCount': 1
            }
    
    return data

def main():
    pageNum = 201
    data = {}
    for page in range(1, pageNum):
        # data = crawlData(page, data, dateTimestamp('2018-09-02'), dateTimestamp('2018-09-10'), 0)
        data = crawlData(page, data, '', '', 'author')
        print('已完成: %s/%s' % (page, pageNum - 1))
        page += 1
    col = 2
    ws1['A1'] = '日期'
    ws1['B1'] = '查看人数'
    ws1['C1'] = '评论人数'
    ws1['D1'] = '发布数量'
    for postCount in data:
        col_A = 'A%s' % col
        col_B = 'B%s' % col
        col_C = 'C%s' % col
        col_D = 'D%s' % col
        col_E = 'E%s' % col
        col_F = 'F%s' % col
        ws1[col_A] = postCount
        ws1[col_B] = data[postCount]['view']
        ws1[col_C] = data[postCount]['commont']
        ws1[col_D] = data[postCount]['postCount']
        col += 1
            
    wb.save(filename=destFilename)
    print('-------------SUCCESS--------------')

if __name__ == '__main__':
    main()
