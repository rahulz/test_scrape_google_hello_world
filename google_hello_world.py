import pandas
import requests
from lxml import html

if __name__ == '__main__':
    query = "Hello+World"
    url = f"https://www.google.com/search?q={query}"
    res = requests.get(url)
    tree = html.fromstring(res.content)
    results = tree.xpath("//*[@id='main']/div")
    out = []

    for element in results:
        try:
            hrf = element.xpath('div/div/a')[0]
            url = hrf.attrib['href'].replace('/url?q=', '').split('&sa=')[0]
            assert url.startswith('http')
            title = hrf.xpath('h3')[0].text_content().strip()
            out.append([title, url])
        except (IndexError, AssertionError):
            pass
        pandas.DataFrame(out, columns=['title', 'url']).to_csv(f'{query}_result.csv', index=False)
