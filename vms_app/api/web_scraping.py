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
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import base64  
from io import BytesIO
from PIL import Image
import pdb



@frappe.whitelist(allow_guest=True)
def get_data_from_page():

	#url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
	url = "https://microcrispr.bio/"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	#content_div = soup.find(id='mw-content-text')
	#paragraphs = content_div.find_all('p')
	#pdb.set_trace()
	paragraphs = soup.find_all('p')
	for paragraph in paragraphs:
		print(paragraph.text)

	return paragraphs

@frappe.whitelist(allow_guest=True)
def download_media(url, folder):
	os.makedirs(folder, exist_ok=True)
	if url.startswith('data:image'):
	    data = url.split(',')[1]
	    img_data = base64.b64decode(data)
	    img = Image.open(BytesIO(img_data))
	    filename = f"image_{hash(url)}.png"
	    filepath = os.path.join(folder, filename)
	    img.save(filepath)
	else:
	    filename = url.split('/')[-1]
	    filepath = os.path.join(folder, filename)
	    with open(filepath, 'wb') as f:
	        response = requests.get(url)
	        f.write(response.content)

@frappe.whitelist(allow_guest=True)
def get_media_from_page():
	url = "https://microcrispr.bio/"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')

	videos = soup.find_all('video')
	for video in videos:
	    src = video.get('src')
	    if src:
	        download_media(src, './downloads')

	images = soup.find_all('img')
	for image in images:
	    src = image.get('src')
	    if src:
	        absolute_url = urljoin(url, src)
	        download_media(absolute_url, './downloads')


get_media_from_page()