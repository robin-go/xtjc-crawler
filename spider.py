import requests
from lxml import etree
import csv
import time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s : %(message)s')
logger = logging.getLogger('spider')
logger.setLevel(logging.INFO)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
url0 = 'http://www.xtjc.com/zizhi/si/list-0-0-%s.html'
count = 1
detail_abandon = []
list_abandon = []


# 列表页爬取
def list_crawl(i):
    list_url = url0 % i
    response = requests.get(url=list_url, headers=headers)

    # 判断爬取是否成功
    if response.status_code == 200:
        logger.info('列表页%s 爬取成功 %d' % (i, response.status_code))
    else:
        raise Exception('列表页%s 爬取失败 %d 程序结束' % (i, response.status_code))

    # 获取详情页url的列表
    response = etree.HTML(response.content)

    detail_urls = response.xpath('//div[@class="list_zz"]//tr[position()>1]/td/a/@href')
    return detail_urls


# 详情页爬取
def detail_crawl(detail_url):
    global count
    response = requests.get(url=detail_url, headers=headers)

    # 判断爬取是否成功
    if response.status_code == 200:
        logger.info('第%d个, %s 爬取成功 %d' % (count, detail_url, response.status_code))
    else:
        raise Exception('%s 爬取失败 %d 程序结束 共爬取%d个' % (detail_url, response.status_code, count))

    response = etree.HTML(response.content)
    name = response.xpath('//div[@class="name"]/text()')[0]
    area = response.xpath('//div[@class="contact"]/li[1]/a//text()')[0]
    qualification = response.xpath('//div[@class="contact"]/li[2]/a//text()')
    qualification = '、'.join(qualification)
    telephone = response.xpath('//div[@class="contact"]/li[3]/text()')[0][5:]
    address = response.xpath('//div[@class="contact"]/li[4]/text()')[0][5:]
    website = response.xpath('//div[@class="contact"]/li[5]/text()')[0][5:]
    business = response.xpath('//div[@class="contact"]/span/text()')[0]

    # 保存到csv文件
    info_list = [name, area, qualification, telephone, address, website, business]
    with open('info.csv', 'a') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(info_list)

    count += 1


def main():
    for i in range(1, 247):
        try:
            detail_urls = list_crawl(i)
            for detail_url in detail_urls:
                try:
                    detail_crawl(detail_url)
                    time.sleep(2)
                # 捕获报错的详情页并记录下来
                except Exception as e:
                    logger.error(e)
                    detail_abandon.append(detail_url)
        # 捕获报错的列表页并记录下来
        except Exception as e:
            logger.error(e)
            list_abandon.append(i)

    with open('list_abandon.csv', 'w') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(list_abandon)

    with open('detail_abandon.csv', 'w') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(detail_abandon)

    logger.info('Mission Complete. Congratulations!')


if __name__ == '__main__':
    main()
