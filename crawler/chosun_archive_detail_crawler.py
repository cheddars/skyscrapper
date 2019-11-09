import requests
from time import sleep
from datetime import datetime, date
from bs4 import BeautifulSoup
import timeit
from calendar import monthrange

class ChosunArchiveDetailCrawler:
  def __init__(self):
    print("ChosunCrawling init")

  def crawling(self, id_list):
    items = list()
    for id in id_list:
      content = self._fetch_content(id)
      items.append((content, id))
      sleep(0.2)

    return items

  def _fetch_content(self, article_id):
    print(f"fetching for {article_id}")
    cookies = {
      '_ga': 'GA1.2.1600924469.1565777017',
      'OAX': 'eYqXAV1T3HcAAMWt',
      '__gads': 'ID=e968ab3c5fe7bb33:T=1569671729:S=ALNI_MYgRV-tUYTDTk2TW9vu2oZM3fvTsg',
      'PCID': '15709069183121289406763',
      '_gid': 'GA1.2.1965972637.1573126407',
      'fontIdx': '3',
      '_td': '60d7d6bc-05b2-4b5a-885a-dfb78f889cac',
      'JSESSIONID': '994085FE121BB0A4DDD7DE5EA6189665.dbcs1',
      '_gat': '1',
      '_gat_chosun_total': '1',
    }

    headers = {
      'Connection': 'keep-alive',
      'Cache-Control': 'max-age=0',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
      'Referer': 'http://srchdb1.chosun.com/pdf/i_service/pdf_SearchList.jsp',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
    }

    params = (
      ('ID', article_id),
    )

    response = requests.get('http://srchdb1.chosun.com/pdf/i_service/pdf_ReadBody.jsp', headers=headers, params=params,
                            cookies=cookies, verify=False)

    response.encoding = "euc-kr"
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find("div", class_="article")

    if article != None:
      paragraphs = article.findAll("p")
      contents = '\n'.join(p.text.strip() for p in paragraphs)

      if len(contents) < 20:
        return article.text.strip()

      return contents
    else:
      return "PARSE_ERROR"

if __name__ == "__main__":
  test = ChosunArchiveDetailCrawler()

  result = test.crawling(["2007010100020"])

  print(result)
