import time
import configparser
from datetime import datetime

class Util:
  def __init__(self):
    self.config = configparser.ConfigParser()
    self.config.read("config.ini")

  def chunks(self, items, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(items), n):
      yield items[i:i + n]

  def ymd(self, dt=datetime.now()):
    return dt.strftime('%Y%m%d')

  def hhmm(self, dt=datetime.now()):
    hh = dt.strftime("%H")
    mm = int(dt.strftime("%M"))
    return "{}{}".format(hh, ("0" + str(int(mm / 5) * 5))[-2:])

  def prop(self, key, group="db"):
    return self.config[group].get(key)

  def millis(self):
    return int(round(time.time() * 1000))

  def sleep_mins(self, min):
    time.sleep(min * 60)

  def delta_in_seconds(self, start_mills, end_mills):
    return (end_mills - start_mills) / 1000

  def chunksize(self, exchange, item_size):
    split = ["0", "10"]  # 0:장내 10:코스닥, 30:K-OTC, 50:코넥스(KONEX)
    return int(item_size / 10) + 1 if exchange in split else item_size + 1



class DictUtil:
  def merge_dict(self, l1, l2, key):
    merged = {}
    for item in l1 + l2:
      if item[key] in merged:
        merged[item[key]].update(item)
      else:
        merged[item[key]] = item
    return [val for (_, val) in merged.items()]

  def rename_fields(self, items, fields, prefix):
    for item in items:
      for field in fields:
        item.update({"{}_{}".format(prefix, field) : item[field]})

    return items

import traceback
import logging

class Logger:
    def __init__(self, logname):
      u = Util()
      log_dir = u.prop("log_dir", "common")
      file = "{}/{}_{}".format(log_dir, "info", u.ymd())
      self.logger = logging.getLogger(logname)
      self.logger.setLevel(logging.DEBUG)
      handler = logging.FileHandler(file)
      handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
      self.logger.addHandler(handler)
      self.logger.addHandler(logging.StreamHandler())

    def debug(self, msg):
      self.logger.debug(msg)

    def info(self, msg):
      self.logger.info(msg)

    def error(self, msg):
      self.logger.error(msg)
