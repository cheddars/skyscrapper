from crawler.chosun_archive_detail_crawler import ChosunArchiveDetailCrawler
from dao.chosun_archive_dao import ChosunArchiveDao
from time import sleep
from util.util import Util

class ChosunArchiveDetail:
  def __init__(self):
    self.app = ChosunArchiveDetailCrawler()
    self.dao = ChosunArchiveDao()

  def parse_and_save(self, year, page):
    util = Util()

    entities = self.dao.findRaw(year, page)

    def entity_to_tuple(x):
      return (x[1])

    id_list = [entity_to_tuple(i) for i in entities]

    chunked_id_list = util.chunks(id_list, 50)

    for ids in chunked_id_list:
      items = self.app.crawling(ids)
      self.dao.updateRaws(items)

if __name__ == "__main__":
  a = ChosunArchiveDetail()

  year_range = range(1998, 2020)

  for year in year_range:
    a.parse_and_save(year, None)

