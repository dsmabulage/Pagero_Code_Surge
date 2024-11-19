from bs4 import BeautifulSoup
import requests
from constant import react_base_url


def get_data_pane(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find("article").find("div", class_="max-w-7xl mx-auto")
