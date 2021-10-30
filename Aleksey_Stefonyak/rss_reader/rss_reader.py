import json
import os
import argparse
import sys
import requests
import sqlite3
import FB2
from urllib import request
from time import sleep
from bs4 import BeautifulSoup as Bs
from fpdf import FPDF
from tabulate import tabulate
from datetime import datetime


class RssParser:
    """Class RSSPage is capable of parsing RSS pages according to RSS 2.0 Specification.
     All RSS docs can be found at https://www.rssboard.org/rss-specification"""

    def __init__(self, rss_url=None):
        """
        Rss url link :param rss_url:
        """
        self.url = rss_url
        self.rss_page_info = {}
        self.channel = "channel"
        self.rss_channel_elem_dict = {"title": None, "link": None, "description": None, "language": None,
                                      "copyright": None, "managingEditor": None, "webMaster": None, "pubDate": None,
                                      "lastBuildDate": None, "category": None, "generator": None, "docs": None,
                                      "cloud": None, "ttl": None,
                                      "image": ["url", "title", "link", "width", "height", "description"],
                                      "rating": None, "textInput": ["title", "description", "name", "link"],
                                      "skipHours": None, "skipDays": None}
        # Source: RSS 2.0 Specification
        self.item = "item"
        self.rss_item_elem_dict = {"title": None, "link": None, "description": None, "author": None, "category": None,
                                   "comments": None, "enclosure": None, "guid": None, "pubDate": None, "source": None}
        # Source: RSS 2.0 Specification
        self.soup = None
        self.conn = None
        self.cursor = None
        self.pub_date = None
        self.file_directory = str(os.path.dirname(os.path.abspath(__file__)))

    def connect_to_source(self):
        """Connects to source if it's provided correctly"""
        try:
            page = requests.get(self.url)
            if page.status_code == 200:
                pass
            elif page.status_code != 200:
                quit(f"Error, status code: {page.status_code}")
        except Exception as e:
            quit(e)
        self.soup = Bs(page.text, "xml")
        return self.soup

    def connect_to_history_db(self):
        """Creates records history database for the application"""
        db_dir = self.file_directory + "\\rss-parser-out\\history\\" + "history.db"
        self.conn = sqlite3.connect(db_dir)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"CREATE TABLE news ("
                                f"channel_pubDate text,"
                                f"url text, "
                                f"item_num integer, "
                                f"{' text, '.join(self.rss_item_elem_dict.keys())} text)")
            self.cursor.execute("CREATE INDEX news_date_url_index ON news(channel_pubDate, url)")
            self.conn.commit()
        except sqlite3.DatabaseError:
            pass
        return db_dir

    def clear_history_db(self, table: str):
        """Clears selected database table. If it receives 'clear_all' then clears database"""
        if table == "clear_all":
            yn = input("This action removes all earlier requests data.\n Continue y/n?\n")
            if yn == "y":
                try:
                    self.conn.close()
                    os.remove(self.file_directory + "\\rss-parser-out\\history\\" + "history.db")
                    print(f"EVERYTHING deleted =(((")
                except Exception as e:
                    quit(e)
            elif yn != "y":
                quit("Action canceled. All information is on it\'s place. Parser feels happy!")
        if table != "clear_all":
            try:
                self.cursor.execute(f"DROP TABLE {table}")
                print(f"Table {table} deleted =(")
            except sqlite3.DatabaseError as e:
                quit(e)

    def prepare_env(self, directory: str):
        """Creates environment needed for application"""
        new_dir = self.file_directory + f"\\{directory}\\"
        try:
            os.mkdir(new_dir)
        except FileExistsError:
            pass
        return new_dir

    def get_page(self):
        """.get_page allows to show page in xml format"""
        sys.stdout.write(self.soup.prettify())

    def get_page_file(self):
        """.get_page allows to show page in xml format"""
        try:
            xml_full_path = f"{self.file_directory}\\rss-parser-out\\xml\\{self.url.replace('http://', '').replace('/', '_')}_" \
                            f"{str(datetime.date(datetime.now()))}.xml"
            with open(xml_full_path, 'w+', encoding="UTF-8") as xml_file:
                xml_file.write(self.soup.prettify())
            print(f"XML Content successfully saved.\nFile path: {xml_full_path}")
        except Exception as e:
            quit(e)
        return xml_full_path

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

        rss_elements_to_dict(self.channel, self.rss_channel_elem_dict)
        rss_elements_to_dict(self.item, self.rss_item_elem_dict)
        return self.rss_page_info

    @staticmethod
    def make_brief(string, symbols=90):
        string = str(string)
        if symbols < len(string):
            string = string[:symbols] + "..."

        return string

    def show_full_feed_info(self):
        """
        Prints out full feed information in table format
        """
        feed_info_list = []
        try:
            if self.rss_page_info[self.channel]:
                for feed in self.rss_page_info[self.channel]:
                    for i, elem in enumerate(feed.keys()):
                        if feed[elem] is not None:
                            if isinstance(feed[elem], str):
                                feed_info_list.append([elem, "", feed[elem]])
                            elif isinstance(feed[elem], dict):
                                for j, e in enumerate(feed[elem].keys()):
                                    if feed[elem][e] is not None:
                                        feed_info_list.append([elem, e, self.make_brief(feed[elem][e], 70)])
                print(tabulate(feed_info_list, headers=["Element", "Sub-element", "Content"], tablefmt="pretty"))
            else:
                print(f"{self.channel} info should be parsed first. Use .parse() method to parse RssPage object")
        except KeyError:
            print(f"{self.channel.upper()} info is not provided.")

    def show_full_item_info(self, limit=None):
        """
        Prints out full items information in table format
        :param limit: limits items printed
        """
        if limit is None:
            limit = len(self.rss_page_info[self.item])
        if self.rss_page_info[self.item]:
            for j, item in enumerate(self.rss_page_info[self.item]):
                j += 1
                if j <= limit:
                    item_info_list = []
                    for i, elem in enumerate(item.keys()):
                        if item[elem] is not None:
                            item_info_list.append([elem, self.make_brief(item[elem])])
                    print(f"Item {j}")
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
                j += 1
                if j <= limit:
                    item_info_list = []
                    for i, elem in enumerate(item.keys()):
                        if item[elem] is not None:
                            if elem in item_info_essentials:
                                item_info_list.append([elem, self.make_brief(item[elem])])
                    print()
                    print(f"Item {j}")
                    print(tabulate(item_info_list, headers=["Element", "Content"], tablefmt="github"))
        else:
            print("Feed and item info should be parsed first. Use .parse() method to parse RssPage object")

    def rss_page_to_json(self, pub_date=None, limit=None):
        """Saves result into json file, located in \\\\json\\\\ folder"""
        if limit is None:
            limit = len(self.rss_page_info[self.item])
        if pub_date is None:
            pub_date = str(datetime.date(datetime.now()))
        try:
            try:
                json_title_name = self.file_directory + "\\rss-parser-out\\json\\" + \
                                  self.rss_page_info[self.channel][0]['title']
                json_path = f"{json_title_name}_({self.rss_page_info[self.channel][0]['pubDate'][:16]}).json"
            except KeyError:
                json_title_name = self.file_directory + "\\rss-parser-out\\json\\" + self.url.replace('http://',
                                                                                                      '').replace('/',
                                                                                                                  '_')
                json_path = f"{json_title_name}_({pub_date}).json"
            json_file_ = open(json_path, "w+", encoding="utf8")
            try:
                rss_page = {self.channel: self.rss_page_info[self.channel],
                            self.item: self.rss_page_info[self.item][:limit]}
            except KeyError:
                rss_page = {self.item: self.rss_page_info[self.item][:limit]}
            json.dump(rss_page, json_file_, indent=4, ensure_ascii=False)

            print(f"RSS Content successfully saved.\nFile path: {json_path}")
            json_file_.close()
        except Exception as e:
            quit(e)
        return json_path

    def rss_page_to_json_stdout(self, limit=None):
        """Prints out a result as a json file"""
        if limit is None:
            limit = len(self.rss_page_info[self.item])
        try:
            rss_page = {self.channel: self.rss_page_info[self.channel],
                        self.item: self.rss_page_info[self.item][:limit]}
        except KeyError:
            rss_page = {self.item: self.rss_page_info[self.item][:limit]}
        json_out = json.dumps(rss_page, indent=4)
        sys.stdout.write(json_out)
        return json_out

    def make_date(self):
        """Sets value of self.pub_date variable, looking on all available variables values"""
        try:
            self.pub_date = datetime.strptime(self.rss_page_info[self.channel][0]["pubDate"],
                                              "%a, %d %b %Y %H:%M:%S %Z")
        except (ValueError, IndexError, KeyError):
            try:
                self.pub_date = datetime.strptime(self.rss_page_info[self.channel][0]["pubDate"],
                                                  "%a, %d %b %Y %H:%M:%S %z")

            except (KeyError, IndexError):
                try:
                    self.pub_date = datetime.strptime(self.rss_page_info[self.item][0]["pubDate"], "%Y-%m-%dT%H:%M:%SZ")
                except (ValueError, IndexError):
                    try:
                        self.pub_date = datetime.strptime(self.rss_page_info[self.item][0]["pubDate"],
                                                          "%a, %d %b %Y %H:%M:%S %Z")
                    except (ValueError, IndexError):
                        try:
                            self.pub_date = datetime.strptime(self.rss_page_info[self.item][0]["pubDate"],
                                                              "%a, %d %b %Y %H:%M:%S %Z")
                        except (ValueError, IndexError):
                            try:
                                self.pub_date = datetime.now()
                            except Exception as e:
                                quit(e)
        pub_date = self.pub_date
        return pub_date

    def save_page_to_db(self):
        """Saves news on the page to history database"""
        values_list = []
        pub_date = datetime.date(self.pub_date)
        self.cursor.execute("SELECT DISTINCT channel_pubDate||'_'||url from news")
        existing_records = self.cursor.fetchall()
        for i, records in enumerate(existing_records):
            existing_records[i] = records[0]
        created_records = str(pub_date) + "_" + self.url
        if created_records not in existing_records:
            for i, item in enumerate(self.rss_page_info[self.item]):
                item_elem_list = []
                for elem in self.rss_item_elem_dict:
                    if item[elem] is not None:
                        item_elem_list.append(item[elem].replace('\'', '`'))
                    elif item[elem] is None:
                        item_elem_list.append('NULL')
                value_string = f"(\'{pub_date}\'," \
                               f" \'{self.url}\', {i + 1}, " + "\'{}\')".format('\', \''.join(item_elem_list))
                value_string = value_string.replace("'NULL'", "NULL")
                values_list.append(value_string)
            self.cursor.execute(f"INSERT INTO "
                                f"news VALUES "
                                f"{', '.join(values_list)}")

            self.conn.commit()
            self.conn.close()

    def get_saved_page(self, pub_date: int, limit=None):
        """Initializes queries to get all history database records for specified date and page(if source provided)"""
        try:
            pub_date = datetime.strptime(str(pub_date), "%Y%m%d").date()
        except ValueError:
            quit("Date is incorrect")
        if not self.url and limit is None:
            data = self.cursor.execute(f"SELECT * FROM news WHERE channel_pubDate LIKE \'{str(pub_date)}%\'")
        if not self.url and limit is not None:
            data = self.cursor.execute(
                f"SELECT * FROM news WHERE channel_pubDate LIKE \'{str(pub_date)}%\' LIMIT {limit}")
        if self.url and limit is None:
            data = self.cursor.execute(f"SELECT * FROM news WHERE channel_pubDate LIKE \'{str(pub_date)}%\' "
                                       f"and url = \'{self.url}\'")
        if self.url and limit is not None:
            data = self.cursor.execute(f"SELECT * FROM news WHERE channel_pubDate LIKE \'{str(pub_date)}%\' "
                                       f"and url = \'{self.url}\' LIMIT {limit}")
        result_set = self.cursor.fetchall()
        if not result_set and not self.url:
            quit(f"RSS reader history database has no records for date {pub_date}")
        elif not result_set and self.url:
            quit(f"RSS reader history database has no records for date {pub_date} from source {self.url}")
        columns = [_el[0] for _el in data.description]
        self.rss_page_info[self.item] = []
        for _ in result_set:
            page = dict(zip(columns, _))
            self.rss_page_info[self.item].append(page)
        self.conn.close()
        saved_rss_content = self.rss_page_info
        return saved_rss_content

    def to_pdf(self, limit=None):
        """Converts resulting output to pdf file"""
        if limit is None:
            limit = len(self.rss_page_info[self.item])
        pdf = FPDF("L")
        pdf.add_font('DejaVu', '', 'fonts\\DejaVuSansCondensed.ttf', uni=True)

        def elements_to_pdf(element: str, feed_elements: list, string_format="{:<15}\n" + ("-" * 40) + "\n{}",
                            cell_height=5, cell_width=0, font="DejaVu", font_style="", font_size=12,
                            rss_table_delimiter="-" * 199):
            try:
                for i, elements in enumerate(self.rss_page_info[element]):
                    if i < limit:
                        elem_info_list = []
                        for element_name in feed_elements:
                            try:
                                if elements[element_name] is not None and isinstance(elements[element_name], str):
                                    result_string = string_format.format(element_name.upper(), elements[element_name])
                                    result_string = result_string.encode('utf-8', 'replace').decode('utf-8')
                                    elem_info_list.append(result_string)
                                    elem_info_list.append(rss_table_delimiter)
                            except KeyError:
                                pass
                        if i == 0 or not i % 2:
                            pdf.add_page()
                        pdf.set_font(font, "", font_size + 2)
                        pdf.cell(cell_width, cell_height + 10, element.upper() + f" {i + 1}\n\n", ln=True)
                        pdf.set_font(font, font_style, font_size)
                        for item in elem_info_list:
                            pdf.multi_cell(cell_width, cell_height, item)
            except KeyError:
                pass

        feed_info_essentials = ["title", "description", "pubDate", "link"]
        item_info_essentials = ["source", "title", "description", "link"]
        res_table_str_format = "{:<15}\n" + ("-" * 40) + "\n{}"
        rss_table_main_delimiter = "¯" * 123
        pdf.set_text_color(26, 21, 43)
        try:
            elements_to_pdf(element=self.channel, feed_elements=feed_info_essentials,
                            string_format=res_table_str_format,
                            font_size=14, rss_table_delimiter=rss_table_main_delimiter)
        except KeyError:
            pass
        try:
            image = self.rss_page_info[self.channel][0]["image"]
            pdf.image(image["url"], x=220, y=12)
            pass
        except KeyError:
            pass
        elements_to_pdf(element=self.item, feed_elements=item_info_essentials, string_format=res_table_str_format,
                        font_size=12, cell_height=4)
        file_name = f"{self.url.replace('http://', '').replace('https://', '').replace('/', '_')}_" \
                    f"{str(datetime.date(self.pub_date))}"
        pdf_full_path = f"{self.file_directory}\\rss-parser-out\\pdf\\{file_name}.pdf"
        pdf.output(pdf_full_path)
        print(f"RSS Content successfully saved.\nFile path: {pdf_full_path}")
        return pdf_full_path

    def to_fb2(self, date, limit=None):
        """Converts resulting output to pdf file"""
        items = self.rss_page_info[self.item]
        if limit is None:
            limit = len(items)
        book = FB2.FictionBook2()
        title = book.titleInfo
        item_info_essentials = ["source", "title", "description", "link"]
        try:
            channel = self.rss_page_info[self.channel][0]
            image = request.urlopen(channel["image"]["url"]).read()
            title.title = channel["title"]
            title.annotation = channel["description"]
            title.genres = ["news"]
            title.authors = [FB2.Author(firstName=channel["pubDate"])]
            title.coverPageImages = [image]
        except KeyError:
            if self.url != "":
                title.title = f"News source: {self.url}"
            elif self.url == "":
                title.title = "News"
            title.authors = [FB2.Author(firstName=str(datetime.strptime(str(date), "%Y%m%d").date()))]
        for i, item in enumerate(items):
            if i < limit:
                info = [f"{'_' * 40}", f"Item {i + 1}"]
                for elem in item_info_essentials:
                    if item[elem] is not None:
                        content = f"{elem.upper()} - {item[elem]}"
                        info.append(content)
                book.chapters.append((f"Item {i + 1}", info))
        file_name = f"{self.url.replace('http://', '').replace('https://', '').replace('/', '_')}_" \
                    f"{str(datetime.date(self.pub_date))}"
        fb2_full_path = f"{self.file_directory}\\rss-parser-out\\fb2\\{file_name}.fb2"
        book.write(fb2_full_path)
        print(f"RSS Content successfully saved.\nFile path: {fb2_full_path}")
        return fb2_full_path


def parse_args(com_line_args: list, args_action: dict, args_type: dict, args_help: dict, args_default: dict):
    """Parses given arguments with given parameters"""
    parser = argparse.ArgumentParser()
    for argument in com_line_args:
        if argument not in args_help.keys():
            quit(f"Help message for argument {argument} is not specified")
        elif argument in args_type.keys() and argument not in args_action.keys() and argument in args_default.keys():
            parser.add_argument(argument, help=args_help[argument], type=args_type[argument],
                                default=args_default[argument], nargs='?')
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
rss_parser_version = "1.04"

# Arguments info
cli_args_list = ["source", "--get_page", "--get_page_file", "--essentials", "--version", "--json", "--json_file",
                 "--verbose", "--limit", "--date", "--clear_history", "--to_pdf", "--to_fb2"]
cli_args_store_true_list = ["--verbose", "--get_page", "--get_page_file", "--essentials", "--json", "--json_file",
                            "--version", "--to_pdf", "--to_fb2"]
cli_args_action_store_true = {cli_arg: 'store_true' for cli_arg in cli_args_store_true_list}
cli_args_type = {"source": str, "--limit": int, "--date": int, "--clear_history": str}
cli_args_help = {"source": 'RSS URL', "--get_page": 'Prints page as is in stdout',
                 "--get_page_file": 'Saves page into xml file in \\xml folder in parser file location',
                 "--essentials": 'Shows only essentials (required page elements, according to RSS 2.0 Specification',
                 "--version": ' Print version info', "--json": 'Print result as JSON in stdout',
                 "--json_file": 'Saves result as .json file in \\json folder in parser file location',
                 "--verbose": 'Outputs verbose status messages',
                 "--limit": 'Limit news topics if this parameter provided',
                 "--date": 'specify a date in YYYYMMDD format to watch news for this specific date',
                 "--clear_history": 'clears selected database table. If it receives \'clear_all\' then clears database',
                 "--to_pdf": 'Converts result to pdf file ',
                 "--to_fb2": 'Converts result to fb2 file '}
cli_args_default = {"source": ''}


def rss_parser():
    """Declares an order of script execution"""
    cli_args = parse_args(cli_args_list, cli_args_action_store_true, cli_args_type, cli_args_help, cli_args_default)
    rss = RssParser(cli_args.source)
    rss.prepare_env("rss-parser-out")
    if cli_args.version:
        quit(f"RSS Parser, version: {rss_parser_version}")
    elif cli_args.clear_history:
        rss.connect_to_history_db()
        rss.clear_history_db(cli_args.clear_history)
        quit()
    elif cli_args.source and cli_args.source != "" and not cli_args.date:
        if cli_args.verbose:
            print("RSSPage object was successfully created")
            sleep(0.25)
            rss.connect_to_source()
            print("Successfully connected to source page")
            sleep(0.25)
            print("Parsing...")
            rss.parse()
            sleep(0.5)
            print(cli_args.source, "was parsed successfully")
            sleep(1)
            print("Getting page info...")
            sleep(1)
        else:
            rss.connect_to_source()
            rss.parse()
            rss.prepare_env("rss-parser-out\\history")
            rss.connect_to_history_db()
            rss.make_date()
            rss.save_page_to_db()
        if cli_args.get_page:
            rss.get_page()
        if cli_args.get_page_file:
            rss.prepare_env("rss-parser-out\\xml")
            rss.get_page_file()
    elif cli_args.date:
        if cli_args.verbose:
            print("RSSPage object was successfully created")
            sleep(0.5)
            rss.prepare_env("rss-parser-out\\history")
            rss.connect_to_history_db()
            print("Successfully connected database")
            sleep(0.25)
            print("Getting info from database...")
            rss.get_saved_page(cli_args.date, cli_args.limit)
            sleep(1)
        else:
            rss.prepare_env("rss-parser-out\\history")
            rss.connect_to_history_db()
            rss.get_saved_page(cli_args.date, cli_args.limit)
    elif cli_args.source == '' and not cli_args.date and not cli_args.clear_history and not cli_args.version:
        quit("RSS reader should be provided with source or/and news date")
    if cli_args.essentials or cli_args.json or cli_args.json_file or cli_args.to_pdf or cli_args.to_fb2:
        if cli_args.essentials:
            rss.show_essentials(cli_args.limit)
        if cli_args.json:
            rss.rss_page_to_json_stdout(cli_args.limit)
        if cli_args.json_file:
            rss.prepare_env("rss-parser-out\\json")
            rss.rss_page_to_json(cli_args.date, cli_args.limit)
        if cli_args.to_pdf:
            rss.prepare_env("rss-parser-out\\pdf")
            rss.make_date()
            rss.to_pdf(cli_args.limit)
        if cli_args.to_fb2:
            rss.prepare_env("rss-parser-out\\fb2")
            rss.make_date()
            rss.to_fb2(cli_args.date, cli_args.limit)
    else:
        if not cli_args.get_page and not cli_args.get_page_file:
            rss.show_full_feed_info()
            rss.show_full_item_info(cli_args.limit)


def main():
    rss_parser()


# url = "http://rss.cnn.com/rss/edition_us.rss"
# url = "http://rss.cnn.com/rss/edition.rss"
# url = "http://news.yahoo.com/rss"

if __name__ == "__main__":
    main()
