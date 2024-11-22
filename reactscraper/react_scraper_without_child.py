from constant import react_sections, react_base_url
from utils import get_data_pane, get_soup, json_file_save_path
import json


class ReactDocumentationScraper:
    def __init__(self, base_url, sections):
        self.base_url = base_url
        self.sections = sections

    def fetch_links(self):
        """
        Fetches links for each specified section and its child links.
        :return: A list of dictionaries containing parent and child links.
        """
        links_data = []
        soup = get_soup(f"{self.base_url}/learn")

        for section in self.sections:
            try:
                section_data = self.get_section_links(soup, section)
                links_data.append(section_data)
            except AttributeError:
                print(f"Warning: Section '{section}' not found on the page.")
        return links_data

    def get_section_links(self, soup, section):
        """
        Fetches links for a specific section and its child links.
        :param soup: BeautifulSoup object of the main page
        :param section: Section title to search for
        :return: Dictionary with parent link and child links
        """
        section_parent = soup.find("a", {"title": section}).parent
        section_parent_link = section_parent.find("a")["href"]

        return {
            "title": section,
            "link": f"{self.base_url}{section_parent_link}",
        }

    def fetch_sub_section_content(self, child):
        """
        Fetches content for a specific sub-section.
        :param child: Dictionary containing sub-section information.
        :return: Dictionary with sub-section title and content.
        """

        child_class = child.findChildren("div", recursive=False)

        sub_sections = []

        for child in child_class:
            child_class = child.get("class", [])
            sub_section = {"text": [], "code_snippets": []}
            if "sandpack" in child_class:
                # Its a code segment
                sub_section["code_snippets"].append(child.text)
            else:
                # Its a nested code block or text

                child_tags = child.findChildren(recursive=False)

                for tag in child_tags:
                    tag_class = tag.get("class", [])
                    if "sandpack" in tag_class:
                        sub_section["code_snippets"].append(tag.text)
                    else:
                        sub_section["text"].append(tag.text)

            sub_sections.append(sub_section)

        return sub_sections

    def fetch_section_content(self, links_data):
        """
        Fetches content from each section and its child links.
        :param links_data: List of dictionaries with parent and child link information.
        :return: A JSON array of scraped data.
        """
        json_array = []

        for data in links_data:
            try:
                base = {
                    "title": data["title"],
                    "source": "react",
                    "url": data["link"],
                    "sections": [],
                }

                try:
                    child_content = get_data_pane(data["link"])
                    section_content_list = self.fetch_sub_section_content(child_content)
                    base["sections"].append(
                        section_content_list,
                    )

                except Exception as e:
                    print(
                        f"Error fetching content for child '{data['title']}' in section '{data['parent']['title']}': {e}"
                    )

                json_array.append(base)

            except Exception as e:
                print(
                    f"Error fetching content for section '{data['parent']['title']}': {e}"
                )

        return json_array

    def scrape(self):
        """
        Main method to perform the scraping, processing, and outputting the final JSON.
        :return: None
        """

        try:
            links_data = self.fetch_links()

            json_array = self.fetch_section_content(links_data)

            with open(json_file_save_path(), "w", encoding="utf-8") as json_file:
                json.dump(json_array, json_file, indent=2, ensure_ascii=False)

        except OSError as e:
            print(f"File I/O error: {e}")
        except Exception as e:
            print(f"Unexpected error occurred while saving the file: {e}")


# Run the scraper
scraper = ReactDocumentationScraper(react_base_url, react_sections)
scraper.scrape()
