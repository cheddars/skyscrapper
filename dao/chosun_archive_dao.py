from db.database import DataBase

class ChosunArchiveDao:
  def __init__(self):
    self.db = DataBase()

  def saveRaw(self, items):
    print("archiving...")
    def dict_to_tuple(x):
      return (x.get("id"), x.get("year"), x.get("page"), x.get("title"), x.get("link"),
              x.get("dt"))

    binding = [dict_to_tuple(i) for i in items]

    self.db.insert_many("""
      INSERT INTO chosun_archive (
        article_id, year, page, title, link, press_date
      ) VALUES (
        %s, %s, %s, %s, %s, %s
      )
    """, binding)

  def findRaw(self, year, page):
    query = """
      SELECT id, article_id, year, page, title, link,
        press_date
      FROM chosun_archive
      WHERE year = %s
        AND (content is null or length(content) < 20)
        AND is_photo = false
        AND no_content = false
        AND data_error = false
        AND article_id is not null
    """

    if page != None:
      query = query + f" AND page = '{page}'"

    return self.db.queryList(query, (year))

  def updateRaws(self, content_id_tuples):
    print(content_id_tuples)
    print(f"updating {len(content_id_tuples)} rows")
    self.db.update_many("""
      UPDATE chosun_archive
      SET content = %s
      WHERE article_id = %s
    """, content_id_tuples)
