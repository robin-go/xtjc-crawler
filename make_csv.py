import csv

headers = ['公司', '所在地区', '资质等级', '联系电话', '公司地址', '相关网站', '主营业务']
with open('info.csv', 'w') as f:
    csv_write = csv.writer(f, dialect='excel')
    csv_write.writerow(headers)
