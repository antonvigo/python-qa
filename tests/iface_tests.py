#!/usr/bin/env python3
import unittest
import requests

from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

TEST_URL = "http://unoume-qa12.devops.rebrain.srwx.net"

class TestCalc(unittest.TestCase):

    def test_calc_interface(self):
        operation = "5,+,2"
        expected_result = 7

        # Add some result to DB
        requests.post('/'.join((TEST_URL, 'calc')),
            data={'operation':'998,-,888'})

        # Init object
        browser = RoboBrowser(history=True, parser='html.parser')
        browser.open(TEST_URL)

        # Fill calc form
        calc_form = browser.get_form(action='/calc')
        calc_form['operation'] = operation
        browser.submit_form(calc_form)

        # Get result
        result_raw = browser.find(id="result").text
        self.assertEqual(int(result_raw), expected_result)

        # Check result link
        browser.follow_link(browser.find(id='result_link'))
        self.assertEqual((operation, expected_result),
            (browser.find(id="operation").text, int(browser.find(id="result").text)))

    def test_cleanup_interface(self):
        # Init object
        browser = RoboBrowser(history=True, parser='html.parser')
        browser.open(TEST_URL)

        # Find cleanup form
        cleanup_form = browser.get_form(action='/cleanup')
        self.assertTrue(cleanup_form)

        # Cleanup DB using form
        browser.submit_form(cleanup_form)
        self.assertTrue(browser.find(text="Database cleared"))


if __name__ == '__main__':
    unittest.main()

