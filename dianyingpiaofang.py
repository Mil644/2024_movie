from lxml import etree
import requests
import re

# 设置请求头，模拟浏览器访问，避免被服务器拒绝
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# 发送GET请求获取网页内容
res = requests.get('http://www.boxofficecn.com/boxoffice2024', headers=header)

# 使用lxml的etree解析HTML文本，得到可进行XPath查询的对象
html = etree.HTML(res.text)

# 通过XPath选取所有带有align="left"属性的<tr>标签（这些行包含电影数据和最后一行说明）
tags = html.xpath('//tr[@align="left"]')

# 准备一个列表，用于存储所有电影信息的字典
items = []

# 遍历每个选中的<tr>标签
for i in tags:
    item = {}  # 创建一个空字典，存放当前行的数据

    # 检查当前行第一个<td>中是否有文本（即序号列是否存在，用于过滤掉可能的空行）
    if i.xpath('./td[1]/text()'):
        # 提取序号，去除首尾空白，存入item['rank']
        item['rank'] = i.xpath('./td[1]/text()')[0].strip()

        # 处理年份列：检查第二个<td>中是否有<span>标签（某些年份可能被<span>包裹，如重映电影）
        if i.xpath('./td[2]/span'):
            # 如果有<span>，则提取<span>内的文本作为年份
            item['year'] = i.xpath('./td[2]/span/text()')[0].strip()
        else:
            # 否则直接提取第二个<td>的文本作为年份
            item['year'] = i.xpath('./td[2]/text()')[0].strip()

        # 提取电影名称，去除首尾空白
        name = i.xpath('./td[3]/text()')[0].strip()
        # 用正则替换掉电影名中的中文左括号
        item['title'] = re.sub('（', '', name)

        # 提取票房数据，去除首尾空白
        item['money'] = i.xpath('./td[4]/text()')[0].strip()

        # 将当前电影的数据字典添加到列表中
        items.append(item)

# 将提取的数据写入CSV文件
with open('dianyingpiaofang.csv', 'w', encoding='utf-8') as f:
    # 写入表头
    f.write('排名,上映年份,电影名称,票房\n')
    # 遍历所有电影数据，按行写入CSV
    for item in items:
        f.write(f'{item["rank"]},{item["year"]},{item["title"]},{item["money"]}\n')
        

    


    

