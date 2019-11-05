from db.database import DataBase
import json

class BigKindRawDao:
  def __init__(self):
    self.db = DataBase()

  def saveMeta(self, year, total, page, doc_count):

    self.db.insert("""
      INSERT INTO bigkind_meta (
        year, total_count, page, doc_count
      ) VALUES (
        %s, %s, %s, %s
      )
    """, (year, total, page, doc_count))

  def completedListMeta(self, year):
    self.db.update("""
      UPDATE bigkind_meta
      SET list_completed = true
      WHERE year = %s
    """, (year))

  def saveRaw(self, year, page, params):

    def dict_to_tuple(x):
      date = ''
      if(x.get("DATE") == ''):
        date = None
      else:
        date = x.get("DATE")

      return (year, page, x.get("TITLE"), x.get("NEWS_ID"), date,
              x.get("CONTENT"), x.get("CATEGORY_NAMES"), x.get("PROVIDER"), x.get("BYLINE"),
              json.dumps(x))

    binding = [dict_to_tuple(i) for i in params]

    self.db.insert_many("""
      INSERT INTO bigkind_raw (
        year, page, title, news_id, press_date,
        content_abbr, category_names, provider, byline, checked,
        data
      ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, false,
        %s
      )
    """, binding)

  def updateRaw(self, news_id, content):
    self.db.update("""
      UPDATE bigkind_raw
      SET content = %s
      WHERE news_id = %s
      AND content is null
    """, (content, news_id))

  def findRaw(self, year, page):
    query = """
      SELECT 
        year, page, title, news_id
      FROM bigkind_raw
      WHERE year = %s
        AND content is null
    """

    if page != None:
      query = query + f" AND page = '{page}'"

    return self.db.queryList(query,(year))