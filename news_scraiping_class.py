from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from time import sleep
import re
import pandas as pd
from selenium.webdriver.chrome.options import Options

class URL_SCR:
  def __init__(self):
      self.news_list = []
      self.key = ""

  # 朝日新聞の場合**********************************************************

  def asahi(self,soup,media):
    f_data = []
    for i,elem in enumerate(soup(text=re.compile(self.key))):
      elem_text = elem.replace("\u3000","")
      #テキストタグ
      f = elem.parent
      ff = f.get("href")
      f_dict = {}
      f_dict["media"] = media
      f_dict["text"] = elem_text
      f_dict["url"] = ff
      if f_dict["url"] is None:
        f_dict.clear()
        continue
      else:
          if re.compile("https").search(f_dict["url"]):
              pass
          else:
              f_dict["url"] = "https://www.asahi.com{}".format(f_dict["url"])
      self.news_list.append(f_dict)
    print("朝日OK")

  # ライブドアの場合**********************************************************
  def livedoor(self,soup,media):
    l_data = []
    ele = soup.find(class_="straightList")
    ele_a = ele.find_all("a")

    for element in ele_a:
      l_dict = {} 
      ele_text = element.find(class_="straightTtl")
      if re.compile(self.key).search(ele_text.string):
        l_dict["media"] = media
        l_dict["text"] = ele_text.string
        l_dict["url"] = element["href"]
        if l_dict['url'] is None:
          l_dict.clear()
          continue
        self.news_list.append(l_dict)
    print("ライブOK")

  # NHKの場合**********************************************************
  def nhk(self,soup,media):

    option = Options()                          # オプションを用意
    option.add_argument('--headless')           # ヘッドレスモードの設定を付与
    driver = webdriver.Chrome(options=option) 

    driver.get("https://www3.nhk.or.jp/news/catnew.html")

    footer = driver.find_element_by_tag_name("footer")

    for i in range(5):
      cnt_btn = footer.find_element_by_class_name("button")
      driver.execute_script("arguments[0].click();", cnt_btn)

      
      # cnt_btn.click()
      sleep(1)

    html = driver.page_source
    soup = bs(html,"html.parser")

    n_elements = soup.find_all(class_="title")

    n_data = []
    for n_element in n_elements:
      n_dict = {}
      if re.compile(self.key).search(n_element.string):
        n_dict["media"] = media
        n_dict["text"] = n_element.string
        n_dict["url"] = "https://www3.nhk.or.jp{}".format(n_element.parent["href"])
        if n_dict['url'] is None:
          n_dict.clear()
          continue
        self.news_list.append(n_dict)

    driver.quit()

    print("nhkOK")

  # 宮崎日日新聞の場合**********************************************************
  def miyazaki(self,soup,media):

    m_data = []
    m_elements = soup.select(".item_list a")

    for m_element in m_elements:
      m_dict = {}
      if re.compile(self.key).search(m_element.contents[0].string):
        m_dict["media"] = media
        m_dict["text"] = m_element.contents[0].string
        m_dict["url"] = m_element["href"]
        if m_dict['url'] is None:
          m_dict.clear()
          continue
        self.news_list.append(m_dict)
    print("宮日OK")

  # 読売新聞の場合**********************************************************
  def yomiuri(self,soup,media):

    option = Options()                          # オプションを用意
    option.add_argument('--headless')           # ヘッドレスモードの設定を付与
    driver = webdriver.Chrome(options=option) 
    driver.get("https://www.yomiuri.co.jp/news/")

    cnt_btn = driver.find_element_by_id("ajax_more_button")
    driver.execute_script("arguments[0].click();", cnt_btn)
    # cnt_btn.click()
    sleep(1)

    html = driver.page_source
    soup = bs(html,"html.parser")

    y_lists = soup.find_all(class_="news-top-latest__list")

    y_data = []
    i = 0
    for y_list in y_lists:
      y_elements = y_list.find_all("h3")
      for y_element in y_elements:
        y_dict = {}
        if re.compile(self.key).search(y_element.string):
          y_dict["media"] = media
          y_dict["text"] = y_element.string
          y_dict["url"] = y_element.a["href"]
          if y_dict['url'] is None:
            y_dict.clear()
            continue
          self.news_list.append(y_dict)
    driver.quit()
    print("読売OK")


  
  def scraipe(self,key):
    self.key = key
    url_list = {"朝日新聞":"https://www.asahi.com/news/",
            "読売新聞":"https://www.yomiuri.co.jp/news/",
            "ライブドア":"https://news.livedoor.com/straight_news/",
            "NHK":"https://www3.nhk.or.jp/news/catnew.html",
            "宮崎日日新聞":"https://www.the-miyanichi.co.jp/kennai/"}
    news_list = []
    pass
    for media,url in url_list.items():
      headers = {"User-Agent": "Mozilla/.... Chrome/.... Safari/...."}
      html = requests.get(url, headers = headers)
      soup = bs(html.content, 'html.parser')

      if(media == "朝日新聞"):
        self.asahi(soup,media)
      elif(media == "読売新聞"):
        self.yomiuri(soup,media)
      elif(media == "ライブドア"):
        self.livedoor(soup,media)
      elif(media == "NHK"):
        self.nhk(soup,media)
      elif(media == "宮崎日日新聞"):
        self.miyazaki(soup,media)
      sleep(1)

    df = pd.DataFrame(self.news_list)

    print(df)
    df.to_csv("newsList.csv", encoding='utf_8_sig', index=False)
    df_text = "{}".format(df)
    return df