import json
import os
from email.mime.text import MIMEText
from http.client import responses
import requests
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from exceptions import InvalidInputException, ClientSideException, ServerSideException, RequestsErrorException, \
    DataNotPresent
from typing import List, Dict

URL = 'https://dummyjson.com/products'
RESULTS_FILENAME = 'products.txt'
RESULTS_LOCATION = 'results'
email_recipient = 'stakeholders@mycompany.com'
email_sender = os.environ.get('EMAIL_ID', '<Default Email Id>')
email_sender_pwd = os.environ.get('EMAIL_APP_PASSWORD', '<Default Email Password>')


def api_caller_function(url: str) -> requests.models.Response:
    """
    This is function for api calls.
    It will also raise exceptions as per the status codes.
    :param url:
    :return: requests.models.Response
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response
    elif 400 <= response.status_code < 500:
        raise ClientSideException(
            f"Client Side Error !! HTTP Status Code:{response.status_code} ({responses[response.status_code]})")
    elif response.status_code >= 500:
        raise ServerSideException(
            f"Server Side Error !! HTTP Status Code:{response.status_code} ({responses[response.status_code]})")
    else:
        raise RequestsErrorException(
            f"Something went wrong. HTTP Status Code:{response.status_code} ({responses[response.status_code]})")


def fetch_data() -> List[Dict]:
    """
    This function will call api_caller function and get response object from it.
    It will convert Response object content to Python Dictionary
    Then return the Products (key) from the dictionary
    :return: Products: List[Dict]
    """
    resp = api_caller_function(url=URL)
    data = json.loads(resp.content).get('products')
    if data:
        return data
    raise DataNotPresent('Products not present in the response !')


def sort_data(data: List[Dict], sort_by: str) -> List[Dict]:
    """
    It will sort the dictionaries based on either 'price' or 'title'
    :param data: input data to be sorted. List of Dictionaries
    :param sort_by: key to be used for sorting (title or price)
    :return: Sorted_Products: List[Dict]
    """
    return sorted(data, key=lambda d: d[sort_by])


def save_data(sorted_products: List[Dict], result_path: str = None) -> None:
    """
    It will save sorted data on local txt file
    This file will be a tab-separated values files
    :param sorted_products: List of Dictionaries
    :param result_path: Path where output file should be stored
    :return:
    """
    if result_path is None:
        result_path = os.getcwd() + '/' + RESULTS_LOCATION
    # Creating path /results in current folder to save the sorted data
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # Writing to the file using Tab delimiter ('\t')
    # Here using tab-separated delimiter because we have multiple commas in input file
    # Also we have | (pipe) operator, so used \t as delimiter
    with open(result_path + '/' + RESULTS_FILENAME, 'w', newline='', encoding='utf-8') as output_file:
        dw = csv.DictWriter(output_file, sorted_products[0].keys(), delimiter='\t')
        dw.writeheader()
        dw.writerows(sorted_products)


def send_email(sort_by: str) -> Dict:
    """
    This function will send email upon user make choice to share file via email
    :param sort_by: This is key by which data is sorted. We are using this info to construct email body and filename.
    :return: Empty Dict (Meaning mail has been sent successfully)
    """
    msg = MIMEMultipart()
    msg['Subject'] = "Details of products"
    msg['From'] = email_sender
    msg['To'] = email_recipient

    # Attaching body text
    body = f"Products are sorted by {sort_by}"
    body = MIMEText(body)  # convert the body to MIME compatible string
    msg.attach(body)  # attach it to message

    # Using context manager to read file so that we don't need to worry about closing it
    with open(RESULTS_LOCATION + '/' + RESULTS_FILENAME, "rb") as file:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=sort_by + '_' + RESULTS_FILENAME)
        msg.attach(part)

    # Sending email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        # If you are using gmail then you must create Application Specific Password
        # from gmail security settings
        server.login(email_sender, email_sender_pwd)
        resp = server.send_message(msg)
        return resp


def get_result_location() -> str:
    """
    This is simple function which just returns output/result file location
    :return: output_location: str
    """
    return os.getcwd() + '\\' + RESULTS_LOCATION + '\\' + RESULTS_FILENAME
