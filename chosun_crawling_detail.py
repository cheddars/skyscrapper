from crawler.chosun_detail_crawler import ChosunDetailCrawler
from dao.chosun_raw_dao import ChosunRawDao
from time import sleep
from util.util import Util

class ChosunDetailCrawling:
  def __init__(self):
    self.app = ChosunDetailCrawler()
    self.dao = ChosunRawDao()

  def crawl_detail_and_archive(self, year, month, pages):
    util = Util()
    print(f"start {year} {month} {pages}")

    entities = self.dao.findRaw(year=year, month=month)
    if len(pages) > 0:
      filtered_entities = filter(lambda x: x[3] in pages, entities)
    else:
      filtered_entities = entities

    def entity_to_tuple(x):
      return (x[0], x[5])

    id_link_tuples = [entity_to_tuple(i) for i in filtered_entities]

    chunked_id_link_tuples = util.chunks(id_link_tuples, 50)

    for chunk_id_link_tuple in chunked_id_link_tuples:
      content_id_tuples = self.app.crawling(id_link_tuples=chunk_id_link_tuple)
      self.dao.updateRaws(content_id_tuples=content_id_tuples)
      sleep(1)

if __name__ == "__main__":
  a = ChosunDetailCrawling()

  year_range = range(1998, 1999)
  month_range = range(2, 13)
  pages = []

  for year in year_range:
    for month in month_range:
      a.crawl_detail_and_archive(year, month, pages)

