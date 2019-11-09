from data.chosun_archive_parser import ChosunListParser
from dao.chosun_archive_dao import ChosunArchiveDao
from time import sleep
from util.util import Util

class ChosunArchiveList:
  def __init__(self):
    self.app = ChosunListParser()
    self.dao = ChosunArchiveDao()

  def parse_and_save(self, year, page):
    items = self.app._fetch_list(year, page)
    self.dao.saveRaw(items)

if __name__ == "__main__":
  a = ChosunArchiveList()

  year_range = range(2001, 2002)
  pages = ["01","02", "03","04", "05","06","07","08","09","10","11", "12","13", "14"]

  for year in year_range:
    for page in pages:
      a.parse_and_save(year, page)

