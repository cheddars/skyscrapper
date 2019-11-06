from db.database import DataBase

class ChosunRawDao:
  def __init__(self):
    self.db = DataBase()

  def saveMeta(self, year, month, total, page, page_item):
    self.db.insert("""
      INSERT INTO chosun_meta (
        year, month, total_count, page, items
      ) VALUES (
        %s, %s, %s, %s, %s
      )
    """, (year, month, total, page, page_item))

  def saveRaw(self, year, month, page, params):

    def dict_to_tuple(x):
      return (year, month, page, x.get("title"), x.get("link"),
              x.get("date"), x.get("content_abbr"))

    binding = [dict_to_tuple(i) for i in params]

    self.db.insert_many("""
      INSERT INTO chosun_raw (
        year, month, page, title, link,
        press_date, content_abbr
      ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s
      )
    """, binding)
