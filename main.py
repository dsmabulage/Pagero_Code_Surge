from bs4 import BeautifulSoup
import requests
from constant import react_sections, react_base_url
from utils import get_data_pane
import json

quick_start = requests.get(f"{react_base_url}/learn")

soup = BeautifulSoup(quick_start.content, "html.parser")

# Fetch Links from the page with the relative links

def get_links(section):
    # Find the section's parent element
    section_parent = soup.find("a", {"title": section}).parent
    section_parent_link = section_parent.find("a")["href"]

    # Get each child link's href and text
    child_links = [
        {
            "title": child.find("a").text,
            "link": f"{react_base_url}{child.find('a')['href']}",
        }
        for child in section_parent.find_all("li")
    ]

    return {
        "parent": {"title": section, "link": f"{react_base_url}{section_parent_link}"},
        "children": child_links,
    }


links_data = []

for section in react_sections:
    links_info = get_links(section)
    links_data.append(links_info)

# Fetch Data from page links
json_array = []

for data in links_data:
    data_pane = get_data_pane(data["parent"]["link"])

    base = {
        "title": data["parent"]["title"],
        "url": data["parent"]["link"],
        "source": "react",
        "sections": [],
    }

    for child in data["children"]:
        data_pane = get_data_pane(child["link"])
        base["sections"].append(
            {
                "title": child["title"],
                "url": child["link"],
            }
        )

    json_array.append(base)

# output json
print(json.dumps(json_array, indent=4))
