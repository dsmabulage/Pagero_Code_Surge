from bs4 import BeautifulSoup
import requests
import os


def json_file_save_path():
    path = os.getcwd() 
    return os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "react.json")


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def get_data_pane(url):
    soup = get_soup(url)
    return soup.find("article").find("div", class_="max-w-7xl mx-auto")
