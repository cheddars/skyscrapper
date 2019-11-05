from crawler.bigkinds_crawler import BigKindCrawler

class BigKindCrawling:
  def __init__(self):
    self.app = BigKindCrawler()
    print("init")

  def crawl_list_and_archive(self, year_page_tuple):
    self.app.crawl_list(year_page_tuple_list = year_page_tuple,
                        search_keyword="북한")

  def crawl_detail(self, year_page_tuple):
    self.app.crawl_detail(year_page_tuple_list = year_page_tuple)

if __name__ == "__main__":
  t = BigKindCrawling()
  #t.crawl_list_and_archive(year_page_tuple=[(2005,	[23])])

  t.crawl_detail([(2003, []),(2004, []),
                  (2005, []),(2006, []),(2007, []),(2008, []),(2009, []),
                  (2010, []),(2011, []),(2012, []),(2013, []),(2014, []),
                  (2015, []),(2016, []),(2017, []),(2018, []),(2019, []),
                  ])

