import math
import random
import time

import requests
from loguru import logger
from lxml import etree
import sqlite3

headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
}

def getHTML(url):
    re=requests.get(headers=headers,url=url)
    HTML=etree.HTML(re.text)
    logger.info(re.status_code)
    logger.info("延迟：" + (5 + random.randint(4, 8) + random.random()).__str__())
    time.sleep(5 + random.randint(4, 8) + random.random())
    return  HTML

def getAllJT():
    for i in range(1,11):
        url='https://bbs.guitarchina.com/forum.php?mod=forumdisplay&fid=100&sortid=182&sortid=182&filter=sortid&page={}'.format(i)
        HTML_table = getHTML(url)

        titleNm = HTML_table.xpath('//*[@id="threadlisttableid"]//tbody/tr/th//a[3]/text()')
        titleUrl = HTML_table.xpath('//*[@id="threadlisttableid"]//tbody/tr/th//a[3]//@href')
        logger.info(len(titleNm))
        logger.info(titleNm)
        logger.info(len(titleUrl))
        logger.info(titleUrl)


if __name__ == '__main__':
    conn = sqlite3.connect('JT.db')
    cur = conn.cursor()
    sql = "SELECT * FROM test"
    a = cur.execute(sql)
    for row in a:
        print(str(row[0])+str(row[1])+'\n')


    sql = "insert into test values(999,999)"
    a = cur.execute(sql)
    conn.commit()

    sql = "SELECT * FROM test"
    a = cur.execute(sql)
    for row in a:
        print(str(row[0])+str(row[1])+'\n')


