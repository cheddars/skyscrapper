import requests
from time import sleep
from dao.bigkind_raw_dao import BigKindRawDao
import timeit

class BigKindCrawler:
  def __init__(self):
    self.dao = BigKindRawDao()
    print("BigKind Crawler INIT")


  def crawl_list(self, year_page_tuple_list, search_keyword):
    for year_page_tuple in year_page_tuple_list:
      year = year_page_tuple[0]
      pages = year_page_tuple[1]

      self.fetch_list(year=year,
                      pages=pages,
                      start_date=f"{year}-01-01",
                      end_date=f"{year}-12-31",
                      keyword=search_keyword)

  def crawl_detail(self, year_page_tuple_list):

    for year_page_tuple in year_page_tuple_list:
      year = year_page_tuple[0]
      pages = year_page_tuple[1]

      self.fetch_defail(year=year, pages=pages)

  def fetch_list(self, year, pages, start_date, end_date, keyword):
    items_per_page = 100

    if len(pages) < 1:
      search_pages = range(1, 100)
    else:
      search_pages = pages

    print(f"start for year {year} pages : {pages}")

    for page in search_pages:
      sleep(0.5)
      fetch_start = timeit.default_timer()

      result = self._fetch_list(start_date=start_date,
                              end_date=end_date,
                              start_no = page,
                              keyword=keyword,
                              items_per_page=items_per_page)
      fetch_stop = timeit.default_timer()

      total_count = result["totalCount"]
      items = result["resultList"]
      print(f'current page : {page} document count : {len(items)}')
      self.dao.saveMeta(year=year, total=total_count,
                        page=page, doc_count=len(items))
      meta_archive_stop = timeit.default_timer()
      self.dao.saveRaw(year=year, page=page, params=items)
      raw_archive_stop = timeit.default_timer()

      print(f"timing fetch : {fetch_stop - fetch_start}, meta archive : {meta_archive_stop - fetch_stop}, raw archive : {raw_archive_stop - meta_archive_stop}")

      max_page = int(total_count / items_per_page) + 1
      if max_page <= page:
        break

  def fetch_defail(self, year, pages):
    datas = []
    if len(pages) < 1:
      datas = list(self.dao.findRaw(year=year, page=None))
    else:
      for page in pages:
        data = self.dao.findRaw(year=year, page=page)
        print(list(data))
        datas = datas + list(data)

    for d in datas:
      sleep(0.4)
      page = d[1]
      news_id = d[3]
      print(f"fetch item year : {year}, page : {page}, new_id : {news_id}")
      r = self._fetch_detail(doc_id=news_id)
      detail = r["detail"]
      content = detail["CONTENT"]
      self.dao.updateRaw(news_id=news_id, content=content)

  def _fetch_list(self, start_date, end_date, start_no, keyword, items_per_page):
    # codes to fetch list from server
    cookies = {
      '_ga': 'GA1.3.1310965355.1569468143',
      '_gid': 'GA1.3.1674209465.1569468143',
      'Bigkinds': '8A234DEDE35E7E298A9402BABDBA261F',
      '_gat': '1',
    }

    headers = {
      'Sec-Fetch-Mode': 'cors',
      'Origin': 'https://www.bigkinds.or.kr',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
      'Pragma': 'no-cache',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
      'Content-Type': 'application/json;charset=UTF-8',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Cache-Control': 'no-cache',
      'Referer': 'https://www.bigkinds.or.kr/v2/news/search.do',
      'Sec-Fetch-Site': 'same-origin',
    }

    provider = {"한겨레": "01101001", "조선일보": "01101001"}

    data = '''
            {{"indexName":"news","searchKey":"{0}","searchKeys":[{{}}],"byLine":"",
            "searchFilterType":"1","searchScopeType":"1","searchSortType":"date",
            "sortMethod":"date","mainTodayPersonYn":"",
            "startDate":"{1}",
            "endDate":"{2}",
            "newsIds":[],"categoryCodes":[],
            "providerCodes":["{3}"],"incidentCodes":[],
            "networkNodeType":"","topicOrigin":"","startNo":{4},
            "resultNumber":{5},"dateCodes":[],"isTmUsable":false,"isNotTmUsable":false}}
    '''.format(keyword, start_date, end_date, provider['한겨레'],
               start_no, items_per_page)

    response = requests.post('https://www.bigkinds.or.kr/api/news/search.do', headers=headers, cookies=cookies,
                             data=data.encode("utf-8"))

    r = response.json()
    return r

  def _fetch_detail(self, doc_id):
    cookies = {
      'Bigkinds': '5618A6040DA9B974D88AE8C1162AA8DD',
      '_ga': 'GA1.3.1497040146.1569671045',
      '_gid': 'GA1.3.2054055760.1569671045',
    }

    headers = {
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Referer': 'https://www.bigkinds.or.kr/v2/news/search.do;Bigkinds=5618A6040DA9B974D88AE8C1162AA8DD',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
    }

    params = (
      ('docId', doc_id),
      ('returnCnt', '1'),
      ('sectionDiv', '1000'),
    )

    response = requests.get('https://www.bigkinds.or.kr/news/detailView.do', headers=headers, params=params,
                            cookies=cookies)
    r = response.json()
    return r

if __name__ == "__main__":
  test = BigKindCrawler()

  # test.crawl_list()
  #
  # years = ["1998"]
  # for year in years:
  #   num = test.fetch_list(start_date=f"{year}-01-01",
  #                         end_date=f"{year}-12-31",
  #                         keyword="북한")

  result = test._fetch_detail(doc_id="01101001.20050521100014531")
  print(result)
