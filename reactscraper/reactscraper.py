from constant import react_sections, react_base_url
from utils import get_data_pane, get_soup, json_file_save_path
import json
import html2text


class ReactDocumentationScraper:
    def __init__(self, base_url, sections):
        self.base_url = base_url
        self.sections = sections

    def fetch_links(self):
        links_data = []
        soup = get_soup(f"{self.base_url}/learn")

        for section in self.sections:
            try:
                section_data = self.get_section_links(soup, section)
                links_data.extend(section_data)
            except AttributeError:
                print(f"Warning: Section '{section}' not found on the page.")
        return links_data

    def get_section_links(self, soup, section):
        section_parent = soup.find("a", {"title": section}).parent
        section_parent_link = section_parent.find("a")["href"]

        child_links = [
            {
                "title": child.find("a").text,
                "link": f"{self.base_url}{child.find('a')['href']}",
            }
            for child in section_parent.find_all("li")
        ]

        child_links.insert(
            0, {"title": section, "link": f"{self.base_url}{section_parent_link}"}
        )

        return child_links

    def fetch_sub_section_content(self, child):
        child_class = child.findChildren("div", recursive=False)

        sub_sections = []

        for child in child_class:
            child_class = child.get("class", [])
            sub_section = {"text": [], "code_snippets": []}
            if "sandpack" in child_class:
                # IFrame code block
                code = child.find("div", class_="sp-code-editor")
                sub_section["code_snippets"].append(code.text)

            else:
                # Its a nested code block or text
                child_tags = child.findChildren(recursive=False)

                for tag in child_tags:
                    tag_class = tag.get("class", [])
                    if "sandpack" in tag_class:
                        code = tag.find("div", class_="sp-code-editor")
                        sub_section["code_snippets"].append(
                            html2text.html2text(code.text)
                        )
                    else:
                        sub_section["text"].append(tag.text)

            sub_sections.append(sub_section)

        return sub_sections

    def fetch_section_content(self, links):
        json_array = []

        for data in links:
            try:
                title, link = data["title"], data["link"]
                base = {
                    "title": title,
                    "source": "react",
                    "url": link,
                    "sections": [],
                }

                main_content, nav_urls = get_data_pane(link)
                section_content_list = self.fetch_sub_section_content(main_content)
                base["sections"].append(
                    section_content_list,
                )

                json_array.append(base)

            except Exception as e:
                print(f"Error fetching content for section '{data['title']}': {e}")

        return json_array

    def scrape(self):
        """
        Main method to perform the scraping, processing, and outputting the final JSON.
        :return: None
        """

        try:
            urls = self.fetch_links()

            json_array = self.fetch_section_content(urls)

            with open(json_file_save_path(), "w", encoding="utf-8") as json_file:
                json.dump(json_array, json_file, indent=2, ensure_ascii=False)

        except OSError as e:
            print(f"File I/O error: {e}")
        except Exception as e:
            print(f"Unexpected error occurred while saving the file: {e}")


# Run the scraper
scraper = ReactDocumentationScraper(react_base_url, react_sections)
scraper.scrape()
