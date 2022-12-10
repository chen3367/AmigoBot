import discord
from discord.ext import commands
from discord.ext.commands import Bot

import bs4
import requests
from function.bopomofo import main
from function.ptt import formatted_reply, getdata
from itertools import zip_longest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        await ctx.send('唬爛中...')
        output = self.get_text(topic, minlen)
        await ctx.send(output)

class Wife(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def get_wife(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("disable-dev-shm-usage")
        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = chrome_options)

        driver.get('https://waifulabs.com/generate')

        portrait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]'))
        )
        portrait.click()
        for _ in range(3):
            p = driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div[2]')
            p.click()

        img = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/img')
        time.sleep(2)
        img.screenshot('images/screenshot.png')
        driver.quit()
    
    @commands.command(description='二次元老婆產生器')
    async def wife(self, ctx):
        await ctx.send('生成中...')
        self.get_wife()
        await ctx.send(file = discord.File('images/screenshot.png'))

class Ptt(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    @commands.command(brief = 'ptt <board> <keyword> <n_pages>', description = 'Retrieve titles and urls from ptt by keyword, default n_pages = 3')
    async def ptt(self, ctx, board, keyword, n = 3):
        await ctx.send(f'★看板：{board}；關鍵字：{keyword} 搜尋中...')
        titles, prices, urls = getdata(board, keyword, n)
        reply = formatted_reply(titles, prices, urls)

        if not reply:
            print('No data found!')
            await ctx.send('No data found!')
        
        else:
            print(f'Successfully retrieved {len(reply)} threads!')
            print(reply)
            await ctx.send(reply)

async def setup(bot: Bot):
    await bot.add_cog(Ptt(bot))
    await bot.add_cog(Bs(bot))
    await bot.add_cog(Wife(bot))