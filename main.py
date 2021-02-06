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

def insertESDJT(context_url,shop_createdate,shop_list):
    conn = sqlite3.connect('JT.db')
    cur = conn.cursor()
    sql = "insert into ESDJT values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
        shop_list[0],shop_list[1],shop_list[2],shop_list[3],shop_list[4],shop_list[5].replace("'",''),shop_list[6],
        shop_list[7],shop_list[8],shop_list[9],shop_list[10], shop_list[11],shop_list[12],shop_createdate,
        context_url
    )
    logger.info(sql)
    cur.execute(sql)
    conn.commit()

def getHTML(url):
    re=requests.get(headers=headers,url=url)
    HTML=etree.HTML(re.text.replace('<br />',''))
    # logger.info(re.text)
    logger.info(re.status_code)
    logger.info("延迟：" + (random.randint(4, 8) + random.random()).__str__())
    time.sleep(random.randint(4, 8) + random.random())
    return  HTML

def getESDJT():
    # 获取电吉他二手区前10页
    for i in range(1,11):
        url='https://bbs.guitarchina.com/forum.php?mod=forumdisplay&fid=100&sortid=182&sortid=182&filter=sortid&page={}'.format(i)
        HTML_table = getHTML(url)

        titleNm = HTML_table.xpath('//*[@id="threadlisttableid"]//tbody/tr/th//a[3]/text()')
        titleUrl = HTML_table.xpath('//*[@id="threadlisttableid"]//tbody/tr/th//a[3]//@href')
        logger.info(len(titleNm))
        logger.info(titleNm)
        logger.info(len(titleUrl))
        logger.info(titleUrl)

        for j in range(0,len(titleUrl)):
            context_url='https://bbs.guitarchina.com/'+titleUrl[j]
            logger.info(context_url)
            context_name=titleNm[j]
            logger.info("正在获取"+context_name)
            HTML_context=getHTML(context_url)
            id = HTML_context.xpath('/html/body/div[7]/div[4]/div[2]/div[1]/@id')[0].replace('post_','')
            logger.info(id)
            try:
                shop_create_date = HTML_context.xpath('//*[@id="authorposton{}"]/span/text()'.format(id))[0]
            except BaseException as e:
                shop_create_date = ''
            # logger.info('//*[@id="pid{}"]/tbody/tr[1]/td[2]/div[2]/div/div[1]/table/tbody/tr/th'.format(id))
            shop_lines_names = HTML_context.xpath('//*[@id="pid{}"]//table/tbody/tr/td/text()'.format(id))
            shop_lines_context = HTML_context.xpath('//*[@id="pid{}"]//table/tbody/tr/th/text()'.format(id))
            logger.info(shop_create_date)
            logger.info(shop_lines_names)
            logger.info(shop_lines_context)
            if(len(shop_lines_names)>12):
                insertESDJT(context_url,shop_create_date,shop_lines_names)
            # break
        # break


if __name__ == '__main__':
    getESDJT()
    # conn = sqlite3.connect('JT.db')
    # cur = conn.cursor()
    # sql = "delete from ESDJT"
    # cur.execute(sql)
    # conn.commit()

    # sql = "SELECT * FROM test"
    # a = cur.execute(sql)
    # for row in a:
    #     print(str(row[0])+str(row[1])+'\n')
    #
    #

    #

    # a = cur.execute(sql)
    # for row in a:
    #     print(str(row[0])+str(row[1])+'\n')
    #

