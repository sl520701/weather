import requests
from bs4 import BeautifulSoup
from lxml import etree
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Referer':'http://www.weather.com.cn/textFC/beijing.shtml'
}
def get_detail_url(url):
    Hrefs= []
    response = requests.get(url,headers=HEADERS)
    text = response.content.decode('utf-8')
    html = etree.HTML(text)
    hrefs = html.xpath('//td[@class="rowsPan"]/a/@href')
    for href in hrefs:
        href = 'http://www.weather.com.cn/'+href
        Hrefs.append(href)
    return Hrefs
def parse_detail_url(detail_url):
    details = []
    response = requests.get(detail_url,headers=HEADERS)
    text = response.content.decode('utf-8')
    html = etree.HTML(text)
    divs = html.xpath('//div[@class="conMidtab"]')
    i=11
    for div in divs:
        date = '5月'+str(i)+'日'
        detail_div = [date]
        trs = div.xpath('.//div[2]/table//tr')
        for tr in trs:
            city_detail = {}
            city = tr.xpath('./td/a[@target="_blank"]/text()')[0]
            city_detail['city'] = city
            low = tr.xpath('./td[@width="86"]/text()')[0]
            city_detail['最低气温']= int(low)
            detail_div.append(city_detail)
        details.append(detail_div)
        i += 1
    return details
def spider():
    weathers = []
    eachs = ['hb','db','hd','hz','hn','xb','xn','gat']
    for each in eachs:
        url = 'http://www.weather.com.cn/textFC/'+str(each)+'.shtml'
        detail_urls = get_detail_url(url)
        for detail_url in detail_urls:
            details = parse_detail_url(detail_url)
            weathers.append(details)
    print(weathers)



if __name__ == '__main__':
    spider()