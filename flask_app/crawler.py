from importlib.resources import path
import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

def get_page(page_url):
    soup = None
    page = None

    with requests.get(page_url) as page:
        try:
            page.raise_for_status()
        except HTTPError as Err:
            print(Err)
        else:
            soup = BeautifulSoup(page.content, 'html.parser')

    return soup, page

def collect_naver_data():
    
    BASE_URL = "https://comic.naver.com"
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    # day = "mon"
    webtoons = []        
    
    for day in days:
        
        FULL_URL = BASE_URL + f"/webtoon/weekdayList?week={day}&order=ViewCount&view=list"
        print(FULL_URL)
        soup, page = get_page(FULL_URL)    
        
        trs = soup.select("tr")
        for i, tr in enumerate(trs):
            if i > 5: break
            # print(tr)
            # print("======================================")
            toon = {}
            if None == tr.select_one("a"): continue
            toon["title"] = tr.select_one("a").string
            toon["href"] = BASE_URL + tr.select_one("a")["href"]
            toon["rate"] = float(tr.select_one(".rating_type > strong").string)
            toon["id"] = int(re.findall(r"\d+", toon["href"])[0])
            soup_into, page_into = get_page(toon["href"])
            author = soup_into.select_one(".wrt_nm").string.strip()
            toon["author"] = str.split(author," / ")
            genre = soup_into.select_one(".genre").string.strip()
            toon["genre"] = str.split(genre,", ")
            toon["age"] = soup_into.select_one(".age").string.strip()
            toon["day"] = day
            toon["views_rank"] = i
            print(toon)
            webtoons.append(toon)
            # print(toon)
        
    print(len(webtoons))
    return webtoons

def collect_kakao_data():
    from selenium import webdriver
    # from selenium.common.exceptions import WebDriverException as WDE
    from selenium.webdriver.common.keys import Keys    
    from selenium.webdriver import ActionChains
    import os 
    import time
    from html.parser import HTMLParser

    PATH = os.getcwd() + "/flask_app/chromedriver"
    "https://webtoon.kakao.com/original-webtoon?tab=mon"
    BASE_URL = "https://webtoon.kakao.com"
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    FULL_URL = BASE_URL + f"/original-webtoon?tab=mon"

    browser = webdriver.Chrome(PATH)
    browser.maximize_window()
    # action = ActionChains(driver=browser)
    print(FULL_URL)
    browser.get(FULL_URL)
    time.sleep(1)
    html = browser.page_source
    soup = BeautifulSoup(str(html),'html.parser')
    body = soup.find("body")
    next = body.select_one("#__next > .h-full > main > div > div")
    uniqueid = next.find(__uniqueid="2")
    div6 = uniqueid.select_one("div > .swiper-slide.swiper-slide-active > div > div")

    # div = uniqueid.select_one("div > .swiper-slide.swiper-slide-active > ")
    # next = body.select_one("#__next")
    # h_full = next.select_one(".h-full")
    # main = h_full.select_one("main")
    # div1 = main.select_one("div")
    # div2 = div1.select_one("div")
    # div3 = div2.find(__uniqueid="2")
    # div4 = uniqueid.select_one("div")
    # div5 = div4.select_one(".swiper-slide.swiper-slide-active")
    # div6 = div5.select_one("div > div")

    div7 = div6.select_one(".relative.day-section")
    div8 = div7.select("div")[19]
    relatives = div8.select("div")
    # print(relatives)
    links = set()
    for rel in relatives:
        a = rel.select_one("a")
        if None != a:
            # print(a["href"])
            links.add(a["href"])
    
    # print(links)

    "https://webtoon.kakao.com/content/%EB%AC%B4%EC%A7%80%EA%B0%9C%EB%8B%A4%EB%A6%AC-%ED%8C%8C%EC%88%98%EA%BE%BC/2043"
    for link in links:
        CONTENT_URL = BASE_URL + link
        # print(CONTENT_URL)
        content, page = get_page(CONTENT_URL)
        main = content.select_one("main")
        print(main.get_text())
        for i, val in enumerate(main.get_text()):
            print(i, " : ", val)
        break
        
    #root > main > div > div.page.bg-background.activePage > div > div.h-full.overflow-hidden.w-full.z-1.fixed.inset-0.bg-dark-background > div.w-full.left-0.top-0.relative > div.content-main-wrapper.opacity-0.invisible.relative.current-content-main.opacity-100.\!visible.z-1 > div.pb-20.pt-96.relative.z-1 > div.relative.mx-auto.my-0.w-full.lg\:w-default-max-width > div.mx-20.flex.justify-between.relative.z-1.pointer-events-auto.pt-12 > div > p.whitespace-pre-wrap.break-all.break-words.support-break-word.overflow-hidden.text-ellipsis.\!whitespace-nowrap.s22-semibold-white.leading-33.mb-1.pr-45
        
        
    webtoons = []


    return webtoons

collect_kakao_data()
# naver_webtoons = collect_naver_data()