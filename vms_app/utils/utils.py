from __future__ import unicode_literals
import frappe
from datetime import datetime
from frappe.utils.file_manager import save_url
import requests
import json
from frappe.utils.background_jobs import enqueue
from frappe import _
import sched
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.message import EmailMessage
import fitz
import os
from frappe.utils.file_manager import get_files_path
from vms_app.api.send_email import SendEmail
import frappe.sessions
from datetime import datetime
from frappe.auth import LoginManager
from requests.auth import HTTPBasicAuth
from cryptography.fernet import Fernet
import base64
from vms_app.api.config.api import SAP_BASE_URL



def send_request(url, payload, method="GET", headers=None, auth=None):
    if payload is None:
        payload = {}
    if headers is None:
        headers = {}
    headers = {
        'Content-Type': 'application/json',
        **headers
    }
    if method == "POST" or method == "PUT":
        response = requests.request(
            method, url, auth=auth, headers=headers, data=json.dumps(payload, default=str))
        print("***********************from IF*********************************************")
        print(response.status_code)
    else:
        auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
        response = requests.get(method, url, headers=headers, auth=auth)
        print("***********************from ELSE*********************************************")
        print(response.status_code)
    return response


def get_token_from_sap():
    try:
        url = f"{SAP_BASE_URL}/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
        headers = {"X-CSRF-TOKEN": "Fetch"}
        return send_request(url, headers=headers, method="GET")
    except Exception as e:
        return ({"status": "failure", "message": f"An error occurred: {str(e)}"})