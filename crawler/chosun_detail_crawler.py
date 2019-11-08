import requests
from time import sleep
from datetime import datetime, date
from bs4 import BeautifulSoup
import timeit
from calendar import monthrange

class ChosunDetailCrawler:
  def __init__(self):
    print("ChosunCrawling init")

  def crawling(self, id_link_tuples):
    items = list()
    for id_link_tuple in id_link_tuples:
      id, link = id_link_tuple
      item = self._fetch_detail(link)
      items.append((item, id))
      sleep(0.2)

    return items

  def _fetch_detail(self, link):
    fetch_start = timeit.default_timer()
    if link.find("html_dir") > 0 :
      content = self.parse_content_v1(link)
    else :
      content = self.parse_content_v2(link)
   
    fetch_end = timeit.default_timer()
    print(f"fetching for {link} duration : {fetch_end - fetch_start}")

    return content

  def parse_content_v1(self, link):

    cookies = {
      '_ga': 'GA1.2.1600924469.1565777017',
      'OAX': 'eYqXAV1T3HcAAMWt',
      '__gads': 'ID=e968ab3c5fe7bb33:T=1569671729:S=ALNI_MYgRV-tUYTDTk2TW9vu2oZM3fvTsg',
      'PCID': '15709069183121289406763',
      '_gid': 'GA1.2.1817332432.1572930938',
      'dable_uid': '77420962.1560391597749',
      'fontIdx': '3',
      '_gat': '1',
      '_gat_chosun_total': '1',
      '_td': '60d7d6bc-05b2-4b5a-885a-dfb78f889cac',
    }

    headers = {
      'Connection': 'keep-alive',
      'Cache-Control': 'max-age=0',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
    }

    response = requests.get(link, headers=headers,
                            cookies=cookies, verify=False)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find("div", class_="par")

    if tag == None and soup.find("title").text == "요청하신 페이지를 찾지 못했습니다.":
      print("Not Found")
      return "NOT_FOUND"
    elif tag != None and len(tag.text) > 10:
      return tag.text
    else:
      return None

  def parse_content_v2(self, link):
    cid = link.split("?")[1].replace("contid=",'')
    year = cid[:4]
    mm = cid[4:6]
    dd = cid[6:8]

    cookies = {
      'PCID': '15669814276938141840367',
      '_ga': 'GA1.2.457771752.1566981428',
      'dable_uid': '64529104.1550819316180',
      '_td': '30dcac2c-2c8e-4030-8b6e-4266c15c62a4',
      '__gads': 'ID=9353bb8a93b73ef5:T=1569570531:S=ALNI_MZXpnMGzNVvevy_hv2WrUvVTkQRvA',
      'OAX': '0t4F+V270/sAAH5d',
      '__utma': '222464713.457771752.1566981428.1572590587.1572590587.1',
      '__utmc': '222464713',
      '__utmz': '222464713.1572590587.1.1.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided)',
      'fontIdx': '3',
      '_gid': 'GA1.2.1735109905.1573021636',
      '_gat': '1',
      '_gat_chosun_total': '1',
      '_gali': 'news_body_id',
    }

    headers = {
      'Pragma': 'no-cache',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
      'Accept': '*/*',
      'Referer': 'http://news.chosun.com/svc/content_view/content_view.html?contid=1998032370293',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
      'Cache-Control': 'no-cache',
    }

    response = requests.get(f'http://news.chosun.com/priv/data/www/news/{year}/{mm}/{dd}/{cid}.xml', headers=headers,
                            cookies=cookies, verify=False)
    soup = BeautifulSoup(response.text, 'lxml-xml')

    text_node = soup.find("text")

    if text_node == None:
        return None
    else:
        return text_node.text.strip()


  def _parse_content(self, dl):
    title_tag = dl.select("dt[discription='기사 제목']")[0].find("a")
    title = title_tag.text
    link = title_tag.get('href')
    content_tag_list = dl.select("dd.desc")

    if len(content_tag_list) > 0:
      content_tags = content_tag_list[0].contents
      content_str = map(str, content_tags)
    else:
      print(f"exception : {content_tag_list}")
      content_str = []

    if len(dl.select("span.date")) > 0 :
      press_date = str(dl.select("span.date")[0].string).strip()
    else:
      press_date = None

    return {
      "title": str(title).strip(),
      "link" : link,
      "content_abbr": " ".join(content_str).strip(),
      "date": press_date
    }

if __name__ == "__main__":
  test = ChosunDetailCrawler()

  # startDate = "19980101"
  # endDate = "19980131"
  # result = test.fetch_list(startDate, endDate)
  # print(result)

  link = "http://news.chosun.com/site/data/html_dir/2014/07/01/2014070102175.html"
  link = "http://news.chosun.com/svc/content_view/content_view.html?contid=1998032370293"
  content = test._fetch_detail(link)
  print(content)
