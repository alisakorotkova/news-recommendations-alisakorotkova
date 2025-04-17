import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news = []
    articles = parser.find_all("article")
    for article in articles:
        title_tag = article.find("h2")
        if not title_tag:
            continue
        title = title_tag.text.strip()
        link_tag = title_tag.find("a")
        url = "https://habr.com" + link_tag["href"] if link_tag else ""

        author_tag = article.find("span", class_="tm-user-info__username")
        author = author_tag.text.strip() if author_tag else "Unknown"

        complexity = "Средний"

        news.append({"title": title, "author": author, "url": url, "complexity": complexity})
    return news


def extract_next_page(parser):
    """ Extract next page URL """
    # PUT YOUR CODE HERE
    next_link = parser.find("a", class_="tm-pagination__block tm-pagination__block_next")
    return next_link["href"] if next_link else None



def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        news.extend(news_list)
        next_page = extract_next_page(soup)
        if not next_page:
            print("Следующая страница не найдена — остановка.")
            break
        url = "https://habr.com" + next_page
        n_pages -= 1
    return news

