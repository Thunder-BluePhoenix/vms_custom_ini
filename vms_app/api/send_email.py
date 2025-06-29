from __future__ import unicode_literals
import frappe
from datetime import date
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



class SendEmail:

    def __init__(self):
        pass
    
    @frappe.whitelist(allow_guest=True)
    def send_email(self, from_address, to_address, subject):

        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        self.from_address = from_address 
        self.to_address = to_address
        self.subject = subject
        body = "Quoatation has been submitted by Vendor ."
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(smtp_user, smtp_password)  
                server.sendmail(from_address, to_address, msg.as_string()) 
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
