from bs4 import BeautifulSoup
import requests

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def get_data_pane(url):
    soup = get_soup(url)
    return soup.find("article").find("div", class_="max-w-7xl mx-auto")
