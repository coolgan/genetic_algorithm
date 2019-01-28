import requests
import pandas as pd
from lxml import etree

user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
header = {'user-agent':user_agent}

urls = pd.read_excel('p2pUrls.xlsx')
urls = urls['urls']

def get_operation_condition(url):
    pingtai_url = url + '/beian/'
    pingtai_res = requests.get(pingtai_url,headers = header)
    pingtai_res.encoding = "utf-8"
    pingtai_selector = etree.HTML(pingtai_res.text)
    name = pingtai_selector.xpath('//*[@class="name"]/@title')[0]
    #记录变更
    record_change = pingtai_selector.xpath('//*[@class="account"]/a[1]/div[1]/text()')[0]
    #异常经营
    abnormal_operate = pingtai_selector.xpath('//*[@class="account"]/a[2]/div[1]/text()')[0]
    #失信人
    default_person = pingtai_selector.xpath('//*[@class="account"]/a[3]/div[1]/text()')[0]
    info = {
        "name":name,
        "record_change":record_change,
        "abnormal_operate":abnormal_operate,
        "default_person":default_person
    }
    
    return info

def get_gongshang_info(gongshang_url):
    gongshang_res = requests.get(gongshang_url,headers = header)
    gongshang_res.encoding = "utf-8"
    gongshang_selector = etree.HTML(gongshang_res.text)
    name = gongshang_selector.xpath('//*[@class="name"]/@title')[0]
    
	try:
	#项目类型
        project_type = gongshang_selector.xpath('//*[@class="product-info clearfix"]/li[1]/span[2]/text()')[0]
    #投标周期
        bid_period = gongshang_selector.xpath('//*[@class="product-info clearfix"]/li[2]/span[2]/text()')[0]
    #保障方式
        insurance_type = gongshang_selector.xpath('//*[@class="product-info clearfix"]/li[3]/span[2]/text()')[0]
    #投标转让
        transform = gongshang_selector.xpath('//*[@class="product-info clearfix"]/li[4]/span[2]/text()')[0]
		info = {
			"name":name,
			"project_type":project_type,
			"bid_period":bid_period,
			"insurance_type":insurance_type,
			"transform":transform
		}
	except Exception:
		info = {
			"name":'None',
			"project_type":'None',
			"bid_period":'None',
			"insurance_type":'None',
			"transform":'None'
		}
    return info

if __name__ == '__main__':
	content = []
	for url in urls:
		content.append(get_operation_condition(url))
		#content.append(get_gongshang_info(url))
	df = pd.DataFrame(content)
	df.to_excel('operation_condition.xlsx')