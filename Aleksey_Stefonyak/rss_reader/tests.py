import datetime
from os import path

from rss_reader import *
import unittest


class Parser_Tester(unittest.TestCase):

    def setUp(self) -> None:
        self.source = "http://rss.cnn.com/rss/edition_us.rss"
        self.test_rss = RssParser(self.source)
        self.test_rss.prepare_env("rss-parser-out")
        self.date = None  # To specify, enter date in YYYYMMDD format as 'int' type, ex: 20211231

    def test_soup(self):
        if self.source != "":
            self.test_rss.connect_to_source()
            result = type(self.test_rss.connect_to_source())
            test = type(Bs('', 'xml'))
            self.assertEqual(result, test, f"connect_to_source() returns not a {type(Bs('', 'xml'))} object")
        elif self.source == "":
            pass

    def test_db(self):
        self.test_rss.prepare_env("rss-parser-out\\history")
        result = self.test_rss.connect_to_history_db()
        self.assertTrue(path.exists(result), f"Database not implemented")

    def test_prepare_env(self):
        result = self.test_rss.prepare_env("rss-parser-out\\test_dir")
        self.assertTrue(path.exists(result), "Directory not implemented")

    def test_get_page_file(self):
        if self.source != "" and self.source is not None:
            self.test_rss.connect_to_source()
            self.test_rss.prepare_env("rss-parser-out\\xml")
            result = self.test_rss.get_page_file()
            self.assertTrue(path.exists(result), "Page file not implemented")

    def test_parser(self):
        if self.source != "" and self.source is not None:
            self.test_rss.connect_to_source()
            result = self.test_rss.parse()
            self.assertIsNotNone(result, "Parser did nothing (returned None)")
            result_channel = list(self.test_rss.rss_page_info.keys())[0]
            test_channel = self.test_rss.channel
            result_items = list(self.test_rss.rss_page_info.keys())[1]
            test_items = self.test_rss.item
            self.assertEqual(result_channel, test_channel, "channel not implemented")
            self.assertEqual(result_items, test_items, " channel items not implemented")

    def test_make_brief(self):
        result = self.test_rss.make_brief("Always code as if the guy who ends up maintaining your code will be a "
                                          "violent psychopath who knows where you live. Code for readability. "
                                          "John F. Woods")
        self.assertTrue(isinstance(result, str))

    def test_rss_page_to_json(self):
        if self.source != "" and self.source is not None:
            self.test_rss.connect_to_source()
            self.test_rss.parse()
            self.test_rss.prepare_env("rss-parser-out\\json")
            result = self.test_rss.rss_page_to_json()
            self.assertTrue(path.exists(result), "json file not implemented")

    def test_json_stdout(self):
        if self.source != "" and self.source is not None:
            self.test_rss.connect_to_source()
            self.test_rss.parse()
            result = self.test_rss.rss_page_to_json_stdout()
            self.assertTrue(isinstance(result, str), f"rss_page_to_json_stdout() returns {type(result)}, not str")

    def test_make_date(self):
        if self.source != "" and self.source is not None:
            self.test_rss.connect_to_source()
            self.test_rss.parse()
            result = type(self.test_rss.make_date())
            test = type(datetime.now())
            self.assertEqual(result, test, f"make_date() returns {type(result)}, not datetime.datetime object")

    def test_get_saved_page_from_db(self):
        if self.source == "" and self.date is not None:
            self.test_rss.prepare_env("rss-parser-out\\history")
            self.test_rss.connect_to_history_db()
            self.test_rss.make_date()
            result = self.test_rss.get_saved_page(pub_date=self.date)
            self.assertIsNotNone(result, "Parser did nothing (returned None)")
            result_items = list(self.test_rss.rss_page_info.keys())[0]
            test_items = self.test_rss.item
            self.assertEqual(result_items, test_items, " channel items not implemented")

    def test_pdf(self):
        if self.source != "" and self.source is not None:
            self.test_rss.connect_to_source()
            self.test_rss.parse()
            self.test_rss.make_date()
            self.test_rss.connect_to_history_db()
            self.test_rss.save_page_to_db()
            self.test_rss.prepare_env("rss-parser-out\\pdf")
            result = self.test_rss.to_pdf()
            self.assertTrue(path.exists(result))
        if self.date:
            self.test_rss.prepare_env("rss-parser-out\\history")
            self.test_rss.connect_to_history_db()
            self.test_rss.get_saved_page(self.date)
            self.test_rss.prepare_env("rss-parser-out\\pdf")
            result = self.test_rss.to_pdf()
            self.assertTrue(path.exists(result))

    def test_fb2(self):
        if self.source != "" and self.source is not None:
            self.test_rss.connect_to_source()
            self.test_rss.parse()
            self.test_rss.make_date()
            self.test_rss.connect_to_history_db()
            self.test_rss.save_page_to_db()
            self.test_rss.prepare_env("rss-parser-out\\fb2")
            result = self.test_rss.to_fb2(date=self.date)
            self.assertTrue(path.exists(result))
        if self.date:
            self.test_rss.prepare_env("rss-parser-out\\history")
            self.test_rss.connect_to_history_db()
            self.test_rss.get_saved_page(self.date)
            self.test_rss.prepare_env("rss-parser-out\\fb2")
            result = self.test_rss.to_fb2(date=self.date)
            self.assertTrue(path.exists(result))

    def tearDown(self) -> None:
        print("Testing done. You are awesome!")
