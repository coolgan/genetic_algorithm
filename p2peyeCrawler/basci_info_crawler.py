import requests
import pandas as pd
from lxml import etree

user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
header = {'user-agent':user_agent}

urls = ['https://www.p2peye.com/platform/all/{}'.format('p'+str(i)+'/') for i in range(2,221)]

def extract_element(lists):
    temp = [each.replace('\t','').replace('\n','').replace('\r','').replace(' ','') for each in lists]
    temp2 = [each for each in temp if each != '']
    return temp2
def get_details(url):
    res = requests.get(url,headers = header)
    res.encoding = "gbk"
    selector = etree.HTML(res.text)
    nodes = selector.xpath('//*[@class="ui-result-item"]')
    temp = []
    for node in nodes:
        #平台名称
        name = node.xpath('div[1]/div[1]/div[1]/a/@title')[0]
        #平台标签
        tags = extract_element(node.xpath('div[1]/div[1]/div[1]/div[@class="ui-result-icon"]/div[1]/text()'))
        #预期利率
        if node.xpath('div[1]/div[2]/a/div[1]/p/strong/text()') != []:
            interest_rate = node.xpath('div[1]/div[2]/a/div[1]/p/strong/text()')[0]
        else:
            interest_rate = 'None'
        #平台状态
        state = node.xpath('div[1]/div[2]/a/div[1]/p/text()')[-1]
        #注册资本
        capital = node.xpath('div[1]/div[2]/a/div[2]/div[1]/p/text()')[0]
        #注册地址
        address = node.xpath('div[1]/div[2]/a/div[2]/div[1]/p/text()')[-1]
        info = {
            "name":name,
            "tags":tags,
            "interest_rate":interest_rate,
            "capital":capital,
            "address":address

        }#[name,tags,interest_rate,state,capital,address]
        temp.append(info)
    return temp
	
if __name__ == '__main__':
	content = []
	for url in urls:
		content.append(get_details(url))
	df = pd.DataFrame(content)
	df.to_excel('basic_info.xlsx')