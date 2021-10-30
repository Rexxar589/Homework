import json
import os
import argparse
import sys
import requests
from time import sleep
from bs4 import BeautifulSoup as Bs
from tabulate import tabulate
from datetime import datetime


class RssPage:
    """Class RSSPage is capable of parsing RSS pages according to RSS 2.0 Specification.
     All RSS docs can be found at https://www.rssboard.org/rss-specification"""

    def __init__(self, rss_url: str):
        """
        Rss url link :param rss_url:
        """
        self.url = rss_url
        try:
            self.page = requests.get(self.url)
        except Exception as e:
            quit(e)
        if self.page.status_code == 200:
            pass
        elif self.page.status_code != 200:
            quit(f"Error, status code: {self.page.status_code}")
        self.soup = Bs(self.page.text, "xml")
        self.rss_page_info = {}
        self.channel = "channel"
        self.item = "item"

    def get_page(self):
        """.get_page allows to show page in xml format"""
        sys.stdout.write(self.soup.prettify())

    def get_page_file(self):
        """.get_page allows to show page in xml format"""
        try:
            file_directory = str(os.path.dirname(os.path.abspath(__file__)))
            try:
                os.mkdir(file_directory + "\\xml\\")
            except FileExistsError:
                pass
            xml_full_path = f"{file_directory}\\xml\\{self.url.replace('http://', '').replace('/', '_')}_" \
                            f"{str(datetime.date(datetime.now()))}.xml"
            with open(xml_full_path, 'w+', encoding="UTF-8") as xml_file:
                xml_file.write(self.soup.prettify())
            print(f"XML Content successfully saved.\nFile path: {xml_full_path}")
        except Exception as e:
            print(e)

    def parse(self):
        """
        Parse given RSS Page
        :return: Dictionary in format {channel: [Channel info], item [RSS Page items]}
        """

        def rss_elements_to_dict(part, part_elements):
            """
            Function that does all the magic. It parses both 'channel' and 'item' elements of RSS Page
            :return: List of info, that contains dict with Rss page elements
            """
            feed_info = self.soup.select(part)
            part_list = []
            for rss_part in feed_info:
                elem_dict = {}
                for elem in part_elements.keys():
                    if part_elements[elem] is None:
                        try:
                            elem_content = rss_part.find(elem).get_text()
                        except AttributeError:
                            elem_content = rss_part.find(elem)
                        elem_dict[elem] = elem_content
                    elif part_elements[elem] is not None:
                        elem_info = self.soup.select(f"{part} > {elem}")
                        for some_elem_info in elem_info:
                            elem_content = {}
                            for sub_elem in part_elements.get(elem):
                                try:
                                    sub_elem_content = some_elem_info.find(sub_elem).get_text()
                                except AttributeError:
                                    sub_elem_content = some_elem_info.find(sub_elem)
                                elem_content[sub_elem] = sub_elem_content
                            elem_dict[elem] = elem_content
                part_list.append(elem_dict)
            self.rss_page_info[part] = part_list

        rss_channel_elem_list = {"title": None, "link": None, "description": None, "language": None, "copyright": None,
                                 "managingEditor": None, "webMaster": None, "pubDate": None, "lastBuildDate": None,
                                 "category": None, "generator": None, "docs": None, "cloud": None, "ttl": None,
                                 "image": ["url", "title", "link", "width", "height", "description"], "rating": None,
                                 "textInput": ["title", "description", "name", "link"], "skipHours": None,
                                 "skipDays": None}  # RSS 2.0 Specification
        rss_item_elem_list = {"title": None, "link": None, "description": None, "author": None, "category": None,
                              "comments": None, "enclosure": None, "guid": None,
                              "pubDate": None, "source": None}  # RSS 2.0 Specification
        rss_elements_to_dict(self.channel, rss_channel_elem_list)
        rss_elements_to_dict(self.item, rss_item_elem_list)
        return self.rss_page_info

    @staticmethod
    def make_brief(string):
        n = 90
        if n < len(string):
            string = string[:n] + "..."
        return string

    def show_full_feed_info(self):
        """
        Prints out full feed information in table format
        """
        feed_info_list = []
        if self.rss_page_info[self.channel]:
            for feed in self.rss_page_info[self.channel]:
                for i, elem in enumerate(feed.keys()):
                    if feed[elem] is not None:
                        if isinstance(feed[elem], str):
                            feed_info_list.append([elem, "", feed[elem]])
                        elif isinstance(feed[elem], dict):
                            for j, e in enumerate(feed[elem].keys()):
                                if feed[elem][e] is not None:
                                    feed_info_list.append([elem, e, feed[elem][e]])
            print(tabulate(feed_info_list, headers=["Element", "Sub-element", "Content"], tablefmt="pretty"))
        else:
            print("Feed info should be parsed first. Use .parse() method to parse RssPage object")

    def show_full_item_info(self, limit=None):
        """
        Prints out full items information in table format
        :param limit: limits items printed
        """
        if limit is None:
            limit = len(self.rss_page_info[self.item])
        if self.rss_page_info[self.item]:
            for j, item in enumerate(self.rss_page_info[self.item]):
                if j <= limit:
                    item_info_list = []
                    for i, elem in enumerate(item.keys()):
                        if item[elem] is not None:
                            item_info_list.append([elem, self.make_brief(item[elem])])
                    print(f"Item {j+1}")
                    print(tabulate(item_info_list, headers=["Element", "Content"], tablefmt="github"))
        else:
            print(f"{self.item} info should be parsed first. Use .parse() method to parse RssPage object")

    def show_essentials(self, limit=None, feed_info_essentials=None, item_info_essentials=None):
        """
        Shows essential (required) elements of RSS page
        :param limit: limits items printed
        :param feed_info_essentials: takes list of feed elements that will be printed
        :param item_info_essentials: takes list of item elements that will be printed
        """
        if feed_info_essentials is None:
            feed_info_essentials = ["title", "link", "description"]
            # Essentials are chosen as Required channel elements in RSS 2.0 Specification
        if item_info_essentials is None:
            item_info_essentials = feed_info_essentials.copy()
        if limit is None:
            limit = len(self.rss_page_info[self.item])
        feed_info_list = []
        if self.rss_page_info[self.item]:
            try:
                for feed in self.rss_page_info[self.channel]:
                    for i, elem in enumerate(feed.keys()):
                        if feed[elem] is not None:
                            if elem in feed_info_essentials:
                                if isinstance(feed[elem], str):
                                    feed_info_list.append([elem, "", feed[elem]])
                                elif isinstance(feed[elem], dict):
                                    for j, e in enumerate(feed[elem].keys()):
                                        if feed[elem][e] is not None:
                                            feed_info_list.append([elem, e, self.make_brief(feed[elem][e])])
                print(tabulate(feed_info_list, headers=["Element", "Sub-element", "Content"], tablefmt="pretty"))
            except KeyError:
                print(f"{self.channel} info is not provided")
                pass
            for j, item in enumerate(self.rss_page_info[self.item]):
                if j <= limit:
                    item_info_list = []
                    for i, elem in enumerate(item.keys()):
                        if item[elem] is not None:
                            if elem in item_info_essentials:
                                item_info_list.append([elem, self.make_brief(item[elem])])
                    print()
                    print(f"Item {j+1}")
                    print(tabulate(item_info_list, headers=["Element", "Content"], tablefmt="github"))
        else:
            print("Feed and item info should be parsed first. Use .parse() method to parse RssPage object")

    def rss_page_to_json(self, limit=None):
        """Saves result into json file, located in \\\\json\\\\ folder"""
        if limit is None:
            limit = len(self.rss_page_info[self.item])
        try:
            file_directory = str(os.path.dirname(os.path.abspath(__file__)))
            try:
                os.mkdir(file_directory + "\\json\\")
            except FileExistsError:
                pass
            json_title_name = file_directory + "\\json\\" + self.rss_page_info[self.channel][0]['title']
            if self.rss_page_info[self.channel][0]['pubDate']:
                json_path = f"{json_title_name} ({self.rss_page_info[self.channel][0]['pubDate'][:16]}).json"
            elif not self.rss_page_info[self.channel][0]['pubDate']:
                json_path = f"{json_title_name} ({str(datetime.date(datetime.now()))}).json"
            json_file = open(json_path, "w+", encoding="utf8")
            rss_page = {self.channel: self.rss_page_info[self.channel],
                        self.item: self.rss_page_info[self.item][:limit]}
            json.dump(rss_page, json_file, indent=4, ensure_ascii=False)

            print(f"RSS Content successfully saved.\nFile path: {json_path}")
        except Exception as e:
            print(e)
        finally:
            json_file.close()

    def rss_page_to_json_stdout(self, limit=None):
        """Prints out a result as a json file"""
        if limit is None:
            limit = len(self.rss_page_info[self.item])
        rss_page = {self.channel: self.rss_page_info[self.channel], self.item: self.rss_page_info[self.item][:limit]}
        json_out = json.dumps(rss_page, indent=4)
        sys.stdout.write(json_out)


def parse_args(com_line_args: list, args_action: dict, args_type: dict, args_help: dict):
    """Parses given arguments with given parameters"""
    parser = argparse.ArgumentParser()
    for argument in com_line_args:
        if argument not in args_help.keys():
            quit(f"Help message for argument {argument} is not specified")
        elif argument in args_type.keys() and argument not in args_action.keys():
            parser.add_argument(argument, help=args_help[argument], type=args_type[argument])
        elif argument in args_action.keys() and argument not in args_type.keys():
            parser.add_argument(argument, action=args_action[argument], help=args_help[argument])
        else:
            parser.add_argument(argument, help=args_help[argument])
    cli_arguments = parser.parse_args()
    return cli_arguments


#########################################################################################################
# Version info
rss_parser_version = "1.00"

# Arguments info
cli_args_list = ["source", "--get_page", "--get_page_file", "--essentials", "--version", "--json", "--json_file",
                 "--verbose", "--limit"]
cli_args_action = {"--verbose": 'store_true', "--get_page": 'store_true', "--get_page_file": 'store_true',
                   "--essentials": 'store_true', "--json": 'store_true', "--json_file": 'store_true',
                   "--version": 'store_true'}
cli_args_type = {"source": str, "--limit": int}
cli_args_help = {"source": 'RSS URL', "--get_page": 'Prints page as is in stdout',
                 "--get_page_file": 'Saves page into xml file in \\xml folder in parser file location',
                 "--essentials": 'Shows only essentials (required page elements, according to RSS 2.0 Specification',
                 "--version": ' Print version info', "--json": 'Print result as JSON in stdout',
                 "--json_file": 'Saves result as .json file in \\json folder in parser file location',
                 "--verbose": 'Outputs verbose status messages',
                 "--limit": 'Limit news topics if this parameter provided'}


def main():
    """Declares an order of script execution"""
    cli_args = parse_args(cli_args_list, cli_args_action, cli_args_type, cli_args_help)
    rss = RssPage(cli_args.source)
    if cli_args.verbose:
        print("RSSPage object was successfully created")
        sleep(0.5)
        print("Parsing...")
        rss.parse()
        sleep(1)
        print(cli_args.source, "was parsed successfully")
        sleep(1)
        print("Getting page info...")
        sleep(1)
    else:
        rss.parse()
    if cli_args.essentials:
        rss.show_essentials(cli_args.limit)
    elif cli_args.json:
        rss.rss_page_to_json_stdout(cli_args.limit)
    elif cli_args.json_file:
        rss.rss_page_to_json(cli_args.limit)
    elif cli_args.version:
        print(f"RSS Parser, version: {rss_parser_version}")
    elif cli_args.get_page:
        rss.get_page()
    elif cli_args.get_page_file:
        rss.get_page_file()
    else:
        rss.show_full_feed_info()
        rss.show_full_item_info(cli_args.limit)


# url = "http://rss.cnn.com/rss/edition_us.rss"
# url = "http://rss.cnn.com/rss/edition.rss"
# url = "http://news.yahoo.com/rss"

if __name__ == "__main__":
    main()
