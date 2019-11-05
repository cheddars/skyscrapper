import pymysql
import configparser

class DataBase:
  def __init__(self):
    config = configparser.ConfigParser()
    config.read("config.ini")
    self.db_config = config['db']

  def open(self):
    self.db = pymysql.connect(host=self.db_config["host"],port=int(self.db_config["port"]),
                              user=self.db_config["user"], passwd=self.db_config["passwd"],
                              db=self.db_config["database"],
                              charset="utf8")
                              #init_command="SET SESSION time_zone='Asia/Seoul'")

  def close(self):
    self.db.close()


  def queryOne(self, query, binding):
    row = None
    try:
      self.open()
      with self.db.cursor() as cursor:
        cursor.execute(query, binding)
        row = cursor.fetchone()
    finally:
      self.db.close()
    return row

  def queryList(self, query, binding):
    rows = None
    try:
      self.open()
      with self.db.cursor() as cursor:
        cursor.execute(query, binding)
        rows = cursor.fetchall()
    finally:
      self.db.close()
    return rows

  def insert(self, query, binding):
    try:
      self.open()
      with self.db.cursor() as cursor:
        cursor.execute(query, binding)

      self.db.commit()
    except Exception as e:
      print(e.value)

    finally:
      self.db.close()

  def update(self, query, binding):
    try:
      self.open()
      with self.db.cursor() as cursor:
        cursor.execute(query, binding)

      self.db.commit()
    except Exception as e:
      print(e.value)

    finally:
      self.db.close()

  def insert_many(self, query, binding):
    try:
      self.open()
      with self.db.cursor() as cursor:
        cursor.executemany(query, binding)

      self.db.commit()
    except Exception as e:
      print(e)

    finally:
      self.db.close()

  def escape(self, str):
    self.open()
    s = self.db.escape_string(str)
    self.close()
    return s


if __name__ == "__main__":
  db = DataBase();

  #db.insert("INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)", ('webmaster@python.org', 'very-secret'))

  rows = db.queryList("select * from stock where 1=1 and '' <> %s", ('webmaster@python.org',))
  row = db.queryOne("select * from stock where 1 = 1", ())
  print(row)
  print(rows)