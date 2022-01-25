import json
import requests
import argparse
import yaml
from mysql import connector as myc
from datetime import datetime,timedelta

class TILT2BF:
  def __init__(self, args):
    self.args = args
    configfile = 'config.yaml'
    if args.config is not None:
      configfile = args.config
    self.config = yaml.safe_load(open(configfile, 'r'))
    self.time_start = datetime.now() - timedelta(seconds=900)
    self.time_end = datetime.now()
    self.cnx = myc.connect(**self.config['db'])


  def send_to_api(self, color, temp, sg):
    url = 'https://log.brewersfriend.com/stream/'
    headers = {
      'Content-Type': 'application/json',
      'X-API-KEY': self.config["API_KEY"]
    }
    body = {
      'device_source': "Tilt {}".format(color),
      'report_source': 'tilt2bf',
      'name': "Tilt {}".format(color),
      'temp': temp,
      'temp_unit': 'F',
      'gravity': sg,
      'gravity_unit': 'G'
    }
    r = requests.post(url, headers=headers, data=json.dumps(body))
    # print('Response Code: {}'.format(r.status_code))
    # print(r.text)


  def get_colors(self):
    query = "select distinct color from tilt_readings where insert_dttm between %s and %s"
    colors = []
    cursor = self.cnx.cursor()
    cursor.execute(query, (self.time_start, self.time_end))
    for color in cursor:
      colors.append(color[0])
    cursor.close()
    return colors


  def get_values(self, color):
    query = "select temperature, sg from tilt_readings where color = %s and insert_dttm between %s and %s"
    temperature = []
    sg = []
    cursor = self.cnx.cursor()
    cursor.execute(query, (color, self.time_start, self.time_end))
    for (t,s) in cursor:
      temperature.append(t)
      sg.append(s)
    cursor.close()
    avg_temp = round(sum(temperature) / len(temperature))
    avg_sg = round(sum(sg) / len(sg), 3)
    return (avg_temp, avg_sg)


  def close_db_connection(self):
    self.cnx.close()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config', help="Location of the configuration file", default="config.yaml")
  args = parser.parse_args()

  t2bf = TILT2BF(args)
  try:
    colors = t2bf.get_colors()
    for color in colors:
      temperature, sg = t2bf.get_values(color)
      t2bf.send_to_api(color, temperature, sg)

  except:
    pass

  finally:
    t2bf.close_db_connection()