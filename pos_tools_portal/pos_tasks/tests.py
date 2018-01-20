# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.
class LoginTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(LoginTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(LoginTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        #Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/login/')
        #find the form element
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')

        submit = selenium.find_element_by_id('login-form')

        #Fill the form with data
        username.send_keys('test')
        password.send_keys('test')

        #submitting the form
        submit.send_keys(Keys.RETURN)

        #check the returned result
        assert 'Username' in selenium.page_source
