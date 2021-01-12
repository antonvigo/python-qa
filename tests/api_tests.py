#!/usr/bin/env python3
# API tests for QA-12

import requests
from bs4 import BeautifulSoup
from integrate import TestCase, test

class Test(TestCase):
    "AVG QA-12 API tests"

    test_id = ''

    @test()
    def root_test(self, check):
        "Root page API test"
        # API request to /
        web_page = requests.get('http://unoume-qa12.devops.rebrain.srwx.net').text
        soup = BeautifulSoup(web_page, 'html.parser')
        check.is_true(
            soup.find('input', {'name':'operation'}).get('type') == 'text' and
            soup.find('input', {'value':'Посчитать'}).get('type') == 'submit')


    @test()
    def cleanup_test(self, check):
        "Cleanup page API test"
        # API request to cleanup
        web_page = requests.post('http://unoume-qa12.devops.rebrain.srwx.net/cleanup').text
        check.is_true(web_page == 'Database cleared')


    @test(skip_if_failed = ["cleanup_test"])
    def calc_test1(self, check):
        "Calc page API test #1"
        operation = "3,+,18"
        result = "21"
        # API request to calc
        web_page = requests.post('http://unoume-qa12.devops.rebrain.srwx.net/calc',
            data={'operation':operation}).text
        soup = BeautifulSoup(web_page, 'html.parser')
        check.equal(
            (soup.find(id = "operation").string,
            soup.find(id = "result").string),
            (operation, result))


    @test(skip_if_failed = ["cleanup_test"])
    def calc_test2(self, check):
        "Calc page API test #2"
        operation = "49,-,17"
        result = "32"
        # API request to calc
        web_page = requests.post('http://unoume-qa12.devops.rebrain.srwx.net/calc',
            data={'operation':operation}).text
        soup = BeautifulSoup(web_page, 'html.parser')
        check.equal(
            (soup.find(id = "operation").string,
            soup.find(id = "result").string),
            (operation, result))


    @test(skip_if_failed = ["calc_test1", "calc_test2"])
    def results_test(self, check):
        "Results_secret page API test"
        operation = "49,-,17"
        result = "32"
        result_id = "deadbeaf"
        second_result = []
        # API request to results_secret
        web_page = requests.get('http://unoume-qa12.devops.rebrain.srwx.net/results_secret').text
        soup = BeautifulSoup(web_page, 'html.parser')
        for child in soup.findAll("tr")[2].children:
            if child.name == 'td':
                second_result.append(str(child.string))
        self.test_id = second_result[0]
        check.equal(
            (second_result[1], second_result[2]),
            (operation, result))


    @test(skip_if_failed = ["results_test"])
    def result_id_test(self, check):
        "Result/<id> page API test"
        operation = "49,-,17"
        result = "32"
        # API request to result/<result_id>
        web_page = requests.get(
            'http://unoume-qa12.devops.rebrain.srwx.net/result/{}'.format(self.test_id)).text
        soup = BeautifulSoup(web_page, 'html.parser')
        check.equal(
            (soup.find(id = "operation").string,
            soup.find(id = "result").string),
            (operation, result))
