import os
import unittest
from email.mime.multipart import MIMEMultipart
from unittest.mock import patch, MagicMock
import requests
from exceptions import *
from utils import fetch_data, sort_data, save_data, send_email, get_result_location
from pathlib import Path
from utils import RESULTS_FILENAME, RESULTS_LOCATION
from utils import email_sender, email_sender_pwd


class TestFetchData(unittest.TestCase):
    """
    This class is for testing fetch_data, get_result_location,
    sort_data, save_data functions
    """
    TEST_RESULTS_LOCATION = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = None
        cls.TEST_RESULTS_LOCATION = os.getcwd() + '/test'
        cls.sort_by = 'title'

    @classmethod
    def tearDownClass(cls) -> None:
        # Cleaning up test files after test is run
        import shutil
        if os.path.exists(cls.TEST_RESULTS_LOCATION):
            shutil.rmtree(cls.TEST_RESULTS_LOCATION)

    @patch('utils.requests.get')
    def test_fetch_data_success(self, mock_get):
        """
        Mocking requests.get function to receive successful response
        :param mock_get:
        :return:
        """
        mock_get.return_value.status_code = 200

        with open('mock_objects/bytes_data', 'rb') as file:
            mock_get.return_value.content = file.read()

        TestFetchData.data = fetch_data()

        # Assert that the request-response cycle completed successfully.
        self.assertIsInstance(self.data, list)

    @patch('utils.requests.get')
    def test_fetch_data_client_error(self, mock_get):
        """
        Mocking requests.get function to receive client side http error
        :param mock_get:
        :return:
        """
        mock_get.return_value.status_code = 404  # Mock status code of response.
        self.assertRaises(ClientSideException, fetch_data)

    @patch('utils.requests.get')
    def test_fetch_data_server_error(self, mock_get):
        """
        Mocking requests.get function to receive server side http error
        :param mock_get:
        :return:
        """
        mock_get.return_value.status_code = 500  # Mock status code of response.
        self.assertRaises(ServerSideException, fetch_data)

    @patch('utils.requests.get')
    def test_fetch_data_requests_conn_error(self, mock_obj):
        """
        Mocking requests.get function to raise Connection Exception
        :param mock_obj:
        :return:
        """
        # mock_get.return_value.status_code = 500  # Mock status code of response.
        # self.assertRaises(ServerSideException, fetch_data)
        mock_obj.side_effect = requests.exceptions.ConnectionError()
        self.assertRaises(requests.exceptions.ConnectionError, fetch_data)

    @patch('utils.requests.get')
    def test_fetch_data_requests_invalid_json_error(self, mock_obj):
        """
        Mocking requests.get function to raise Invalid JSON Exception from source
        :param mock_obj:
        :return:
        """
        # mock_get.return_value.status_code = 500  # Mock status code of response.
        # self.assertRaises(ServerSideException, fetch_data)
        mock_obj.side_effect = requests.exceptions.InvalidJSONError()
        self.assertRaises(requests.exceptions.InvalidJSONError, fetch_data)

    @patch('utils.requests.get')
    def test_fetch_data_requests_timeout_error(self, mock_obj):
        """
        Mocking requests.get function to raise Invalid JSON Exception from source
        :param mock_obj:
        :return:
        """
        # mock_get.return_value.status_code = 500  # Mock status code of response.
        # self.assertRaises(ServerSideException, fetch_data)
        mock_obj.side_effect = requests.exceptions.Timeout()
        self.assertRaises(requests.exceptions.Timeout, fetch_data)

    def test_get_result_location(self):
        temp = os.getcwd() + '\\' + RESULTS_LOCATION + '\\' + RESULTS_FILENAME
        self.assertEqual(temp, get_result_location())

    def test_sort_data_success(self):
        """
        Tests sort data successful
        :return:
        """
        sort_methods = ['price', 'title']

        for sort_by in sort_methods:
            data = sort_data(self.data, sort_by)

            self.assertIsInstance(data, list)
            self.assertEqual(data, sorted(self.data, key=lambda d: d[sort_by]))

    def test_sort_data_failure(self):
        """
        Tests sort data failure
        :return:
        """
        data = sort_data(self.data, 'title')
        self.assertIsInstance(data, list)
        self.assertNotEqual(data, sorted(self.data, key=lambda d: d['price']))

    def test_save_data_success(self):
        """
        Tests save data successful
        """
        save_data(sort_data(self.data, 'price'), self.TEST_RESULTS_LOCATION)
        path = Path(f'{self.TEST_RESULTS_LOCATION}/{RESULTS_FILENAME}')
        assert path.is_file()


class TestSendEmail(unittest.TestCase):
    """
    This class is for testing Email functionality
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.sort_by = 'title'

    @patch('smtplib.SMTP')
    def test_sendmail_starttls(self, mock_obj):
        """Test that send_message return {} empty dict after successful sending email"""

        class CustomSMTPMock(MagicMock):
            def ehlo(self):
                pass

            def starttls(self, *args, **kwargs):
                pass

            def login(self, user, password):
                assert user == email_sender
                assert password == email_sender_pwd

            def send_message(self, *args, **kwargs):
                assert isinstance(args[0], MIMEMultipart)
                return {}

        mock_obj.return_value = CustomSMTPMock()

        resp = send_email(self.sort_by)
        self.assertEqual(resp, {})
