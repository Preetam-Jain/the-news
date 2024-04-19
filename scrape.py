import requests
import re
from bs4 import BeautifulSoup
'''
urls = ['https://www.cnn.com/2024/04/18/middleeast/us-united-nations-resolution-palestine-membership-intl/index.html',
        'https://www.cnn.com/2024/03/22/middleeast/us-gaza-ceasefire-proposal-veto-intl/index.html?iid=cnn_buildContentRecirc_end_recirc',
        'https://www.cnn.com/2024/04/18/africa/kenya-military-chief-dead-in-helicopter-crash-afr/index.html',
        'https://www.cnn.com/2024/04/15/middleeast/oman-flash-floods-intl-latam/index.html?iid=cnn_buildContentRecirc_end_recirc',
        'https://www.cnn.com/2024/04/17/americas/toronto-airport-heist-arrests/index.html',
        'https://www.cnn.com/2024/04/11/europe/russia-navalny-memoir-intl/index.html',
        'https://www.cnn.com/2013/11/04/us/violence-against-u-s-politicians-and-diplomats-fast-facts/index.html',
        'https://www.cnn.com/2023/10/24/politics/supreme-court-florida-anti-drag-law/index.html',
        'https://www.cnn.com/2024/04/18/politics/biden-kennedy-family-endorsements-rfk-jr/index.html'
        ]

for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    header = soup.find('div', class_='headline headline--has-lowertext')
    if header:
        print(f'Found header for: {url}')

    main_body = soup.find('div', class_='article__content')
    if main_body:
        print(f'Found main body for: {url}')
'''
def get_article_links(base_url):
    links = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    keywords = ['israel', 'palestine', 'gaza']
    regex = re.compile('|'.join(keywords), re.IGNORECASE)
    links = soup.find_all('a', href=lambda href: href and regex.search(href))
    unique_links = set()

    for link in links:
        link_string = str(link)
        if 'data-link-type="article"' in link_string:
            url_begin_index = link_string.index('href="')
            url_end_index = link_string.index("/index.html")
            link_url = link_string[url_begin_index + 6:url_end_index + 11]
            unique_links.add(base_url + link_url)

    return unique_links

category_url = 'https://www.cnn.com/world/middle-east'
article_links = get_article_links(category_url)
for link in list(article_links):
    print(link)