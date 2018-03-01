import requests
import lxml.html as html
from lxml.cssselect import CSSSelector
import asyncio
import time
import concurrent.futures
from itertools import chain

responseList = []

def get_words_frequency():
    dict = {}
    for i in chain.from_iterable(responseList):
        dict[i] = dict.setdefault(i, 0) + 1
    asdict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return asdict[:10]


def get_name():
    r = requests.get('https://www.namefake.com/')
    text = r.text
    page = html.fromstring(text)
    sel = CSSSelector('h2')
    result = sel(page)
    fullnamelist = result[0].text_content().split(' ')
    htmlresult = []
    prefixes = {'Mrs.', 'Mr.', 'Prof.', 'Dr.', 'Miss', 'Ms.'}
    if len(fullnamelist) == 2:
        htmlresult = fullnamelist
    elif len(fullnamelist) == 3:
        if fullnamelist[0] in prefixes:
            htmlresult = fullnamelist[1:]
        else:
            htmlresult = fullnamelist[:-1]
    else:
        htmlresult = fullnamelist[1:-1]
    return htmlresult


async def req():
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = (
            loop.run_in_executor(executor, get_name)
            for i in range(100)
        )
        for response in await asyncio.gather(*futures):
            responseList.append(response)


start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(req())
loop.close()
end = time.time()
print(get_words_frequency())
print('time is ', end - start)
