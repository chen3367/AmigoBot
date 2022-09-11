import bs4
import requests
from function.bopomofo import main
from itertools import zip_longest

def get_index(board, n):
    """
    Get the last n index on a given board
    """
    url = f"https://www.ptt.cc/bbs/{board}/index.html"
    root = readurl(url)
    last_url = root.find("a", class_ = "btn", text = "‹ 上頁").get("href")
    start_idx = last_url.find("index") + 5
    end_idx = last_url.find('.', start_idx)
    index = last_url[start_idx:end_idx]
    return str(int(index) - int(n) + 2)

def readurl(url):
    """
    Read the content of an url
    """    
    web = requests.get(url, headers = {'cookie':'over18=1'})
    if web.status_code == 404: return False
    data = web.text
    root = bs4.BeautifulSoup(data, 'html.parser')
    return root

def getvalue(text, string):
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

def getprice(url):
    """
    Get price
    """
    root = readurl(url)
    content = root.find("div", class_ = 'bbs-screen bbs-content')

    # get content text
    text = content.text

    # get price
    price = getvalue(text, '售價')

    return price

def getdatabyindex(index, board, keyword, titles, prices, urls):
    url = f"https://www.ptt.cc/bbs/{board}/index{index}.html"
    root = readurl(url)

    # 404 not found
    if not root: 
        print(f"Index {index} not found")
        return titles, prices, urls
    print(f'【Successfully accessed to {board} board {index}】')

    # Find all instances
    articles = root.find_all("div", class_ = "r-ent")
    for article in articles:
        title = article.find("div", class_ = "title")
        if not (title.a and title.a.text): continue
        title = title.a.text

        if main.in_string(keyword, title):
            href = "https://www.ptt.cc" + article.find("div", class_ = "title").a.get("href")
            titles.append(title)
            urls.append(href)
            if board.lower() == 'gamesale':
                price = '非販售文' if '售' not in title else getprice(href)
                prices.append(price)
    
    # Direct to next page
    return getdatabyindex(str(int(index) + 1), board, keyword, titles, prices, urls)

def getdata(board, keyword, n):
    reply = []
    index = get_index(board, n)
    print(f"Start searching keyword '{keyword}' on board {board} in the latest {n} pages...")
    titles, prices, urls = getdatabyindex(index, board, keyword, [], [], [])
    return titles, prices, urls
