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

def getprice(url, board):
    root = readurl(url)
    content = root.find('div', class_ = 'bbs-screen bbs-content')
    text = content.text
    try:
        text = text.replace(' ', '')
        start_index = text.index('【售價】' if board == 'gamesale' else '[售價]') + 4 + int(board == 'gamesale')
        end_index = text.index('★' if board == 'gamesale' else '[', start_index)
        value = text[start_index:end_index].strip('\n')
        return '\n' + value if '\n' in value else value
    except Exception as Ex:
        return str(Ex)

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
            if board.lower() in ('gamesale', 'macshop'):
                price = '非販售文' if '售' not in title else getprice(href, board)
                prices.append(price)
    
    # Direct to next page
    return getdatabyindex(str(int(index) + 1), board, keyword, titles, prices, urls)

def formatted_reply(titles, prices, urls):
    reply = []
    for i, (title, price, url) in enumerate(zip_longest(titles, prices, urls)):
        reply_list = []
        reply_list.append(f'標題：{title}')
        if prices:
            reply_list.append(f'價格：{price}')
        reply_list.append(f'網址：{url}')
        reply.append('\n'.join(reply_list))
    reply = ('\n' + '-' * 80 +'\n').join(reply)
    return reply

def getdata(board, keyword, n):
    reply = []
    index = get_index(board, n)
    print(f"Start searching keyword '{keyword}' on board {board} in the latest {n} pages...")
    titles, prices, urls = getdatabyindex(index, board, keyword, [], [], [])
    return titles, prices, urls
