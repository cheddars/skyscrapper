from crawler.chosun_crawler import ChosunCrawler
from dao.chosun_raw_dao import ChosunRawDao
from time import sleep

class ChosunCrawling:
  def __init__(self):
    self.app = ChosunCrawler()
    self.dao = ChosunRawDao()

  def crawl_list_and_archive(self, year, month, pages):
    datas = self.app.crawling(year = year, month=month, pages=pages)

    for data in datas:
      print(data)
      self.dao.saveMeta(year, month, data[0], data[1], data[2])
      self.dao.saveRaw(year, month, data[1], data[3])


if __name__ == "__main__":
  a = ChosunCrawling()

  #for year in range(2004, 2020):
  #  for month in range(1, 13):
  #    a.crawl_list_and_archive(year = year, month=month, pages=[])
  #    sleep(5)
  #  sleep(10)

  for month in range(11, 13):
    a.crawl_list_and_archive(year = 2014, month=month, pages=[])
