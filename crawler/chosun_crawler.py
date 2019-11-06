import requests
from time import sleep
from datetime import datetime, date
from bs4 import BeautifulSoup
import timeit
from calendar import monthrange

class ChosunCrawler:
  def __init__(self):
    print("ChosunCrawling init")

  def crawling(self, year, month, pages):
    mr = monthrange(year, month)
    print(mr)
    startDate = date(year, month, 1).strftime("%Y%m%d")
    endDate = date(year, month, mr[1]).strftime("%Y%m%d")
    return self.fetch_list(year, pages, startDate, endDate)

  def fetch_list(self, year, pages, startDate, endDate):
    merged_items = list()
    items_per_page = 10

    if len(pages) < 1:
      search_pages = range(1, 100)
    else:
      search_pages = pages

    print(f"start for year {year} {startDate} {endDate} pages : {pages}")

    for page in search_pages:
      sleep(0.5)
      fetch_start = timeit.default_timer()
      result = self._fetch_list(startDate = startDate, endDate=endDate, pageNum=page)
      fetch_end = timeit.default_timer()
      print(f"fetching... page : {page} duration : {fetch_end-fetch_start}")
      total_count = result[0]
      merged_items.append(result)

      max_page = int(total_count / items_per_page) + 1
      if max_page <= page:
        break

    return merged_items

  def _fetch_list(self, startDate, endDate, pageNum):
    cookies = {
      '_ga': 'GA1.2.1600924469.1565777017',
      'OAX': 'eYqXAV1T3HcAAMWt',
      '_td': '60d7d6bc-05b2-4b5a-885a-dfb78f889cac',
      '_gid': 'GA1.2.595092956.1569671727',
      '_gat': '1',
      '_gat_chosun_total': '1',
      '__gads': 'ID=e968ab3c5fe7bb33:T=1569671729:S=ALNI_MYgRV-tUYTDTk2TW9vu2oZM3fvTsg',
    }

    headers = {
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
      'Referer': 'http://nsearch.chosun.com/search/total.search?query=%EB%B6%81%ED%95%9C&pageconf=total',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
    }

    params = (
      ('query', '\uBD81\uD55C'),
      ('siteid', 'www'),
      ('category', ''),
      ('sort', '1'),
      ('writer', ''),
      ('field', ''),
      ('date_period', ''),
      ('date_start', startDate),
      ('date_end', endDate),
      ('emd_word', ''),
      ('expt_word', ''),
      ('opt_chk', 'true'),
      ('pn', pageNum)
    )

    response = requests.get('http://nsearch.chosun.com/search/total.search', headers=headers, params=params,
                            cookies=cookies, verify=False)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text, 'html.parser')
    count_box = soup.select("div.count_box")[0].contents[0].strip()
    count_before_split = count_box.split("건")
    count = int(count_before_split[0].replace(',', ''))
    count_page = count_before_split[1].replace('중', '').strip()

    result_dl = soup.select("dl.search_news")
    contents = list(map(self._parse_content, result_dl))
    return (count, pageNum, count_page, contents)

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
  test = ChosunCrawler()

  # startDate = "19980101"
  # endDate = "19980131"
  # result = test.fetch_list(startDate, endDate)
  # print(result)
  r = test.crawling(1998,1,[1, 2])
