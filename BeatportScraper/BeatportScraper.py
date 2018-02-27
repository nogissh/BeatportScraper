import os, sys, time

from modules import TrackScraper


class BeatportScraper:

  def __init__(self):
    try:
      os.mkdir("data")
    except FileExistsError:
      pass

  def getid_fromUrl(self, url):
    return url.split("/")[-1]


  def excheck_json(self, path):
    #ファイルの有無チェック（JSON）
    return os.path.isfile(path)


  def run(self, url, loop=1, jsonfile=False):

    t = self.getid_fromUrl(url) #URLからIDを抽出

    idlist = [t]
    for i in range(loop):

      # ファイルがあればスキップ
      path = "data/{}.json".format(idlist[i])
      if self.excheck_json(path) and jsonfile:
        continue

      # 楽曲のデータを取得
      ts = TrackScraper(idlist[i])
      ts.run(jsonfile)
      idlist += ts.recommendlist #オススメ曲IDをリストに追加

      # jsonfileがTrueならファイル吐き出し
      if jsonfile == True:
        ts.writeJSON(path)

      del ts #デストラクト

      if i < loop-1:
        time.sleep(1)

    return None


if __name__ == "__main__":

  url = sys.argv[1]

  bs = BeatportScraper()
  bs.run(url, loop=1, jsonfile=True)