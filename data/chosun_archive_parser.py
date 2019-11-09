import requests
from time import sleep
from datetime import datetime, date
from bs4 import BeautifulSoup
import timeit
from calendar import monthrange
from pathlib import Path

class ChosunListParser:
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

  def _fetch_list(self, year, page):
    print(f"parsing {year} {page}")
    base_path = Path(__file__).parent
    file_path = (base_path / f"./chosun/{year}/{page}.html").resolve()
    soup = BeautifulSoup(open(file_path, encoding="euc-kr"), 'html.parser')
    items = list()

    articles = soup.findAll("div", id="search_list")

    for article in articles:
      span = article.find("span", class_="list_tit")
      gigos = article.findAll("div", class_="gigoja")
      gigo = list(filter(lambda x: "[발행일]" in x.text, gigos))

      dt = None
      press = None
      if len(gigo) > 0:
        press = gigo[0].text.strip().replace("\n", " ").replace("[발행일] ", "").replace("      ", " ")
        dt = press.split(" ")[1].replace(".", "-")

      a = span.a

      if a != None:
        title = a.text.strip()
        href = a["href"]
        id = href.split("=")[1]
        item = {"year" : year, "page" : page, "title" : title, "link" : href, "id" : id, "press" : press, "dt" : dt }
        items.append(item)
      else:
        item = {"year" : year, "page" : page, "title" : "exception", "link" : None, "id" : None, "press" : press, "dt" : dt}
        items.append(item)

    return items

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
  test = ChosunListParser()

  years = range(1998, 1999)
  pages = ["02"]
  for year in years:
    for page in pages:
      test._fetch_list(year, page)

