import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Bot

import bs4
import requests
from function.bopomofo import main
from itertools import zip_longest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

class Bs(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def get_text(self, topic, minlen):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("disable-dev-shm-usage")
        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = chrome_options)

        # Direct to 唬爛產生器
        driver.get('https://howtobullshit.me/')

        # 標題
        t = driver.find_element(By.ID, 'topic')
        t.send_keys(topic)
        
        # 字數要求
        m = driver.find_element(By.ID, 'minlen')
        m.send_keys(minlen)

        # 產生(timeout 10 seconds)
        generate = driver.find_element(By.XPATH, '/html/body/main/div/blockquote[2]/div/a')
        generate.click()
        timeout = 10
        for _ in range(10):
            if len(driver.find_element(By.ID, 'content').text) > 0:
                output = driver.find_element(By.ID, 'content').text.replace(' ', '')
                print('Bullshit successfully')
                driver.quit()
                return output
            time.sleep(1)
        else:
            output = f'Timeout ({timeout} seconds)'
            print(output)
            driver.quit()
            return output

    @commands.command(brief='唬爛 <關鍵字> <字數要求(上限1000)>', aliases = ['唬爛'], description='唬爛產生器，Amigo唬爛給你聽')
    async def bs(self, ctx, topic, minlen: int = 10):
        print('Start to bullshit...')
        output = self.get_text(topic, minlen)
        await ctx.send(output)

class Ptt(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.titles = []
        self.prices = []
        self.urls = []

    def get_index(self, board, n):
        """
        Get the last n index on a given board
        """
        url = f"https://www.ptt.cc/bbs/{board}/index.html"
        root = self.readurl(url)
        last_url = root.find("a", class_ = "btn", text = "‹ 上頁").get("href")
        start_idx = last_url.find("index") + 5
        end_idx = last_url.find('.', start_idx)
        index = last_url[start_idx:end_idx]
        return str(int(index) - int(n) + 2)

    def readurl(self, url):
        """
        Read the content of an url
        """    
        web = requests.get(url, headers = {'cookie':'over18=1'})
        if web.status_code == 404: return False
        data = web.text
        root = bs4.BeautifulSoup(data, 'html.parser')
        return root

    def getvalue(self, text, string):
        """
        Get the value of a given text(key)
        """
        try:
            text = text.replace(' ', '').replace('\n', ', ')
            string_index = text.index(f'【{string}】')
            start_index = text.index('：', string_index) + 1
            end_index = text.index(', , ', start_index + 1)
            value = text[start_index:end_index].strip(', ')
            if '★' in value:
                index = value.find('★')
                value = value[:index].strip(',').strip(', ')
            if '【' in value:
                index = value.find('【')
                value = value[:index].strip(',').strip(', ')
            return value
        except:
            return ''

    def getprice(self, url):
        """
        Get price
        """
        root = self.readurl(url)
        content = root.find("div", class_ = 'bbs-screen bbs-content')

        # get content text
        text = content.text

        # get price
        price = self.getvalue(text, '售價')

        return price

    def getdatabyindex(self, index, board, keyword):
        url = f"https://www.ptt.cc/bbs/{board}/index{index}.html"
        root = self.readurl(url)

        # 404 not found
        if not root: 
            print(f"Index {index} not found")
            return self.titles, self.prices, self.urls
        print(f'【Successfully accessed to {board} board {index}】')

        # Find all instances
        articles = root.find_all("div", class_ = "r-ent")
        for article in articles:
            title = article.find("div", class_ = "title")
            if not (title.a and title.a.text): continue
            title = title.a.text

            if main.in_string(keyword, title):
                href = "https://www.ptt.cc" + article.find("div", class_ = "title").a.get("href")
                self.titles.append(title)
                self.urls.append(href)
                if board.lower() == 'gamesale':
                    price = '非販售文' if '售' not in title else self.getprice(href)
                    self.prices.append(price)
        
        # Direct to next page
        return self.getdatabyindex(str(int(index) + 1), board, keyword)

    def getdata(self, board, keyword, n):
        reply = []
        index = self.get_index(board, n)
        print(f"Start searching keyword '{keyword}' on board {board} in the latest {n} pages...")
        
        titles, prices, urls = self.getdatabyindex(index, board, keyword)
        # Clean list cache
        self.titles, self.prices, self.urls = [], [], []

        return titles, prices, urls

    @commands.command(brief = 'ptt <board> <keyword> <n_pages>', description = 'Retrieve titles and urls from ptt by keyword, default n_pages = 3')
    async def ptt(self, ctx, board, keyword, n = 3):
        reply = [f'★看板：{board}；關鍵字：{keyword}']
        titles, prices, urls = self.getdata(board, keyword, n)

        for i, (title, price, url) in enumerate(zip_longest(titles, prices, urls)):
            reply_list = []
            reply_list.append(f'標題：{title}')

            if board.lower() == 'gamesale':
                reply_list.append(f'價格：{price}')
            reply_list.append(f'網址：{url}')
            reply.append('\n'.join(reply_list))

        if len(reply) == 1:
            print('No data found!')
            await ctx.send('No data found!')
        
        else:
            print(f'Successfully retrieved {len(reply)-1} threads!')
            reply = ('\n' + '-' * 80 +'\n').join(reply)
            print(reply)
            await ctx.send(reply)

def setup(bot: Bot):
    bot.add_cog(Ptt(bot))
    bot.add_cog(Bs(bot))