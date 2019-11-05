
class ChosunCrawler:
  def __init__(self):
    print("ChosunCrawling init")

  def crawling(self):
    print("crawling")

  def _fetch_list(self, startDate, endDate):
    import requests
    from bs4 import BeautifulSoup

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

    startDate = "1980-01-24"
    endDate = "2019-08-24"

    params = (
      ('query', '\uBD81\uD55C'),
      ('siteid', ''),
      ('category', ''),
      ('sort', '1'),
      ('writer', ''),
      ('field', ''),
      ('date_period', ''),
      ('date_start', '1980-01-24'),
      ('date_end', '2019-08-24'),
      ('emd_word', ''),
      ('expt_word', ''),
      ('opt_chk', ''),
    )

    response = requests.get('http://nsearch.chosun.com/search/total.search', headers=headers, params=params,
                            cookies=cookies, verify=False)


if __name__ == "__main__":
  test = ChosunCrawler()

  test.crawling()