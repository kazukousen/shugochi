# coding:utf-8
import urllib2
from bs4 import *
from urlparse import urljoin
import sqlite3 as sqlite

# 無視すべき単語のリストをつくる
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])

class crawler:
  # データベースの名前でクローラを初期化する
  def __init__(self, dbname):
    self.con = sqlite.connect(dbname)

  def __del__(self):
    self.con.close()

  def dbcommit(self):
    self.con.commit()

  # エントリIDを取得したり、それが存在しない場合には追加
  # するための補助関数
  def getentryid(self, table, field, value, createnew=True):
    return None

  # 個々のページをインデックスする
  def addtoindex(self, url, soup):
    print 'Indexing %s' % url

  # HTMLのページからタグのない状態でテキストを摘出する
  def gettextonly(self, soup):
    return None

  # 空白以外の文字で単語を分割する
  def separetewords(self, text):
    return None

  # URLが既にインデックスされていたらtrueを返す
  def isindexed(self, url):
    return False

  # 2つのページの間にリンクを付け加える
  def addlinkref(self, urlFrom, urlTo, linkText):
    pass

  # データベースのテーブルを作る
  def createindextables(self):
    self.con.execute('create table urllist(url)')
    self.con.execute('create table wordlist(word)')
    self.con.execute('create table wordlocation(urlid, wordid, location)')
    self.con.execute('create table link(fromid integer, toid integer)')
    self.con.execute('create table linkwords(wordid, linkid)')
    self.con.execute('create index wordidx on wordlist(word)')
    self.con.execute('create index urlidx on urllist(url)')
    self.con.execute('create index wordurlidx on wordlocation(wordid)')
    self.con.execute('create index urltoidx on link(toid)')
    self.con.execute('create index urlfromidx on link(fromid)')
    self.dbcommit()

  # ページのリストを受け取り、与えられた深さで幅優先の検索を行い
  # ページをインデクシングする
  def crawl(self, pages, depth=2):
    for i in range(depth):
      newpages=set()
      for page in pages:
        try:
          c=urllib2.urlopen(page)
        except:
          print "Could not open %s" % page
          continue
        soup = BeautifulSoup(c.read())
        self.addtoindex(page, soup)

        links = soup('a')
        for link in links:
          if ('href' in dict(link.attrs)):
            url = urljoin(page, link['href'])
            if url.find("'")!=-1: continue
            url = url.split("#")[0] # アンカーを取り除く
            if url[0:4]=='http' and not self.isindexed(url):
              newpages.add(url)
            linkText = self.gettextonly(link)
            self.addlinkref(page, url, linkText)

        self.dbcommit()
      pages = newpages
