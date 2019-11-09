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

  def findRaw(self, year, month):
    return self.db.queryList("""
      SELECT id, year, month, page, title, link,
        press_date
      FROM chosun_raw
      WHERE year = %s
        AND month = %s
        AND content is null
        AND is_photo = false
        AND no_content = false
        AND data_error = false
    """, (year, month))

  def updateRaws(self, content_id_tuples):
    print(content_id_tuples)
    print(f"updating {len(content_id_tuples)} rows")
    self.db.update_many("""
      UPDATE chosun_raw
      SET content = %s
      WHERE id = %s
    """, content_id_tuples)
