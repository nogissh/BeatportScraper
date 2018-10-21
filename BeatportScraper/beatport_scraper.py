import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class BeatportScraper:

  def __init__(self):
    # Ready for getting beatport data

    self.data = {}

    # Set User-Agent to `chrome`
    ua = UserAgent()
    self.headers = {
      "User-Agent": str(ua.chrome),
    }

    # Save pass
    self.savePass = './data/{}.json'
  

  def find_json(self):
    # Find and transport to json
    t = self.soup.find_all("script")
    t = t[5].string
    t = t.replace("\n     window.ProductDetail = ", "")
    self.bp_json = json.loads(t)
    return None


  def get_id(self):
    # Track id
    self.data["beatport_id"] = self.bp_json["id"]
    return None


  def get_title(self):
    # Track title
    self.data["title"] = self.bp_json["name"]
    return None

  
  def get_mix(self):
    # Track mix
    self.data["mix"] = self.bp_json["mix"]
    return None


  def get_artists(self):
    # Artists
    self.data["artists"] = []
    for p in self.bp_json["artists"]:
      self.data["artists"].append(p)
    return None


  def get_remixers(self):
    # Remixier
    self.data["remixers"] = []
    for p in self.bp_json["remixers"]:
      self.data["remixers"].append(p)


  def get_genres(self):
    # Genre 
    self.data["genres"] = []
    for p in self.bp_json["genres"]:
      self.data["genres"].append(p)


  def get_bpm(self):
    # BPM
    self.data["bpm"] = self.bp_json["bpm"]
    return None


  def get_key(self):
    # Transport binary text to normal text
    t = (self.bp_json["key"]).encode()
    if b"\xe2\x99\xaf" in t:
      t = t.replace(b"\xe2\x99\xaf", b"#") # "#"
    elif b"\xe2\x99\xad" in t:
      t = t.replace(b"\xe2\x99\xad", b"b") # "b"
    self.data["key"] = t.decode()
    return None


  def get_length(self):
    # Track length
    t = self.bp_json["duration"]["milliseconds"]
    t = int(t / 1000)
    self.data["length"] = t
    return None

  
  def get_label(self):
    # label
    self.data["label"] = {}
    self.data['label']['id'] = self.bp_json['label']['id']
    self.data['label']['name'] = self.bp_json["label"]["name"]
    return None


  def get_date(self):
    # Release date
    self.data["date"] = self.bp_json["date"]["released"]
    return None


  def get_url(self):
    # Track URL of Beatport
    self.data["url"] = \
      "https://www.beatport.com/track/{}/{}".format(self.bp_json["slug"], self.data["beatport_id"])


  def get_artwork(self):
    # Track artwork
    self.data["artwork"] = self.bp_json["images"]["large"]["url"]
    return None


  def get_recommendation(self):

    def forError(soup, i):
      try:
        t = soup.select("#data-objects")
        t = t[0].string
        t = t.split(";")
        t = t[i]
        t = t.replace("         window.Playables = ", "")
        return json.loads(t)
      except json.decoder.JSONDecodeError:
        if i > 20:
          return None
        return forError(soup, i+1)

    # Recommendation track list
    t = forError(self.soup, 1)
    rec_id = []
    for i in range(len(t['tracks'])):
      rec_id.append(t['tracks'][i]['id'])
    self.recommendlist = rec_id


  def writeJSON(self):
    filepath = self.savePass.format(self.data['beatport_id'])
    with open(filepath, "w") as f:
      json.dump(self.data, f, indent=2, separators=(",", ":"))


  def run(self, url, jsonfile=False):

    # Get `soup` object
    html = requests.get(url, self.headers)
    self.soup = BeautifulSoup(html.text, "lxml")

    # Complete data all you need
    self.find_json()
    self.get_id()
    self.get_title()
    self.get_mix()
    self.get_artists()
    self.get_remixers()
    self.get_genres()
    self.get_bpm()
    self.get_key()
    self.get_length()
    self.get_label()
    self.get_date()
    self.get_url()
    self.get_artwork()
    self.get_recommendation()
    self.writeJSON()


import sys
if __name__ == '__main__':
  bs = BeatportScraper()
  bs.run(sys.argv[1])
  del bs
