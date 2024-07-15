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
#import fitz
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
from vms_app.utils.utils import get_token_from_sap, send_request
import uuid
from frappe.utils.file_manager import save_file
import pandas as pd




# @frappe.whitelist()
# def new_login(usr, pwd):


# Token 061940ef4019166:99c6e92f817521e




#*********************************Purchase Order API**************************************************

# @frappe.whitelist(allow_guest=True)
# def show_purchase_order(**kwargs):

#     rfq_number = kwargs.get("rfq_number")
#     rfq = show_rfq_detail(rfq_number)
#     purchase_detail = frappe.db.sql(""" select * from `tabPurchase Order` where rfq_code=%s """,(rfq_number), as_dict=1)
#     parent = frappe.db.get_value("Purchase Order", filters={'rfq_code': rfq_number}, fieldname=["name"])
#     purchase_items = frappe.db.sql(""" select * from `tabPurchase Order Item` where parent=%s  """,(parent),as_dict=1)
#     full_detail = purchase_detail + purchase_items
#     return full_detail


# @frappe.whitelist(allow_guest=True)
# def show_single_purchase_order(**kwargs):

#     name = kwargs.get("name")
#     #name = show_rfq_detail(rfq_number)
#     purchase_detail = frappe.db.sql(""" select * from `tabPurchase Order` where name=%s """,(name), as_dict=1)
#     #parent = frappe.db.get_value("Purchase Order", filters={'rfq_code': rfq_number}, fieldname=["name"])
#     purchase_items = frappe.db.sql(""" select * from `tabPurchase Order Item` where parent=%s  """,(name),as_dict=1)
    
    
#     for detail in purchase_detail:
#         if detail.get('material_code'):
#             material_name = frappe.db.get_value("Material Master", detail['material_code'], "material_code")
#             detail['material_code'] = material_code
#         if detail.get('product_code'):
#             product_name = frappe.db.get_value("Product Master", detail['product_code'], "product_name")
#             detail['product_code'] = product_code
#         if detail.get('purchase_group'):
#             purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
#             detail['purchase_group'] = purchase_group_name
    
#     for item in purchase_items:
#         if item.get('material_code'):
#             material_name = frappe.db.get_value("Material Master", item['material_code'], "material_name")
#             item['material_code'] = material_code
#         if item.get('product_code'):
#             product_name = frappe.db.get_value("Product Master", item['product_code'], "product_name")
#             item['product_code'] = product_code

#     full_detail = purchase_detail + purchase_items
#     return full_detail


# @frappe.whitelist(allow_guest=True)
# def show_single_purchase_order(**kwargs):
#     name = kwargs.get("name")
    
#     if name:
#         purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` WHERE name=%s """, (name,), as_dict=1)
#         purchase_items = frappe.db.sql(""" SELECT * FROM `tabPurchase Order Item` WHERE parent=%s """, (name,), as_dict=1)
#     else:
#         purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` """, as_dict=1)
#         purchase_items = frappe.db.sql(""" SELECT * FROM `tabPurchase Order Item` """, as_dict=1)

#     for detail in purchase_detail:
#         if detail.get('material_code'):
#             material_name = frappe.db.get_value("Material Master", detail['material_code'], "material_name")
#             detail['material_code'] = material_name
#         if detail.get('product_code'):
#             product_name = frappe.db.get_value("Product Master", detail['product_code'], "product_name")
#             detail['product_code'] = product_name
#         if detail.get('purchase_group'):
#             purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
#             detail['purchase_group'] = purchase_group_name

#     for item in purchase_items:
#         if item.get('material_code'):
#             material_name = frappe.db.get_value("Material Master", item['material_code'], "material_name")
#             item['material_code'] = material_name
#         if item.get('product_code'):
#             product_name = frappe.db.get_value("Product Master", item['product_code'], "product_name")
#             item['product_code'] = product_name

#     full_detail = purchase_detail + purchase_items
#     return full_detail



# # @frappe.whitelist(allow_guest=True)
# # def show_single_purchase_order(**kwargs):
# #     name = kwargs.get("name")
# #     purchase_detail = frappe.db.sql(""" select * from `tabPurchase Order` where name=%s """, (name), as_dict=1)
# #     purchase_items = frappe.db.sql(""" select * from `tabPurchase Order Item` where parent=%s """, (name), as_dict=1)

# #     for detail in purchase_detail:
# #         if detail.get('material_code'):
# #             material_name = frappe.db.get_value("Material Master", detail['material_code'], "material_name")
# #             detail['material_code'] = material_name
# #         if detail.get('product_code'):
# #             product_name = frappe.db.get_value("Product Master", detail['product_code'], "product_name")
# #             detail['product_code'] = product_name
# #         if detail.get('purchase_group'):
# #             purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
# #             detail['purchase_group'] = purchase_group_name

# #     for item in purchase_items:
# #         if item.get('material_code'):
# #             material_name = frappe.db.get_value("Material Master", item['material_code'], "material_name")
# #             item['material_code'] = material_name
# #         if item.get('product_code'):
# #             product_name = frappe.db.get_value("Product Master", item['product_code'], "product_name")
# #             item['product_code'] = product_name

# #     full_detail = purchase_detail + purchase_items
# #     return full_detail




# @frappe.whitelist()
# def show_purchase_order(**kwargs):
#     rfq_number = kwargs.get("rfq_number")
#     rfq = show_rfq_detail(rfq_number)
#     purchase_detail = frappe.db.sql("""SELECT * FROM `tabPurchase Order` WHERE rfq_code=%s""", (rfq_number), as_dict=1)
#     parent = frappe.db.get_value("Purchase Order", filters={'rfq_code': rfq_number}, fieldname=["name"])
#     purchase_items = frappe.db.sql("""SELECT * FROM `tabPurchase Order Item` WHERE parent=%s""", (parent), as_dict=1)

    
#     for detail in purchase_detail:
#         if detail.get('material_code'):
#             material_code = frappe.db.get_value("Material Master", detail['material_code'], "material_code")
#             detail['material_code'] = material_code

#         if detail.get('purchase_group'):
#             purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
#             detail['purchase_group'] = purchase_group_name
#         if detail['company_code']:
#             company_code = frappe.db.get_value("Company Master", detail['company_code'], "company_code")
#             detail['company_code'] = company_code
#         if detail.get('product_category'):
#             product_category_name = frappe.db.get_value("Product Category Master", detail['product_category'], "product_category_name")
#             detail['product_category'] = product_category_name
#         if detail.get('material_category'):
#             material_category_name = frappe.db.get_value("Material Category Master", detail['material_category'], "material_category_name")
#             detail['material_category'] = material_category_name
#         if detail.get('quantity_unit'):
#             uom = frappe.db.get_value("UOM Master", detail['quantity_unit'], "uom")
#             detail['quantity_unit'] = uom
#         if detail.get('plant'):
#             plant_name = frappe.db.get_value("Plant Master", detail['plant'], "plant_name")
#             detail['plant'] = plant_name
#         if detail.get('city'):
#             city_name = frappe.db.get_value("City Master", detail['city'], "city_name")
#             detail['city'] = city_name
#         if detail.get('district'):
#             district_name = frappe.db.get_value("District Master", detail['district'], "district_name")
#             detail['district'] = district_name
#         if detail.get('state'):
#             state_name = frappe.db.get_value("State Master", detail['state'], "state_name")
#             detail['state'] = state_name
#         if detail.get('country'):
#             country_name = frappe.db.get_value("Country Master", detail['country'], "country_name")
#             detail['country'] = country_name
#         if detail.get('pincode'):
#             pincode = frappe.db.get_value("Pincode Master", detail['pincode'], "pincode")
#             detail['pincode'] = pincode
#         if detail.get('shipping_city'):
#             city_name = frappe.db.get_value("City Master", detail['shipping_city'], "city_name")
#             detail['shipping_city'] = city_name
#         if detail.get('shipping_district'):
#             district_name = frappe.db.get_value("District Master", detail['shipping_district'], "district_name")
#             detail['shipping_district'] = district_name
#         if detail.get('shipping_state'):
#             state_name = frappe.db.get_value("State Master", detail['shipping_state'], "state_name")
#             detail['shipping_state'] = state_name
#         if detail.get('shipping_country'):
#             country_name = frappe.db.get_value("Country Master", detail['shipping_country'], "country_name")
#             detail['shipping_country'] = country_name
#         if detail.get('shipping_pincode'):
#             pincode = frappe.db.get_value("Pincode Master", detail['shipping_pincode'], "pincode")
#             detail['shipping_pincode'] = pincode

@frappe.whitelist()
def show_purchase_order(**kwargs):
    rfq_number = kwargs.get("rfq_number")
    rfq = show_rfq_detail(rfq_number)
    purchase_detail = frappe.db.sql("""SELECT * FROM `tabPurchase Order` WHERE rfq_code=%s""", (rfq_number), as_dict=1)
    parent = frappe.db.get_value("Purchase Order", filters={'rfq_code': rfq_number}, fieldname=["name"])
    purchase_items = frappe.db.sql("""SELECT * FROM `tabPurchase Order Item` WHERE parent=%s""", (parent), as_dict=1)

    
    for detail in purchase_detail:
        if detail.get('material_code'):
            material_code = frappe.db.get_value("Material Master", detail['material_code'], "material_code")
            detail['material_code'] = material_code

        if detail.get('purchase_group'):
            purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
            detail['purchase_group'] = purchase_group_name
        if detail['company_code']:
            company_code = frappe.db.get_value("Company Master", detail['company_code'], "company_code")
            detail['company_code'] = company_code
        if detail.get('product_category'):
            product_category_name = frappe.db.get_value("Product Category Master", detail['product_category'], "product_category_name")
            detail['product_category'] = product_category_name
        if detail.get('material_category'):
            material_category_name = frappe.db.get_value("Material Category Master", detail['material_category'], "material_category_name")
            detail['material_category'] = material_category_name
        if detail.get('quantity_unit'):
            uom = frappe.db.get_value("UOM Master", detail['quantity_unit'], "uom")
            detail['quantity_unit'] = uom
        if detail.get('plant'):
            plant_name = frappe.db.get_value("Plant Master", detail['plant'], "plant_name")
            detail['plant'] = plant_name
        if detail.get('city'):
            city_name = frappe.db.get_value("City Master", detail['city'], "city_name")
            detail['city'] = city_name
        if detail.get('district'):
            district_name = frappe.db.get_value("District Master", detail['district'], "district_name")
            detail['district'] = district_name
        if detail.get('state'):
            state_name = frappe.db.get_value("State Master", detail['state'], "state_name")
            detail['state'] = state_name
        if detail.get('country'):
            country_name = frappe.db.get_value("Country Master", detail['country'], "country_name")
            detail['country'] = country_name
        if detail.get('pincode'):
            pincode = frappe.db.get_value("Pincode Master", detail['pincode'], "pincode")
            detail['pincode'] = pincode
        if detail.get('shipping_city'):
            city_name = frappe.db.get_value("City Master", detail['shipping_city'], "city_name")
            detail['shipping_city'] = city_name
        if detail.get('shipping_district'):
            district_name = frappe.db.get_value("District Master", detail['shipping_district'], "district_name")
            detail['shipping_district'] = district_name
        if detail.get('shipping_state'):
            state_name = frappe.db.get_value("State Master", detail['shipping_state'], "state_name")
            detail['shipping_state'] = state_name
        if detail.get('shipping_country'):
            country_name = frappe.db.get_value("Country Master", detail['shipping_country'], "country_name")
            detail['shipping_country'] = country_name
        if detail.get('shipping_pincode'):
            pincode = frappe.db.get_value("Pincode Master", detail['shipping_pincode'], "pincode")
            detail['shipping_pincode'] = pincode






    
    for item in purchase_items:
        if item.get('material_code'):
            material_code = frappe.db.get_value("Material Master", item['material_code'], "material_code")
            item['material_code'] = material_code
        if item.get('product_code'):
            product_code = frappe.db.get_value("Product Master", item['product_code'], "product_code")
            item['product_code'] = product_code
        if item.get('product_name'):
            product_name = frappe.db.get_value("Product Master", item['product_name'], "product_name")
            item['product_name'] = product_name


    full_detail = purchase_detail + purchase_items

   
    frappe.log_error(message=str(full_detail), title="Debug: Full Purchase Order Details")

    return full_detail


# @frappe.whitelist(allow_guest=True)
# def show_single_purchase_order(**kwargs):
#     name = kwargs.get("name")

#     if name:
#         purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` WHERE name=%s """, (name,), as_dict=1)
#     else:
#         purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` """, as_dict=1)

#     for detail in purchase_detail:
       
#         purchase_items = frappe.db.sql(""" SELECT * FROM `tabPurchase Order Item` WHERE parent=%s """, (detail['name'],), as_dict=1)
        
        
#         detail['items'] = purchase_items

      
#         if detail.get('material_code'):
#             material_name = frappe.db.get_value("Material Master", detail['material_code'], "material_name")
#             detail['material_code'] = material_name
#         if detail.get('product_code'):
#             product_name = frappe.db.get_value("Product Master", detail['product_code'], "product_name")
#             detail['product_code'] = product_name
#         if detail.get('purchase_group'):
#             purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
#             detail['purchase_group'] = purchase_group_name
#         if detail.get('company_code'):
#             company_name = frappe.db.get_value("Company Master", detail['company_code'], "company_name")
#             detail['company_code'] = company_name
#         if detail.get('product_category'):
#             product_category_name = frappe.db.get_value("Product Category Master", detail['product_category'], "product_category_name")
#             detail['product_category'] = product_category_name
#         if detail.get('material_category'):
#             material_category_name = frappe.db.get_value("Material Category Master", detail['material_category'], "material_category_name")
#             detail['material_category'] = material_category_name
#         if detail.get('city'):
#             city_name = frappe.db.get_value("City Master", detail['city'], "city_name")
#             detail['city'] = city_name
#         if detail.get('state'):
#             state_name = frappe.db.get_value("State Master", detail['state'], "state_name")
#             detail['state'] = state_name
#         if detail.get('country'):
#             country_name = frappe.db.get_value("Country Master", detail['country'], "country_name")
#             detail['country'] = country_name
#         if detail.get('district'):
#             district_name = frappe.db.get_value("District Master", detail['district'], "district_name")
#             detail['district'] = district_name
#         if detail.get('pincode'):
#             pincode = frappe.db.get_value("Pincode Master", detail['pincode'], "pincode")
#             detail['pincode'] = pincode
#         if detail.get('shipping_city'):
#             city_name = frappe.db.get_value("City Master", detail['shipping_city'], "city_name")
#             detail['shipping_city'] = city_name
#         if detail.get('shipping_state'):
#             state_name = frappe.db.get_value("State Master", detail['shipping_state'], "state_name")
#             detail['shipping_state'] = state_name
#         if detail.get('shipping_country'):
#             country_name = frappe.db.get_value("Country Master", detail['shipping_country'], "country_name")
#             detail['shipping_country'] = country_name
#         if detail.get('shipping_district'):
#             district_name = frappe.db.get_value("District Master", detail['shipping_district'], "district_name")
#             detail['shipping_district'] = district_name
#         if detail.get('shipping_pincode'):
#             pincode = frappe.db.get_value("Pincode Master", detail['shipping_pincode'], "pincode")
#             detail['shipping_pincode'] = pincode
#         if detail.get('currency'):
#             currency_name = frappe.db.get_value("Currency Master", detail['currency'], "currency_name")
#             detail['currency'] = currency_name
#         if detail.get('bill_to_company'):
#             bill_to_company_name = frappe.db.get_value("Company Master", detail['bill_to_company'], "company_name")
#             detail['bill_to_company'] = bill_to_company_name
#         if detail.get('ship_to_company'):
#             ship_to_company_name = frappe.db.get_value("Company Master", detail['ship_to_company'], "company_name")
#             detail['ship_to_company'] = ship_to_company_name
#         if detail.get('terms_of_payment'):
#             terms_of_payment_name = frappe.db.get_value("Terms Of Payment Master", detail['terms_of_payment'], "terms_of_payment_name")
#             detail['terms_of_payment'] = terms_of_payment_name



       
#         for item in purchase_items:
#             if item.get('material_code'):
#                 material_name = frappe.db.get_value("Material Master", item['material_code'], "material_name")
#                 item['material_code'] = material_name
#             if item.get('product_code'):
#                 product_name = frappe.db.get_value("Product Master", item['product_code'], "product_name")
#                 item['product_code'] = product_name
#             if item.get('product_name'):
#                 product_name = frappe.db.get_value("Product Master", item['product_name'], "product_name")

#     return purchase_detail

@frappe.whitelist(allow_guest=True)
def show_single_purchase_order(**kwargs):
    name = kwargs.get("name")

    if name:
        purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` WHERE name=%s """, (name,), as_dict=1)
    else:
        purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order`""", as_dict=1)

    for detail in purchase_detail:
       
        purchase_items = frappe.db.sql(""" SELECT * FROM `tabPurchase Order Item` WHERE parent=%s """, (detail['name'],), as_dict=1)
        
        
        detail['items'] = purchase_items

      
        if detail.get('material_code'):
            material_name = frappe.db.get_value("Material Master", detail['material_code'], "material_name")
            detail['material_code'] = material_name
        if detail.get('product_code'):
            product_name = frappe.db.get_value("Product Master", detail['product_code'], "product_name")
            detail['product_code'] = product_name
        if detail.get('purchase_group'):
            purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
            detail['purchase_group'] = purchase_group_name
        if detail.get('company_code'):
            company_name = frappe.db.get_value("Company Master", detail['company_code'], "company_name")
            detail['company_code'] = company_name
        if detail.get('product_category'):
            product_category_name = frappe.db.get_value("Product Category Master", detail['product_category'], "product_category_name")
            detail['product_category'] = product_category_name
        if detail.get('material_category'):
            material_category_name = frappe.db.get_value("Material Category Master", detail['material_category'], "material_category_name")
            detail['material_category'] = material_category_name
        if detail.get('city'):
            city_name = frappe.db.get_value("City Master", detail['city'], "city_name")
            detail['city'] = city_name
        if detail.get('state'):
            state_name = frappe.db.get_value("State Master", detail['state'], "state_name")
            detail['state'] = state_name
        if detail.get('country'):
            country_name = frappe.db.get_value("Country Master", detail['country'], "country_name")
            detail['country'] = country_name
        if detail.get('district'):
            district_name = frappe.db.get_value("District Master", detail['district'], "district_name")
            detail['district'] = district_name
        if detail.get('pincode'):
            pincode = frappe.db.get_value("Pincode Master", detail['pincode'], "pincode")
            detail['pincode'] = pincode
        if detail.get('shipping_city'):
            city_name = frappe.db.get_value("City Master", detail['shipping_city'], "city_name")
            detail['shipping_city'] = city_name
        if detail.get('shipping_state'):
            state_name = frappe.db.get_value("State Master", detail['shipping_state'], "state_name")
            detail['shipping_state'] = state_name
        if detail.get('shipping_country'):
            country_name = frappe.db.get_value("Country Master", detail['shipping_country'], "country_name")
            detail['shipping_country'] = country_name
        if detail.get('shipping_district'):
            district_name = frappe.db.get_value("District Master", detail['shipping_district'], "district_name")
            detail['shipping_district'] = district_name
        if detail.get('shipping_pincode'):
            pincode = frappe.db.get_value("Pincode Master", detail['shipping_pincode'], "pincode")
            detail['shipping_pincode'] = pincode
        if detail.get('currency'):
            currency_name = frappe.db.get_value("Currency Master", detail['currency'], "currency_name")
            detail['currency'] = currency_name
        if detail.get('bill_to_company'):
            bill_to_company_name = frappe.db.get_value("Company Master", detail['bill_to_company'], "company_name")
            detail['bill_to_company'] = bill_to_company_name
        if detail.get('ship_to_company'):
            ship_to_company_name = frappe.db.get_value("Company Master", detail['ship_to_company'], "company_name")
            detail['ship_to_company'] = ship_to_company_name



       
        for item in purchase_items:
            if item.get('material_code'):
                material_name = frappe.db.get_value("Material Master", item['material_code'], "material_name")
                item['material_code'] = material_name
            if item.get('product_code'):
                product_name = frappe.db.get_value("Product Master", item['product_code'], "product_name")
                item['product_code'] = product_name
            if item.get('product_name'):
                product_name = frappe.db.get_value("Product Master", item['product_name'], "product_name")
            if item.get('uom'):
                uom = frappe.db.get_value("UOM Master", item['uom'], "uom")
                item['uom'] = uom

    return purchase_detail

# ==============================
# @frappe.whitelist(allow_guest=True)
# def show_single_purchase_order(**kwargs):
#     name = kwargs.get("name")

#     if name:
#         purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` WHERE name=%s """, (name,), as_dict=1)
#     else:
#         purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` """, as_dict=1)

#     for detail in purchase_detail:
#         # Fetch related purchase order items
#         purchase_items = frappe.db.sql(""" SELECT * FROM `tabPurchase Order Item` WHERE parent=%s """, (detail['name'],), as_dict=1)
        
#         # Add items to the purchase order
#         detail['items'] = purchase_items

#         # Replace codes with names
#         if detail.get('material_code'):
#             material_name = frappe.db.get_value("Material Master", detail['material_code'], "material_name")
#             detail['material_code'] = material_name
#         if detail.get('product_code'):
#             product_name = frappe.db.get_value("Product Master", detail['product_code'], "product_name")
#             detail['product_code'] = product_name
#         if detail.get('purchase_group'):
#             purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
#             detail['purchase_group'] = purchase_group_name

#         # Replace codes with names in items
#         for item in purchase_items:
#             if item.get('material_code'):
#                 material_name = frappe.db.get_value("Material Master", item['material_code'], "material_name")
#                 item['material_code'] = material_name
#             if item.get('product_code'):
#                 product_name = frappe.db.get_value("Product Master", item['product_code'], "product_name")
#                 item['product_code'] = product_name

#     return purchase_detail

    
#     for item in purchase_items:
#         if item.get('material_code'):
#             material_code = frappe.db.get_value("Material Master", item['material_code'], "material_code")
#             item['material_code'] = material_code
#         if item.get('product_code'):
#             product_code = frappe.db.get_value("Product Master", item['product_code'], "product_code")
#             item['product_code'] = product_code
#         if item.get('product_name'):
#             product_name = frappe.db.get_value("Product Master", item['product_name'], "product_name")
#             item['product_name'] = product_name


#     full_detail = purchase_detail + purchase_items

   
#     frappe.log_error(message=str(full_detail), title="Debug: Full Purchase Order Details")

#     return full_detail


#**********************************Purchase Order API Closed*******************************************************************

#*******************************************GST NUMBER VERIFICATION API *********************************************************
@frappe.whitelist()
def get_id_token():
    username = "P000207"
    password = "C4kIuUEIWZJ36ydy"
    
    auth_string = f"{username}:{password}"
    base64_auth_string = base64.b64encode(auth_string.encode()).decode()

    
    url = "https://aspsapapi0e80xtdo8w6.eu2.hana.ondemand.com:443/aspsapapi-0.0.2-SNAPSHOT/api/generateAccessToken.do"
    
    
    headers = {
        "Authorization": f"Basic {base64_auth_string}"
    }

    try:
      
        response = requests.post(url, headers=headers)

       
        if response.status_code == 200:
            response_data = response.json()
            
            
            id_token = response_data.get("resp", {}).get("id_token")
            
            if id_token:
                return id_token
            else:
                frappe.throw("ID token not found in the response.")
        else:
            frappe.throw(f"API request failed with status code {response.status_code}")
    
    except Exception as e:
        frappe.throw(f"An error occurred while making the API request: {str(e)}")

@frappe.whitelist()
def get_tax_payer_details(**kwargs):
    gst_number = kwargs.get("gstin")
    id_token = get_id_token()
    
    if not id_token:
        frappe.throw("Unable to retrieve ID token.")
    
    url = "https://aspsapapi0e80xtdo8w6.eu2.hana.ondemand.com/aspsapapi-0.0.2-SNAPSHOT/api/getTaxPayerDetails.do"
    
    headers = {
        "IDTOKEN": id_token,
        "Content-Type": "application/json"
    }

    data = {
    "req": {
        "gstin": gst_number
        }
    }
    print("****************gstin", data)
    
    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            hdr = response_data.get("hdr", {})
            resp = response_data.get("resp", {})
            
            status = hdr.get("status")
            message = hdr.get("message")
            print("**************", status, resp)
            
            return {"status": status, "resp": resp}
        else:
            frappe.throw(f"API request failed with status code {response.status_code}")
    
    except Exception as e:
        frappe.throw(f"An error occurred while making the API request: {str(e)}")




#*******************************************GST NUMBER VERIFICATION API CLOSED ************************************************



#***********************************Show Product Master Details  FULL SINGLE/ALL***********************************************************************
@frappe.whitelist()
def show_full_product_detail(**kwargs):
    name = kwargs.get('name')
    query = """
        SELECT 
            pd.product_code AS product_code,
            pd.product_name AS product_name,
            pdc.product_category_name AS product_category_name,
            pd.model_number AS model_number,
            bm.brand_name AS brand_name,
            pd.manufacturing_date AS manufacturing_date,
            pd.product_license_number AS product_license_number,
            uom.uom AS uom,
            mm.material_name AS material_name,
            pd.established_year AS established_year,
            cm.country_name AS company_name,
            pd.description AS description,
            pd.product_dimension AS product_dimension,
            pd.product_weight AS product_weight,
            mm2.material_name AS material_name,
            pd.product_variants AS product_variants,
            pd.product_image_and_video AS product_image_and_video,
            pd.certificates_and_approval AS certificates_and_approval,
            pd.product_pricing AS product_pricing,
            pd.stocks AS stocks,
            pd.lead_time AS lead_time,
            pd.packaging_and_shipping_detail AS packaging_and_shipping_detail,
            pd.warranty_and_support_detail AS warranty_and_support_detail,
            pd.return_and_refund_policy_detail AS return_and_refund_policy_detail,
            pd.product_user_manual AS product_user_manual
        FROM
            `tabProduct Master` pd
            LEFT JOIN `tabProduct Category Master` pdc ON pd.product_category = pdc.name
            LEFT JOIN `tabBrand Master` bm ON pd.brand = bm.name
            LEFT JOIN `tabUOM Master` uom ON pd.uom = uom.name
            LEFT JOIN `tabMaterial Master` mm ON pd.material_type = mm.name
            LEFT JOIN `tabCountry Master` cm ON pd.country_of_origin = cm.name
            LEFT JOIN `tabMaterial Master` mm2 ON pd.material_used = mm2.name
    """

    if name:
        query += " WHERE pd.name=%s"
        product = frappe.db.sql(query, (name,), as_dict=1)
    else:
        product = frappe.db.sql(query, as_dict=1)

    return product

# @frappe.whitelist()
# def show_full_product_detail(**kwargs):

#     name = kwargs.get('name')
#     query = frappe.db.sql("""

#         SELECT 

#         pd.product_code AS product_code,
#         pd.product_name AS product_name,
#         pdc.product_category_name AS product_category_name,
#         pd.model_number AS model_number,
#         bm.brand_name AS brand_name,
#         pd.manufacturing_date AS manufacturing_date,
#         pd.product_license_number AS product_license_number,
#         uom.uom AS uom,
#         mm.material_name AS material_name,
#         pd.established_year AS established_year,
#         cm.country_name AS company_name,
#         pd.description AS description,
#         pd.product_license_number AS product_license_number,
#         pd.product_dimension AS product_dimension,
#         pd.product_weight AS product_weight,
#         mm2.material_name AS material_name,
#         pd.product_variants AS product_variants,
#         pd.product_image_and_video AS product_image_and_video,
#         pd.certificates_and_approval AS certificates_and_approval,
#         pd.product_pricing AS product_pricing,
#         pd.stocks AS stocks,
#         pd.lead_time AS lead_time,
#         pd.packaging_and_shipping_detail AS packaging_and_shipping_detail,
#         pd.warranty_and_support_detail AS warranty_and_support_detail,
#         pd.return_and_refund_policy_detail AS return_and_refund_policy_detail,
#         pd.product_user_manual AS product_user_manual


#         FROM
#         `tabProduct Master` pd
#         LEFT JOIN
#             `tabProduct Category Master` pdc ON pd.product_category = pdc.name
#         LEFT JOIN
#             `tabBrand Master` bm ON pd.brand = bm.name
#         LEFT JOIN
#             `tabUOM Master` uom ON pd.uom = uom.name
#         LEFT JOIN
#             `tabMaterial Master` mm ON pd.material_type = mm.name
#         LEFT JOIN
#             `tabCountry Master` cm ON pd.country_of_origin = cm.name
#         LEFT JOIN
#             `tabMaterial Master` mm2 ON pd.material_used = mm2.name

#         WHERE 
#         pd.name=%s

#      """, (name), as_dict=1)
#     if name:
#         query += "WHERE pd.name=%s"
#         product = frappe.db.sql(query, (name), as_dict=1)
#     else:
#         product = frappe.db.sql(query, as_dict=1)
#         return product





#***********************************Show Product Master Details  FULL CLOSED*****************************************************************







@frappe.whitelist()
def token():
    print("*******************************************************")
    return frappe.local.session.data.csrf_token

@frappe.whitelist()
def is_user_logged_in(email):
    user_session = frappe.db.exists('User', {'email': email, 'last_login': ['!=', None]})
    if user_session:
        return {"message": "User is logged in"}
    else:
        return {"message": "User is not logged in"}




obj = SendEmail()



@frappe.whitelist()
def check_rfq_date(**kwargs):
    name = kwargs.get("rfq_number")
    rfq_cutoff_date = frappe.db.get_value("Request For Quotation", filters={'name': name}, fieldname='rfq_cutoff_date')
    #datetime_obj = datetime.strptime(rfq_cutoff_date, '%d-%m%Y %H:%M:%S')
    date = rfq_cutoff_date.date()
    time = rfq_cutoff_date.time()
    today_datetime = datetime.now()
    print("************************************")
    print(rfq_cutoff_date)
    today_date = today_datetime.date()
    today_time = today_datetime.time()
    print(today_date , today_time)

    return (date, time)

    # current_user = frappe.session.user
    # current_user_designation_id = frappe.db.get_value("User", filters={'name': current_user}, fieldname='designation')
    # current_user_designation_name = frappe.db.get_value("Designation Master", filters={'name': current_user_designation_id}, fieldname='designation_name')


@frappe.whitelist()
def onboarding_detail(**kwargs):

    name = kwargs.get('name')
    values = frappe.db.sql(""" select * from `tabVendor Onboarding` where name=%s """,(name),as_dict=True)
    return values



#****************************************************Login API******************************************************************************



@frappe.whitelist( allow_guest=True )
def login(usr, pwd):

    try:

        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key":0,
            "message":"Authentication Error!"
        }

        return

    # api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)
    print("***********************************************")
    user_designation_id = frappe.db.get_value("User", filters={'email': user.email}, fieldname='designation')
    print(user_designation_id)
    user_designation_name = frappe.db.get_value("Designation Master", filters={'name': user_designation_id}, fieldname='designation_name')
    print(user_designation_name)
    refno = frappe.db.get_value("Vendor Master", filters={'office_email_primary': user.email}, fieldname='name')
    frappe.response["message"] = {

        "success_key":1,
        "message":"Authentication success",
        "sid":frappe.session.sid,
      #  "api_key":user.api_key,
       # "api_secret":api_generate,
        'designation_name': user_designation_name,
        "username":user.username,
        "email":user.email,
        "refno": refno

    }

def generate_keys(user):

    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)
    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
    user_details.api_secret = api_secret
    user_details.save()

    return api_secret

#****************************************************Login API Closed************************************************************************************


@frappe.whitelist(allow_guest=True)
def upload_file(docname, doctype, attachmentFieldName):
    file = frappe.request.files['file']
    is_private = frappe.form_dict.is_private or 0

    # Save the file and link it to the specific document
    saved_file = save_file(file.filename, file.stream.read(), doctype, docname, is_private=int(is_private))
    
    # Update the document field with the file URL
    doc = frappe.get_doc(doctype, docname)

    #attachmentFieldName = ['address_proofattachment','bank_proof','gst_proof','pan_proof','entity_proof','iec_proof','organisation_structure_document','certificate_proof']

    if(attachmentFieldName == 'address_proofattachment'):
        doc.address_proofattachment = saved_file.file_url
    elif(attachmentFieldName == 'bank_proof'): 
        doc.bank_proof =saved_file.file_url
    elif(attachmentFieldName == 'gst_proof'): 
        doc.gst_proof =saved_file.file_url
    elif(attachmentFieldName == 'pan_proof'): 
        doc.pan_proof =saved_file.file_url 
    elif(attachmentFieldName == 'entity_proof'): 
        doc.entity_proof =saved_file.file_url 
    elif(attachmentFieldName == 'iec_proof'): 
        doc.iec_proof =saved_file.file_url
    elif(attachmentFieldName == 'organisation_structure_document'): 
        doc.organisation_structure_document =saved_file.file_url
    elif(attachmentFieldName == 'certificate_proof'): 
        doc.certificate_proof =saved_file.file_url
    else:
        console.log("no field")

    doc.save()

    return {
        'file_url': saved_file.file_url,
        'file_name': saved_file.name
    }



# @frappe.whitelist()
# def send_email(data, method):
#     name = data.get("name")

#     print("*********************************", name)
#     frappe.db.sql(""" update `tabVendor Master` set purchase_team_approval='In Process' where name=%s """, (name))
#     frappe.db.commit()
#     frappe.db.sql(""" update `tabVendor Master` set purchase_head_approval='In Process' where name=%s """, (name) )
#     frappe.db.commit()
#     frappe.db.sql(""" update `tabVendor Master` set accounts_team_approval='In Process' where name=%s """, (name) )
#     frappe.db.commit()
#     print("*********************Hi from Docevents*****************")
#     print(frappe.session.user)
#     current_user = frappe.session.user
#     current_user_email = frappe.db.get_value("User", filters={'full_name': current_user}, fieldname='email')
#     print(current_user_email)
#     frappe.db.sql(""" UPDATE tabVendor Master SET registered_by=%s WHERE name=%s """,(current_user, name))
#     frappe.db.commit()
#     reciever_email = data.get("office_email_primary")
#     print(reciever_email)
#     print("****************EMAIL******************", current_user, reciever_email)
#     smtp_server = "smtp.transmail.co.in"
#     smtp_port = 587
#     smtp_user = "emailapikey"  
#     smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
#     from_address = current_user
#     to_address = reciever_email  
#     subject = "Request for Vendor Onboarding ."
#     body = "You have been Successfully Registered on the VMS Portal. Please complete the On boarding process on this link http://localhost:3000/onboarding?Refno=" + str(name)
#     msg = MIMEMultipart()
#     msg["From"] = from_address
#     msg["To"] = to_address
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))
#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()  
#             server.login(smtp_user, smtp_password)  
#             server.sendmail(from_address, to_address, msg.as_string()) 
#             print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")


@frappe.whitelist()
def send_email(data, method):
    name = data.get("name")
    print("&^$$#$%^&*(*&^%$^&*()*&^%$#^&*())", name)

    print("*********************************", name)
    frappe.db.sql(""" update `tabVendor Master` set purchase_team_approval='In Process' where name=%s """, (name))
    frappe.db.commit()
    frappe.db.sql(""" update `tabVendor Master` set purchase_head_approval='In Process' where name=%s """, (name) )
    frappe.db.commit()
    frappe.db.sql(""" update `tabVendor Master` set accounts_team_approval='In Process' where name=%s """, (name) )
    frappe.db.commit()
    print("*********************Hi from Docevents*****************")
    print(frappe.session.user)
    current_user = frappe.session.user
    print("***********()()(T&^%@#$%^&*(**CURRENT USER*****", current_user)
    current_user_email = frappe.db.get_value("User", filters={'full_name': current_user}, fieldname='email')
    print(current_user_email)
    frappe.db.sql(""" UPDATE `tabVendor Master` SET registered_by=%s WHERE name=%s """,(current_user, name))
    frappe.db.commit()
    reciever_email = data.get("office_email_primary")
    print(reciever_email)
    print("****************EMAIL******************", current_user, reciever_email)
    smtp_server = "smtp.transmail.co.in"
    smtp_port = 587
    smtp_user = "emailapikey"  
    smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
    from_address = current_user
    to_address = reciever_email  
    subject = "Request for Vendor Onboarding ."
    body = "You have been Successfully Registered on the VMS Portal. Please complete the On boarding process on this link http://localhost:3000/onboarding?Refno=" + str(name)
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



@frappe.whitelist()
def show_po_count(**kwargs):
    vendor_code = kwargs.get('vendor_code')
    print("Vendor Code:", vendor_code)  

    if vendor_code:
        total_po = frappe.db.sql("""
            SELECT count(*) as total_count FROM `tabPurchase Order` WHERE vendor_code = %s""", (vendor_code), as_dict=1)
    else:
        total_po = frappe.db.sql("""
            SELECT count(*) as total_count FROM `tabPurchase Order` """, as_dict=1)

    return total_po


# @frappe.whitelist()
# def send_email_on_onboarding(data, method):

#     print("***********Details filled***********")
#     name = data.get('ref_no')
#     current_user_email = data.get('office_email_primary')
#     print("hjagdfkjsdgfkSDfhvzskfhzjkdsl,hdkjgfdjkgbjkhbdkszjfjkdslj",current_user_email)
#     company_name = data.get('company_name')
#     print(company_name)
#     #reciever_email = frappe.db.get_value("Vendor Master", filters={'company_name': company_name}, fieldname=['registered_by'])
#     reciever_email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': current_user_email}, fieldname=['registered_by'])
#     print(reciever_email)
#     subject = "Email sent successfully!"
#    # obj.send_email(reciever_email, current_user_email, subject)
#     smtp_server = "smtp.transmail.co.in"
#     smtp_port = 587
#     smtp_user = "emailapikey"  
#     smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
#     from_address = current_user_email 
#     to_address = reciever_email  
#     subject = "Test email"
#     #body = "This is a Test email ...!"
#     #body = "Vendor has successfully submitted the Onboarding form on the VMS Portal. Please check the details  on this link "http://localhost:3000/purchase-team/vendor-detail?office_email_primary=" " + str(office_email_primary)
#     body = "Vendor has successfully submitted the Onboarding form on the VMS Portal. Please check the details on this link http://localhost:3000/purchase-team/vendor-detail/" + str(current_user_email)

#     msg = MIMEMultipart()
#     msg["From"] = from_address
#     msg["To"] = to_address
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))
#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()  
#             server.login(smtp_user, smtp_password)  
#             server.sendmail(from_address, to_address, msg.as_string()) 
#             print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")


# @frappe.whitelist()
# def send_email_on_onboarding(data, method):
#     print("***********Details filled***********")
    
#     # Print the entire data dictionary to debug
#     print("Received data:", data)
    
#     # Extract office_email_primary
#     name = data.get('office_email_primary')
#     # name = data.get('office_email_secondary')
#     if not name:
#         print("Error: office_email_primary is None")
#         return
    
#     print("%%%%%%%%%%%%%%%%%%%%", name)
    
#     # Get reference number from Vendor Master
#     refno = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['name'])
#     if refno is None:
#         print("Error: refno is None")
#         return
    
#     # Update Vendor Onboarding
#     frappe.db.sql("""UPDATE `tabVendor Onboarding` SET ref_no=%s WHERE office_email_primary=%s""", (refno, name))
#     frappe.db.commit()
    
#     current_user_email = data.get('office_email_primary')
#     if not current_user_email:
#         print("Error: current_user_email is None")
#         return
    
#     print("hjagdfkjsdgfkSDfhvzskfhzjkdsl,hdkjgfdjkgbjkhbdkszjfjkdslj", current_user_email)
    
#     company_name = data.get('company_name')
#     print(company_name)
    
#     # Get receiver email from Vendor Master
#     reciever_email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': current_user_email}, fieldname=['registered_by'])
#     if not reciever_email:
#         print("Error: reciever_email is None")
#         return
    
#     print(reciever_email)
    

# Latest code ====================
@frappe.whitelist()
def send_email_on_onboarding(data, method):

    print("***********Details filled***********")
   # print("Data type:", type(data))
    #print("Data content:", data)
    name = data.get('office_email_primary')
    print("%%%%%%%%%%%%%%%%%%%%", name)
    refno = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['name'])
    frappe.db.sql(""" UPDATE `tabVendor Onboarding` SET ref_no=%s WHERE office_email_primary=%s """, (refno, name))
    frappe.db.commit()
    current_user_email = data.get('office_email_primary')
    print("hjagdfkjsdgfkSDfhvzskfhzjkdsl,hdkjgfdjkgbjkhbdkszjfjkdslj",current_user_email)
    company_name = data.get('company_name')
    print(company_name)
    #reciever_email = frappe.db.get_value("Vendor Master", filters={'company_name': company_name}, fieldname=['registered_by'])
    reciever_email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': current_user_email}, fieldname=['registered_by'])
    print(reciever_email)
    subject = "Email sent successfully!"
   # obj.send_email(reciever_email, current_user_email, subject)
    smtp_server = "smtp.transmail.co.in"
    smtp_port = 587
    smtp_user = "emailapikey"  
    smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
    from_address = current_user_email 
    to_address = reciever_email  
    subject = "Test email"
    #body = "This is a Test email ...!"
    #body = "Vendor has successfully submitted the Onboarding form on the VMS Portal. Please check the details  on this link "http://localhost:3000/purchase-team/vendor-detail?office_email_primary=" " + str(office_email_primary)
    body = "Vendor has successfully submitted the Onboarding form on the VMS Portal. Please check the details on this link http://localhost:3000/purchase-team/vendor-detail/" + str(name)

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
#
# LAtest Code




# @frappe.whitelist()
# def send_email_on_onboarding(data, method):

#     print("***********Details filled***********")
#     name = data.get('office_email_primary')
#     print("%%%%%%%%%%%%%%%%%%%%", name)
#     refno = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['name'])
#     frappe.db.sql(""" UPDATE `tabVendor Onboarding` SET ref_no=%s WHERE office_email_primary=%s """, (refno, name))
#     frappe.db.commit()
#     current_user_email = data.get('office_email_primary')
#     print("hjagdfkjsdgfkSDfhvzskfhzjkdsl,hdkjgfdjkgbjkhbdkszjfjkdslj",current_user_email)
#     company_name = data.get('company_name')
#     print(company_name)
#     #reciever_email = frappe.db.get_value("Vendor Master", filters={'company_name': company_name}, fieldname=['registered_by'])
#     reciever_email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': current_user_email}, fieldname=['registered_by'])
#     print(reciever_email)
#     subject = "Email sent successfully!"
#    # obj.send_email(reciever_email, current_user_email, subject)
#     smtp_server = "smtp.transmail.co.in"
#     smtp_port = 587
#     smtp_user = "emailapikey"  
#     smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
#     from_address = current_user_email 
#     to_address = reciever_email  
#     subject = "Test email"
#     #body = "This is a Test email ...!"
#     #body = "Vendor has successfully submitted the Onboarding form on the VMS Portal. Please check the details  on this link "http://localhost:3000/purchase-team/vendor-detail?office_email_primary=" " + str(office_email_primary)
#     body = "Vendor has successfully submitted the Onboarding form on the VMS Portal. Please check the details on this link http://localhost:3000/purchase-team/vendor-detail?Refno=" + str(name)

#     msg = MIMEMultipart()
#     msg["From"] = from_address
#     msg["To"] = to_address
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))
#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()  
#             server.login(smtp_user, smtp_password)  
#             server.sendmail(from_address, to_address, msg.as_string()) 
#             print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")



@frappe.whitelist()
def hit():
    print("****************Hi there!*******************")
    purchase_head_key = frappe.db.get_value("Designation Master", {"designation_name": "Purchase Head"}, "name")
    accounts_team_key = frappe.db.get_value("Designation Master", {"designation_name": "Accounts Team"}, "name")
    purchase_head_users = frappe.db.get_list("User", filters={"designation": purchase_head_key}, fields=["email"])
    accounts_team_users = frappe.db.get_list("User", filters={"designation": accounts_team_key}, fields=["email"])
    all_emails = [user["email"] for user in accounts_team_users] + [user["email"] for user in purchase_head_users]
    print(all_emails)
    smtp_server = "smtp.transmail.co.in"
    smtp_port = 587
    smtp_user = "emailapikey"  
    smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
    from_address = "noreply@merillife.com" 
    subject = "Test email"
    body = "This is a Test email ...!"
    for to_address in all_emails:
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
                print(f"Email sent successfully to {to_address}!")
        except Exception as e:
            print(f"Failed to send email to {to_address}: {e}")

# ======================
# @frappe.whitelist()
# def show_dispatch_order_detail(**kwargs):
#     po_number = kwargs.get('po_number') 
#     vendor_code = frappe.db.get_value("Purchase Order", filters={"name": po_number}, fieldname=['vendor_code'])
#     vendor_name = frappe.db.get_value("Vendor Master", filters={"vendor_code": vendor_code}, fieldname=['vendor_name'])
#     print("#$%^&*()_VENDOR NAME", vendor_name, vendor_code)

#     if po_number:
#         dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item` WHERE purchase_number=%s""", (po_number), as_dict=1)
#     else:
#         dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item` """, as_dict=1)

#     for detail in dispatch_detail:
#         dispatch_order_item = frappe.db.sql("""SELECT * FROM `tabDispatch Order Items` WHERE parent=%s""", (detail['name']), as_dict=1)
#         detail['dispatch_order_item'] = dispatch_order_item 

#         for item in dispatch_order_item:

#             if item.get('uom'):
#                 uom = frappe.db.get_value("UOM Master", item['uom'], "uom")
#                 item['uom'] = uom
#             if item.get('product_code'):
#                 product_code = frappe.db.get_value("Product Master", item['product_code'], "product_code")
#                 item['product_code'] = product_code
#             if item.get('product_name'):
#                 product_name = frappe.db.get_value("Product Master", item['product_name'], "product_name")
#                 item['product_name'] = product_name
#     if dispatch_detail:
#         dispatch_detail[-1]['vendor_name'] = vendor_name
#     return dispatch_detail

# ==============================
# @frappe.whitelist()
# def show_dispatch_order_detail(**kwargs):
#     po_number = kwargs.get('po_number') 
#     vendor_code = frappe.db.get_value("Purchase Order", filters={"name": po_number}, fieldname=['vendor_code', 'po_number'])
#     vendor_name = frappe.db.get_value("Vendor Master", filters={"vendor_code": vendor_code[0]}, fieldname=['vendor_name'])

#     print("********The Vendor Name", vendor_name, vendor_code)

#     if po_number:
#         dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item` WHERE purchase_number=%s""", (po_number), as_dict=1)
#     else:
#         dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item`""", as_dict=1)

#     for detail in dispatch_detail:
#         dispatch_order_item = frappe.db.sql("""SELECT * FROM `tabDispatch Order Items` WHERE parent=%s""", (detail['name']), as_dict=1)
#         detail['dispatch_order_item'] = dispatch_order_item 

#         for item in dispatch_order_item:

#             if item.get('uom'):
#                 uom = frappe.db.get_value("UOM Master", item['uom'], "uom")
#                 item['uom'] = uom
#             if item.get('product_code'):
#                 product_code = frappe.db.get_value("Product Master", item['product_code'], "product_code")
#                 item['product_code'] = product_code
#             if item.get('product_name'):
#                 product_name = frappe.db.get_value("Product Master", item['product_name'], "product_name")
#                 item['product_name'] = product_name
#     if dispatch_detail:
#         dispatch_detail[-1]['vendor_name'] = vendor_name
#         dispatch_detail[-1]['po_number'] = vendor_code[1]  
#     return dispatch_detail 
# ========================
# @frappe.whitelist()
# def show_dispatch_order_detail(**kwargs):
#     po_number = kwargs.get('po_number')  # Use kwargs to get the parameters

#     if po_number:
#         dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item` WHERE purchase_number=%s""", (po_number), as_dict=1)
#     else:
#         dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item` """, as_dict=1)

#     for detail in dispatch_detail:
#         dispatch_order_item = frappe.db.sql("""SELECT * FROM `tabDispatch Order Items` WHERE parent=%s""", (detail['name']), as_dict=1)
#         detail['dispatch_order_item'] = dispatch_order_item 

#         for item in dispatch_order_item:

#             if item.get('uom'):
#                 uom = frappe.db.get_value("UOM Master", item['uom'], "uom")
#                 item['uom'] = uom
#             if item.get('product_code'):
#                 product_code = frappe.db.get_value("Product Master", item['product_code'], "product_code")
#                 item['product_code'] = product_code
#             if item.get('product_name'):
#                 product_name = frappe.db.get_value("Product Master", item['product_name'], "product_name")
#                 item['product_name'] = product_name
#     return dispatch_detail

@frappe.whitelist()
def show_dispatch_order_detail(**kwargs):
    pno = kwargs.get('pno') 

    if pno:
        vendor_code = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname='vendor_code')
        vendor_name = frappe.db.get_value("Vendor Master", vendor_code, "vendor_name") if vendor_code else None
        po_number = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname='po_number')
        dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item` WHERE purchase_number=%s""", (pno), as_dict=1)
    else:
        dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item`""", as_dict=1)

    for detail in dispatch_detail:
        dispatch_order_item = frappe.db.sql("""SELECT * FROM `tabDispatch Order Items` WHERE parent=%s""", (detail['name']), as_dict=1)
        detail['dispatch_order_item'] = dispatch_order_item 

        if not pno:  
            vendor_code = frappe.db.get_value("Purchase Order", filters={"name": detail['purchase_number']}, fieldname='vendor_code')
            vendor_name = frappe.db.get_value("Vendor Master", vendor_code, "vendor_name") if vendor_code else None
            po_number = frappe.db.get_value("Purchase Order", filters={"name": detail['purchase_number']}, fieldname='po_number')
        
        
        detail['vendor_name'] = vendor_name
        detail['po_number'] = po_number

        for item in dispatch_order_item:
            if item.get('uom'):
                uom = frappe.db.get_value("UOM Master", item['uom'], "uom")
                item['uom'] = uom
            if item.get('product_code'):
                product_code = frappe.db.get_value("Product Master", item['product_code'], "product_code")
                item['product_code'] = product_code
            if item.get('product_name'):
                product_name = frappe.db.get_value("Product Master", item['product_name'], "product_name")
                item['product_name'] = product_name

    return dispatch_detail
    
# ================================================================
# @frappe.whitelist()
# def hitt(data, method):
#     print("****************Hi there!*******************")
#     vendor_type_id = data.get('select_service')
#     name = data.get('name')
#     print("&^*&^&^*&^*&", name)
#     vendors = frappe.db.sql(""" select office_email_primary from `tabVendor Onboarding` where vendor_type=%s """,(vendor_type_id))
#     # vendors = []
#     email_id_of_rfq_creator = frappe.session.user
#     print("*******************************************************")
#     print(email_id_of_rfq_creator)
#     email_addresses = [vendor[0] for vendor in vendors]
#     print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&",email_addresses)
#     smtp_server = "smtp.transmail.co.in"
#     smtp_port = 587
#     smtp_user = "emailapikey"  
#     smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
#     from_address = "noreply@merillife.com" 
#     subject = "Test email"
#     body = "This is a Test email to Vendor regarding RFQ ...! RFQ Link http://localhost:3000/vendor/dashboard/quotation?Refno=" +str(name)
#     for to_address in email_addresses:
#         msg = MIMEMultipart()
#         msg["From"] = from_address
#         msg["To"] = to_address
#         msg["Subject"] = subject
#         msg.attach(MIMEText(body, "plain"))
#         try:
#             with smtplib.SMTP(smtp_server, smtp_port) as server:
#                 server.starttls()  
#                 server.login(smtp_user, smtp_password)  
#                 server.sendmail(from_address, to_address, msg.as_string()) 
#                 print(f"Email sent successfully to {to_address}!")
#         except Exception as e:
#             print(f"Failed to send email to {to_address}: {e}")

@frappe.whitelist()
def hitt(data, method):
    
    list_of_names = data.get('list', [])
    
    
    all_office_emails = []
    
    
    for name in list_of_names:
        vendors = frappe.db.sql("""
            SELECT office_email_primary 
            FROM tabVendor Master 
            WHERE name = %s
        """, (name,), as_dict=True)
        
        
        office_emails = [vendor.get('office_email_primary') for vendor in vendors]
        
        
        all_office_emails.extend(office_emails)
    
    print("List of office_email_primary:", all_office_emails)


    # vendor_emails = data.get('vendor_emails')
    # mylist = []
    # for i in vendor_emails:

    #     mylist.append(i)
    

    # print("Vendor Emails:", vendor_emails)
    
    # if not vendor_emails:
    #     print("No vendor emails provided")
    #     return

    email_id_of_rfq_creator = frappe.session.user
    print("Email ID of RFQ Creator:", email_id_of_rfq_creator)
    
    smtp_server = "smtp.transmail.co.in"
    smtp_port = 587
    smtp_user = "emailapikey"
    smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="
    from_address = "noreply@merillife.com"
    subject = "Test email"
    body = "This is a Test email to Vendor regarding RFQ ...! RFQ Link http://localhost:3000/vendor/dashboard/quotation?Refno=" +str(name)
    
    for to_address in all_office_emails:
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
                print(f"Email sent successfully to {to_address}!")
        except Exception as e:
            print(f"Failed to send email to {to_address}: {e}")   

def set_rfq_raisers_name(data, method):

    email_id_of_rfq_creator = frappe.session.user
    frappe.db.sql("update `tabRequest For Quotation` SET raised_by=%s",(email_id_of_rfq_creator))
    frappe.db.commit()


def send_email_on_quotation_creation(data, method):

    rfq_number = data.get('rfq_number')
    reciever_address = frappe.db.get_value("Request For Quotation", filters={'name': rfq_number}, fieldname=['raised_by'])
    sender_address = frappe.session.user
    print(reciever_address, sender_address)
    print(rfq_number)
    print("******************************************************")
    subject = "Hi there from SendEmail Class ...!"
    obj.send_email(reciever_address, sender_address, subject)
    #test_send_email()
    # smtp_server = "smtp.transmail.co.in"
    # smtp_port = 587
    # smtp_user = "emailapikey"  
    # smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
    # from_address = sender_address 
    # to_address = reciever_address
    # subject = "Test email"
    # body = "Quoatation has been submitted by Vendor ."
    # msg = MIMEMultipart()
    # msg["From"] = from_address
    # msg["To"] = to_address
    # msg["Subject"] = subject
    # msg.attach(MIMEText(body, "plain"))
    # try:
    #     with smtplib.SMTP(smtp_server, smtp_port) as server:
    #         server.starttls()  
    #         server.login(smtp_user, smtp_password)  
    #         server.sendmail(from_address, to_address, msg.as_string()) 
    #         print("Email sent successfully!")
    # except Exception as e:
    #     print(f"Failed to send email: {e}")

  
# @frappe.whitelist(allow_guest=True)
# def test_send_email(from_address, to_address, subject):

#     smtp_server = "smtp.transmail.co.in"
#     smtp_port = 587
#     smtp_user = "emailapikey"  
#     smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
#     from_address = from_address 
#     to_address = to_address
#     subject = subject
#     body = "Quoatation has been submitted by Vendor ."
#     msg = MIMEMultipart()
#     msg["From"] = from_address
#     msg["To"] = to_address
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))
#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()  
#             server.login(smtp_user, smtp_password)  
#             server.sendmail(from_address, to_address, msg.as_string()) 
#             print("Email sent successfully!")
#     except Exception as e:
#         print(f"Failed to send email: {e}")


@frappe.whitelist()
def show_all_detailed_vendor_quotation(vendor_code):
    quotation = frappe.db.sql(""" 
        SELECT
            rfq.name AS name,
            co.company_name AS company_name,
            vm.name AS name,
            qo.rfq_date AS rfq_date,
            qo.quotation_deadline AS quotation_deadline,
            qo.delivery_date AS delivery_date,
            qo.vendor_name AS vendor_name,
            qo.vendor_contact AS vendor_contact,
            qo.contact_person AS contact_person,
            qo.quote_amount AS quote_amount,
            qo.contact_email AS contact_email,
            pm.product_code AS product_code,
            pc.product_category_name AS product_category_name,
            mm.material_code AS material_code,
            mcm.material_category_name AS material_category_name,
            m.material_name AS material_name,
            qo.rfq_quantity AS rfq_quantity,
            qo.storage_location AS storage_location,
            qo.remark AS remark,
            qo.status AS status,
            qo.rfq_number AS rfq_number
        FROM
            `tabQuotation` qo
            LEFT JOIN `tabRequest For Quotation` rfq ON qo.rfq_number = rfq.name
            LEFT JOIN `tabCompany Master` co ON qo.company_name = co.name
            LEFT JOIN `tabVendor Master` vm ON qo.vendor_code = vm.name
            LEFT JOIN `tabProduct Master` pm ON qo.product_code = pm.name
            LEFT JOIN `tabProduct Category Master` pc ON qo.product_category = pc.name
            LEFT JOIN `tabMaterial Master` mm ON qo.material_code = mm.name
            LEFT JOIN `tabMaterial Category Master` mcm ON qo.material_category = mcm.name
            LEFT JOIN `tabMaterial Master` m ON qo.material_name = m.name
        WHERE
            qo.vendor_code=%s
    """, (vendor_code), as_dict=1)
    return quotation


@frappe.whitelist()
def show_all_quotations_against_rfq_number(rfq_number):
    quotation = frappe.db.sql(""" 
        SELECT
            rfq.name AS name,
            co.company_name AS company_name,
            vm.name AS name,
            qo.rfq_date AS rfq_date,
            qo.quotation_deadline AS quotation_deadline,
            qo.delivery_date AS delivery_date,
            qo.vendor_name AS vendor_name,
            qo.vendor_contact AS vendor_contact,
            qo.contact_person AS contact_person,
            qo.quote_amount AS quote_amount,
            qo.contact_email AS contact_email,
            pm.product_code AS product_code,
            pc.product_category_name AS product_category_name,
            mm.material_code AS material_code,
            mcm.material_category_name AS material_category_name,
            m.material_name AS material_name,
            qo.rfq_quantity AS rfq_quantity,
            qo.storage_location AS storage_location,
            qo.remark AS remark,
            qo.status AS status,
            qo.rfq_number AS rfq_number
        FROM
            `tabQuotation` qo
            LEFT JOIN `tabRequest For Quotation` rfq ON qo.rfq_number = rfq.name
            LEFT JOIN `tabCompany Master` co ON qo.company_name = co.name
            LEFT JOIN `tabVendor Master` vm ON qo.vendor_code = vm.name
            LEFT JOIN `tabProduct Master` pm ON qo.product_code = pm.name
            LEFT JOIN `tabProduct Category Master` pc ON qo.product_category = pc.name
            LEFT JOIN `tabMaterial Master` mm ON qo.material_code = mm.name
            LEFT JOIN `tabMaterial Category Master` mcm ON qo.material_category = mcm.name
            LEFT JOIN `tabMaterial Master` m ON qo.material_name = m.name
        WHERE
            qo.rfq_number=%s
    """, (rfq_number), as_dict=1)
    return quotation
    


@frappe.whitelist()
def send_email_on_po_creation(data, method):

    po_creator = frappe.session.user
    name = data.get('name')
    rfq_number = data.get("rfq_code")
    vendor_code= data.get("purchase_organization")
    vendor_email = frappe.db.get_value("Vendor Master", filters={'name': vendor_code}, fieldname=['office_email_primary'])
    print("********************************************")
    print(po_creator, vendor_email, vendor_code)
    smtp_server = "smtp.transmail.co.in"
    smtp_port = 587
    smtp_user = "emailapikey"  
    smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
    from_address = po_creator
    to_address = vendor_email
    subject = "Test email"
    body = "Purchase Order has been created please check on the VMS Portal for more details .http://localhost:3000/vendor/dashboard/purchase-order?POName=" + str(name)
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



@frappe.whitelist(allow_guest=True)
def check_approval_and_send_mail_on_all_3_approvals(name):
    name = name
    approvals = frappe.db.sql("""
        SELECT purchase_team_approval, purchase_head_approval, accounts_team_approval
        FROM `tabVendor Master`
        WHERE name=%s
    """, (name,), as_dict=False)
    
    
    frappe.logger().debug(f"Approvals fetched for {name}: {approvals}")

    if approvals and len(approvals) > 0 and len(approvals[0]) == 3:
        if (approvals[0][0] == 'Approved' and
            approvals[0][1] == 'Approved' and
            approvals[0][2] == 'Approved'):
            return 1

    return 0




@frappe.whitelist()
def set_vendor_onboarding_status(**kwargs):
    name = kwargs.get("name")
    print(name)
    current_user = frappe.session.user
    print(current_user)
    current_user_designation_key = frappe.db.get_value("User", filters={'email': current_user}, fieldname='designation')

    current_user_designation_name = frappe.db.get_value("Designation Master", filters={'name': current_user_designation_key}, fieldname=['designation_name'])
    #print("*******************************************")
    vendor_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='office_email_primary')
    #print(vendor_email)
    print(current_user_designation_name)
    
    if current_user_designation_name == "Account Team":
        frappe.db.sql(""" UPDATE `tabVendor Master` SET accounts_team_approval='Approved', status='Onboarded' WHERE office_email_primary=%s """,(vendor_email) )
        frappe.db.commit()
        #print("&%^&%^^^^^^^^^^^^^^", current_user)
        frappe.db.sql(""" UPDATE `tabVendor Onboarding` SET accounts_team_approval='Approved', onboarding_form_status='Onboarded' WHERE office_email_primary=%s """,(vendor_email))
        frappe.db.commit()
        print("()()()()((()(()()()())))", "above Count method")
        if  check_approval_and_send_mail_on_all_3_approvals(name) == 1:
            print("()()()()((()(()()()())))", "from Count method")
            sap_fetch_token(name)
            registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')

            smtp_server = "smtp.transmail.co.in"
            smtp_port = 587
            smtp_user = "emailapikey"  
            smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
            from_address = current_user 
            to_address = vendor_email  
            subject = "Test email"
            body = "Your request has been approved Accounts Team ."
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
                    return 200 ,'ok'
            except Exception as e:
                print(f"Failed to send email: {e}")
                return 500


    if current_user_designation_name == "Purchase Team":

        frappe.db.sql(""" UPDATE `tabVendor Master` SET purchase_team_approval='Approved' WHERE name=%s """, (name) )
        frappe.db.commit()
        frappe.db.sql(""" UPDATE `tabVendor Onboarding` SET purchase_team_approval='Approved' WHERE office_email_primary=%s """,(vendor_email))
        frappe.db.commit()
        registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')
        print("****************************",registered_by_email, name)
        print("*****************(*&^%$#$%^&*(*&^%$))")
        smtp_server = "smtp.transmail.co.in"
        smtp_port = 587
        smtp_user = "emailapikey"  
        smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
        from_address = current_user 
        to_address = vendor_email  
        subject = "Test email"
        body = "Your request has been approved Purchase Team ."
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
                return 200 ,'ok' 
        except Exception as e:
            print(f"Failed to send email: {e}")
            return 500

    if current_user_designation_name == "Purchase Head":
        frappe.db.sql(""" UPDATE `tabVendor Master` SET purchase_head_approval='Approved', status='Onboarded' WHERE office_email_primary=%s """,(vendor_email) )
        frappe.db.commit()
        #print("&%^&%^^^^^^^^^^^^^^", current_user)
        frappe.db.sql(""" UPDATE `tabVendor Onboarding` SET purchase_head_approval='Approved', onboarding_form_status='Onboarded' WHERE office_email_primary=%s """,(vendor_email))
        frappe.db.commit()
        print("()()()()((()(()()()())))", "above Count method")

        if  check_approval_and_send_mail_on_all_3_approvals(name) == 1:
            print("()()()()((()(()()()())))", "from Count method")
            sap_fetch_token(name)
            registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')

            smtp_server = "smtp.transmail.co.in"
            smtp_port = 587
            smtp_user = "emailapikey"  
            smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
            from_address = current_user 
            to_address = vendor_email  
            subject = "Test email"
            body = "Your request has been approved Purchase Head ."
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
                    return 200 ,'ok'
            except Exception as e:
                print(f"Failed to send email: {e}")
                return 500
        return 200



@frappe.whitelist()
def create_user(**kwargs):

    email = kwargs.get('email')
    doc = frappe.get_doc({


        'doctype': 'User',
        'enabled': 1,
        'first_name': kwargs.get('first_name'),
        'middle_name': kwargs.get('middle_name'),
        'last_name': kwargs.get('last_name'),
        "designation": "2e0b13974e",
        'email': kwargs.get('email'),
        'username': kwargs.get('username')


        })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    def set_user_role_and_password():
        print("************HI FROM INNER")
        password = "Meril@123"
        url = f'http://localhost:8000/api/resource/User/{email}'
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token 061940ef4019166:2e891e182a05238' 
        }
        data = {
        'new_password': password
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("Password updated successfully")
        else:
            print(f"Failed to update password: {response.status_code}, {response.text}")
    set_user_role_and_password()




    return doc
    
@frappe.whitelist()
def calculate(data, method):
    print("***********Calculated**********************")
    chargable_weight = data.get("chargable_weight")
    ratekg = data.get("ratekg")
    fuel_sur_charge = data.get("fuel_sur_charge")
    sur_charge = data.get("sur_charge")
    xray = data.get("xray")
    pickuporigin = data.get("pickuporigin")
    xrxecom = data.get("xrxecom")
    destination_charges_inr = data.get("destination_charges_inr")
    freight_mode = data.get("freight_mode")
    shipping_line_charges = data.get("shipping_line_charges")
    total_freight = chargable_weight * (ratekg + fuel_sur_charge + sur_charge) + xray + pickuporigin
    ex_works = xray + pickuporigin
    total_freight_inr = total_freight * xrxecom
    frappe.db.sql(""" update `tabImport Entry` set total_freight=%s, ex_works=%s, xrxecom=%s """,(total_freight, ex_works, xrxecom))
    frappe.db.commit()
    if freight_mode == "Air":
        total_landing_priceinr = total_freight_inr + destination_charges_inr
        frappe.db.sql(""" update `tabImport Entry` set total_landing_priceinr=%s """,(total_landing_priceinr))
        frappe.db.commit()
    elif freight_mode == "Ocean":
        total_landing_priceinr = total_freight_inr + destination_charges_inr + shipping_line_charges
        frappe.db.sql(""" update `tabImport Entry` set total_landing_priceinr=%s """,(total_landing_priceinr))
        frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def calculate_export_entry(data, method):
    parent = data.get("parent")
    shipment_mode = data.get("shipment_mode")
    ratekg = int(data.get("ratekg") or 0)
    fuel_surcharge = int(data.get("fuel_surcharge") or 0)
    sc = int(data.get("sc") or 0)
    xray = int(data.get("xray") or 0)
    name = data.get("name")
    other_charges_in_total = int(data.get("other_charges_in_total") or 0)
    chargeable_weight = int(data.get("chargeable_weight") or 0)
    
    total_freight = (ratekg + fuel_surcharge + sc + xray) * chargeable_weight + other_charges_in_total
    #frappe.db.set_value('Quotation',{'name': name},'total_freightinr', total_freight)
    #frappe.db.commit()
    
    #val = frappe.db.sql(""" UPDATE tabQuotation SET total_freightinr=%s WHERE name=%s""", (total_freight, name))
    val = frappe.db.sql(""" UPDATE tabQuotation SET total_freightinr=%s WHERE name=%s""", (total_freight, name))
          
   
    print("*******************", total_freight, name)



# @frappe.whitelist(allow_guest=True)
# def calculate_export_entry(data, method):

#     parent = data.get("parent")
#     shipment_mode = data.get("shipment_mode")
#     ratekg = data.get("ratekg")
#     fuel_surcharge = data.get("fuel_surcharge")
#     sc = data.get("sc")
#     xray = data.get("xray")
#     name = data.get("name")
#     other_charges_in_total = data.get("other_charges_in_total")
#     chargeable_weight = data.get("chargeable_weight")
#     total_freight = (ratekg + fuel_surcharge + sc + xray) * chargeable_weight + other_charges_in_total
#     #total_freight = (ratekg + fuel_surcharge + sc + xray) * chargeable_weight + other_charges_in_total
#     frappe.db.sql(""" update `tabExport Entry Vendor` set total_freight=%s where name=%s""",(total_freight, name))
#     frappe.db.commit()



# @frappe.whitelist(allow_guest=True)
# def compare_quotation(**kwargs):

#     rfq_number = kwargs.get("rfq_number")
#     ordered_list_of_quotations = frappe.db.sql(""" SELECT * FROM `tabQuotation` WHERE rfq_number=%s ORDER BY quote_amount  ASC """, (rfq_number), as_dict=True)

#     for quotation in ordered_list_of_quotations:
        
#         product_code = frappe.db.get_value("Product Master", filters={"name": quotation.product_code}, fieldname="product_code")
        
#         quotation["product_code"] = product_code

#     return ordered_list_of_quotations


# @frappe.whitelist(allow_guest=True)
# def compare_quotation(**kwargs):

#     rfq_number = kwargs.get("rfq_number")
#     orderd_list = frappe.db.sql(""" SELECT * FROM `tabQuotation` WHERE rfq_number = %s AND creation IN (SELECT MAX(creation) FROM `tabQuotation` WHERE rfq_number = %s GROUP BY vendor_code) ORDER BY creation ASC""",(rfq_number, rfq_number), as_dict=True)
#     for quotation in orderd_list:
        
#         product_code = frappe.db.get_value("Product Master", filters={"name": quotation.product_code}, fieldname="product_code")
        
#         quotation["product_code"] = product_code

#     return orderd_list

# @frappe.whitelist(allow_guest=True)
# def show_all_detailed_quotaions():

#     all_quotations = frappe.db.sql(""" SELECT * from `tabQuotations`  """,as_dict=1)



@frappe.whitelist()
def show_vendors_quotation(**kwargs):

    vendor_code = kwargs.get("vendor_code")
    rfq_number = kwargs.get("rfq_number")
    quotation = frappe.db.sql(""" 
        SELECT * FROM `tabQuotation`
        where rfq_number =%s and vendor_code=%s
        AND creation IN (
            SELECT MAX(creation)
            FROM `tabQuotation`
            WHERE rfq_number=%s and vendor_code=%s

            ) 


     """,(rfq_number, vendor_code, rfq_number, vendor_code),as_dict=1)
    quotation = quotation[0]
    product_code = frappe.db.get_value("Product Master", filters={"name": quotation.product_code}, fieldname="product_code")
    quotation["product_code"] = product_code
    company_name = frappe.db.get_value("Company Master", filters={"name": quotation.company_name}, fieldname="company_name")
    quotation["company_name"] = company_name
    product_category_name = frappe.db.get_value("Product Category Master", filters={"name": quotation.product_category}, fieldname="product_category_name")
    quotation["product_category"] = product_category_name
    material_code = frappe.db.get_value("Material Master", filters={"name": quotation.material_code}, fieldname="material_code")
    quotation["material_code"] = material_code
    material_category_name = frappe.db.get_value("Material Category Master", filters={"name": quotation.material_category}, fieldname="material_category_name")
    quotation["material_category"] = material_category_name
    material_name = frappe.db.get_value("Material Master", filters={"name": quotation.material_name}, fieldname="material_name")
    quotation["material_name"] = material_name
    return quotation



# @frappe.whitelist()
# def compare_quotation(**kwargs):

#     rfq_number = kwargs.get("rfq_number")
#     ordered_list = frappe.db.sql(""" 
#         SELECT * FROM `tabQuotation` 
#         WHERE rfq_number = %s 
#         AND creation IN (
#             SELECT MAX(creation) 
#             FROM `tabQuotation` 
#             WHERE rfq_number = %s 
#             GROUP BY vendor_code
#         ) 
#         ORDER BY creation ASC
#     """, (rfq_number, rfq_number), as_dict=True)
    
#     for quotation in ordered_list:
        
#         product_code = frappe.db.get_value("Product Master", filters={"name": quotation.product_code}, fieldname="product_code")
#         quotation["product_code"] = product_code
        
        
#         company_name = frappe.db.get_value("Company Master", filters={"name": quotation.company_name}, fieldname="company_name")
#         quotation["company_name"] = company_name

        
#         product_category_name = frappe.db.get_value("Product Category Master", filters={"name": quotation.product_category}, fieldname="product_category_name")
#         quotation["product_category"] = product_category_name

#         material_code = frappe.db.get_value("Material Master", filters={"name": quotation.material_code}, fieldname="material_code")
#         quotation["material_code"] = material_code

#         material_category_name = frappe.db.get_value("Material Category Master", filters={"name": quotation.material_category}, fieldname="material_category_name")
#         quotation["material_category"] = material_category_name

#         material_name = frappe.db.get_value("Material Master", filters={"name": quotation.material_name}, fieldname="material_name")
#         quotation["material_name"] = material_name


#     return ordered_list

@frappe.whitelist()
def compare_quotation_price(**kwargs):

    rfq_number = kwargs.get("rfq_number")
    ordered_list = frappe.db.sql(""" 
        SELECT * FROM `tabQuotation` 
        WHERE rfq_number = %s 
        AND creation IN (
            SELECT MAX(creation) 
            FROM `tabQuotation` 
            WHERE rfq_number = %s 
            GROUP BY vendor_code
        ) 
        ORDER BY creation ASC
    """, (rfq_number, rfq_number), as_dict=True)
    
    for quotation in ordered_list:
        
        product_code = frappe.db.get_value("Product Master", filters={"name": quotation.product_code}, fieldname="product_code")
        quotation["product_code"] = product_code
        
        
        company_name = frappe.db.get_value("Company Master", filters={"name": quotation.company_name}, fieldname="company_name")
        quotation["company_name"] = company_name

        
        product_category_name = frappe.db.get_value("Product Category Master", filters={"name": quotation.product_category}, fieldname="product_category_name")
        quotation["product_category"] = product_category_name

        material_code = frappe.db.get_value("Material Master", filters={"name": quotation.material_code}, fieldname="material_code")
        quotation["material_code"] = material_code

        material_category_name = frappe.db.get_value("Material Category Master", filters={"name": quotation.material_category}, fieldname="material_category_name")
        quotation["material_category"] = material_category_name

        material_name = frappe.db.get_value("Material Master", filters={"name": quotation.material_name}, fieldname="material_name")
        quotation["material_name"] = material_name


    return ordered_list

@frappe.whitelist()
def compare_quotation_lead_time(**kwargs):

    rfq_number = kwargs.get("rfq_number")
    ordered_list = frappe.db.sql(""" 
    SELECT * FROM `tabQuotation` 
    WHERE rfq_number = %s 
    AND creation IN (
    SELECT MAX(creation) 
    FROM `tabQuotation` 
    WHERE rfq_number = %s 
    GROUP BY vendor_code
) 
ORDER BY (rfq_date::timestamp - delivery_date::timestamp)::interval DESC;
    """, (rfq_number, rfq_number), as_dict=True)

    for quotation in ordered_list:
        
        product_code = frappe.db.get_value("Product Master", filters={"name": quotation.product_code}, fieldname="product_code")
        quotation["product_code"] = product_code
        
        
        company_name = frappe.db.get_value("Company Master", filters={"name": quotation.company_name}, fieldname="company_name")
        quotation["company_name"] = company_name

        
        product_category_name = frappe.db.get_value("Product Category Master", filters={"name": quotation.product_category}, fieldname="product_category_name")
        quotation["product_category"] = product_category_name

        material_code = frappe.db.get_value("Material Master", filters={"name": quotation.material_code}, fieldname="material_code")
        quotation["material_code"] = material_code

        material_category_name = frappe.db.get_value("Material Category Master", filters={"name": quotation.material_category}, fieldname="material_category_name")
        quotation["material_category"] = material_category_name

        material_name = frappe.db.get_value("Material Master", filters={"name": quotation.material_name}, fieldname="material_name")
        quotation["material_name"] = material_name


    return ordered_list





@frappe.whitelist()
def lowest_quoted_price(**kwargs):

    rfq_number = kwargs.get("rfq_number")
    lowest_quoted_price_list = frappe.db.sql(""" SELECT quote_amount FROM `tabQuotation` WHERE rfq_number=%s AND creation IN (SELECT MAX(creation) FROM `tabQuotation` WHERE rfq_number = %s GROUP BY vendor_code) ORDER BY creation ASC """,(rfq_number, rfq_number),as_dict=1)
    
    if lowest_quoted_price_list:
        first_lowest_quoted_price = lowest_quoted_price_list[0]
        return first_lowest_quoted_price
    else:
        return {}




# @frappe.whitelist(allow_guest=True)
# def lowest_quoted_price(**kwargs):

#     rfq_number = kwargs.get("rfq_number")
#     lowest_quoted_price = frappe.db.sql(""" SELECT * FROM `tabQuotation` WHERE rfq_number=%s AND creation IN (SELECT MAX(creation) FROM `tabQuotation` WHERE rfq_number = %s GROUP BY vendor_code) ORDER BY creation ASC """,(rfq_number, rfq_number),as_dict=1)
#     return lowest_quoted_price[0]



#RFQ/MIPL/####


@frappe.whitelist()
def test_method(self, method):
    if self.file_name:
        file_doc = frappe.get_doc("File", {"file_url": self.file_name})
        frappe.msgprint(f"File URL: {file_doc.file_url}")
            


@frappe.whitelist()
def test_method(self, method):
    if self.file_name:
       
        file_path = frappe.get_site_path(self.file_name.lstrip("/"))

    
        if os.path.exists(file_path):
            frappe.msgprint("File exists.")
        else:
            frappe.msgprint("File does not exist.")

        
        file_doc = frappe.get_doc("File", {"file_url": self.file_name})
        frappe.msgprint(f"File URL: {file_doc.file_url}")



@frappe.whitelist()
def total_vendors():
    total_vendors = frappe.db.sql(""" select count(*) from `tabVendor Master` """,as_dict=1)
    return total_vendors

@frappe.whitelist()
def total_in_process_vendors():

    total_in_process_vendors = frappe.db.sql(""" select count(*) from `tabVendor Master` where status='In Process' """,as_dict=1)
    return total_in_process_vendors

@frappe.whitelist()
def inprocess_vendor_detail():
    total_in_process_vendors = frappe.db.sql(""" select * from `tabVendor Master` where status='In Process' """,as_dict=1)
    return total_in_process_vendors




@frappe.whitelist()
def total_onboarded_vendors():

    total_in_process_vendors = frappe.db.sql(""" select count(*) from `tabVendor Master` where status='Onboarded' """,as_dict=1)
    return total_in_process_vendors


@frappe.whitelist()
def total_rfq():

    total_rfq = frappe.db.sql(""" select count(*) from `tabRequest For Quotation` """, as_dict=1)
    return total_rfq
@frappe.whitelist()
def total_number_of_quotation():

    count = frappe.db.sql(""" select count(*) from `tabQuotation` """,as_dict=1)
    return count


@frappe.whitelist()
def total_vendors_registerd_in_month():

    current_month = datetime.now.strftime("%B")
    current_year = datetime.now.year
    return current_month, current_year

@frappe.whitelist()
def all_rfq_detail():

    all_rfq = frappe.db.sql("""  SELECT 
            rfq.name, 
            rfq.rfq_date, 
            rfq.required_by, 
            mm.material_name, 
            rfq.quantity 
        FROM 
            `tabRequest For Quotation` rfq
        INNER JOIN 
            `tabMaterial Master` mm ON rfq.material = mm.name """,as_dict=1)
    return all_rfq

#####ISKO UNCOMMENT KARNA HAI ******************************************************************************
# @frappe.whitelist()
# def main_function(data, method):
#     #time.sleep(3)
#     print("*****************************Hi From Main**************************************")
#     name = data.get("name")
#     file = frappe.db.sql(""" select file_name from `tabImport Entry` where name=%s """,(name))
#     print(file)
#     with fitz.open(file) as doc:
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         print(text)

# @frappe.whitelist()
# def extract_text_from_pdf(data, method):
#     pdf_path = data.get("file_name")
#     #pdf_path = frappe.request.files.get("file_name")
    
#     with fitz.open(pdf_path) as doc:
#         text = ""
#         for page in doc:
#             text += page.get_text()
   

#     lines = text.split('\n')
#     resume_dict = {}

#     current_section = None
#     for line in lines:
#         if line.strip() == "":
#             continue
#         if ":" in line:
#             key, value = line.split(':', 1)
#             key = key.strip()
#             value = value.strip()
           
#             if current_section is not None:
               
#                 if current_section not in resume_dict or isinstance(resume_dict[current_section], list):
#                     resume_dict[current_section] = {}
#                 resume_dict[current_section][key] = value
#             else:
#                 resume_dict[key] = value
#         else:
           
#             if current_section is None or isinstance(resume_dict.get(current_section, None), dict):
#                 current_section = line.strip()
              
#                 if current_section in resume_dict and isinstance(resume_dict[current_section], list):
#                     continue
#                 else:
#                     resume_dict[current_section] = []  
#             else:
#                 resume_dict[current_section].append(line.strip())
   
#     text = extract_text_from_pdf(pdf_path)
#     resume_dict = parse_resume_text(text)
#     for key, value in resume_dict.items():
#         if isinstance(value, dict):
#             print(f"{key}:")
#         for sub_key, sub_value in value.items():
#             print(f"  {sub_key}: {sub_value}")
#         if isinstance(value, list):
#             print(f"{key}:")
#         for item in value:
#             print(f"  - {item}")
#     else:
#         print(f"{key}: {value}")
#     print()  
#     print(type(resume_dict))


# scheduler = sched.scheduler(time.time, time.sleep)

# @frappe.whitelist(allow_guest=True)
# def cron_method():

#     print("********************************")
#     print("Hi from Scheduler")



# def periodic_task(sc):
#     cron_method()  
#     scheduler.enter(1, 1, periodic_task, (sc,))  


# scheduler.enter(1, 1, periodic_task, (scheduler,))
# scheduler.run()

@frappe.whitelist()
def show_rca_detail(**kwargs):
    name = kwargs.get("name")
    
    if name:
        values = frappe.db.sql("""
            SELECT rca.*, agm.account_group_name
            FROM `tabReconciliation Account` AS rca
            LEFT JOIN `tabAccount Group Master` AS agm ON rca.account_group = agm.name
            WHERE rca.name = %s
        """, (name), as_dict=1)
        
        if values:
            return values[0]  # Return the first result if found
        else:
            return None  # Handle the case where no result is found for the given name
    else:
        values = frappe.db.sql("""
            SELECT rca.*, agm.account_group_name
            FROM `tabReconciliation Account` AS rca
            LEFT JOIN `tabAccount Group Master` AS agm ON rca.account_group = agm.name
        """, as_dict=1)
        
        return values


@frappe.whitelist(allow_guest=True)
def get_po():
    try:
        data = frappe.request.get_json()
        if data and "items" in data:
            
            first_item = data["items"][0]
            
            po_no = first_item.get("EBELN", "")
            supplier_name = first_item.get("VENDNAME", "")
            material_code = first_item.get("MATNR", "")
            delivery_date = first_item.get("EINDT", "")
            product_category = first_item.get("PSTYP", "")
            total_input_cgst = first_item.get("CGST", "")
            total_input_sgst = first_item.get("SGST", "")
            vendor_code = first_item.get("LIFNR", "")
            purchase_organization = first_item.get("EKORG", "")
            currency = first_item.get("WAERS", "")
            plant = first_item.get("RESWK", "")
            company_code = first_item.get("BUKRS", "")
            short_text = first_item.get("TXZ01", "")
            country = first_item.get("LANDX", "")
            material_category = first_item.get("ATTYP", "")
            purchase_requisition_number == first_item.get("BANFN", "")
            purchase_group = first_item.get("EKGRP", "")
            total_gross_amount = first_item.get("GROSS_AMT", "")
            collection_number = first_item.get("SUBMI", "")
            
            purchase_order_doc = frappe.new_doc("Purchase Order")
            purchase_order_doc.po_number = po_no
            purchase_order_doc.supplier = supplier_name
            purchase_order_doc.material_code = material_code
            purchase_order_doc.delivery_date = delivery_date
            purchase_order_doc.product_category = product_category
            purchase_order_doc.total_input_cgst = total_input_cgst
            purchase_order_doc.total_input_sgst = total_input_sgst
            purchase_order_doc.vendor_code = vendor_code
            purchase_organization = purchase_organization
            currency = currency
            plant = plant
            company_code = company_code
            short_text = short_text
            country = country
            material_category = material_category
            purchase_requisition_number = purchase_requisition_number
            purchase_group = purchase_group
            total_gross_amount = total_gross_amount
            collection_number = collection_number


            
            for item in data["items"]:
                table_jsfj = purchase_order_doc.append("table_jsfj", {})
                table_jsfj.product_code = item.get("EBELP", "")
                table_jsfj.price = item.get("NET_AMT", "")
                table_jsfj.hsnsac = item.get("J_1BNBM", "")
                table_jsfj.uom = item.get("BSTME", "")
            
            purchase_order_doc.insert()
            purchase_order_doc.save()

            return "Purchase Order Created Successfully."
        else:
            return "No valid data received or 'items' key not found."
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_po Error")
        return {"status": "error", "message": str(e)}








#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$WORKING CODE CLOSED&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


# @frappe.whitelist(allow_guest=True)
# def get_pr():
#     try:
#         data = frappe.request.get_json()
#         if data and "items" in data:

#             first_item = data["items"][0]
            
#             pr_no = data.get("pr_no", "")
            
#             pr_doc = frappe.new_doc("Purchase Requisition")
#             pr_doc.purchase_requisition_number = pr_no
#             pr_doc.pr_items = []

#             for item in data["items"]:
#                 pr_item = pr_doc.append("pr_items", {})
#                 pr_item.item_code = item.get("BNFPO", "")
#                 pr_item.item_category = item.get("EPSTP", "")
#                 pr_item.material = item.get("MATNR", "")
#                 pr_item.short_text = item.get("TXZ01",)
#                 pr_item.quantity_requested = item.get("MENGE", "")
#                 pr_item.unit = item.get("MEINS", "")
#                 pr_item.plant = item.get("WERKS", "")
#                 pr_item.requisitioner = item.get("AFNAM", "")
#                 pr_item.delivery_date = item.get("EEIND", "")
#                 pr_item.requisition_date = item.get("BADAT", "")
#                 pr_item.document_type = item.get("BSART", "")
#                 pr_item.release_date = item.get("FRGDT", "")
#                 pr_item.valuation = item.get("PREIS", "")
#                 pr_item.price_unit = item.get("PEINH", "")
#                 pr_item.total_value = item.get("GSWRT", "")
#                 pr_item.currency = item.get("WAERS", "")
#                 pr_item.planned_delivery_date = item.get("PLIFZ", "")
#                 pr_item.delivery_date_fromto = item.get("LFDAT", "")
#                 pr_item.period_ind_for = item.get("IPRKZ", "")
#                 pr_item.goods_receipt = item.get("WEPOS", "")
#                 pr_item.gr_non_valuated = item.get("WEUNB", "")
#                 pr_item.invoice = data.get("REPOS", "")
#                 pr_item.mrp = data.get("DISPO", "")
#                 pr_item.storage_location = data.get("LGORT", "")
#                 pr_item.expected_delivery_date = data.get("BEDNR", "")
#                 pr_item.desired_vendor = data.get("LIFNR", "")
#                 pr_item.fixed_vendor = data.get("FLIEF", "")
#                 pr_item.supplying_plant = data.get("RESWK", "")
#                 pr_item.purchase_organization = data.get("EKORG", "")
#                 pr_item.outlet_agreement = data.get("KONNR", "")
#                 pr_item.principal = data.get("KTPNR", "")
#                 pr_item.purchasing_information_rec = data.get("INFNR", "")
#                 pr_item.mpn_material = data.get("EMATN", "")
#                 pr_item.material_group = data.get("MATKL", "")
#                 pr_item.po_date = data.get("BEDAT", "")
#                 pr_item.purchase_number = data.get("EBELN", "")
#                 pr_item.value_price = data.get("PREIS", "")
#                 pr_item.pr_change_date = data.get("ERDAT", "")
#                 pr_item.account_assign_category = data.get("KNTTP", "")


#             pr_doc.insert()
#             pr_doc.save()

#             return "Purchase Requisition Created Successfully."
#         else:
#             return "No valid data received or 'items' key not found."
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "create_purchase_requisition Error")
#         return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_pr():
    try:
        data = frappe.request.get_json()
        if data and "items" in data:
            pr_no = data.get("pr_no", "")
            
            pr_doc = frappe.new_doc("Purchase Requisition")
            pr_doc.purchase_requisition_number = pr_no
            pr_doc.pr_items = []

            for item in data["items"]:
                pr_item = pr_doc.append("pr_items", {
                    "item_code": item.get("BNFPO", ""),
                    "item_category": item.get("EPSTP", ""),
                    "material": item.get("MATNR", ""),
                    "short_text": item.get("TXZ01", ""),
                    "quantity_requested": item.get("MENGE", ""),
                    "unit": item.get("MEINS", ""),
                    "plant": item.get("WERKS", ""),
                    "requisitioner": item.get("AFNAM", ""),
                    "delivery_date": parse_date(item.get("EEIND", "")),
                    "requisition_date": parse_date(item.get("BADAT", "")),
                    "document_type": item.get("BSART", ""),
                    "release_date": parse_date(item.get("FRGDT", "")),
                    "valuation": item.get("PREIS", ""),
                    "price_unit": item.get("PEINH", ""),
                    "total_value": item.get("GSWRT", ""),
                    "currency": item.get("WAERS", ""),
                    "planned_delivery_date": parse_date(item.get("PLIFZ", "")),
                    "delivery_date_fromto": parse_date(item.get("LFDAT", "")),
                    "period_ind_for": item.get("IPRKZ", ""),
                    "goods_receipt": item.get("WEPOS", ""),
                    "gr_non_valuated": item.get("WEUNB", ""),
                    "invoice": item.get("REPOS", ""),
                    "mrp": item.get("DISPO", ""),
                    "storage_location": item.get("LGORT", ""),
                    "expected_delivery_date": parse_date(item.get("BEDNR", "")),
                    "desired_vendor": item.get("LIFNR", ""),
                    "fixed_vendor": item.get("FLIEF", ""),
                    "supplying_plant": item.get("RESWK", ""),
                    "purchase_organization": item.get("EKORG", ""),
                    "outlet_agreement": item.get("KONNR", ""),
                    "principal": item.get("KTPNR", ""),
                    "purchasing_information_rec": item.get("INFNR", ""),
                    "mpn_material": item.get("EMATN", ""),
                    "material_group": item.get("MATKL", ""),
                    "po_date": parse_date(item.get("BEDAT", "")),
                    "purchase_number": item.get("EBELN", ""),
                    "value_price": item.get("PREIS", ""),
                    "pr_change_date": parse_date(item.get("ERDAT", "")),
                    "account_assign_category": item.get("KNTTP", "")
                })

            pr_doc.insert()
            pr_doc.save()

            return "Purchase Requisition Created Successfully."
        else:
            return "No valid data received or 'items' key not found."
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_purchase_requisition Error")
        return {"status": "error", "message": str(e)}

def parse_date(date_str):
    if isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            frappe.log_error(frappe.get_traceback(), f"Invalid date format: {date_str}")
    return None




# @frappe.whitelist(allow_guest=True)
# def show_all_vendors():

#     all_vendors = frappe.db.sql(""" SELECT
#     vm.name AS name,
#     status AS status,
#     purchase_team_approval AS purchase_team_approval,
#     purchase_head_approval AS purchase_head_approval,
#     accounts_team_approval AS accounts_team_approval,
#     office_email_primary AS office_email_primary,
#     vendor_name AS vendor_name,
#     cm.company_name AS company_name 
    
# FROM 
#     `tabVendor Master` vm 
# LEFT JOIN 
#     `tabCompany Master` cm ON vm.company_name = cm.name 


# """, as_dict=1)

#     return all_vendors

# Descending order change
@frappe.whitelist(allow_guest=True)
def show_all_vendors():
    all_vendors = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.status AS status,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.office_email_primary AS office_email_primary,
            vm.vendor_name AS vendor_name,
            cm.company_name AS company_name
        FROM 
            `tabVendor Master` vm 
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name
        ORDER BY 
            vm.creation DESC, vm.modified DESC
    """, as_dict=1)

    return all_vendors

@frappe.whitelist(allow_guest=True)
def show_all_vendors_current_month():
    current_month_start = datetime.now().strftime('%Y-%m-01 00:00:00')
    current_month_end = datetime.now().strftime('%Y-%m-%d 23:59:59')

    all_vendors = frappe.db.sql(f"""
        SELECT
            vm.name AS name,
            status AS status,
            purchase_team_approval AS purchase_team_approval,
            purchase_head_approval AS purchase_head_approval,
            accounts_team_approval AS accounts_team_approval,
            office_email_primary AS office_email_primary,
            vendor_name AS vendor_name,
            cm.company_name AS company_name,
            vm.creation AS creation
        FROM 
            `tabVendor Master` vm 
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name
        WHERE
            vm.creation BETWEEN '{current_month_start}' AND '{current_month_end}'
    """, as_dict=1)

    return all_vendors


# @frappe.whitelist()
# def show_detailed_quotation(name):

#     quotation = frappe.db.sql(""" 


#         SELECT
#         rfq.name AS name,
#         co.company_name AS company_name,
#         vm.name AS name,
#         qo.rfq_date AS rfq_date,
#         qo.quotation_deadline AS quotation_deadline,
#         qo.delivery_date AS delivery_date,
#         qo.vendor_name AS vendor_name,
#         qo.vendor_contact AS vendor_contact,
#         qo.contact_person AS contact_person,
#         qo.quote_amount AS quote_amount,
#         qo.contact_email AS contact_email,
#         pm.product_code AS product_code,
#         pc.product_category_name AS product_category_name,
#         mm.material_code AS material_code,
#         mcm.material_category_name AS material_category_name,
#         m.material_name AS material_name,
#         qo.rfq_quantity AS rfq_quantity,
#         qo.storage_location AS storage_location,
#         qo.remark AS remark,
#         qo.status AS status,
#         qo.rfq_number AS rfq_number,
#         qo.shipment_mode AS shipment_mode,
#         qo.airlinevessel_name AS airlinevessel_name,
#         qo.chargeable_weight AS chargeable_weight,
#         qo.ratekg AS ratekg,
#         qo.fuel_surcharge AS fuel_surcharge,
#         qo.sc AS sc,
#         qo.xray AS xray,
#         qo.pickuporigin AS pickuporigin,
#         qo.ex_works AS ex_works,
#         qo.transit_days AS transit_days,
#         qo.total_freight,
#         qo.exchange_rate AS exchange_rate,
#         qo.total_freightinr AS total_freightinr,
#         qo.destination_charge AS destination_charge,
#         qo.shipping_line_charge AS shipping_line_charge,
#         qo.cfs_charge AS cfs_charge,
#         qo.total_landing_price AS total_landing_price,
#         qo.remarks AS remarks,
#         frmcr.currency_name AS from_currency_name,
#         tocr.currency_name AS to_currency_name



#         FROM
#         tabQuotation qo
#         LEFT JOIN
#         tabRequest For Quotation rfq ON qo.rfq_number = rfq.name
#         LEFT JOIN
#         tabCompany Master co ON qo.company_name = co.name
#         LEFT JOIN
#         tabVendor Master vm ON qo.vendor_code = vm.name
#         LEFT JOIN
#         tabProduct Master pm ON qo.product_code = pm.name
#         LEFT JOIN
#         tabProduct Category Master pc ON qo.product_category = pc.name
#         LEFT JOIN
#         tabMaterial Master mm ON qo.material_code = mm.name
#         LEFT JOIN
#         tabMaterial Category Master mcm ON qo.material_category = mcm.name
#         LEFT JOIN
#         tabMaterial Master m ON qo.material_name = m.name
#         LEFT JOIN
#         tabCurrency Master frmcr ON qo.from_currency = frmcr.name
#         LEFT JOIN
#         tabCurrency Master tocr ON qo.to_currency = tocr.name

#         where qo.name=%s

#      """,(name),as_dict=1)
#     return quotation

@frappe.whitelist()
def show_detailed_quotation(name):

    quotation = frappe.db.sql(""" 


        SELECT
        rfq.name AS name,
        co.company_name AS company_name,
        vm.name AS name,
        qo.rfq_date AS rfq_date,
        qo.quotation_deadline AS quotation_deadline,
        qo.delivery_date AS delivery_date,
        qo.vendor_name AS vendor_name,
        qo.vendor_contact AS vendor_contact,
        qo.contact_person AS contact_person,
        qo.quote_amount AS quote_amount,
        qo.contact_email AS contact_email,
        pm.product_code AS product_code,
        pc.product_category_name AS product_category_name,
        mm.material_code AS material_code,
        mcm.material_category_name AS material_category_name,
        m.material_name AS material_name,
        qo.rfq_quantity AS rfq_quantity,
        qo.storage_location AS storage_location,
        qo.remark AS remark,
        qo.status AS status,
        qo.rfq_number AS rfq_number,
        qo.shipment_mode AS shipment_mode,
        qo.airlinevessel_name AS airlinevessel_name,
        qo.chargeable_weight AS chargeable_weight,
        qo.ratekg AS ratekg,
        qo.fuel_surcharge AS fuel_surcharge,
        qo.sc AS sc,
        qo.xray AS xray,
        qo.pickuporigin AS pickuporigin,
        qo.ex_works AS ex_works,
        qo.transit_days AS transit_days,
        qo.total_freight,
        qo.exchange_rate AS exchange_rate,
        qo.total_freightinr AS total_freightinr,
        qo.destination_charge AS destination_charge,
        qo.shipping_line_charge AS shipping_line_charge,
        qo.cfs_charge AS cfs_charge,
        qo.total_landing_price AS total_landing_price,
        qo.remarks AS remarks,
        frmcr.currency_name AS from_currency_name,
        tocr.currency_name AS to_currency_name


        FROM
        `tabQuotation` qo
        LEFT JOIN
        `tabRequest For Quotation` rfq ON qo.rfq_number = rfq.name
        LEFT JOIN
        `tabCompany Master` co ON qo.company_name = co.name
        LEFT JOIN
        `tabVendor Master` vm ON qo.vendor_code = vm.name
        LEFT JOIN
        `tabProduct Master` pm ON qo.product_code = pm.name
        LEFT JOIN
        `tabProduct Category Master` pc ON qo.product_category = pc.name
        LEFT JOIN
        `tabMaterial Master` mm ON qo.material_code = mm.name
        LEFT JOIN
        `tabMaterial Category Master` mcm ON qo.material_category = mcm.name
        LEFT JOIN
        `tabMaterial Master` m ON qo.material_name = m.name
        LEFT JOIN
        `tabCurrency Master` frmcr ON qo.from_currency = frmcr.name
        LEFT JOIN
        `tabCurrency Master` tocr ON qo.to_currency = tocr.name

        where qo.name=%s

     """,(name),as_dict=1)
    return quotation



# @frappe.whitelist()
# def show_detailed_quotation(name):

#     quotation = frappe.db.sql(""" 


#         SELECT
#         rfq.name AS name,
#         co.company_name AS company_name,
#         vm.name AS name,
#         qo.rfq_date AS rfq_date,
#         qo.quotation_deadline AS quotation_deadline,
#         qo.delivery_date AS delivery_date,
#         qo.vendor_name AS vendor_name,
#         qo.vendor_contact AS vendor_contact,
#         qo.contact_person AS contact_person,
#         qo.quote_amount AS quote_amount,
#         qo.contact_email AS contact_email,
#         pm.product_code AS product_code,
#         pc.product_category_name AS product_category_name,
#         mm.material_code AS material_code,
#         mcm.material_category_name AS material_category_name,
#         m.material_name AS material_name,
#         qo.rfq_quantity AS rfq_quantity,
#         qo.storage_location AS storage_location,
#         qo.remark AS remark,
#         qo.status AS status,
#         qo.rfq_number AS rfq_number
                              

#         FROM
#         `tabQuotation` qo
#         LEFT JOIN
#         `tabRequest For Quotation` rfq ON qo.rfq_number = rfq.name
#         LEFT JOIN
#         `tabCompany Master` co ON qo.company_name = co.name
#         LEFT JOIN
#         `tabVendor Master` vm ON qo.vendor_code = vm.name
#         LEFT JOIN
#         `tabProduct Master` pm ON qo.product_code = pm.name
#         LEFT JOIN
#         `tabProduct Category Master` pc ON qo.product_category = pc.name
#         LEFT JOIN
#         `tabMaterial Master` mm ON qo.material_code = mm.name
#         LEFT JOIN
#         `tabMaterial Category Master` mcm ON qo.material_category = mcm.name
#         LEFT JOIN
#         `tabMaterial Master` m ON qo.material_name = m.name

#         where qo.name=%s

#      """,(name),as_dict=1)
#     return quotation


# @frappe.whitelist(allow_guest=True)
# def show_me(name):
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name
#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabCompany Master` cm ON vm.company_name = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         WHERE 
#             vm.name=%s
#     """, (name,), as_dict=1)

#     return vendor

@frappe.whitelist()
def import_entry_detail(name):

    entry = frappe.db.sql("""

        SELECT
            ie.rfq_number AS rfq_number,
            ie.rfq_date AS rfq_date,
            vm3.vendor_name AS vendor_name,
            ie.ff_ref_number AS fff_ref_number,
            ie.freight_mode AS freight_mode,
            cnt.country_name AS country_name,
            pt.port_name AS port_name,
            pt2.port_code AS port_code,
            inc.incoterm_name AS incoterm_name,
            ie.meril_invoice_number As meril_invoice_number,
            ie.invoice_date AS invoice_date,
            ie.shipper_name AS shipper_name,
            ie.package_type AS package_type,
            ie.pkg_units AS pkg_units,
            pct.product_category_name AS product_category_name,
            ie.vol_weight AS vol_weight,
            ie.actual_weight AS actual_weight,
            ie.shipment_date_meril AS shipment_date_meril,
            ie.statutory_permission AS statutory_permission,
            ie.shipment_mode AS shipment_mode,
            ie.name1 AS name1,
            ie.chargable_weight AS chargable_weight,
            ie.ratekg AS ratekg,
            ie.fuel_sur_charge AS fuel_sur_charge,
            ie.sur_charge AS sur_charge,
            ie.xray AS xray,
            ie.pickuporigin AS pickuporigin,
            ie.ex_works AS ex_works,
            ie.total_freight AS total_freight,
            cur.currency_name AS currency_name,
            cur2.currency_name AS currency_name,
            ie.xrxecom AS xrxecom,
            ie.total_freight_inr AS total_freight_inr,
            ie.destination_charges_inr AS destination_charges_inr,
            ie.shipping_line_charges AS shipping_line_charges,
            ie.cfs_charges AS cfs_charges,
            ie.total_landing_priceinr,
            ie.remarks AS remarks


            

            FROM
            `tabImport Entry` ie
            LEFT JOIN
            `tabVendor Master` vm3 ON ie.freight_forwarder = vm3.name
            LEFT JOIN
            `tabCountry Master` cnt ON ie.origin_country = cnt.name
            LEFT JOIN
            `tabPort Master` pt ON ie.destination_port = pt.name
            LEFT JOIN
            `tabPort Master` pt2 ON ie.port_code = pt2.name
            LEFT JOIN
            `tabIncoterm Master` inc ON ie.freight_basis = inc.name
            LEFT JOIN
            `tabProduct Category Master` pct ON ie.product_category = pct.name
            LEFT JOIN
            `tabCurrency Master` cur ON ie.from_currency = cur.name
            LEFT JOIN
            `tabCurrency Master` cur2 ON ie.to_currency = cur2.name


            WHERE ie.name=%s


     """,(name), as_dict=1)

    return entry

@frappe.whitelist()
def approve_quotation(name):

    rfq_number = frappe.db.get_value('Quotation', filters={'name': name}, fieldname='rfq_number')

    if rfq_number:

        frappe.db.sql("""UPDATE `tabQuotation`
                        SET `status` = 'Rejected'
                        WHERE `rfq_number` = %s
                        AND `name` != %s""",
                      (rfq_number, name))
        frappe.db.sql("""UPDATE `tabRequest For Quotation`
                        SET `status` = 'Closed'
                        WHERE `name` = %s""",
                      (rfq_number,))


        frappe.db.set_value('Quotation', name, 'status', 'Approved')

        frappe.db.commit()
        vendor_name = frappe.db.get_value("Quotation", filters={'name': name}, fieldname=['vendor_code'])
        naammee = frappe.db.get_value("Vendor Master", filters={'vendor_code'}, fieldname=['name'])
        reciever_email = frappe.db.get_value("Vendor Master",filters={'name': vendor_name}, fieldname='office_email_primary')
        sender_address = "noreply@merillife.com" 
        smtp_server = "smtp.transmail.co.in"
        smtp_port = 587
        smtp_user = "emailapikey"  
        smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
        from_address = sender_address 
        to_address = reciever_email
        subject = "Quoatation Approval"
        body = "Congratulations Your Quotation Has been Approved By Meril"
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        print("*********",from_address, to_address,subject,body)
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(smtp_user, smtp_password)  
                server.sendmail(from_address, to_address, msg.as_string()) 
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
        # print("*****vendorname and email*****",vendor_name,reciever_email, naammee)
        # obj.send_email(reciever_email, sender_address, subject, body)
        return "Quotation approved successfully and others rejected"
    else:
        return "RFQ number not found for the quotation"

        
# @frappe.whitelist(allow_guest=True)
# def import_entry_detail(name):

#     entry = frappe.db.sql(""" 

#         SELECT

#         ee.rfq_cutoff_date_time AS rfq_cutoff_date_time,
        



#      """,(name),as_dict=1)




# @frappe.whitelist()
# def show_me(name):
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             vm.payee_in_document AS payee_in_document,
#             vm.check_double_invoice AS check_double_invoice,
#             vm.gr_based_inv_ver AS gr_based_inv_ver,
#             vm.service_based_inv_ver AS service_based_inv_ver,
#             curn.currency_name AS order_currency,
#             term.terms_of_payment_name AS terms_of_payment,
#             incoterm.incoterm_name AS incoterms,
#             purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name




#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.country_name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#         LEFT JOIN
#             `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         LEFT JOIN
#             `tabCurrency Master` curn ON vm.order_currency = curn.name
#         LEFT JOIN
#             `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
#         LEFT JOIN
#             `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
#         LEFT JOIN
#             `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)




#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     dic = {
#         "id": email 
#     }

#     val = vendor + [dic]

#     return val


# @frappe.whitelist()
# def show_me(name):
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             crtc.certificate_code AS certificate_code,
#             vm.valid_till AS valid_till,
#             vm.payee_in_document AS payee_in_document,
#             vm.check_double_invoice AS check_double_invoice,
#             vm.gr_based_inv_ver AS gr_based_inv_ver,
#             vm.service_based_inv_ver AS service_based_inv_ver,
#             curn.currency_name AS order_currency,
#             term.terms_of_payment_name AS terms_of_payment,
#             incoterm.incoterm_name AS incoterms,
#             purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name
#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#         LEFT JOIN
#             `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         LEFT JOIN
#             `tabCertificate Master` crtc ON vm.certificate_code = crtc.name
#         LEFT JOIN
#             `tabCurrency Master` curn ON vm.order_currency = curn.name
#         LEFT JOIN
#             `tabTerms Of Payment Master` term ON cm.terms_of_payment = term.name
#         LEFT JOIN
#             `tabIncoterm Master` incoterm ON cm.Incoterms = incoterm.name
#         LEFT JOIN
#             `tabPurchase Group Master` purchase ON cm.purchase_groupm = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)

#     primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
#     banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """,(primary_key), as_dict=1)
#     supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """,(primary_key), as_dict=1)
#     number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """,(primary_key), as_dict=1)
#     machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """,(primary_key), as_dict=1)
#     testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """,(primary_key), as_dict=1)
#     reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """,(primary_key), as_dict=1)

#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
    
#     response = {
#         "vendor_details": vendor,
#         "banker_details": banker_details,
#         "supplied_items": supplied,
#         "number_of_employees": number_of_employees,
#         "machinery_details": machinery_detail,
#         "testing_facilities": testing_facility,
#         "reputed_partners": reputed_partners,
#         "extra_info": {
#             "id": email
#         }
#     }

#     return response


# @frappe.whitelist()
# def show_me(name):
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             --vm.payee_in_document AS payee_in_document,
#             --vm.check_double_invoice AS check_double_invoice,
#             --vm.gr_based_inv_ver AS gr_based_inv_ver,
#             --vm.service_based_inv_ver AS service_based_inv_ver,
#             --curn.currency_name AS order_currency,
#             --term.terms_of_payment_name AS terms_of_payment,
#             --incoterm.incoterm_name AS incoterms,
#             --purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name
#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#         LEFT JOIN
#             `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         --LEFT JOIN
#           --  `tabCurrency Master` curn ON vm.order_currency = curn.name
#         --LEFT JOIN
#          --   `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
#         --LEFT JOIN
#          --   `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
#         --LEFT JOIN
#          --   `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)

#     primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
#     banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """, (primary_key), as_dict=1)
#     supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """, (primary_key), as_dict=1)
#     number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """, (primary_key), as_dict=1)
#     machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """, (primary_key), as_dict=1)
#     testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """, (primary_key), as_dict=1)
#     reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """, (primary_key), as_dict=1)

#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     ordercurrency = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['order_currency']) #add
#     currency_name = frappe.db.get_value("Currency Master", filters={'name': ordercurrency}, fieldname=['currency_name'])
#     term_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['terms_of_payment'])
#     term_name = frappe.db.get_value("Terms Of Payment Master", filters={'name': term_id}, fieldname=['terms_of_payment_name']) #add
#     inco_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['incoterms'])
#     inco_name = frappe.db.get_value("Incoterm Master", filters={'name': inco_id}, fieldname=['incoterm_name']) #add
#     payee = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['payee']) #add
#     gr_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['gr_based_inv_ver']) #add
#     service_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['service_based_inv_ver']) #add
#     check_double_invoice = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['check_double_invoice']) #add
#     purchase_group_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_groupm'])
#     purchase_group_name = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_group_id}, fieldname=['purchase_group_name']) #add
#     account_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
#     account_name = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['account_group_name']) #add
#     purchase_org_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_organization'])
#     pruchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name': purchase_org_id}, fieldname=['purchase_organization_name']) #add
#     company_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
#     company_name = frappe.db.get_value("Company Master", filters={'name': company_id}, fieldname=['company_name']) #add

#     extra_details = {
#     "order_currency": ordercurrency,
#     "terms_of_payment_name": term_name,
#     "incoterm_name": inco_name,
#     "payee": payee,
#     "gr_based_inv_ver": gr_based_inv_ver,
#     "service_based_inv_ver": service_based_inv_ver,
#     "check_double_invoice": check_double_invoice,
#     "purchase_group_name": purchase_group_name,
#     "account_group": account_name,
#     "purchase_organization": pruchase_org_name,
#     "company_name": company_name
# }

#     print("###################################", purchase_group_name)

    
#     response = {
#         "vendor_details": vendor,
#         "banker_details": banker_details,
#         "supplied_items": supplied,
#         "number_of_employees": number_of_employees,
#         "machinery_details": machinery_detail,
#         "testing_facilities": testing_facility,
#         "reputed_partners": reputed_partners,
#         "extra_details": extra_details,
#         "extra_info": {
#             "id": email
#         }
#     }

#     return response

# @frappe.whitelist()
# def show_me(**kwargs):
#     name = kwargs.get('name')
    
    
#     record_exists = frappe.db.exists("Vendor Onboarding", {'office_email_primary': name})
#     if not record_exists:
#         return {"message": "Record does not exist"}
    
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             --cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             --vm.payee_in_document AS payee_in_document,
#             --vm.check_double_invoice AS check_double_invoice,
#             --vm.gr_based_inv_ver AS gr_based_inv_ver,
#             --vm.service_based_inv_ver AS service_based_inv_ver,
#             --curn.currency_name AS order_currency,
#             --term.terms_of_payment_name AS terms_of_payment,
#             --incoterm.incoterm_name AS incoterms,
#             --purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name
#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#        -- LEFT JOIN
#        --     `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         --LEFT JOIN
#           --  `tabCurrency Master` curn ON vm.order_currency = curn.name
#         --LEFT JOIN
#          --   `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
#         --LEFT JOIN
#          --   `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
#         --LEFT JOIN
#          --   `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)

#     primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
#     banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """, (primary_key), as_dict=1)
#     supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """, (primary_key), as_dict=1)
#     number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """, (primary_key), as_dict=1)
#     machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """, (primary_key), as_dict=1)
#     testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """, (primary_key), as_dict=1)
#     reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """, (primary_key), as_dict=1)

#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     ordercurrency = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['order_currency'])
#     print("%%%%%%%%%%%%%%%%%((((((((((((((()))))))))))))))",ordercurrency) #add
#     currency_namee = frappe.db.get_value("Currency Master", filters={'name': ordercurrency}, fieldname=['currency_name'])
#     term_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['terms_of_payment'])
#     term_name = frappe.db.get_value("Terms Of Payment Master", filters={'name': term_id}, fieldname=['terms_of_payment_name']) #add
#     inco_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['incoterms'])
#     inco_name = frappe.db.get_value("Incoterm Master", filters={'name': inco_id}, fieldname=['incoterm_name']) #add
#     payee = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['payee']) #add
#     gr_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['gr_based_inv_ver']) #add
#     check_double_invoice = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['check_double_invoice'])
#     service_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['service_based_inv_ver']) #add
#     purchase_group_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_groupm'])
#     purchase_group_name = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_group_id}, fieldname=['purchase_group_name'])
#     account_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
#     account_name = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['account_group_name']) #add
#     purchase_org_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_organization'])
#     pruchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name': purchase_org_id}, fieldname=['purchase_organization_name']) #add
#     company_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
#     company_name = frappe.db.get_value("Company Master", filters={'name': company_id}, fieldname=['company_name']) #add

#     if vendor:
#         vendor[0].update({
#             "banker_details": banker_details,
#             "supplied": supplied,
#             "number_of_employees": number_of_employees,
#             "machinery_detail": machinery_detail,
#             "testing_facility": testing_facility,
#             "reputed_partners": reputed_partners,
#             "payee_in_document": payee,
#             "check_double_invoice": check_double_invoice,
#             "gr_based_inv_ver": gr_based_inv_ver,
#             "service_based_inv_ver": service_based_inv_ver,
#             "order_currency": currency_namee,
#             "terms_of_payment": term_name,
#             "incoterms": inco_name,
#             "purchase_group": purchase_group_name,
#             "account_name": account_name,
#             "purchase_organization": pruchase_org_name,
#             "company": company_name
#         })

#     return vendor

@frappe.whitelist()
def show_me(**kwargs):
    name = kwargs.get('name')
    
    
    record_exists = frappe.db.exists("Vendor Onboarding", {'office_email_primary': name})
    if not record_exists:
        return {"message": "Record does not exist"}
    
    vendor = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.office_email_primary AS office_email_primary,
            vm.address_proofattachment AS address_proofattachment,
            vm.bank_proof AS bank_proof,
            vm.gst_proof AS gst_proof,
            vm.pan_proof AS pan_proof,
            vm.entity_proof AS entity_proof,
            vm.iec_proof AS iec_proof,
            vm.organisation_structure_document AS organisation_structure_document,
            --vm.certificate_proof AS certificate_proof,
            cm.company_name AS company_name,
            sm.state_name AS state_name,
            cnm.company_nature_name AS company_nature_name,
            bnm.business_nature_name AS business_nature_name,
            vt.vendor_type_name AS vendor_type_name,
            cn.country_name AS country_name,
            vm.type_of_business AS type_of_business,
            vm.size_of_company AS size_of_company,
            vm.website AS website,
            vm.telephone_number AS telephone_number,
            vm.office_email_secondary AS office_email_secondary,
            vm.corporate_identification_number AS corporate_identification_number,
            vm.cin_date AS cin_date,
            vm.registered_office_number AS registered_office_number,
            vm.established_year AS established_year,
            vm.address_line_1 AS address_line_1,
            vm.address_line_2 AS address_line_2,
            ct.city_name AS city_name,
            dst.district_name AS district_name,
            pin.pincode AS pincode,
            vm.street_1 AS street_1,
            vm.street_2 AS street_2,
            mfst.state_name AS manufacturing_state_name,
            mscty.country_name AS manufacturing_country_name,
            pi.pincode AS manufacturing_pincode,
            mfc.city_name AS manufacturing_city,
            mfd.district_name AS manufacturing_district,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            bk.bank_name As bank_name,
            vm.ifsc_code AS ifsc_code,
            vm.account_number AS account_number,
            vm.type_of_account AS type_of_account,
            cur.currency_name AS currency_name,
            vm.name_of_account_holder AS name_of_account_holder,
            vm.gst_number AS gst_number,
            vm.cind As cind,
            vm.company_pan_number AS company_pan_number,
            vm.name_on_company_pan AS name_on_company_pan,
            vm.enterprise_registration_number AS enterprise_registration_number,
            vm.iec As iec,
            vm.rtgs AS rtgs,
            vm.neft AS neft,
            gst.registration_type_name AS registration_type_name,
            vm.details_of_product_manufactured AS details_of_product_manufactured,
            vm.storage_capacity AS storage_capacity,
            vm.spare_capacity AS spare_capacity,
            vm.type_of_premises AS type_of_premises,
            vm.working_hours AS working_hours,
            vm.weekly_holiday AS weekly_holiday,
            vm.number_of_manpower AS number_of_manpower,
            vm.annual_revenue AS annual_revenue,
            vm.google_address_pin AS google_address_pin,
            vm.first_name AS first_name,
            vm.last_name As last_name,
            vm.designation AS designation,
            vm.email AS email,
            vm.contact_number AS contact_number,
            vm.f_name AS f_name,
            vm.l_name AS l_name,
            vm.dnation AS dnation,
            vm.mail AS mail,
            vm.cnot AS cnot,
            crt.certificate_name AS certificate_name,
            vm.valid_till AS valid_till,
            --vm.payee_in_document AS payee_in_document,
            --vm.check_double_invoice AS check_double_invoice,
            --vm.gr_based_inv_ver AS gr_based_inv_ver,
            --vm.service_based_inv_ver AS service_based_inv_ver,
            --curn.currency_name AS order_currency,
            --term.terms_of_payment_name AS terms_of_payment,
            --incoterm.incoterm_name AS incoterms,
            --purchase.purchase_group_name AS purchase_group,
            vm.purchase_team_remarks AS purchase_team_remarks,
            vm.purchase_head_remark AS purchase_head_remark,
            vm.enterprise AS enterprise,
            vm.reconciliation_account AS reconciliation_account,
            vm.accounts_team_remark AS accounts_team_remark,
            vm.ref_no AS ref_no,
            vm.company_name AS company_name

        FROM 
            `tabVendor Onboarding` vm 
        LEFT JOIN 
            `tabVendor Master` cm ON vm.ref_no = cm.name 
        LEFT JOIN
            `tabState Master` sm ON vm.state = sm.name
        LEFT JOIN 
            `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
        LEFT JOIN
            `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
        LEFT JOIN 
            `tabVendor Type Master` vt ON vm.vendor_type = vt.name
        LEFT JOIN
            `tabCountry Master` cn ON vm.country = cn.name
        LEFT JOIN
            `tabCity Master` ct ON vm.city = ct.name
        LEFT JOIN
            `tabDistrict Master` dst ON vm.district = dst.name
        LEFT JOIN 
            `tabPincode Master` pin ON vm.pincode = pin.name
        LEFT JOIN
            `tabState Master` mfst ON vm.manufacturing_state = mfst.name
        LEFT JOIN
            `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
        LEFT JOIN
            `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
        LEFT JOIN
            `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
        LEFT JOIN
            `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
        LEFT JOIN
            `tabBank Master` bk ON vm.bank_name = bk.name
       LEFT JOIN
            `tabCurrency Master` cur ON vm.currency = cur.name
        LEFT JOIN
            `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
        LEFT JOIN
            `tabCertificate Master` crt ON vm.certificate_name = crt.name
        --LEFT JOIN
          --  `tabCurrency Master` curn ON vm.order_currency = curn.name
        --LEFT JOIN
         --   `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
        --LEFT JOIN
         --   `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
        --LEFT JOIN
         --   `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
        WHERE 
            vm.office_email_primary=%s
    """, (name), as_dict=1)

    primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
    banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """, (primary_key), as_dict=1)
    supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """, (primary_key), as_dict=1)
    number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """, (primary_key), as_dict=1)
    machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """, (primary_key), as_dict=1)
    testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """, (primary_key), as_dict=1)
    reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """, (primary_key), as_dict=1)

    xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
    email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
    ordercurrency = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['order_currency'])
    # print("%%%%%%%%%%%%%%%%%((((((((((((((()))))))))))))))",ordercurrency) #add
    currency_namee = frappe.db.get_value("Currency Master", filters={'name': ordercurrency}, fieldname=['currency_name'])
    term_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['terms_of_payment'])
    term_name = frappe.db.get_value("Terms Of Payment Master", filters={'name': term_id}, fieldname=['terms_of_payment_name']) #add
    inco_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['incoterms'])
    inco_name = frappe.db.get_value("Incoterm Master", filters={'name': inco_id}, fieldname=['incoterm_name']) #add
    payee = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['payee']) #add
    gr_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['gr_based_inv_ver']) #add
    check_double_invoice = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['check_double_invoice'])
    service_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['service_based_inv_ver']) #add
    purchase_group_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_groupm'])
    purchase_group_name = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_group_id}, fieldname=['purchase_group_name', 'description'])
    account_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
    account_name = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['account_group_name']) #add
    purchase_org_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_organization'])
    pruchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name': purchase_org_id}, fieldname=['purchase_organization_name']) #add
    company_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
    company_name = frappe.db.get_value("Company Master", filters={'name': company_id}, fieldname=['company_name']) #add
    vendor_name = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['vendor_name'])
    vendor_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['vendor_type'])
    vendor_type_name = frappe.db.get_value("Vendor Type Master", filters={'name': vendor_id}, fieldname=['vendor_type_name'])
    accountgrp_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
    account_group_description = frappe.db.get_value("Account Group Master", filters={'name': accountgrp_id}, fieldname=['description'])
    certficates = frappe.db.sql(""" SELECT * FROM `tabOnboarding Certificates` WHERE parent=%s """, (primary_key), as_dict=1)
    for cert in certficates:
        certificate_name = cert.get('certificate_name')
        certificate_doc = frappe.get_doc("Certificate Master", certificate_name)
        if certificate_doc:
            cert_name = certificate_doc.certificate_name
            cert_code = certificate_doc.certificate_code  # Fetch the certificate code
            cert['certificate_name'] = cert_name
            cert['certificate_code'] = cert_code  # Add the certificate code to the dictionary
            # print(f"Updated certificate_name for {cert.get('name')} to {cert_name}")
            print(f"Updated certificate_name for {cert.get('name')} to {cert_name} with code {cert_code}")
        else:
            print(f"Certificate {certificate_name} not found in Certificate Master")


    if vendor:
        vendor[0].update({
            "banker_details": banker_details,
            "supplied": supplied,
            "number_of_employees": number_of_employees,
            "machinery_detail": machinery_detail,
            "testing_facility": testing_facility,
            "reputed_partners": reputed_partners,
            "payee_in_document": payee,
            "check_double_invoice": check_double_invoice,
            "gr_based_inv_ver": gr_based_inv_ver,
            "service_based_inv_ver": service_based_inv_ver,
            "order_currency": currency_namee,
            "terms_of_payment": term_name,
            "incoterms": inco_name,
            "purchase_group": purchase_group_name,
            "account_name": account_name,
            "purchase_organization": pruchase_org_name,
            "company": company_name,
            "vendor_name": vendor_name,
            "vendor_type": vendor_type_name,
            "account_group_description": account_group_description,
            "certificates": certficates
        })

    return vendor


# @frappe.whitelist()
# def show_me(**kwargs):
#     name = kwargs.get('name')
    
    
#     record_exists = frappe.db.exists("Vendor Onboarding", {'office_email_primary': name})
#     if not record_exists:
#         return {"message": "Record does not exist"}
    
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             --cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             --cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             --vm.payee_in_document AS payee_in_document,
#             --vm.check_double_invoice AS check_double_invoice,
#             --vm.gr_based_inv_ver AS gr_based_inv_ver,
#             --vm.service_based_inv_ver AS service_based_inv_ver,
#             --curn.currency_name AS order_currency,
#             --term.terms_of_payment_name AS terms_of_payment,
#             --incoterm.incoterm_name AS incoterms,
#             --purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name

#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#        -- LEFT JOIN
#        --     `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         --LEFT JOIN
#           --  `tabCurrency Master` curn ON vm.order_currency = curn.name
#         --LEFT JOIN
#          --   `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
#         --LEFT JOIN
#          --   `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
#         --LEFT JOIN
#          --   `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)

#     primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
#     banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """, (primary_key), as_dict=1)
#     supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """, (primary_key), as_dict=1)
#     number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """, (primary_key), as_dict=1)
#     machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """, (primary_key), as_dict=1)
#     testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """, (primary_key), as_dict=1)
#     reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """, (primary_key), as_dict=1)

#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     ordercurrency = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['order_currency'])
#     print("%%%%%%%%%%%%%%%%%((((((((((((((()))))))))))))))",ordercurrency) #add
#     currency_namee = frappe.db.get_value("Currency Master", filters={'name': ordercurrency}, fieldname=['currency_name'])
#     term_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['terms_of_payment'])
#     term_name = frappe.db.get_value("Terms Of Payment Master", filters={'name': term_id}, fieldname=['terms_of_payment_name']) #add
#     inco_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['incoterms'])
#     inco_name = frappe.db.get_value("Incoterm Master", filters={'name': inco_id}, fieldname=['incoterm_name']) #add
#     payee = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['payee']) #add
#     gr_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['gr_based_inv_ver']) #add
#     check_double_invoice = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['check_double_invoice'])
#     service_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['service_based_inv_ver']) #add
#     purchase_group_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_groupm'])
#     purchase_group_name = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_group_id}, fieldname=['purchase_group_name'])
#     account_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
#     account_name = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['account_group_name']) #add
#     purchase_org_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_organization'])
#     pruchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name': purchase_org_id}, fieldname=['purchase_organization_name']) #add
#     company_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
#     company_name = frappe.db.get_value("Company Master", filters={'name': company_id}, fieldname=['company_name']) #add
#     vendor_name = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['vendor_name'])

#     if vendor:
#         vendor[0].update({
#             "banker_details": banker_details,
#             "supplied": supplied,
#             "number_of_employees": number_of_employees,
#             "machinery_detail": machinery_detail,
#             "testing_facility": testing_facility,
#             "reputed_partners": reputed_partners,
#             "payee_in_document": payee,
#             "check_double_invoice": check_double_invoice,
#             "gr_based_inv_ver": gr_based_inv_ver,
#             "service_based_inv_ver": service_based_inv_ver,
#             "order_currency": currency_namee,
#             "terms_of_payment": term_name,
#             "incoterms": inco_name,
#             "purchase_group": purchase_group_name,
#             "account_name": account_name,
#             "purchase_organization": pruchase_org_name,
#             "company": company_name,
#             "vendor_name": vendor_name
#         })

#     return vendor

# @frappe.whitelist()
# def show_me(**kwargs):
#     name = kwargs.get('name')
    
    
#     record_exists = frappe.db.exists("Vendor Onboarding", {'office_email_primary': name})
#     if not record_exists:
#         return {"message": "Record does not exist"}
    
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vm.vendor_type AS vendor_type,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             --cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             --vm.payee_in_document AS payee_in_document,
#             --vm.check_double_invoice AS check_double_invoice,
#             --vm.gr_based_inv_ver AS gr_based_inv_ver,
#             --vm.service_based_inv_ver AS service_based_inv_ver,
#             --curn.currency_name AS order_currency,
#             --term.terms_of_payment_name AS terms_of_payment,
#             --incoterm.incoterm_name AS incoterms,
#             --purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name

#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#        -- LEFT JOIN
#        --     `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         --LEFT JOIN
#           --  `tabCurrency Master` curn ON vm.order_currency = curn.name
#         --LEFT JOIN
#          --   `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
#         --LEFT JOIN
#          --   `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
#         --LEFT JOIN
#          --   `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)

#     primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
#     banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """, (primary_key), as_dict=1)
#     supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """, (primary_key), as_dict=1)
#     number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """, (primary_key), as_dict=1)
#     machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """, (primary_key), as_dict=1)
#     testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """, (primary_key), as_dict=1)
#     reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """, (primary_key), as_dict=1)

#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     ordercurrency = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['order_currency'])
#     # print("%%%%%%%%%%%%%%%%%((((((((((((((()))))))))))))))",ordercurrency) #add
#     currency_namee = frappe.db.get_value("Currency Master", filters={'name': ordercurrency}, fieldname=['currency_name'])
#     term_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['terms_of_payment'])
#     term_name = frappe.db.get_value("Terms Of Payment Master", filters={'name': term_id}, fieldname=['terms_of_payment_name']) #add
#     inco_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['incoterms'])
#     inco_name = frappe.db.get_value("Incoterm Master", filters={'name': inco_id}, fieldname=['incoterm_name']) #add
#     payee = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['payee']) #add
#     gr_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['gr_based_inv_ver']) #add
#     check_double_invoice = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['check_double_invoice'])
#     service_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['service_based_inv_ver']) #add
#     purchase_group_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_groupm'])
#     purchase_group_name = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_group_id}, fieldname=['purchase_group_name', 'description'])
#     account_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
#     account_name = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['account_group_name']) #add
#     purchase_org_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_organization'])
#     pruchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name': purchase_org_id}, fieldname=['purchase_organization_name']) #add
#     company_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
#     company_name = frappe.db.get_value("Company Master", filters={'name': company_id}, fieldname=['company_name']) #add
#     vendor_name = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['vendor_name'])
#     accountgrp_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
#     account_group_description = frappe.db.get_value("Account Group Master", filters={'name': accountgrp_id}, fieldname=['description'])
#     vendor_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary'}, fieldname=['vendor_type'])
#     vendor_type = frappe.db.get_value("Vendor Master", filters={'name': vendor_id}, fieldname=['vendor_type'])
#     # print("@@@@@@@@@@@@@@@@@@@@@@@@@", accountgrp_id)


#     if vendor:
#         vendor[0].update({
#             "banker_details": banker_details,
#             "supplied": supplied,
#             "number_of_employees": number_of_employees,
#             "machinery_detail": machinery_detail,
#             "testing_facility": testing_facility,
#             "reputed_partners": reputed_partners,
#             "payee_in_document": payee,
#             "check_double_invoice": check_double_invoice,
#             "gr_based_inv_ver": gr_based_inv_ver,
#             "service_based_inv_ver": service_based_inv_ver,
#             "order_currency": currency_namee,
#             "terms_of_payment": term_name,
#             "incoterms": inco_name,
#             "purchase_group": purchase_group_name[0],
#             "account_name": account_name,
#             "purchase_organization": pruchase_org_name,
#             "company": company_name,
#             "vendor_name": vendor_name,
#             "account_group_description": account_group_description,
#             "vendor_type": vendor_type
#         })

#     return vendor

# @frappe.whitelist()
# def show_me(**kwargs):
#     name = kwargs.get('name')
    
    
#     record_exists = frappe.db.exists("Vendor Onboarding", {'office_email_primary': name})
#     if not record_exists:
#         return {"message": "Record does not exist"}
    
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             --cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             --vm.payee_in_document AS payee_in_document,
#             --vm.check_double_invoice AS check_double_invoice,
#             --vm.gr_based_inv_ver AS gr_based_inv_ver,
#             --vm.service_based_inv_ver AS service_based_inv_ver,
#             --curn.currency_name AS order_currency,
#             --term.terms_of_payment_name AS terms_of_payment,
#             --incoterm.incoterm_name AS incoterms,
#             --purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name

#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#        -- LEFT JOIN
#        --     `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         --LEFT JOIN
#           --  `tabCurrency Master` curn ON vm.order_currency = curn.name
#         --LEFT JOIN
#          --   `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
#         --LEFT JOIN
#          --   `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
#         --LEFT JOIN
#          --   `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)

#     primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
#     banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """, (primary_key), as_dict=1)
#     supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """, (primary_key), as_dict=1)
#     number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """, (primary_key), as_dict=1)
#     machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """, (primary_key), as_dict=1)
#     testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """, (primary_key), as_dict=1)
#     reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """, (primary_key), as_dict=1)

#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     ordercurrency = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['order_currency'])
#     print("%%%%%%%%%%%%%%%%%((((((((((((((()))))))))))))))",ordercurrency) #add
#     currency_namee = frappe.db.get_value("Currency Master", filters={'name': ordercurrency}, fieldname=['currency_name'])
#     term_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['terms_of_payment'])
#     term_name = frappe.db.get_value("Terms Of Payment Master", filters={'name': term_id}, fieldname=['terms_of_payment_name']) #add
#     inco_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['incoterms'])
#     inco_name = frappe.db.get_value("Incoterm Master", filters={'name': inco_id}, fieldname=['incoterm_name']) #add
#     payee = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['payee']) #add
#     gr_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['gr_based_inv_ver']) #add
#     check_double_invoice = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['check_double_invoice'])
#     service_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['service_based_inv_ver']) #add
#     purchase_group_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_groupm'])
#     purchase_group_name = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_group_id}, fieldname=['purchase_group_name', 'description'])
#     account_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
#     account_name = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['account_group_name']) #add
#     purchase_org_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_organization'])
#     pruchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name': purchase_org_id}, fieldname=['purchase_organization_name']) #add
#     company_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
#     company_name = frappe.db.get_value("Company Master", filters={'name': company_id}, fieldname=['company_name']) #add
#     vendor_name = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['vendor_name'])
#     accountgrp_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
#     account_group_description = frappe.db.get_value("Account Group Master", filters={'name': accountgrp_id}, fieldname=['description'])
#     certficates = frappe.db.sql(""" SELECT * FROM `tabOnboarding Certificates` WHERE parent=%s """, (primary_key), as_dict=1)
#     for cert in certficates:
#         certificate_name = cert.get('certificate_name')
#         certificate_doc = frappe.get_doc("Certificate Master", certificate_name)
#         if certificate_doc:
#             cert_name = certificate_doc.certificate_name
#             cert['certificate_name'] = cert_name
#             print(f"Updated certificate_name for {cert.get('name')} to {cert_name}")
#         else:
#             print(f"Certificate {certificate_name} not found in Certificate Master")


#     if vendor:
#         vendor[0].update({
#             "banker_details": banker_details,
#             "supplied": supplied,
#             "number_of_employees": number_of_employees,
#             "machinery_detail": machinery_detail,
#             "testing_facility": testing_facility,
#             "reputed_partners": reputed_partners,
#             "payee_in_document": payee,
#             "check_double_invoice": check_double_invoice,
#             "gr_based_inv_ver": gr_based_inv_ver,
#             "service_based_inv_ver": service_based_inv_ver,
#             "order_currency": currency_namee,
#             "terms_of_payment": term_name,
#             "incoterms": inco_name,
#             "purchase_group": purchase_group_name[0],
#             "account_name": account_name,
#             "purchase_organization": pruchase_org_name,
#             "company": company_name,
#             "vendor_name": vendor_name,
#             "account_group_description": account_group_description,
#             "certificates": certficates
#         })

#     return vendor


# @frappe.whitelist()
# def show_me(name):
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             vm.payee_in_document AS payee_in_document,
#             vm.check_double_invoice AS check_double_invoice,
#             vm.gr_based_inv_ver AS gr_based_inv_ver,
#             vm.service_based_inv_ver AS service_based_inv_ver,
#             curn.currency_name AS order_currency,
#             term.terms_of_payment_name AS terms_of_payment,
#             incoterm.incoterm_name AS incoterms,
#             purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name




#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#         LEFT JOIN
#             `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         LEFT JOIN
#             `tabCurrency Master` curn ON vm.order_currency = curn.name
#         LEFT JOIN
#             `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
#         LEFT JOIN
#             `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
#         LEFT JOIN
#             `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)

#     primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
#     banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """,(primary_key), as_dict=1)
#     supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """,(primary_key), as_dict=1)
#     number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """,(primary_key), as_dict=1)
#     machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """,(primary_key), as_dict=1)
#     testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """,(primary_key), as_dict=1)
#     reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """,(primary_key), as_dict=1)


#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     dic = {
#         "id": email 
#     }

#     val = vendor + [dic] + banker_details + supplied + number_of_employees + machinery_detail + testing_facility + reputed_partners

#     return val



# @frappe.whitelist()
# def show_me(name):
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             vm.payee_in_document AS payee_in_document,
#             vm.check_double_invoice AS check_double_invoice,
#             vm.gr_based_inv_ver AS gr_based_inv_ver,
#             vm.service_based_inv_ver AS service_based_inv_ver,
#             curn.currency_name AS order_currency,
#             term.terms_of_payment_name AS terms_of_payment,
#             incoterm.incoterm_name AS incoterms,
#             purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name




#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#         LEFT JOIN
#             `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         LEFT JOIN
#             `tabCurrency Master` curn ON vm.order_currency = curn.name
#         LEFT JOIN
#             `tabTerms Of Payment Master` term ON vm.terms_of_payment = term.name
#         LEFT JOIN
#             `tabIncoterm Master` incoterm ON vm.incoterms = incoterm.name
#         LEFT JOIN
#             `tabPurchase Group Master` purchase ON vm.purchase_group = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)

#     primary_key = frappe.db.get_value("Vendor Onboarding", filters={'office_email_primary': name}, fieldname=["name"])
#     banker_details = frappe.db.sql(""" SELECT * FROM `tabBanker Details` WHERE parent=%s """,(primary_key), as_dict=1)
#     supplied = frappe.db.sql(""" SELECT * FROM `tabSupplied` WHERE parent=%s """,(primary_key), as_dict=1)
#     number_of_employees = frappe.db.sql(""" SELECT * FROM `tabEmployee Number` WHERE parent=%s """,(primary_key), as_dict=1)
#     machinery_detail = frappe.db.sql(""" SELECT * FROM `tabMachinery Detail` WHERE parent=%s """,(primary_key), as_dict=1)
#     testing_facility = frappe.db.sql(""" SELECT * FROM `tabTesting Facility` WHERE parent=%s """,(primary_key), as_dict=1)
#     reputed_partners = frappe.db.sql(""" SELECT * FROM `tabReputed Partners` WHERE parent=%s """,(primary_key), as_dict=1)


#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     dic = {
#         "id": email 
#     }

#     val = vendor + [dic] + banker_details + supplied + number_of_employees + machinery_detail + testing_facility + reputed_partners

#     return val

# @frappe.whitelist()
# def show_me(name):
#     vendor = frappe.db.sql("""
#         SELECT
#             vm.name AS name,
#             vm.office_email_primary AS office_email_primary,
#             vm.address_proofattachment AS address_proofattachment,
#             vm.bank_proof AS bank_proof,
#             vm.gst_proof AS gst_proof,
#             vm.pan_proof AS pan_proof,
#             vm.entity_proof AS entity_proof,
#             vm.iec_proof AS iec_proof,
#             vm.organisation_structure_document AS organisation_structure_document,
#             vm.certificate_proof AS certificate_proof,
#             cm.company_name AS company_name,
#             sm.state_name AS state_name,
#             cnm.company_nature_name AS company_nature_name,
#             bnm.business_nature_name AS business_nature_name,
#             vt.vendor_type_name AS vendor_type_name,
#             cn.country_name AS country_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.website AS website,
#             vm.telephone_number AS telephone_number,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number AS corporate_identification_number,
#             vm.cin_date AS cin_date,
#             vm.registered_office_number AS registered_office_number,
#             vm.established_year AS established_year,
#             vm.address_line_1 AS address_line_1,
#             vm.address_line_2 AS address_line_2,
#             ct.city_name AS city_name,
#             dst.district_name AS district_name,
#             pin.pincode AS pincode,
#             vm.street_1 AS street_1,
#             vm.street_2 AS street_2,
#             mfst.state_name AS manufacturing_state_name,
#             mscty.country_name AS manufacturing_country_name,
#             pi.pincode AS manufacturing_pincode,
#             mfc.city_name AS manufacturing_city,
#             mfd.district_name AS manufacturing_district,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             bk.bank_name As bank_name,
#             vm.ifsc_code AS ifsc_code,
#             vm.account_number AS account_number,
#             vm.type_of_account AS type_of_account,
#             cur.currency_name AS currency_name,
#             vm.name_of_account_holder AS name_of_account_holder,
#             vm.gst_number AS gst_number,
#             vm.cind As cind,
#             vm.company_pan_number AS company_pan_number,
#             vm.name_on_company_pan AS name_on_company_pan,
#             vm.enterprise_registration_number AS enterprise_registration_number,
#             vm.iec As iec,
#             vm.rtgs AS rtgs,
#             vm.neft AS neft,
#             gst.registration_type_name AS registration_type_name,
#             vm.details_of_product_manufactured AS details_of_product_manufactured,
#             vm.storage_capacity AS storage_capacity,
#             vm.spare_capacity AS spare_capacity,
#             vm.type_of_premises AS type_of_premises,
#             vm.working_hours AS working_hours,
#             vm.weekly_holiday AS weekly_holiday,
#             vm.number_of_manpower AS number_of_manpower,
#             vm.annual_revenue AS annual_revenue,
#             vm.google_address_pin AS google_address_pin,
#             vm.first_name AS first_name,
#             vm.last_name As last_name,
#             vm.designation AS designation,
#             vm.email AS email,
#             vm.contact_number AS contact_number,
#             vm.f_name AS f_name,
#             vm.l_name AS l_name,
#             vm.dnation AS dnation,
#             vm.mail AS mail,
#             vm.cnot AS cnot,
#             crt.certificate_name AS certificate_name,
#             vm.valid_till AS valid_till,
#             cm.payee AS payee_in_document,
#             cm.check_double_invoice AS check_double_invoice,
#             cm.gr_based_inv_ver AS gr_based_inv_ver,
#             cm.service_based_inv_ver AS service_based_inv_ver,
#             curn.currency_name AS order_currency,
#             term.terms_of_payment_name AS terms_of_payment,
#             incoterm.incoterm_name AS incoterms,
#             purchase.purchase_group_name AS purchase_group,
#             vm.purchase_team_remarks AS purchase_team_remarks,
#             vm.purchase_head_remark AS purchase_head_remark,
#             vm.enterprise AS enterprise,
#             vm.reconciliation_account AS reconciliation_account,
#             vm.accounts_team_remark AS accounts_team_remark,
#             vm.ref_no AS ref_no,
#             vm.company_name AS company_name




#         FROM 
#             `tabVendor Onboarding` vm 
#         LEFT JOIN 
#             `tabVendor Master` cm ON vm.ref_no = cm.name 
#         LEFT JOIN
#             `tabState Master` sm ON vm.state = sm.name
#         LEFT JOIN 
#             `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
#         LEFT JOIN
#             `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
#         LEFT JOIN 
#             `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#         LEFT JOIN
#             `tabCountry Master` cn ON vm.country = cn.name
#         LEFT JOIN
#             `tabCity Master` ct ON vm.city = ct.name
#         LEFT JOIN
#             `tabDistrict Master` dst ON vm.district = dst.name
#         LEFT JOIN 
#             `tabPincode Master` pin ON vm.pincode = pin.name
#         LEFT JOIN
#             `tabState Master` mfst ON vm.manufacturing_state = mfst.name
#         LEFT JOIN
#             `tabCountry Master` mscty ON vm.manufacturing_country = mscty.name
#         LEFT JOIN
#             `tabPincode Master` pi ON vm.manufacturing_pincode = pi.name
#         LEFT JOIN
#             `tabCity Master` mfc ON vm.manufacturing_city = mfc.name
#         LEFT JOIN
#             `tabDistrict Master` mfd ON vm.manufacturing_district = mfd.name
#         LEFT JOIN
#             `tabBank Master` bk ON vm.bank_name = bk.name
#         LEFT JOIN
#             `tabCurrency Master` cur ON vm.currency = cur.name
#         LEFT JOIN
#             `tabGST Registration Type Master` gst ON vm.gst_registration_type = gst.name
#         LEFT JOIN
#             `tabCertificate Master` crt ON vm.certificate_name = crt.name
#         LEFT JOIN
#             `tabCurrency Master` curn ON cm.order_currency = curn.name
#         LEFT JOIN
#             `tabTerms Of Payment Master` term ON cm.terms_of_payment = term.name
#         LEFT JOIN
#             `tabIncoterm Master` incoterm ON cm.incoterms = incoterm.name
#         LEFT JOIN
#             `tabPurchase Group Master` purchase ON cm.purchase_groupm = purchase.name
#         WHERE 
#             vm.office_email_primary=%s
#     """, (name), as_dict=1)




#     xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=["office_email_primary"])
#     email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
#     dic = {
#         "id": email 
#     }

#     val = vendor + [dic]

#     return val




# @frappe.whitelist()
# def show_vendor_registration_details(**kwargs):

#     name= kwargs.get('name')

#     vendor = frappe.db.sql(""" 

#         SELECT
#             cm.company_name AS company_name,
#             -- cm.company_code AS company_code,
#             vm.website AS website,
#             vt.vendor_type_name As vendor_type_name,
#             at.account_group_name AS account_group_name,
#             dp.department_name AS department_name,
#             mt.material_name AS material_name,
#             vm.search_term AS search_term,
#             bn.business_nature_name AS business_nature_name,
#             vm.payee AS payee_in_document,
#             vm.gr_based_inv_ver AS gr_based_inv_ver,
#             vm.service_based_inv_ver AS service_based_inv_ver,
#             vm.check_double_invoice AS check_double_invoice,
#             oc.currency_name AS currency_name,
#             tp.terms_of_payment_name As terms_of_payment_name,
#             inc.incoterm_name As incoterm_name,
#             pg.purchase_group_name AS purchase_group_name,
#             vm.registered_date AS registered_date,
#             vm.purchase_organization AS company_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.registered_office_number AS registered_office_number,
#             vm.telephone_number AS telephone_number,
#             vm.established_year AS established_year,
#             vm.office_email_primary AS office_email_primary,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number As corporate_identification_number,
#             vm.cin_date AS cin_date,
#             con.company_nature_name AS company_nature_name,
#             vm.vendor_name AS vendor_name,
#             rfq.rfq_name AS rfq_name,
#             vm.mobile_number AS mobile_number,
#             vm.office_address_line_1 AS office_address_line_1,
#             vm.office_address_line_2 AS office_address_line_2,
#             vm.office_address_line_3 AS office_address_line_3,
#             vm.office_address_line_4 AS office_address_line_4,
#             cty.city_name AS city_name,
#             st.state_name AS state_name,
#             cnt.country_name AS country_name,
#             dst.district_name As district_name,
#             pin.pincode AS pincode,
#             vm.manufacturing_address_line_1 AS manufacturing_address_line_1,
#             vm.manufacturing_address_line_2 AS manufacturing_address_line_2,
#             vm.manufacturing_address_line_3 AS manufacturing_address_line_3,
#             vm.manufacturing_address_line_4 AS manufacturing_address_line_4,
#             vm.registered_by As registered_by,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             vm.status AS status,
#             vm.vendor_code AS vendor_code


#             FROM `tabVendor Master` vm 
#             LEFT JOIN
#                 `tabCompany Master` cm ON vm.company_name = cm.name
#             LEFT JOIN
#                 `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#             LEFT JOIN
#                 `tabAccount Group Master` at ON vm.account_group = at.name
#             LEFT JOIN
#                 `tabDepartment Master` dp ON vm.department = dp.name
#             LEFT JOIN
#                 `tabMaterial Master` mt ON vm.material_to_be_supplied = mt.name
#             LEFT JOIN
#                 `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
#             LEFT JOIN
#                 `tabCurrency Master` oc ON vm.order_currency = oc.name
#             LEFT JOIN
#                 `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
#             LEFT JOIN
#                 `tabIncoterm Master` inc ON vm.incoterms = inc.name
#             LEFT JOIN
#                 `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
#             LEFT JOIN
#                 `tabCompany Nature Master` con ON vm.nature_of_company = con.name
#             LEFT JOIN
#                 `tabRFQ Type Master` rfq ON vm.rfq_type = rfq.name
#             LEFT JOIN
#                 `tabCompany Master` ct ON vm.city = ct.name
#             LEFT JOIN
#                 `tabState Master` st ON vm.state = st.name
#             LEFT JOIN
#                 `tabCountry Master` cnt ON vm.country = cnt.name
#             LEFT JOIN
#                 `tabDistrict Master` dst ON vm.district = dst.name
#             LEFT JOIN
#                 `tabPincode Master` pin ON vm.pincode = pin.name
#             LEFT JOIN
#                 `tabCity Master` cty ON vm.city = cty.name
#             -- LEFT JOIN
#             --     `tabCompany Master` cm on 

#             where vm.name=%s



#         """,(name), as_dict=1)
#     return vendor


@frappe.whitelist()
def show_vendor_registration_details(**kwargs):

    name= kwargs.get('name')

    vendor = frappe.db.sql(""" 

        SELECT
            --cm.company_name AS company_name,
            -- cm.company_code AS company_code,
            vm.website AS website,
            vt.vendor_type_name As vendor_type_name,
            at.account_group_name AS account_group_name,
            dp.department_name AS department_name,
            mt.material_name AS material_name,
            vm.search_term AS search_term,
            bn.business_nature_name AS business_nature_name,
            vm.payee AS payee_in_document,
            vm.gr_based_inv_ver AS gr_based_inv_ver,
            vm.service_based_inv_ver AS service_based_inv_ver,
            vm.check_double_invoice AS check_double_invoice,
            oc.currency_name AS currency_name,
            tp.terms_of_payment_name As terms_of_payment_name,
            inc.incoterm_name As incoterm_name,
            pg.purchase_group_name AS purchase_group_name,
            vm.registered_date AS registered_date,
            vm.purchase_organization AS company_name,
            vm.type_of_business AS type_of_business,
            vm.size_of_company AS size_of_company,
            vm.registered_office_number AS registered_office_number,
            vm.telephone_number AS telephone_number,
            vm.established_year AS established_year,
            vm.office_email_primary AS office_email_primary,
            vm.office_email_secondary AS office_email_secondary,
            vm.corporate_identification_number As corporate_identification_number,
            vm.cin_date AS cin_date,
            con.company_nature_name AS company_nature_name,
            vm.vendor_name AS vendor_name,
            rfq.rfq_name AS rfq_name,
            vm.mobile_number AS mobile_number,
            vm.office_address_line_1 AS office_address_line_1,
            vm.office_address_line_2 AS office_address_line_2,
            vm.office_address_line_3 AS office_address_line_3,
            vm.office_address_line_4 AS office_address_line_4,
            cty.city_name AS city_name,
            st.state_name AS state_name,
            cnt.country_name AS country_name,
            dst.district_name As district_name,
            pin.pincode AS pincode,
            vm.manufacturing_address_line_1 AS manufacturing_address_line_1,
            vm.manufacturing_address_line_2 AS manufacturing_address_line_2,
            vm.manufacturing_address_line_3 AS manufacturing_address_line_3,
            vm.manufacturing_address_line_4 AS manufacturing_address_line_4,
            vm.registered_by As registered_by,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.status AS status,
            vm.vendor_code AS vendor_code,
            cmm.company_name AS company_name


            FROM `tabVendor Master` vm 
            --LEFT JOIN
              --  `tabCompany Master` cm ON vm.company_name = cm.company_name
            LEFT JOIN
                `tabVendor Type Master` vt ON vm.vendor_type = vt.name
            LEFT JOIN
                `tabAccount Group Master` at ON vm.account_group = at.name
            LEFT JOIN
                `tabDepartment Master` dp ON vm.department = dp.name
            LEFT JOIN
                `tabMaterial Master` mt ON vm.material_to_be_supplied = mt.name
            LEFT JOIN
                `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
            LEFT JOIN
                `tabCurrency Master` oc ON vm.order_currency = oc.name
            LEFT JOIN
                `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
            LEFT JOIN
                `tabIncoterm Master` inc ON vm.incoterms = inc.name
            LEFT JOIN
                `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
            LEFT JOIN
                `tabCompany Nature Master` con ON vm.nature_of_company = con.name
            LEFT JOIN
                `tabRFQ Type Master` rfq ON vm.rfq_type = rfq.name
            LEFT JOIN
                `tabCompany Master` ct ON vm.city = ct.name
            LEFT JOIN
                `tabState Master` st ON vm.state = st.name
            LEFT JOIN
                `tabCountry Master` cnt ON vm.country = cnt.name
            LEFT JOIN
                `tabDistrict Master` dst ON vm.district = dst.name
            LEFT JOIN
                `tabPincode Master` pin ON vm.pincode = pin.name
            LEFT JOIN
                `tabCity Master` cty ON vm.city = cty.name
             LEFT JOIN
                 `tabCompany Master` cmm ON vm.company_name = cmm.name

            where vm.name=%s



        """,(name), as_dict=1)
    return vendor



#*********************This API will show RFQ with its items*****************************

# @frappe.whitelist()
# def show_rfq_detail_with_items(name):
#     rfq = frappe.db.sql(""" 

#         SELECT
#         rfq.name AS rfq_number,
#         prt4.port_name AS destination_port,
#         rfq.meril_invoice_date AS meril_invoice_date,
#         vt.vendor_type_name AS vendor_type_name,
#         rfq.rfq_cutoff_date AS rfq_cutoff_date,
#         comp.company_name AS division_name,
#         rfq.mode_of_shipment AS mode_of_shipment,
#         prt.port_name AS port_name,
#         rfq.ship_to_address AS ship_to_address,
#         rfq.no_of_pkg_units As no_of_pkg_units,
#         rfq.vol_weight AS vol_weight,
#         rfq.invoice_date AS invoice_date,
#         rfq.shipment_date AS shipment_date,
#         rfq.remarks AS remarks,
#         rfq.consignee_name AS consignee_name,
#         rfq.sr_no AS sr_no,
#         rfq.rfq_date AS rfq_date,
#         cnt.country_name AS country_name,
#         pt.port_code AS port_code,
#         inc.incoterm_name AS incoterm_name,
#         pty.package_name AS package_name,
#         pcat.product_category_name AS product_category_name,
#         rfq.actual_weight AS actual_weight,
#         rfq.invoice_no AS invoice_no,
#         sty.shipment_type_name AS shipment_type_name,
#         rft.rfq_name AS rfq_name,
#         rfq.raised_by AS raised_by,
#         rfq.status AS status,
#         mm.material_name AS material_name,
#         rfq.quantity AS quantity,
#         rfq.required_by AS required_by,
#         rfq.pr_code AS pr_code,
#         comp2.company_code AS company_code,
#         porg.purchase_organization_name AS purchase_organization_name,
#         pg.purchase_group_name AS purchase_group_name,
#         cur.currency_name AS currency_name,
#         rfq.collection_number AS collection_number,
#         rfq.quotation_deadline AS quotation_deadline,
#         rfq.validity_start_date AS validity_start_date,
#         rfq.validity_end_date AS validity_end_date,
#         rfq.requestor_name AS requestor_name,
#         pd.product_code AS product_code,
#         pdc.product_category_name AS product_category_name,
#         rfq.item_description AS item_description,
#         rfq.item_dimension AS item_dimension,
#         rfq.add_special_remarksif_any AS add_special_remarksif_any,
#         mtc.material_category_name AS material_category_name,
#         pltm.plant_code AS plant_code,
#         rfq.short_text AS short_text,
#         rfq.catalogue_number AS catalogue_number,
#         rfq.make AS make,
#         rfq.pack_size AS pack_size,
#         rfq.rfq_quantity AS rfq_quantity,
#         rfq.quantity_unit AS quantity_unit,
#         rfq.delivery_date AS delivery_date,
#         rfq.first_reminder AS first_reminder,
#         rfq.second_reminder AS second_reminder,
#         rfq.third_reminder AS third_reminder,
#         rfq.non_negotiable AS non_negotiable,
#         rfq.negotiable AS negotiable,
#         vm2.name AS name,
#         rfq.bidding_person AS bidding_person,
#         rfq.select_language AS select_language,
#         rfq.service_code AS service_code,
#         rfq.service_category AS service_category,
#         rfq.storage_location AS storage_location,
#         productcat.product_category_name AS product_category,
#         ReFQ.rfq_quantity AS rfq_quantity,
#         prt2.port_name AS port_of_loading,
#         pck.package_name AS package_type_name                



#         FROM `tabRequest For Quotation` rfq
#         LEFT JOIN
#             `tabVendor Type Master` vt ON rfq.select_service = vt.name
#         LEFT JOIN
#             `tabCompany Master` comp ON rfq.division = comp.name
#         LEFT JOIN
#             `tabPort Master` prt ON rfq.destination_port = prt.name
#         LEFT JOIN
#             `tabPort Master` prt2 ON rfq.port_of_loading = prt2.name
#         LEFT JOIN
#             `tabPort Master` prt4 ON rfq.destination_port = prt4.name
#         LEFT JOIN
#             `tabPort Master` pt ON rfq.port_code = pt.name
#         LEFT JOIN
#             `tabCountry Master` cnt ON rfq.country = cnt.name
#         LEFT JOIN
#             `tabIncoterm Master` inc ON rfq.inco_terms = inc.name
#         LEFT JOIN
#             `tabPackage Type Master` pty ON rfq.package_type = pty.name
#         LEFT JOIN
#             `tabProduct Category Master` pcat ON rfq.product_category = pcat.name
#         LEFT JOIN
#             `tabShipment Type Master` sty ON rfq.shipment_type = sty.name
#         LEFT JOIN
#             `tabRFQ Type Master` rft ON rfq.rfq_type = rft.name
#         LEFT JOIN
#             `tabMaterial Master` mm ON rfq.material = mm.name
#         LEFT JOIN
#             `tabCompany Master` comp2 ON rfq.company_code = comp2.name
#         LEFT JOIN
#             `tabPurchase Organization Master` porg ON rfq.purchase_organization = porg.name
#         LEFT JOIN
#             `tabPurchase Group Master` pg ON rfq.purchase_group = pg.name
#         LEFT JOIN
#             `tabCurrency Master` cur ON rfq.currency = cur.name
#         LEFT JOIN
#             `tabProduct Master` pd ON rfq.item_code = pd.name
#         LEFT JOIN
#             `tabProduct Category Master` pdc ON rfq.item_code = pdc.name
#         LEFT JOIN
#             `tabMaterial Category Master` mtc ON rfq.material_category = mtc.name
#         LEFT JOIN
#             `tabPlant Master` pltm ON rfq.plant_code = pltm.name
#         LEFT JOIN
#             `tabVendor Master` vm2 ON rfq.vendor_code = vm2.name
#         LEFT JOIN
#             `tabProduct Category Master` productcat ON rfq.product_category = productcat.name
#         LEFT JOIN
#             `tabQuotation` ReFQ ON ReFQ.rfq_number = rfq.name
#         LEFT JOIN
#             `tabPackage Type Master` pck ON rfq.package_type = pck.name



#         WHERE rfq.name=%s


#         """,(name), as_dict=1)

#     rfq_items = frappe.db.sql("""

#         SELECT 

#         pd.product_code AS product_code,
#         pd2.product_name AS product_name,
#         rqi.quantity AS quantity,
#         rqi.price AS price 

#         FROM `tabRFQ Items` rqi

#         LEFT JOIN
#             `tabProduct Master` pd ON rqi.product_code = pd.name
#         LEFT JOIN
#             `tabProduct Master` pd2 ON rqi.product_name = pd2.name

#         WHERE rqi.name=%s

#         """,(name), as_dict=1)

#     all_values = {

#         "rfq_details": rfq[0],
#         "rfq_items": rfq_items

#     }
#     print("*******************************")
#     print(rfq)
#     print(rfq_items)

#     return rfq, rfq_items

@frappe.whitelist()
def show_rfq_detail_with_items(name):
    rfq = frappe.db.sql(""" 
        SELECT
        rfq.name AS rfq_number,
        prt4.port_name AS destination_port,
        rfq.meril_invoice_date AS meril_invoice_date,
        vt.vendor_type_name AS vendor_type_name,
        rfq.rfq_cutoff_date AS rfq_cutoff_date,
        comp.company_name AS division_name,
        rfq.mode_of_shipment AS mode_of_shipment,
        prt.port_name AS port_name,
        rfq.ship_to_address AS ship_to_address,
        rfq.no_of_pkg_units As no_of_pkg_units,
        rfq.vol_weight AS vol_weight,
        rfq.invoice_date AS invoice_date,
        rfq.shipment_date AS shipment_date,
        rfq.remarks AS remarks,
        rfq.consignee_name AS consignee_name,
        rfq.sr_no AS sr_no,
        rfq.rfq_date AS rfq_date,
        cnt.country_name AS country_name,
        pt.port_code AS port_code,
        inc.incoterm_name AS incoterm_name,
        pty.package_name AS package_name,
        pcat.product_category_name AS product_category_name,
        rfq.actual_weight AS actual_weight,
        rfq.invoice_no AS invoice_no,
        sty.shipment_type_name AS shipment_type_name,
        rft.rfq_name AS rfq_name,
        rfq.raised_by AS raised_by,
        rfq.status AS status,
        mm.material_name AS material_name,
        rfq.quantity AS quantity,
        rfq.required_by AS required_by,
        rfq.pr_code AS pr_code,
        comp2.company_code AS company_code,
        porg.purchase_organization_name AS purchase_organization_name,
        pg.purchase_group_name AS purchase_group_name,
        cur.currency_name AS currency_name,
        rfq.collection_number AS collection_number,
        rfq.quotation_deadline AS quotation_deadline,
        rfq.validity_start_date AS validity_start_date,
        rfq.validity_end_date AS validity_end_date,
        rfq.requestor_name AS requestor_name,
        pd.product_code AS product_code,
        pdc.product_category_name AS product_category_name,
        rfq.item_description AS item_description,
        rfq.item_dimension AS item_dimension,
        rfq.add_special_remarksif_any AS add_special_remarksif_any,
        mtc.material_category_name AS material_category_name,
        pltm.plant_code AS plant_code,
        rfq.short_text AS short_text,
        rfq.catalogue_number AS catalogue_number,
        rfq.make AS make,
        rfq.pack_size AS pack_size,
        rfq.rfq_quantity AS rfq_quantity,
        rfq.quantity_unit AS quantity_unit,
        rfq.delivery_date AS delivery_date,
        rfq.first_reminder AS first_reminder,
        rfq.second_reminder AS second_reminder,
        rfq.third_reminder AS third_reminder,
        rfq.non_negotiable AS non_negotiable,
        rfq.negotiable AS negotiable,
        vm2.name AS name,
        rfq.bidding_person AS bidding_person,
        rfq.select_language AS select_language,
        rfq.service_code AS service_code,
        rfq.service_category AS service_category,
        rfq.storage_location AS storage_location,
        productcat.product_category_name AS product_category,
        prt2.port_name AS port_of_loading,
        pck.package_name AS package_type_name 
                        
        FROM `tabRequest For Quotation` rfq
        LEFT JOIN
            `tabVendor Type Master` vt ON rfq.select_service = vt.name
        LEFT JOIN
            `tabCompany Master` comp ON rfq.division = comp.name
        LEFT JOIN
            `tabPort Master` prt ON rfq.destination_port = prt.name
        LEFT JOIN
            `tabPort Master` prt2 ON rfq.port_of_loading = prt2.name
        LEFT JOIN
            `tabPort Master` prt4 ON rfq.destination_port = prt4.name
        LEFT JOIN
            `tabPort Master` pt ON rfq.port_code = pt.name
        LEFT JOIN
            `tabCountry Master` cnt ON rfq.country = cnt.name
        LEFT JOIN
            `tabIncoterm Master` inc ON rfq.inco_terms = inc.name
        LEFT JOIN
            `tabPackage Type Master` pty ON rfq.package_type = pty.name
        LEFT JOIN
            `tabProduct Category Master` pcat ON rfq.product_category = pcat.name
        LEFT JOIN
            `tabShipment Type Master` sty ON rfq.shipment_type = sty.name
        LEFT JOIN
            `tabRFQ Type Master` rft ON rfq.rfq_type = rft.name
        LEFT JOIN
            `tabMaterial Master` mm ON rfq.material = mm.name
        LEFT JOIN
            `tabCompany Master` comp2 ON rfq.company_code = comp2.name
        LEFT JOIN
            `tabPurchase Organization Master` porg ON rfq.purchase_organization = porg.name
        LEFT JOIN
            `tabPurchase Group Master` pg ON rfq.purchase_group = pg.name
        LEFT JOIN
            `tabCurrency Master` cur ON rfq.currency = cur.name
        LEFT JOIN
            `tabProduct Master` pd ON rfq.item_code = pd.name
        LEFT JOIN
            `tabProduct Category Master` pdc ON rfq.item_code = pdc.name
        LEFT JOIN
            `tabMaterial Category Master` mtc ON rfq.material_category = mtc.name
        LEFT JOIN
            `tabPlant Master` pltm ON rfq.plant_code = pltm.name
        LEFT JOIN
            `tabVendor Master` vm2 ON rfq.vendor_code = vm2.name
        LEFT JOIN
            `tabProduct Category Master` productcat ON rfq.product_category = productcat.name
        LEFT JOIN
             `tabPackage Type Master` pck ON rfq.package_type = pck.name
        WHERE rfq.name=%s
        """, (name), as_dict=1)

#use def again error in frontend.
    rfq_items = frappe.db.sql("""
        SELECT 
        pd.product_code AS product_code,
        pd2.product_name AS product_name,
        rqi.quantity AS quantity,
        rqi.price AS price 
        FROM `tabRFQ Items` rqi
        LEFT JOIN
            `tabProduct Master` pd ON rqi.product_code = pd.name
        LEFT JOIN
            `tabProduct Master` pd2 ON rqi.product_name = pd2.name
        WHERE rqi.parent=%s
        """, (name), as_dict=1)

    all_values = {
        "rfq_details": rfq[0],
        "rfq_items": rfq_items
    }
    return all_values


# @frappe.whitelist()
# def show_rfq_and_item_details(name):
#     rfq = frappe.db.sql(""" 

#         SELECT
#         rfq.name AS rfq_number,
#         prt4.port_name AS destination_port,
#         rfq.meril_invoice_date AS meril_invoice_date,
#         vt.vendor_type_name AS vendor_type_name,
#         rfq.rfq_cutoff_date AS rfq_cutoff_date,
#         comp.company_name AS division_name,
#         rfq.mode_of_shipment AS mode_of_shipment,
#         prt.port_name AS port_name,
#         rfq.ship_to_address AS ship_to_address,
#         rfq.no_of_pkg_units As no_of_pkg_units,
#         rfq.vol_weight AS vol_weight,
#         rfq.invoice_date AS invoice_date,
#         rfq.shipment_date AS shipment_date,
#         rfq.remarks AS remarks,
#         rfq.consignee_name AS consignee_name,
#         rfq.sr_no AS sr_no,
#         rfq.rfq_date AS rfq_date,
#         cnt.country_name AS country_name,
#         pt.port_code AS port_code,
#         inc.incoterm_name AS incoterm_name,
#         pty.package_name AS package_name,
#         pcat.product_category_name AS product_category_name,
#         rfq.actual_weight AS actual_weight,
#         rfq.invoice_no AS invoice_no,
#         sty.shipment_type_name AS shipment_type_name,
#         rft.rfq_name AS rfq_name,
#         rfq.raised_by AS raised_by,
#         rfq.status AS status,
#         mm.material_name AS material_name,
#         rfq.quantity AS quantity,
#         rfq.required_by AS required_by,
#         rfq.pr_code AS pr_code,
#         comp2.company_code AS company_code,
#         porg.purchase_organization_name AS purchase_organization_name,
#         pg.purchase_group_name AS purchase_group_name,
#         cur.currency_name AS currency_name,
#         rfq.collection_number AS collection_number,
#         rfq.quotation_deadline AS quotation_deadline,
#         rfq.validity_start_date AS validity_start_date,
#         rfq.validity_end_date AS validity_end_date,
#         rfq.requestor_name AS requestor_name,
#         pd.product_code AS product_code,
#         pdc.product_category_name AS product_category_name,
#         rfq.item_description AS item_description,
#         rfq.item_dimension AS item_dimension,
#         rfq.add_special_remarksif_any AS add_special_remarksif_any,
#         mtc.material_category_name AS material_category_name,
#         pltm.plant_code AS plant_code,
#         rfq.short_text AS short_text,
#         rfq.catalogue_number AS catalogue_number,
#         rfq.make AS make,
#         rfq.pack_size AS pack_size,
#         rfq.rfq_quantity AS rfq_quantity,
#         rfq.quantity_unit AS quantity_unit,
#         rfq.delivery_date AS delivery_date,
#         rfq.first_reminder AS first_reminder,
#         rfq.second_reminder AS second_reminder,
#         rfq.third_reminder AS third_reminder,
#         rfq.non_negotiable AS non_negotiable,
#         rfq.negotiable AS negotiable,
#         vm2.name AS name,
#         rfq.bidding_person AS bidding_person,
#         rfq.select_language AS select_language,
#         rfq.service_code AS service_code,
#         rfq.service_category AS service_category,
#         rfq.storage_location AS storage_location,
#         productcat.product_category_name AS product_category,
#         ReFQ.rfq_quantity AS rfq_quantity



#         FROM `tabRequest For Quotation` rfq
#         LEFT JOIN
#             `tabVendor Type Master` vt ON rfq.select_service = vt.name
#         LEFT JOIN
#             `tabCompany Master` comp ON rfq.division = comp.name
#         LEFT JOIN
#             `tabPort Master` prt ON rfq.destination_port = prt.name
#         LEFT JOIN
#             `tabPort Master` prt2 ON rfq.port_of_loading = prt2.name
#         LEFT JOIN
#             `tabPort Master` prt4 ON rfq.destination_port = prt4.name
#         LEFT JOIN
#             `tabPort Master` pt ON rfq.port_code = pt.name
#         LEFT JOIN
#             `tabCountry Master` cnt ON rfq.country = cnt.name
#         LEFT JOIN
#             `tabIncoterm Master` inc ON rfq.inco_terms = inc.name
#         LEFT JOIN
#             `tabPackage Type Master` pty ON rfq.package_type = pty.name
#         LEFT JOIN
#             `tabProduct Category Master` pcat ON rfq.product_category = pcat.name
#         LEFT JOIN
#             `tabShipment Type Master` sty ON rfq.shipment_type = sty.name
#         LEFT JOIN
#             `tabRFQ Type Master` rft ON rfq.rfq_type = rft.name
#         LEFT JOIN
#             `tabMaterial Master` mm ON rfq.material = mm.name
#         LEFT JOIN
#             `tabCompany Master` comp2 ON rfq.company_code = comp2.name
#         LEFT JOIN
#             `tabPurchase Organization Master` porg ON rfq.purchase_organization = porg.name
#         LEFT JOIN
#             `tabPurchase Group Master` pg ON rfq.purchase_group = pg.name
#         LEFT JOIN
#             `tabCurrency Master` cur ON rfq.currency = cur.name
#         LEFT JOIN
#             `tabProduct Master` pd ON rfq.item_code = pd.name
#         LEFT JOIN
#             `tabProduct Category Master` pdc ON rfq.item_code = pdc.name
#         LEFT JOIN
#             `tabMaterial Category Master` mtc ON rfq.material_category = mtc.name
#         LEFT JOIN
#             `tabPlant Master` pltm ON rfq.plant_code = pltm.name
#         LEFT JOIN
#             `tabVendor Master` vm2 ON rfq.vendor_code = vm2.name
#         LEFT JOIN
#             `tabProduct Category Master` productcat ON rfq.product_category = productcat.name
#         LEFT JOIN
#             `tabQuotation` ReFQ ON ReFQ.rfq_number = rfq.name
        



#         WHERE rfq.name=%s


#         """,(name), as_dict=1)

#     rfq_items = frappe.db.sql("""

#         SELECT 

#         pd.product_code AS product_code,
#         pd2.product_name AS product_name,
#         rqi.quantity AS quantity,
#         rqi.price AS price 

#         FROM `tabRFQ Items` rqi

#         LEFT JOIN
#             `tabProduct Master` pd ON rqi.product_code = pd.name
#         LEFT JOIN
#             `tabProduct Master` pd2 ON rqi.product_name = pd2.name

#         WHERE rqi.name=%s

#         """,(name), as_dict=1)

#     all_values = {

#         "rfq_details": rfq[0],
#         "rfq_items": rfq_items

#     }
#     print("*******************************")
#     print(rfq)
#     print(rfq_items)

#     return rfq, rfq_items

# ****************************************MASTER DATA QUERY********************************************


# @frappe.whitelist()
# def importt():
#     excel_file_path = '/home/rishi_hingad/account_group_master.xlsx'

#     # Read the Excel file into a DataFrame
#     df = pd.read_excel(excel_file_path)

#     try:
#         for index, row in df.iterrows():
#             account_group_name = row['account_group_name']
#             purchase_organisation = row['purchase_organisation']
#             account_group_code = row['account_group_name']
#             # account_group_description = row['account_group_description']
            
#             # Check if 'description' column exists
#             if 'description' in row:
#                 description = row['description']
#             else:
#                 # Handle the missing 'description' column case
#                 description = ''

#             # Create the document
#             account_group_master = frappe.get_doc({
#                 'doctype': 'Account Group Master',
#                 'account_group_name': account_group_name,
#                 'purchase_organisation': purchase_organisation,
#                 'account_group_code': account_group_name
#                 # 'account_group_description': account_group_description
#             })

#             # Insert the document into the database
#             account_group_master.insert()
#             frappe.db.commit()

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), 'Account Group Master Error')
#         frappe.throw(str(e))

# @frappe.whitelist()
# def importt():
#     excel_file_path = '/home/rishi_hingad/company_master.xlsx'

   
#     df = pd.read_excel(excel_file_path)

#     try:
#         for index, row in df.iterrows():
#             company_code = row['company_code']
#             company_name = row['company_name']
           

            
#             new_company = frappe.get_doc({
#                 'doctype': 'Company Master',
#                 'company_code': company_code,
#                 'company_name': company_name
                
#             })
            
            
#             new_company.insert()
#             frappe.db.commit()

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), 'Company Master Import Error')
#         frappe.throw(str(e))

#*******************************************show rfq with its items CLOSED**************************************

@frappe.whitelist()
def show_rfq_detail(rfq_number):

    rfq = frappe.db.sql(""" 

        SELECT
        rfq.name AS rfq_number,
        prt4.port_name AS destination_port,
        rfq.meril_invoice_date AS meril_invoice_date,
        vt.vendor_type_name AS vendor_type_name,
        rfq.rfq_cutoff_date AS rfq_cutoff_date,
        comp.company_name AS division_name,
        rfq.mode_of_shipment AS mode_of_shipment,
        prt.port_name AS port_name,
        rfq.ship_to_address AS ship_to_address,
        rfq.no_of_pkg_units As no_of_pkg_units,
        rfq.vol_weight AS vol_weight,
        rfq.invoice_date AS invoice_date,
        rfq.shipment_date AS shipment_date,
        rfq.remarks AS remarks,
        rfq.consignee_name AS consignee_name,
        rfq.sr_no AS sr_no,
        rfq.rfq_date AS rfq_date,
        cnt.country_name AS country_name,
        pt.port_code AS port_code,
        inc.incoterm_name AS incoterm_name,
        pty.package_name AS package_name,
        pcat.product_category_name AS product_category_name,
        rfq.actual_weight AS actual_weight,
        rfq.invoice_no AS invoice_no,
        sty.shipment_type_name AS shipment_type_name,
        rft.rfq_name AS rfq_name,
        rfq.raised_by AS raised_by,
        rfq.status AS status,
        mm.material_name AS material_name,
        rfq.quantity AS quantity,
        rfq.required_by AS required_by,
        rfq.pr_code AS pr_code,
        comp2.company_code AS company_code,
        porg.purchase_organization_name AS purchase_organization_name,
        pg.purchase_group_name AS purchase_group_name,
        cur.currency_name AS currency_name,
        rfq.collection_number AS collection_number,
        rfq.quotation_deadline AS quotation_deadline,
        rfq.validity_start_date AS validity_start_date,
        rfq.validity_end_date AS validity_end_date,
        rfq.requestor_name AS requestor_name,
        pd.product_code AS product_code,
        pdc.product_category_name AS product_category_name,
        rfq.item_description AS item_description,
        rfq.item_dimension AS item_dimension,
        rfq.add_special_remarksif_any AS add_special_remarksif_any,
        mtc.material_category_name AS material_category_name,
        pltm.plant_code AS plant_code,
        rfq.short_text AS short_text,
        rfq.catalogue_number AS catalogue_number,
        rfq.make AS make,
        rfq.pack_size AS pack_size,
        rfq.rfq_quantity AS rfq_quantity,
        rfq.quantity_unit AS quantity_unit,
        rfq.delivery_date AS delivery_date,
        rfq.first_reminder AS first_reminder,
        rfq.second_reminder AS second_reminder,
        rfq.third_reminder AS third_reminder,
        rfq.non_negotiable AS non_negotiable,
        rfq.negotiable AS negotiable,
        vm2.name AS name,
        rfq.bidding_person AS bidding_person,
        rfq.select_language AS select_language,
        rfq.service_code AS service_code,
        rfq.service_category AS service_category,
        rfq.storage_location AS storage_location,
        productcat.product_category_name AS product_category



        FROM `tabRequest For Quotation` rfq
        LEFT JOIN
            `tabVendor Type Master` vt ON rfq.select_service = vt.name
        LEFT JOIN
            `tabCompany Master` comp ON rfq.division = comp.name
        LEFT JOIN
            `tabPort Master` prt ON rfq.destination_port = prt.name
        LEFT JOIN
            `tabPort Master` prt2 ON rfq.port_of_loading = prt2.name
        LEFT JOIN
            `tabPort Master` prt4 ON rfq.destination_port = prt4.name
        LEFT JOIN
            `tabPort Master` pt ON rfq.port_code = pt.name
        LEFT JOIN
            `tabCountry Master` cnt ON rfq.country = cnt.name
        LEFT JOIN
            `tabIncoterm Master` inc ON rfq.inco_terms = inc.name
        LEFT JOIN
            `tabPackage Type Master` pty ON rfq.package_type = pty.name
        LEFT JOIN
            `tabProduct Category Master` pcat ON rfq.product_category = pcat.name
        LEFT JOIN
            `tabShipment Type Master` sty ON rfq.shipment_type = sty.name
        LEFT JOIN
            `tabRFQ Type Master` rft ON rfq.rfq_type = rft.name
        LEFT JOIN
            `tabMaterial Master` mm ON rfq.material = mm.name
        LEFT JOIN
            `tabCompany Master` comp2 ON rfq.company_code = comp2.name
        LEFT JOIN
            `tabPurchase Organization Master` porg ON rfq.purchase_organization = porg.name
        LEFT JOIN
            `tabPurchase Group Master` pg ON rfq.purchase_group = pg.name
        LEFT JOIN
            `tabCurrency Master` cur ON rfq.currency = cur.name
        LEFT JOIN
            `tabProduct Master` pd ON rfq.item_code = pd.name
        LEFT JOIN
            `tabProduct Category Master` pdc ON rfq.item_code = pdc.name
        LEFT JOIN
            `tabMaterial Category Master` mtc ON rfq.material_category = mtc.name
        LEFT JOIN
            `tabPlant Master` pltm ON rfq.plant_code = pltm.name
        LEFT JOIN
            `tabVendor Master` vm2 ON rfq.vendor_code = vm2.name
        LEFT JOIN
            `tabProduct Category Master` productcat ON rfq.product_category = productcat.name



        WHERE rfq.name=%s


        """,(rfq_number), as_dict=1)

    return rfq 
################## NEW API ############################### 
# @frappe.whitelist()
# def show_vendor_registration_details_filtered(**kwargs):

    
#     status = kwargs.get('status')

#     vendor = frappe.db.sql(""" 

#         SELECT
#             --cm.company_name AS company_name,
#             -- cm.company_code AS company_code,
#             vm.website AS website,
#             vt.vendor_type_name As vendor_type_name,
#             at.account_group_name AS account_group_name,
#             dp.department_name AS department_name,
#             mt.material_name AS material_name,
#             vm.search_term AS search_term,
#             bn.business_nature_name AS business_nature_name,
#             vm.payee AS payee_in_document,
#             vm.gr_based_inv_ver AS gr_based_inv_ver,
#             vm.service_based_inv_ver AS service_based_inv_ver,
#             vm.check_double_invoice AS check_double_invoice,
#             oc.currency_name AS currency_name,
#             tp.terms_of_payment_name As terms_of_payment_name,
#             inc.incoterm_name As incoterm_name,
#             pg.purchase_group_name AS purchase_group_name,
#             vm.registered_date AS registered_date,
#             vm.purchase_organization AS company_name,
#             vm.type_of_business AS type_of_business,
#             vm.size_of_company AS size_of_company,
#             vm.registered_office_number AS registered_office_number,
#             vm.telephone_number AS telephone_number,
#             vm.established_year AS established_year,
#             vm.office_email_primary AS office_email_primary,
#             vm.office_email_secondary AS office_email_secondary,
#             vm.corporate_identification_number As corporate_identification_number,
#             vm.cin_date AS cin_date,
#             con.company_nature_name AS company_nature_name,
#             vm.vendor_name AS vendor_name,
#             rfq.rfq_name AS rfq_name,
#             vm.mobile_number AS mobile_number,
#             vm.office_address_line_1 AS office_address_line_1,
#             vm.office_address_line_2 AS office_address_line_2,
#             vm.office_address_line_3 AS office_address_line_3,
#             vm.office_address_line_4 AS office_address_line_4,
#             cty.city_name AS city_name,
#             st.state_name AS state_name,
#             cnt.country_name AS country_name,
#             dst.district_name As district_name,
#             pin.pincode AS pincode,
#             vm.manufacturing_address_line_1 AS manufacturing_address_line_1,
#             vm.manufacturing_address_line_2 AS manufacturing_address_line_2,
#             vm.manufacturing_address_line_3 AS manufacturing_address_line_3,
#             vm.manufacturing_address_line_4 AS manufacturing_address_line_4,
#             vm.registered_by As registered_by,
#             vm.purchase_head_approval AS purchase_head_approval,
#             vm.purchase_team_approval AS purchase_team_approval,
#             vm.accounts_team_approval AS accounts_team_approval,
#             vm.status AS status,
#             vm.vendor_code AS vendor_code,
#             cmm.company_name AS company_name,
#             vm.creation AS creation


#             FROM `tabVendor Master` vm 
#             --LEFT JOIN
#               --  `tabCompany Master` cm ON vm.company_name = cm.company_name
#             LEFT JOIN
#                 `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#             LEFT JOIN
#                 `tabAccount Group Master` at ON vm.account_group = at.name
#             LEFT JOIN
#                 `tabDepartment Master` dp ON vm.department = dp.name
#             LEFT JOIN
#                 `tabMaterial Master` mt ON vm.material_to_be_supplied = mt.name
#             LEFT JOIN
#                 `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
#             LEFT JOIN
#                 `tabCurrency Master` oc ON vm.order_currency = oc.name
#             LEFT JOIN
#                 `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
#             LEFT JOIN
#                 `tabIncoterm Master` inc ON vm.incoterms = inc.name
#             LEFT JOIN
#                 `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
#             LEFT JOIN
#                 `tabCompany Nature Master` con ON vm.nature_of_company = con.name
#             LEFT JOIN
#                 `tabRFQ Type Master` rfq ON vm.rfq_type = rfq.name
#             LEFT JOIN
#                 `tabCompany Master` ct ON vm.city = ct.name
#             LEFT JOIN
#                 `tabState Master` st ON vm.state = st.name
#             LEFT JOIN
#                 `tabCountry Master` cnt ON vm.country = cnt.name
#             LEFT JOIN
#                 `tabDistrict Master` dst ON vm.district = dst.name
#             LEFT JOIN
#                 `tabPincode Master` pin ON vm.pincode = pin.name
#             LEFT JOIN
#                 `tabCity Master` cty ON vm.city = cty.name
#              LEFT JOIN
#                  `tabCompany Master` cmm ON vm.company_name = cmm.name

#             where status=%s ORDER BY creation DESC



#         """,(status), as_dict=1)
#     return vendor

@frappe.whitelist()
def show_vendor_registration_details_filtered(**kwargs):
    status = kwargs.get('status')
    values_type = kwargs.get('values_type')

    if values_type == 'creation':
        order_by_clause = 'vm.creation DESC'
    elif values_type == 'modified':
        order_by_clause = 'vm.modified DESC'
    else:
        order_by_clause = 'vm.creation DESC'  # Default sorting

    vendor = frappe.db.sql(f"""
        SELECT
            vm.website AS website,
            vt.vendor_type_name AS vendor_type_name,
            at.account_group_name AS account_group_name,
            dp.department_name AS department_name,
            mt.material_name AS material_name,
            vm.search_term AS search_term,
            bn.business_nature_name AS business_nature_name,
            vm.payee AS payee_in_document,
            vm.gr_based_inv_ver AS gr_based_inv_ver,
            vm.service_based_inv_ver AS service_based_inv_ver,
            vm.check_double_invoice AS check_double_invoice,
            oc.currency_name AS currency_name,
            tp.terms_of_payment_name AS terms_of_payment_name,
            inc.incoterm_name AS incoterm_name,
            pg.purchase_group_name AS purchase_group_name,
            vm.registered_date AS registered_date,
            vm.purchase_organization AS company_name,
            vm.type_of_business AS type_of_business,
            vm.size_of_company AS size_of_company,
            vm.registered_office_number AS registered_office_number,
            vm.telephone_number AS telephone_number,
            vm.established_year AS established_year,
            vm.office_email_primary AS office_email_primary,
            vm.office_email_secondary AS office_email_secondary,
            vm.corporate_identification_number AS corporate_identification_number,
            vm.cin_date AS cin_date,
            con.company_nature_name AS company_nature_name,
            vm.vendor_name AS vendor_name,
            rfq.rfq_name AS rfq_name,
            vm.mobile_number AS mobile_number,
            vm.office_address_line_1 AS office_address_line_1,
            vm.office_address_line_2 AS office_address_line_2,
            vm.office_address_line_3 AS office_address_line_3,
            vm.office_address_line_4 AS office_address_line_4,
            cty.city_name AS city_name,
            st.state_name AS state_name,
            cnt.country_name AS country_name,
            dst.district_name AS district_name,
            pin.pincode AS pincode,
            vm.manufacturing_address_line_1 AS manufacturing_address_line_1,
            vm.manufacturing_address_line_2 AS manufacturing_address_line_2,
            vm.manufacturing_address_line_3 AS manufacturing_address_line_3,
            vm.manufacturing_address_line_4 AS manufacturing_address_line_4,
            vm.registered_by AS registered_by,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.status AS status,
            vm.vendor_code AS vendor_code,
            cmm.company_name AS company_name,
            vm.creation AS creation,
            vm.modified AS modified
                           
        FROM `tabVendor Master` vm 
        LEFT JOIN `tabVendor Type Master` vt ON vm.vendor_type = vt.name
        LEFT JOIN `tabAccount Group Master` at ON vm.account_group = at.name
        LEFT JOIN `tabDepartment Master` dp ON vm.department = dp.name
        LEFT JOIN `tabMaterial Master` mt ON vm.material_to_be_supplied = mt.name
        LEFT JOIN `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
        LEFT JOIN `tabCurrency Master` oc ON vm.order_currency = oc.name
        LEFT JOIN `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
        LEFT JOIN `tabIncoterm Master` inc ON vm.incoterms = inc.name
        LEFT JOIN `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
        LEFT JOIN `tabCompany Nature Master` con ON vm.nature_of_company = con.name
        LEFT JOIN `tabRFQ Type Master` rfq ON vm.rfq_type = rfq.name
        LEFT JOIN `tabCompany Master` ct ON vm.city = ct.name
        LEFT JOIN `tabState Master` st ON vm.state = st.name
        LEFT JOIN `tabCountry Master` cnt ON vm.country = cnt.name
        LEFT JOIN `tabDistrict Master` dst ON vm.district = dst.name
        LEFT JOIN `tabPincode Master` pin ON vm.pincode = pin.name
        LEFT JOIN `tabCity Master` cty ON vm.city = cty.name
        LEFT JOIN `tabCompany Master` cmm ON vm.company_name = cmm.name
        WHERE vm.status = %s 
        ORDER BY {order_by_clause}
    """, (status, ), as_dict=1)

    return vendor




#############################################################
@frappe.whitelist()
def show_in_process_vendors():

    all_vendors = frappe.db.sql(""" SELECT
    vm.name AS name,
    status AS status,
    purchase_team_approval AS purchase_team_approval,
    purchase_head_approval AS purchase_head_approval,
    accounts_team_approval AS accounts_team_approval,
    vendor_name AS vendor_name,
    cm.company_name AS company_name 
    
  

FROM 
    `tabVendor Master` vm 
LEFT JOIN 
    `tabCompany Master` cm ON vm.company_name = cm.name where status='In Process'


""", as_dict=1)

    return all_vendors

@frappe.whitelist()
def onboarded_vendors():

    all_vendors = frappe.db.sql(""" SELECT
    vm.name AS name,
    status AS status,
    purchase_team_approval AS purchase_team_approval,
    purchase_head_approval AS purchase_head_approval,
    accounts_team_approval AS accounts_team_approval,
    vendor_name AS vendor_name,
    cm.company_name AS company_name 
    
  

FROM 
    `tabVendor Master` vm 
LEFT JOIN 
    `tabCompany Master` cm ON vm.company_name = cm.name where status='Onboarded'


""", as_dict=1)

    return all_vendors

@frappe.whitelist()
def show_single_vendor(**kwargs):

    vendor_id = kwargs.get('name')
    single_vendor = frappe.db.sql(""" SELECT
    vm.name AS name,
    status AS status,
    purchase_team_approval AS purchase_team_approval,
    purchase_head_approval AS purchase_head_approval,
    accounts_team_approval AS accounts_team_approval,
    vendor_name AS vendor_name,
    cm.company_name AS company_name 
    
  

FROM 
    `tabVendor Master` vm 
LEFT JOIN 
    `tabCompany Master` cm ON vm.company_name = cm.name where vm.name=%s


""",(vendor_id),as_dict=1)

    return single_vendor


#*********************************On Vendor Onboarding Page load####################################

@frappe.whitelist()
def on_vendor_onboarding_page_load(**kwargs):

    name = kwargs.get('name')
    print("*********", name)

    vendor = frappe.db.sql(""" 

        SELECT
            cm.company_code AS company_code,  
            vt.vendor_type_name As vendor_type_name,
            at.account_group_name AS account_group_name,                       
            bn.business_nature_name AS business_nature_name,
            oc.currency_name AS currency_name,
            pg.purchase_group_name AS purchase_group_name,
            vm.purchase_organization AS company_name,
            vm.type_of_business AS type_of_business,
            vm.registered_office_number AS registered_office_number,
            vm.telephone_number AS telephone_number,
            vm.office_email_primary AS office_email_primary,
            vm.office_email_secondary AS office_email_secondary,
            vm.corporate_identification_number As corporate_identification_number,
            vm.cin_date AS cin_date,
            con.company_nature_name AS company_nature_name,
            vm.office_address_line_1 AS office_address_line_1,
            vm.office_address_line_2 AS office_address_line_2,
            vm.office_address_line_3 AS office_address_line_3,
            vm.office_address_line_4 AS office_address_line_4,
            cty.city_name AS city_name,
            st.state_name AS state_name,
            cnt.country_name AS country_name,
            dst.district_name As district_name,
            pin.pincode AS pincode


            FROM `tabVendor Master` vm 
            LEFT JOIN
                `tabCompany Master` cm ON vm.company_name = cm.name
            LEFT JOIN
                `tabVendor Type Master` vt ON vm.vendor_type = vt.name
            LEFT JOIN
                `tabAccount Group Master` at ON vm.account_group = at.name
            LEFT JOIN
                `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
            LEFT JOIN
                `tabCurrency Master` oc ON vm.order_currency = oc.name
            LEFT JOIN
                `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
            LEFT JOIN
                `tabIncoterm Master` inc ON vm.incoterms = inc.name
            LEFT JOIN
                `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
            LEFT JOIN
                `tabCompany Nature Master` con ON vm.nature_of_company = con.name

            LEFT JOIN
                `tabCompany Master` ct ON vm.city = ct.name
            LEFT JOIN
                `tabState Master` st ON vm.state = st.name
            LEFT JOIN
                `tabCountry Master` cnt ON vm.country = cnt.name
            LEFT JOIN
                `tabDistrict Master` dst ON vm.district = dst.name
            LEFT JOIN
                `tabPincode Master` pin ON vm.pincode = pin.name
            LEFT JOIN
                `tabCity Master` cty ON vm.city = cty.name

            where vm.name=%s



        """,(name), as_dict=1)
    return vendor



    # company_name,vendor_type,nature_of_business,order_currency,bank,city,district,state,country,office_email_primary,office_address_line_1,2,3,4,pincode,name,
    #office_email_secondary
    # telephone_number,cin_date



@frappe.whitelist()
def converttox(name):

    json_data = frappe.db.sql(""" SELECT payee, gr_based_inv_ver, service_based_inv_ver, check_double_invoice  FROM `tabVendor Master` where name=%s """, (name), as_dict=1)
    payee = 'X' if json_data[0]['payee'] == 1 else ''
    gr_based_inv_ver = 'X' if json_data[0]['gr_based_inv_ver'] == 1 else ''
    service_based_inv_ver = 'X' if json_data[0]['service_based_inv_ver'] == 1 else ''
    check_double_invoice = 'X' if json_data[0]['check_double_invoice'] == 1 else ''
    
    mylist = [payee, gr_based_inv_ver, service_based_inv_ver, check_double_invoice, ]

    return mylist, json_data


#*****************************************Vendor Onboarding Page Load Closed########################

# @frappe.whitelist(allow_guest=True)
#def sap_fetch_token(data, method):
# def sap_fetch_token(name):

#     name = name
#     print("*********************************", name)
#     vendor = frappe.db.sql(""" 
#     SELECT
#         cm.company_name AS company_name,
#         cm2.company_code AS company_code,
#         vm.website AS website,
#         vt.vendor_type_name As vendor_type_name,
#         at.account_group_name AS account_group_name,
#         dp.department_name AS department_name,
#         mt.material_name AS material_name,
#         vm.search_term AS search_term,
#         bn.business_nature_name AS business_nature_name,
#         vm.payee AS payee_in_document,
#         vm.gr_based_inv_ver AS gr_based_inv_ver,
#         vm.service_based_inv_ver AS service_based_inv_ver,
#         vm.check_double_invoice AS check_double_invoice,
#         oc.currency_code AS currency_code,
#         tp.terms_of_payment_name As terms_of_payment_name,
#         inc.incoterm_name As incoterm_name,
#         pg.purchase_group_name AS purchase_group_name,
#         pg2.purchase_organization_code AS purchase_organization_code,
#         vm.registered_date AS registered_date,
#         vm.purchase_organization AS company_name,
#         vm.type_of_business AS type_of_business,
#         vm.size_of_company AS size_of_company,
#         vm.registered_office_number AS registered_office_number,
#         vm.telephone_number AS telephone_number,
#         vm.established_year AS established_year,
#         vm.office_email_primary AS office_email_primary,
#         vm.office_email_secondary AS office_email_secondary,
#         vm.corporate_identification_number As corporate_identification_number,
#         vm.cin_date AS cin_date,
#         con.company_nature_name AS company_nature_name,
#         vm.vendor_name AS vendor_name,
#         rfq.rfq_name AS rfq_name,
#         vm.mobile_number AS mobile_number,
#         vm.office_address_line_1 AS office_address_line_1,
#         vm.office_address_line_2 AS office_address_line_2,
#         vm.office_address_line_3 AS office_address_line_3,
#         vm.office_address_line_4 AS office_address_line_4,
#         cty.city_name AS city_name,
#         st.state_name AS state_name,
#         cnt.country_code AS country_code,
#         dst.district_name As district_name,
#         pin.pincode AS pincode,
#         vm.manufacturing_address_line_1 AS manufacturing_address_line_1,
#         vm.manufacturing_address_line_2 AS manufacturing_address_line_2,
#         vm.manufacturing_address_line_3 AS manufacturing_address_line_3,
#         vm.manufacturing_address_line_4 AS manufacturing_address_line_4,
#         vm.registered_by As registered_by,
#         vm.purchase_head_approval AS purchase_head_approval,
#         vm.purchase_team_approval AS purchase_team_approval,
#         vm.accounts_team_approval AS accounts_team_approval,
#         vm.status AS status,
#         vm.vendor_code AS vendor_code,
#         inc2.incoterm_name AS incoterm_name2,
#         vm.gst_number AS gst_number,
#         vm.pan_number AS pan_number,
#         bk.bank_name AS bank_name,
#         vm.account_number AS account_number

#     FROM `tabVendor Master` vm 
#     LEFT JOIN
#         `tabCompany Master` cm ON vm.company_name = cm.name
#     LEFT JOIN
#         `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#     LEFT JOIN
#         `tabAccount Group Master` at ON vm.account_group = at.name
#     LEFT JOIN
#         `tabDepartment Master` dp ON vm.department = dp.name
#     LEFT JOIN
#         `tabMaterial Master` mt ON vm.material_to_be_supplied = mt.name
#     LEFT JOIN
#         `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
#     LEFT JOIN
#         `tabCurrency Master` oc ON vm.order_currency = oc.name
#     LEFT JOIN
#         `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
#     LEFT JOIN
#         `tabIncoterm Master` inc ON vm.incoterms = inc.name
#     LEFT JOIN
#         `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
#     LEFT JOIN
#         `tabPurchase Organization Master` pg2 ON vm.purchase_organization = pg2.name
#     LEFT JOIN
#         `tabCompany Nature Master` con ON vm.nature_of_company = con.name
#     LEFT JOIN
#         `tabRFQ Type Master` rfq ON vm.rfq_type = rfq.name
#     LEFT JOIN
#         `tabCompany Master` ct ON vm.city = ct.name
#     LEFT JOIN
#         `tabState Master` st ON vm.state = st.name
#     LEFT JOIN
#         `tabCountry Master` cnt ON vm.country = cnt.name
#     LEFT JOIN
#         `tabDistrict Master` dst ON vm.district = dst.name
#     LEFT JOIN
#         `tabPincode Master` pin ON vm.pincode = pin.name
#     LEFT JOIN
#         `tabCity Master` cty ON vm.city = cty.name
#     LEFT JOIN
#         `tabCompany Master` cm2 ON vm.company_code = cm2.name
#     LEFT JOIN
#         `tabIncoterm Master` inc2 ON vm.incoterms2 = inc2.name
#     LEFT JOIN
#         `tabBank Master` bk ON vm.bank1 = bk.name

#     WHERE vm.name=%s
# """, (name), as_dict=1)

#     company_code = vendor[0].get('company_code') if vendor else None
#     purchase_organization_code = vendor[0].get('purchase_organization_code') if vendor else None
#     account_group_name = vendor[0].get('account_group_name') if vendor else None
#     vendor_name = vendor[0].get('vendor_name') if vendor else None
#     search_term = vendor[0].get('search_term') if vendor else None
#     office_address_line_1 = vendor[0].get('office_address_line_1') if vendor else None
#     pincode = vendor[0].get('pincode') if vendor else None
#     city = vendor[0].get('city_name') if vendor else None
#     country = vendor[0].get('country_code') if vendor else None
#     mobile_number = vendor[0].get('mobile_number') if vendor else None
#     office_email_primary = vendor[0].get('office_email_primary') if vendor else None
#     office_email_secondary = vendor[0].get('office_email_secondary') if vendor else None
#     currency_code = vendor[0].get('currency_code') if vendor else None
#     incoterm_name = vendor[0].get('incoterm_name') if vendor else None
#     incoterms2 = vendor[0].get('incoterm_name2') if vendor else None
#     purchase_group_name = vendor[0].get('purchase_group_name') if vendor else None
#     gst_number = vendor[0].get('gst_number') if vendor else None
#     vendor_type_name = vendor[0].get('vendor_type_name') if vendor else None
#     pan_number = vendor[0].get('pan_number') if vendor else None
#     bank_name = vendor[0].get('bank_name') if vendor else None
#     account_number = vendor[0].get('account_number') if vendor else None
#     print("(************************************()()()()())()()()(()()()()())","From sap_fetch_token")

#     data =  {
#     "Bukrs": company_code,
#     "Ekorg": purchase_organization_code,
#     "Ktokk": account_group_name,
#     "Title": "",
#     "Name1": vendor_name,
#     "Name2": "",
#     "Sort1": search_term,
#     "Street": office_address_line_1,
#     "StrSuppl1": office_address_line_1,
#     "StrSuppl2": "",
#     "StrSuppl3": "",
#     "PostCode1": pincode,
#     "City1": city,
#     "Country": country,
#     "J1kftind": "",
#     "Region": "6",
#     "TelNumber": "",
#     "MobNumber": mobile_number,
#     "SmtpAddr": office_email_primary,
#     "SmtpAddr1": office_email_secondary,
#     "Zuawa": "",
#     "Akont": "16101020",
#     "Waers": currency_code,
#     "Zterm": "Z072",
#     "Inco1": incoterm_name,
#     "Inco2": incoterms2,
#     "Kalsk": "",
#     "Ekgrp": purchase_group_name,
#     "Xzemp": "X",
#     "Reprf": "X",
#     "Webre": "X",
#     "Lebre": "",
#     "Stcd3": gst_number,
#     "J1ivtyp": vendor_type_name,
#     "J1ipanno": pan_number,
#     "J1ipanref": "Hitesh Mahto",
#     "Namev": "Hitesh",
#     "Name11": "Mahto",
#     "Bankl": bank_name,
#     "Bankn": account_number,
#     "Bkref": "2001",
#     "Banka": "UTIB0019191",
#     "Xezer": "",
#     "Refno": "VMS/368b008a78/0101",
#     "Vedno": "",
#     "Zmsg": ""

#         }

#     url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
#     headers = {
#     'X-CSRF-TOKEN': 'Fetch',
#      'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ=',
#      'Content-Type': 'application/json'
#     }
#     auth = HTTPBasicAuth('WF-BATCH ', 'M@wb#$%2024')
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         print("******GET CSRF TOKEN*********")
#         csrf_token = response.headers.get('x-csrf-token')
#         key1 = response.cookies.get('SAP_SESSIONID_BHD_200')
#         key2 = response.cookies.get('sap-usercontext')
#         send_detail(csrf_token, data, key1, key2, name)
#         print("*******************KEYYYYY********", key1)
#         print(key2)

#         print(csrf_token)
#         print(response.headers.get('x-csrf-token'))
#         return data
  
        
#        # return csrf_token
#     else:
#         print("Error:", response.status_code)
#        # return "Error: " + str(response.status_code)
#         #send_detail("*************************",csrf_token)


#==========================================================================
# @frappe.whitelist(allow_guest=True)
# def sap_fetch_token(name):

#     name = name
#     print("*********************************", name)
#     vendor = frappe.db.sql(""" 
#     SELECT
#         cm.company_name AS company_name,
#         cm2.company_code AS company_code,
#         vm.website AS website,
#         vt.vendor_type_name As vendor_type_name,
#         at.account_group_name AS account_group_name,
#         dp.department_name AS department_name,
#         mt.material_name AS material_name,
#         vm.search_term AS search_term,
#         bn.business_nature_name AS business_nature_name,
#         vm.payee_in_document AS payee_in_document,
#         vm.gr_based_inv_ver AS gr_based_inv_ver,
#         vm.service_based_inv_ver AS service_based_inv_ver,
#         vm.check_double_invoice AS check_double_invoice,
#         oc.currency_code AS currency_code,
#         tp.terms_of_payment_name As terms_of_payment_name,
#         inc.incoterm_name As incoterm_name,
#         pg.purchase_group_name AS purchase_group_name,
#         pg2.purchase_organization_code AS purchase_organization_code,
#         vm.registered_date AS registered_date,
#         vm.purchase_organization AS company_name,
#         vm.type_of_business AS type_of_business,
#         vm.size_of_company AS size_of_company,
#         vm.registered_office_number AS registered_office_number,
#         vm.telephone_number AS telephone_number,
#         vm.established_year AS established_year,
#         vm.office_email_primary AS office_email_primary,
#         vm.office_email_secondary AS office_email_secondary,
#         vm.corporate_identification_number As corporate_identification_number,
#         vm.cin_date AS cin_date,
#         con.company_nature_name AS company_nature_name,
#         vm.vendor_name AS vendor_name,
#         rfq.rfq_name AS rfq_name,
#         vm.mobile_number AS mobile_number,
#         vm.office_address_line_1 AS office_address_line_1,
#         vm.office_address_line_2 AS office_address_line_2,
#         vm.office_address_line_3 AS office_address_line_3,
#         vm.office_address_line_4 AS office_address_line_4,
#         cty.city_name AS city_name,
#         st.state_name AS state_name,
#         cnt.country_code AS country_code,
#         dst.district_name As district_name,
#         pin.pincode AS pincode,
#         vm.manufacturing_address_line_1 AS manufacturing_address_line_1,
#         vm.manufacturing_address_line_2 AS manufacturing_address_line_2,
#         vm.manufacturing_address_line_3 AS manufacturing_address_line_3,
#         vm.manufacturing_address_line_4 AS manufacturing_address_line_4,
#         vm.registered_by As registered_by,
#         vm.purchase_head_approval AS purchase_head_approval,
#         vm.purchase_team_approval AS purchase_team_approval,
#         vm.accounts_team_approval AS accounts_team_approval,
#         vm.status AS status,
#         vm.vendor_code AS vendor_code,
#         inc2.incoterm_name AS incoterm_name2,
#         vm.gst_number AS gst_number,
#         vm.pan_number AS pan_number,
#         bk.bank_name AS bank_name,
#         vm.account_number AS account_number,
#         vm.vendor_name AS vendor_name
        

#     FROM `tabVendor Master` vm 
#     LEFT JOIN
#         `tabCompany Master` cm ON vm.company_name = cm.name
#     LEFT JOIN
#         `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#     LEFT JOIN
#         `tabAccount Group Master` at ON vm.account_group = at.name
#     LEFT JOIN
#         `tabDepartment Master` dp ON vm.department = dp.name
#     LEFT JOIN
#         `tabMaterial Master` mt ON vm.material_to_be_supplied = mt.name
#     LEFT JOIN
#         `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
#     LEFT JOIN
#         `tabCurrency Master` oc ON vm.order_currency = oc.name
#     LEFT JOIN
#         `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
#     LEFT JOIN
#         `tabIncoterm Master` inc ON vm.incoterms = inc.name
#     LEFT JOIN
#         `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
#     LEFT JOIN
#         `tabPurchase Organization Master` pg2 ON vm.purchase_organization = pg2.name
#     LEFT JOIN
#         `tabCompany Nature Master` con ON vm.nature_of_company = con.name
#     LEFT JOIN
#         `tabRFQ Type Master` rfq ON vm.rfq_type = rfq.name
#     LEFT JOIN
#         `tabCompany Master` ct ON vm.city = ct.name
#     LEFT JOIN
#         `tabState Master` st ON vm.state = st.name
#     LEFT JOIN
#         `tabCountry Master` cnt ON vm.country = cnt.name
#     LEFT JOIN
#         `tabDistrict Master` dst ON vm.district = dst.name
#     LEFT JOIN
#         `tabPincode Master` pin ON vm.pincode = pin.name
#     LEFT JOIN
#         `tabCity Master` cty ON vm.city = cty.name
#     LEFT JOIN
#         `tabCompany Master` cm2 ON vm.company_code = cm2.name
#     LEFT JOIN
#         `tabIncoterm Master` inc2 ON vm.incoterms2 = inc2.name
#     LEFT JOIN
#         `tabBank Master` bk ON vm.bank1 = bk.name


#     WHERE vm.name=%s
# """, (name), as_dict=1)


#     termsid = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['terms_of_payment'])
#     terms = frappe.db.get_value("Terms Of Payment Master", filters={'name': termsid}, fieldname=['terms_of_payment_name'])
#    # email_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary'])
#     reconcileid = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['reconciliation_account'])
#     reconciliation_number = frappe.db.get_value("Reconciliation Account", filters={'name': name}, fieldname=['reconcil_account'])
#     company_code = vendor[0].get('company_code') if vendor else None
#     purchase_organization_code = vendor[0].get('purchase_organization_code') if vendor else None
#     account_group_name = vendor[0].get('account_group_name') if vendor else None
#     vendor_name = vendor[0].get('vendor_name') if vendor else None
#     search_term = vendor[0].get('search_term') if vendor else None
#     office_address_line_1 = vendor[0].get('office_address_line_1') if vendor else None
#     pincode = vendor[0].get('pincode') if vendor else None
#     city = vendor[0].get('city_name') if vendor else None
#     country = vendor[0].get('country_code') if vendor else None
#     mobile_number = vendor[0].get('mobile_number') if vendor else None
#     office_email_primary = vendor[0].get('office_email_primary') if vendor else None
#     office_email_secondary = vendor[0].get('office_email_secondary') if vendor else None
#     currency_code = vendor[0].get('currency_code') if vendor else None
#     incoterm_name = vendor[0].get('incoterm_name') if vendor else None
#     incoterms2 = vendor[0].get('incoterm_name2') if vendor else None
#     purchase_group_name = vendor[0].get('purchase_group_name') if vendor else None
#     gst_number = vendor[0].get('gst_number') if vendor else None
#     vendor_type_name = vendor[0].get('vendor_type_name') if vendor else None
#     pan_number = vendor[0].get('pan_number') if vendor else None
#     bank_name = vendor[0].get('bank_name') if vendor else None
#     account_number = vendor[0].get('account_number') if vendor else None
#     state_name = vendor[0].get('state_name') if vendor else None
#     bank_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['bank1'])
#     bank_ifsc = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['ifsc_code', 'bank_name'])
#     account_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['account_group'])
#     account_code = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['acccount_group_code'])
#     purchase_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_groupm'])
#     purchase_code = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_id}, fieldname=['purchase_group_code'])
#     flname = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['first_name', 'last_name'])


#     print("(************************************()()()()())()()()(()()()()())","From sap_fetch_token",bank_ifsc[1])



#     data =  {
#     "Bukrs": company_code,
#     "Ekorg": purchase_organization_code,
#     "Ktokk": account_code,
#     "Title": "",
#     "Name1": vendor_name,
#     "Name2": "",
#     "Sort1": search_term,
#     "Street": office_address_line_1,
#     "StrSuppl1": office_address_line_1,
#     "StrSuppl2": "",
#     "StrSuppl3": "",
#     "PostCode1": pincode,
#     "City1": city,
#     "Country": country,
#     "J1kftind": "",
#     "Region": state_name,
#     "TelNumber": "",
#     "MobNumber": mobile_number,
#     "SmtpAddr": office_email_primary,
#     "SmtpAddr1": office_email_secondary,
#     "Zuawa": "",
#     "Akont": reconciliation_number,
#     "Waers": currency_code,
#     "Zterm": terms,
#     "Inco1": incoterm_name,
#     "Inco2": incoterms2,
#     "Kalsk": "",
#     "Ekgrp": purchase_code,
#     "Xzemp": "X",
#     "Reprf": "X",
#     "Webre": "X",
#     "Lebre": "",
#     "Stcd3": gst_number,
#     "J1ivtyp": vendor_type_name,
#     "J1ipanno": pan_number,
#     "J1ipanref": vendor_name,
#     "Namev": flname[0],
#     "Name11": flname[1],
#     "Bankl": bank_name,
#     "Bankn": account_number,
#     "Bkref": bank_ifsc[0],
#     "Banka": bank_ifsc[1],
#     "Xezer": "",
#     "Refno": name,
#     "Vedno": "",
#     "Zmsg": ""

#         }
    
# #Below is the important one
#     # data =  {
#     # "Bukrs": company_code,
#     # "Ekorg": purchase_organization_code,
#     # "Ktokk": account_group_name,
#     # "Title": "",
#     # "Name1": vendor_name,
#     # "Name2": "",
#     # "Sort1": search_term,
#     # "Street": office_address_line_1,
#     # "StrSuppl1": office_address_line_1,
#     # "StrSuppl2": "",
#     # "StrSuppl3": "",
#     # "PostCode1": pincode,
#     # "City1": city,
#     # "Country": country,
#     # "J1kftind": "",
#     # "Region": state_name,
#     # "TelNumber": "",
#     # "MobNumber": mobile_number,
#     # "SmtpAddr": office_email_primary,
#     # "SmtpAddr1": office_email_secondary,
#     # "Zuawa": "",
#     # "Akont": reconciliation_number,
#     # "Waers": currency_code,
#     # "Zterm": terms,
#     # "Inco1": incoterm_name,
#     # "Inco2": incoterms2,
#     # "Kalsk": "",
#     # "Ekgrp": purchase_group_name,
#     # "Xzemp": "X",
#     # "Reprf": "X",
#     # "Webre": "X",
#     # "Lebre": "",
#     # "Stcd3": gst_number,
#     # "J1ivtyp": vendor_type_name,
#     # "J1ipanno": pan_number,
#     # "J1ipanref": "Hitesh Mahto",
#     # "Namev": "Hitesh",
#     # "Name11": "Mahto",
#     # "Bankl": bank_name,
#     # "Bankn": account_number,
#     # "Bkref": "2001",
#     # "Banka": "UTIB0019191",
#     # "Xezer": "",
#     # "Refno": "VMS/368b008a78/0101",
#     # "Vedno": "",
#     # "Zmsg": ""

#     #     }


#     url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
#     headers = {
#     'X-CSRF-TOKEN': 'Fetch',
#      'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ=',
#      'Content-Type': 'application/json'
#     }
#     auth = HTTPBasicAuth('WF-BATCH ', 'M@wb#$%2024')
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         print("******GET CSRF TOKEN*********")
#         csrf_token = response.headers.get('x-csrf-token')
#         key1 = response.cookies.get('SAP_SESSIONID_BHD_200')
#         key2 = response.cookies.get('sap-usercontext')
#         send_detail(csrf_token, data, key1, key2, name)
#         print("*******************KEYYYYY********", key1)
#         print(key2)

#         print(csrf_token)
#         print(response.headers.get('x-csrf-token'))
#         return data
  
        
#        # return csrf_token
#     else:
#         print("Error:", response.status_code)
#        # return "Error: " + str(response.status_code)
#         #send_detail("*************************",csrf_token)

@frappe.whitelist(allow_guest=True)
#def sap_fetch_token(data, method):
def sap_fetch_token(name):

    name = name
    print("*********************************", name)
    vendor = frappe.db.sql(""" 
    SELECT
        cm.company_name AS company_name,
        cm2.company_code AS company_code,
        vm.website AS website,
        vt.vendor_type_name As vendor_type_name,
        at.account_group_name AS account_group_name,
        dp.department_name AS department_name,
        mt.material_name AS material_name,
        vm.search_term AS search_term,
        bn.business_nature_name AS business_nature_name,
        vm.payee AS payee_in_document,
        vm.gr_based_inv_ver AS gr_based_inv_ver,
        vm.service_based_inv_ver AS service_based_inv_ver,
        vm.check_double_invoice AS check_double_invoice,
        oc.currency_code AS currency_code,
        tp.terms_of_payment_name As terms_of_payment_name,
        inc.incoterm_name As incoterm_name,
        pg.purchase_group_name AS purchase_group_name,
        pg2.purchase_organization_code AS purchase_organization_code,
        vm.registered_date AS registered_date,
        vm.purchase_organization AS company_name,
        vm.type_of_business AS type_of_business,
        vm.size_of_company AS size_of_company,
        vm.registered_office_number AS registered_office_number,
        vm.telephone_number AS telephone_number,
        vm.established_year AS established_year,
        vm.office_email_primary AS office_email_primary,
        vm.office_email_secondary AS office_email_secondary,
        vm.corporate_identification_number As corporate_identification_number,
        vm.cin_date AS cin_date,
        con.company_nature_name AS company_nature_name,
        vm.vendor_name AS vendor_name,
        rfq.rfq_name AS rfq_name,
        vm.mobile_number AS mobile_number,
        vm.office_address_line_1 AS office_address_line_1,
        vm.office_address_line_2 AS office_address_line_2,
        vm.office_address_line_3 AS office_address_line_3,
        vm.office_address_line_4 AS office_address_line_4,
        cty.city_name AS city_name,
        st.state_name AS state_name,
        cnt.country_code AS country_code,
        dst.district_name As district_name,
        pin.pincode AS pincode,
        vm.manufacturing_address_line_1 AS manufacturing_address_line_1,
        vm.manufacturing_address_line_2 AS manufacturing_address_line_2,
        vm.manufacturing_address_line_3 AS manufacturing_address_line_3,
        vm.manufacturing_address_line_4 AS manufacturing_address_line_4,
        vm.registered_by As registered_by,
        vm.purchase_head_approval AS purchase_head_approval,
        vm.purchase_team_approval AS purchase_team_approval,
        vm.accounts_team_approval AS accounts_team_approval,
        vm.status AS status,
        vm.vendor_code AS vendor_code,
        inc2.incoterm_name AS incoterm_name2,
        vm.gst_number AS gst_number,
        vm.pan_number AS pan_number,
        bk.bank_name AS bank_name,
        bk.bank_code AS bank_code, 
        bk.ifsc_code AS ifsc_code,
        vm.account_number AS account_number,
        vm.vendor_name AS vendor_name
        

    FROM `tabVendor Master` vm 
    LEFT JOIN
        `tabCompany Master` cm ON vm.company_name = cm.name
    LEFT JOIN
        `tabVendor Type Master` vt ON vm.vendor_type = vt.name
    LEFT JOIN
        `tabAccount Group Master` at ON vm.account_group = at.name
    LEFT JOIN
        `tabDepartment Master` dp ON vm.department = dp.name
    LEFT JOIN
        `tabMaterial Master` mt ON vm.material_to_be_supplied = mt.name
    LEFT JOIN
        `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
    LEFT JOIN
        `tabCurrency Master` oc ON vm.order_currency = oc.name
    LEFT JOIN
        `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
    LEFT JOIN
        `tabIncoterm Master` inc ON vm.incoterms = inc.name
    LEFT JOIN
        `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
    LEFT JOIN
        `tabPurchase Organization Master` pg2 ON vm.purchase_organization = pg2.name
    LEFT JOIN
        `tabCompany Nature Master` con ON vm.nature_of_company = con.name
    LEFT JOIN
        `tabRFQ Type Master` rfq ON vm.rfq_type = rfq.name
    LEFT JOIN
        `tabCompany Master` ct ON vm.city = ct.name
    LEFT JOIN
        `tabState Master` st ON vm.state = st.name
    LEFT JOIN
        `tabCountry Master` cnt ON vm.country = cnt.name
    LEFT JOIN
        `tabDistrict Master` dst ON vm.district = dst.name
    LEFT JOIN
        `tabPincode Master` pin ON vm.pincode = pin.name
    LEFT JOIN
        `tabCity Master` cty ON vm.city = cty.name
    LEFT JOIN
        `tabCompany Master` cm2 ON vm.company_code = cm2.name
    LEFT JOIN
        `tabIncoterm Master` inc2 ON vm.incoterms2 = inc2.name
    LEFT JOIN
        `tabBank Master` bk ON vm.bank1 = bk.name


    WHERE vm.name=%s
""", (name), as_dict=1)


#     termsid = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['terms_of_payment'])
#     terms = frappe.db.get_value("Terms Of Payment Master", filters={'name': termsid}, fieldname=['terms_of_payment_name'])
#    # email_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary'])
#     reconcileid = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['reconciliation_account'])
#     reconciliation_number = frappe.get_value("Reconciliation Account", filters={'name': reconcileid}, fieldname=['num'])
#     # company_code = vendor[0].get('company_code') if vendor else None
#     company_id = frappe.db.get_value("Vendor Master", filters={"name": name}, fieldname=['company_name'])
#     company_code = frappe.db.get_value("Company Master", filters={"name": company_id}, fieldname=['company_code'])
#     purchase_organization_code = vendor[0].get('purchase_organization_code') if vendor else None
#     account_group_name = vendor[0].get('account_group_name') if vendor else None
#     vendor_name = vendor[0].get('vendor_name') if vendor else None
#     search_term = vendor[0].get('search_term') if vendor else None
#     office_address_line_1 = vendor[0].get('office_address_line_1') if vendor else None
#     pincode = vendor[0].get('pincode') if vendor else None
#     city = vendor[0].get('city_name') if vendor else None
#     country = vendor[0].get('country_code') if vendor else None
#     mobile_number = vendor[0].get('mobile_number') if vendor else None
#     office_email_primary = vendor[0].get('office_email_primary') if vendor else None
#     office_email_secondary = vendor[0].get('office_email_secondary') if vendor else None
#     currency_code = vendor[0].get('currency_code') if vendor else None
#     incoterm_name = vendor[0].get('incoterm_name') if vendor else None
#     incoterms2 = vendor[0].get('incoterm_name2') if vendor else None
#     purchase_group_name = vendor[0].get('purchase_group_name') if vendor else None
#     gst_number = vendor[0].get('gst_number') if vendor else None
#     vendor_type_name = vendor[0].get('vendor_type_name') if vendor else None
#     pan_number = vendor[0].get('pan_number') if vendor else None
#     bank_name = vendor[0].get('bank_name') if vendor else None
#     account_number = vendor[0].get('account_number') if vendor else None
#     state_name = vendor[0].get('state_name') if vendor else None
#     # bank_id = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['bank_name'])
#     # bank_ifsc = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['ifsc_code', 'bank_name'])
#     bank_id = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['bank_name'])
#     # bank = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['bank_name'])
#     bank = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['bank_name', 'ifsc_code'])
#     account_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['account_group'])
#     account_code = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['acccount_group_code'])
#     purchase_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_groupm'])
#     purchase_code = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_id}, fieldname=['purchase_group_code'])
#     flname = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['first_name', 'last_name'])
#     print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", reconcileid,reconciliation_number)

#########################################

    termsid = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['terms_of_payment'])
    terms = frappe.db.get_value("Terms Of Payment Master", filters={'name': termsid}, fieldname=['terms_of_payment_name'])
   # email_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary'])
    reconcileid = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['reconciliation_account'])
    reconciliation_number = frappe.get_value("Reconciliation Account", filters={'name': reconcileid}, fieldname=['num'])
    #company_code = vendor[0].get('company_code') if vendor else None
    company_id = frappe.db.get_value("Vendor Master", filters={"name": name}, fieldname=['company_name'])
    company_code = frappe.db.get_value("Company Master", filters={"name": company_id}, fieldname=['company_code'])
    purchase_organization_code = vendor[0].get('purchase_organization_code') if vendor else None
    account_group_name = vendor[0].get('account_group_name') if vendor else None
    vendor_name = vendor[0].get('vendor_name') if vendor else None
    search_term = vendor[0].get('search_term') if vendor else None
    office_address_line_1 = vendor[0].get('office_address_line_1') if vendor else None
    pincode = vendor[0].get('pincode') if vendor else None
    city = vendor[0].get('city_name') if vendor else None
    country = vendor[0].get('country_code') if vendor else None
    mobile_number = vendor[0].get('mobile_number') if vendor else None
    office_email_primary = vendor[0].get('office_email_primary') if vendor else None
    office_email_secondary = vendor[0].get('office_email_secondary') if vendor else None
    currency_code = vendor[0].get('currency_code') if vendor else None
    incoterm_name = vendor[0].get('incoterm_name') if vendor else None
    incoterms2 = vendor[0].get('incoterm_name2') if vendor else None
    purchase_group_name = vendor[0].get('purchase_group_name') if vendor else None
    gst_number = vendor[0].get('gst_number') if vendor else None
    vendor_type_name = vendor[0].get('vendor_type_name') if vendor else None
    pan_number = vendor[0].get('pan_number') if vendor else None
    bank_name = vendor[0].get('bank_name') if vendor else None
    account_number = vendor[0].get('account_number') if vendor else None
    state_name = vendor[0].get('state_name') if vendor else None
    #bank_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['bank1'])
    #bank_ifsc = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['ifsc_code', 'bank_name'])
    bank_id = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['bank_name'])
    bank = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['bank_name', 'ifsc_code', 'bank_code'])
    account_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['account_group'])
    account_code = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['acccount_group_code'])
    purchase_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_groupm'])
    purchase_code = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_id}, fieldname=['purchase_group_code'])
    flname = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['first_name', 'last_name'])
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", reconcileid,reconciliation_number, company_code)


    # json_data = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['payee_in_document', 'gr_based_inv_ver', 'service_based_inv_ver', 'check_double_invoice'])

    json_data = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['payee', 'gr_based_inv_ver', 'service_based_inv_ver', 'check_double_invoice'])

    print("##############################2345666666666666666666666############", json_data)

    
    payee_in_document, gr_based_inv_ver, service_based_inv_ver, check_double_invoice = json_data

   
    payee = 'X' if payee_in_document == 1 else ''
    gr_based_inv_ver = 'X' if gr_based_inv_ver == 1 else ''
    service_based_inv_ver = 'X' if service_based_inv_ver == 1 else ''
    check_double_invoice = 'X' if check_double_invoice == 1 else ''

 
    print(f"Payee: {payee}, GR Based Invoice Verification: {gr_based_inv_ver}, Service Based Invoice Verification: {service_based_inv_ver}, Check Double Invoice: {check_double_invoice}")



  
    # json_data = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['payee_in_document', 'gr_based_inv_ver', 'service_based_inv_ver', 'check_double_invoice'])
    # print("##############################2345666666666666666666666############", json_data)
    # payee = 'X' if json_data[0]['payee_in_document'] == 1 else ''
    # gr_based_inv_ver = 'X' if json_data[1]['gr_based_inv_ver'] == 1 else ''
    # service_based_inv_ver = 'X' if json_data[2]['service_based_inv_ver'] == 1 else ''
    # check_double_invoice = 'X' if json_data[3]['check_double_invoice'] == 1 else ''
    
    mylist = [payee, gr_based_inv_ver, service_based_inv_ver, check_double_invoice]
    print("***********MYLIST***********", mylist)



    # print("(************************************()()()()())()()()(()()()()())","From sap_fetch_token",bank_ifsc[1])




    # data =  {
    # "Bukrs": company_code,
    # "Ekorg": purchase_organization_code,
    # "Ktokk": account_code,
    # "Title": "",
    # "Name1": "Harin Patel -API 11",
    # "Name2": "",
    # "Sort1": "Harin",
    # "Street": "test",
    # "StrSuppl1": "",
    # "StrSuppl2": "",
    # "StrSuppl3": "",
    # # "PostCode1": pincode,
    # # "City1": city,
    # # "Country": country,
    # # "J1kftind": "",
    # # "Region": state_name,
    # "PostCode1" : "151617",
    # "City1" : "test",
    # "Country" : "IN",
    # "J1kftind" : "",
    # "Region" : "6",
    # "TelNumber" : "",
    # "MobNumber" : "1256651",
    # "SmtpAddr" : "hitesh.mahto@merillife.com",
    # "SmtpAddr1" : "hitesh@gmail.com",
    # # "MobNumber": mobile_number,
    # # "SmtpAddr": office_email_primary,
    # # "SmtpAddr1": office_email_secondary,
    # "Zuawa": "",
    # "Akont": "16101010",
    # "Waers": currency_code,
    # "Zterm": terms,
    # "Inco1": "CIF",
    # "Inco2": "Costs, insurance & freight",
    # "Kalsk": "",
    # "Ekgrp": purchase_code,
    # "Xzemp": payee,
    # "Reprf": gr_based_inv_ver,
    # "Webre": service_based_inv_ver,
    # "Lebre": check_double_invoice,
    # "Stcd3": gst_number,
    # "J1ivtyp": vendor_type_name,
    # "J1ipanno": pan_number,
    # "J1ipanref": vendor_name,
    # "Namev": flname[0],
    # "Name11": flname[1],
    # # "Stcd3" : "GST12345",
    # # "J1ivtyp" : "0",
    # # "J1ipanno" : "PAN11010",
    # # "J1ipanref" : "Hitesh Mahto",
    # # "Namev" : "Hitesh",
    # # "Name11" : "Mahto",
    # "Bankl": bank_name,
    # # "Bankl" : "HDFC0000170",
    # "Bankn": account_number,
    # # "Bankn" : "ac91201001898261",
    # "Bkref": bank_ifsc[0],
    # # "Bkref": "UTIB0019191",
    # "Banka": bank_ifsc[1],
    # # "Banka": "AXIS BANK LTD.",
    # "Xezer": "",
    # "Refno": name,
    # "Vedno": ""

    #     }


    data =  {
        
    "Bukrs": company_code,
    "Ekorg": purchase_organization_code,
    "Ktokk": account_code,
    "Title": "",
    "Name1": vendor_name,
    "Name2": "",
    "Sort1": search_term,
    "Street": office_address_line_1,
    "StrSuppl1": office_address_line_1,
    "StrSuppl2": "",
    "StrSuppl3": "",
    "PostCode1": pincode,
    "City1": city,
    "Country": country,
    "J1kftind": "",
    "Region": state_name,
    "TelNumber": "",
    "MobNumber": mobile_number,
    "SmtpAddr": office_email_primary,
    "SmtpAddr1": office_email_secondary,
    "Zuawa": "",
    "Akont": reconciliation_number,
    "Waers": currency_code,
    "Zterm": terms,
    "Inco1": incoterm_name,
    "Inco2": incoterms2,
    "Kalsk": "",
    "Ekgrp": purchase_code,
    "Xzemp": payee,
    "Reprf": check_double_invoice,
    "Webre": gr_based_inv_ver,
    "Lebre": service_based_inv_ver,
    "Stcd3": gst_number,
    "J1ivtyp": vendor_type_name,
    "J1ipanno": pan_number,
    "J1ipanref": vendor_name,
    "Namev": flname[0],
    "Name11": flname[1],
    "Bankl": bank[2],
    "Bankn": account_number,
    "Bkref": bank[0],
    "Banka": bank[1],
    "Xezer": "",
    "Refno": name,
    "Vedno": "",
    "Zmsg": ""

        }
    
# #Below is the important one
#     # data =  {
#     # "Bukrs": company_code,
#     # "Ekorg": purchase_organization_code,
#     # "Ktokk": account_group_name,
#     # "Title": "",
#     # "Name1": vendor_name,
#     # "Name2": "",
#     # "Sort1": search_term,
#     # "Street": office_address_line_1,
#     # "StrSuppl1": office_address_line_1,
#     # "StrSuppl2": "",
#     # "StrSuppl3": "",
#     # "PostCode1": pincode,
#     # "City1": city,
#     # "Country": country,
#     # "J1kftind": "",
#     # "Region": state_name,
#     # "TelNumber": "",
#     # "MobNumber": mobile_number,
#     # "SmtpAddr": office_email_primary,
#     # "SmtpAddr1": office_email_secondary,
#     # "Zuawa": "",
#     # "Akont": reconciliation_number,
#     # "Waers": currency_code,
#     # "Zterm": terms,
#     # "Inco1": incoterm_name,
#     # "Inco2": incoterms2,
#     # "Kalsk": "",
#     # "Ekgrp": purchase_group_name,
#     # "Xzemp": "X",
#     # "Reprf": "X",
#     # "Webre": "X",
#     # "Lebre": "",
#     # "Stcd3": gst_number,
#     # "J1ivtyp": vendor_type_name,
#     # "J1ipanno": pan_number,
#     # "J1ipanref": "Hitesh Mahto",
#     # "Namev": "Hitesh",
#     # "Name11": "Mahto",
#     # "Bankl": bank_name,
#     # "Bankn": account_number,
#     # "Bkref": "2001",
#     # "Banka": "UTIB0019191",
#     # "Xezer": "",
#     # "Refno": "VMS/368b008a78/0101",
#     # "Vedno": "",
#     # "Zmsg": ""

#     #     }


    url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
    headers = {
    'X-CSRF-TOKEN': 'Fetch',
     'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ=',
     'Content-Type': 'application/json'
    }
    auth = HTTPBasicAuth('WF-BATCH ', 'M@wb#$%2024')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("******GET CSRF TOKEN*********")
        csrf_token = response.headers.get('x-csrf-token')
        key1 = response.cookies.get('SAP_SESSIONID_BHD_200')
        key2 = response.cookies.get('sap-usercontext')
        send_detail(csrf_token, data, key1, key2, name)
        print("*******************KEYYYYY********", key1)
        print(key2)

        print(csrf_token)
        print(response.headers.get('x-csrf-token'))
        return data
  
        
       # return csrf_token
    else:
        print("Error:", response.status_code)
       # return "Error: " + str(response.status_code)
        #send_detail("*************************",csrf_token)


#******************************* SAP PUSH  ************************************************************


@frappe.whitelist(allow_guest=True)
def send_detail(csrf_token, data, key1, key2, name):

   
    url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
    key1 = key1
    key2 = key2
    name = name
    #pdb.set_trace()
    headers = {

        'X-CSRF-TOKEN': csrf_token,
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json',
        'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ=',
        'Cookie': f"SAP_SESSIONID_BHD_200={key1}; sap-usercontext={key2}"

        #'Cookie': "SAP_SESSIONID_BHD_700=wHpHljfZ0I1z-tzSV5pxUO4ejeojGxHvgjQADTo-At8%3d; sap-usercontext=sap-client=700"
    }
    auth = HTTPBasicAuth('WF-BATCH ', 'M@wb#$%2024')
    #print("***********************************************" ,requests.headers)
    
    try:
        response = requests.post(url, headers=headers, auth=auth ,json=data)
        print("**************************POST here*********************", response.json(), response.status_code)
        #return response.json()
        vendor_sap_code = response.json()
        vendor_code = vendor_sap_code['d']['Vedno']
        print("^&%^%^%^*&%%^^^^^^^^^^^^^^^^^^^^^^^^^^", vendor_code)
        
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",name)

        frappe.db.sql(""" UPDATE `tabVendor Master` SET vendor_code=%s where name=%s """, (vendor_code, name))
        frappe.db.commit()
        
        #return response.json()
    except ValueError:
        print("**************************POSTsdfsdf here*********************", response.json())
    
    
    if response.status_code == 201:  
        print("*****************************************")
        print("Vendor details posted successfully.")
        # vendor_sap_code = response.json()
        # vendor_code = vendor_sap_code['d']['Vedno']
        # print("^&%^%^%^*&%%^^^^^^^^^^^^^^^^^^^^^^^^^^", vendor_code)
        return response.json()

        
    else:
        print("******************************************")
        print("Error in POST request:", response.status_code)
        #return "Error in POST request: " + str(response.status_code)

    #return response.json()




# @frappe.whitelist(allow_guest=True)
# #def sap_fetch_token(data, method):
# def sap_fetch_token(name):

#     name = name
#     print("*********************************", name)
#     vendor = frappe.db.sql(""" 
#     SELECT
#         cm.company_name AS company_name,
#         cm2.company_code AS company_code,
#         vm.website AS website,
#         vt.vendor_type_name As vendor_type_name,
#         at.account_group_name AS account_group_name,
#         dp.department_name AS department_name,
#         mt.material_name AS material_name,
#         vm.search_term AS search_term,
#         bn.business_nature_name AS business_nature_name,
#         vm.payee AS payee_in_document,
#         vm.gr_based_inv_ver AS gr_based_inv_ver,
#         vm.service_based_inv_ver AS service_based_inv_ver,
#         vm.check_double_invoice AS check_double_invoice,
#         oc.currency_code AS currency_code,
#         tp.terms_of_payment_name As terms_of_payment_name,
#         inc.incoterm_name As incoterm_name,
#         pg.purchase_group_name AS purchase_group_name,
#         pg2.purchase_organization_code AS purchase_organization_code,
#         vm.registered_date AS registered_date,
#         vm.purchase_organization AS company_name,
#         vm.type_of_business AS type_of_business,
#         vm.size_of_company AS size_of_company,
#         vm.registered_office_number AS registered_office_number,
#         vm.telephone_number AS telephone_number,
#         vm.established_year AS established_year,
#         vm.office_email_primary AS office_email_primary,
#         vm.office_email_secondary AS office_email_secondary,
#         vm.corporate_identification_number As corporate_identification_number,
#         vm.cin_date AS cin_date,
#         con.company_nature_name AS company_nature_name,
#         vm.vendor_name AS vendor_name,
#         rfq.rfq_name AS rfq_name,
#         vm.mobile_number AS mobile_number,
#         vm.office_address_line_1 AS office_address_line_1,
#         vm.office_address_line_2 AS office_address_line_2,
#         vm.office_address_line_3 AS office_address_line_3,
#         vm.office_address_line_4 AS office_address_line_4,
#         cty.city_name AS city_name,
#         st.state_name AS state_name,
#         cnt.country_code AS country_code,
#         dst.district_name As district_name,
#         pin.pincode AS pincode,
#         vm.manufacturing_address_line_1 AS manufacturing_address_line_1,
#         vm.manufacturing_address_line_2 AS manufacturing_address_line_2,
#         vm.manufacturing_address_line_3 AS manufacturing_address_line_3,
#         vm.manufacturing_address_line_4 AS manufacturing_address_line_4,
#         vm.registered_by As registered_by,
#         vm.purchase_head_approval AS purchase_head_approval,
#         vm.purchase_team_approval AS purchase_team_approval,
#         vm.accounts_team_approval AS accounts_team_approval,
#         vm.status AS status,
#         vm.vendor_code AS vendor_code,
#         inc2.incoterm_name AS incoterm_name2,
#         vm.gst_number AS gst_number,
#         vm.pan_number AS pan_number,
#         bk.bank_name AS bank_name,
#         vm.account_number AS account_number,
#         vm.vendor_name AS vendor_name
        

#     FROM `tabVendor Master` vm 
#     LEFT JOIN
#         `tabCompany Master` cm ON vm.company_name = cm.name
#     LEFT JOIN
#         `tabVendor Type Master` vt ON vm.vendor_type = vt.name
#     LEFT JOIN
#         `tabAccount Group Master` at ON vm.account_group = at.name
#     LEFT JOIN
#         `tabDepartment Master` dp ON vm.department = dp.name
#     LEFT JOIN
#         `tabMaterial Master` mt ON vm.material_to_be_supplied = mt.name
#     LEFT JOIN
#         `tabBusiness Nature Master` bn ON vm.nature_of_business = bn.name
#     LEFT JOIN
#         `tabCurrency Master` oc ON vm.order_currency = oc.name
#     LEFT JOIN
#         `tabTerms Of Payment Master` tp ON vm.terms_of_payment = tp.name
#     LEFT JOIN
#         `tabIncoterm Master` inc ON vm.incoterms = inc.name
#     LEFT JOIN
#         `tabPurchase Group Master` pg ON vm.purchase_groupm = pg.name
#     LEFT JOIN
#         `tabPurchase Organization Master` pg2 ON vm.purchase_organization = pg2.name
#     LEFT JOIN
#         `tabCompany Nature Master` con ON vm.nature_of_company = con.name
#     LEFT JOIN
#         `tabRFQ Type Master` rfq ON vm.rfq_type = rfq.name
#     LEFT JOIN
#         `tabCompany Master` ct ON vm.city = ct.name
#     LEFT JOIN
#         `tabState Master` st ON vm.state = st.name
#     LEFT JOIN
#         `tabCountry Master` cnt ON vm.country = cnt.name
#     LEFT JOIN
#         `tabDistrict Master` dst ON vm.district = dst.name
#     LEFT JOIN
#         `tabPincode Master` pin ON vm.pincode = pin.name
#     LEFT JOIN
#         `tabCity Master` cty ON vm.city = cty.name
#     LEFT JOIN
#         `tabCompany Master` cm2 ON vm.company_code = cm2.name
#     LEFT JOIN
#         `tabIncoterm Master` inc2 ON vm.incoterms2 = inc2.name
#     LEFT JOIN
#         `tabBank Master` bk ON vm.bank1 = bk.name


#     WHERE vm.name=%s
# """, (name), as_dict=1)


#     termsid = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['terms_of_payment'])
#     terms = frappe.db.get_value("Terms Of Payment Master", filters={'name': termsid}, fieldname=['terms_of_payment_name'])
#    # email_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary'])
#     reconcileid = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['reconciliation_account'])
#     reconciliation_number = frappe.get_value("Reconciliation Account", filters={'name': reconcileid}, fieldname=['num'])
#     company_code = vendor[0].get('company_code') if vendor else None
#     purchase_organization_code = vendor[0].get('purchase_organization_code') if vendor else None
#     account_group_name = vendor[0].get('account_group_name') if vendor else None
#     vendor_name = vendor[0].get('vendor_name') if vendor else None
#     search_term = vendor[0].get('search_term') if vendor else None
#     office_address_line_1 = vendor[0].get('office_address_line_1') if vendor else None
#     pincode = vendor[0].get('pincode') if vendor else None
#     city = vendor[0].get('city_name') if vendor else None
#     country = vendor[0].get('country_code') if vendor else None
#     mobile_number = vendor[0].get('mobile_number') if vendor else None
#     office_email_primary = vendor[0].get('office_email_primary') if vendor else None
#     office_email_secondary = vendor[0].get('office_email_secondary') if vendor else None
#     currency_code = vendor[0].get('currency_code') if vendor else None
#     incoterm_name = vendor[0].get('incoterm_name') if vendor else None
#     incoterms2 = vendor[0].get('incoterm_name2') if vendor else None
#     purchase_group_name = vendor[0].get('purchase_group_name') if vendor else None
#     gst_number = vendor[0].get('gst_number') if vendor else None
#     vendor_type_name = vendor[0].get('vendor_type_name') if vendor else None
#     pan_number = vendor[0].get('pan_number') if vendor else None
#     bank_name = vendor[0].get('bank_name') if vendor else None
#     account_number = vendor[0].get('account_number') if vendor else None
#     state_name = vendor[0].get('state_name') if vendor else None
#     bank_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['bank1'])
#     # bank_ifsc = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['ifsc_code', 'bank_name'])
#     account_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['account_group'])
#     account_code = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['acccount_group_code'])
#     purchase_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_groupm'])
#     purchase_code = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_id}, fieldname=['purchase_group_code'])
#     flname = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['first_name', 'last_name'])
#     print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", reconcileid,reconciliation_number)



#     json_data = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['payee_in_document', 'gr_based_inv_ver', 'service_based_inv_ver', 'check_double_invoice'])
#     print("##############################2345666666666666666666666############", json_data)

    
#     payee_in_document, gr_based_inv_ver, service_based_inv_ver, check_double_invoice = json_data

   
#     payee = 'X' if payee_in_document == 1 else ''
#     gr_based_inv_ver = 'X' if gr_based_inv_ver == 1 else ''
#     service_based_inv_ver = 'X' if service_based_inv_ver == 1 else ''
#     check_double_invoice = 'X' if check_double_invoice == 1 else ''

 
#     print(f"Payee: {payee}, GR Based Invoice Verification: {gr_based_inv_ver}, Service Based Invoice Verification: {service_based_inv_ver}, Check Double Invoice: {check_double_invoice}")



  
#     # json_data = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['payee_in_document', 'gr_based_inv_ver', 'service_based_inv_ver', 'check_double_invoice'])
#     # print("##############################2345666666666666666666666############", json_data)
#     # payee = 'X' if json_data[0]['payee_in_document'] == 1 else ''
#     # gr_based_inv_ver = 'X' if json_data[1]['gr_based_inv_ver'] == 1 else ''
#     # service_based_inv_ver = 'X' if json_data[2]['service_based_inv_ver'] == 1 else ''
#     # check_double_invoice = 'X' if json_data[3]['check_double_invoice'] == 1 else ''
    
#     mylist = [payee, gr_based_inv_ver, service_based_inv_ver, check_double_invoice]
#     print("***********MYLIST***********", mylist)



    # print("(************************************()()()()())()()()(()()()()())","From sap_fetch_token",bank_ifsc[1])




    # data =  {
    # "Bukrs": company_code,
    # "Ekorg": purchase_organization_code,
    # "Ktokk": account_code,
    # "Title": "",
    # "Name1": vendor_name,
    # "Name2": "",
    # "Sort1": search_term,
    # "Street": office_address_line_1,
    # "StrSuppl1": office_address_line_1,
    # "StrSuppl2": "",
    # "StrSuppl3": "",
    # "PostCode1": pincode,
    # "City1": city,
    # "Country": country,
    # "J1kftind": "",
    # "Region": state_name,
    # "TelNumber": "",
    # "MobNumber": mobile_number,
    # "SmtpAddr": office_email_primary,
    # "SmtpAddr1": office_email_secondary,
    # "Zuawa": "",
    # "Akont": reconciliation_number,
    # "Waers": currency_code,
    # "Zterm": terms,
    # "Inco1": incoterm_name,
    # "Inco2": incoterms2,
    # "Kalsk": "",
    # "Ekgrp": purchase_code,
    # "Xzemp": payee,
    # "Reprf": check_double_invoice,
    # "Webre": gr_based_inv_ver,
    # "Lebre": service_based_inv_ver,
    # "Stcd3": gst_number,
    # "J1ivtyp": vendor_type_name,
    # "J1ipanno": pan_number,
    # "J1ipanref": vendor_name,
    # "Namev": flname[0],
    # "Name11": flname[1],
    # "Bankl": bank_name,
    # "Bankn": account_number,
    # "Bkref": bank_ifsc[0],
    # "Banka": bank_ifsc[1],
    # "Xezer": "",
    # "Refno": name,
    # "Vedno": "",
    # "Zmsg": ""

    #     }
# "Bukrs" : "2000",
# "Ekorg" : "2000",
# "Ktokk" : "ZDOM",
# "Title" : "",
# "Name1" : "Harin Patel -API 11",
# "Name2" : "",
# "Sort1" : "Harin",
# "Street" : "test",
# "StrSuppl1" : "",
# "StrSuppl2" : "",
# "StrSuppl3" : "",
# "PostCode1" : "151617",
# "City1" : "test",
# "Country" : "IN",
# "J1kftind" : "",
# "Region" : "6",
# "TelNumber" : "",
# "MobNumber" : "1256651",
# "SmtpAddr" : "hitesh.mahto@merillife.com",
# "SmtpAddr1" : "hitesh@gmail.com",
# "Zuawa" : "1",
# "Akont" : "16101020",
# "Waers" : "INR",
# "Zterm" : "Z072",
# "Inco1" : "CIF",
# "Inco2" : "CFR Costs and freight",
# "Kalsk" : "",
# "Ekgrp" : "P02",
# "Xzemp" : "X",
# "Reprf" : "X",
# "Webre" : "X",
# "Lebre" : "",
# "Stcd3" : "GST12345",
# "J1ivtyp" : "0",
# "J1ipanno" : "PAN11010",
# "J1ipanref" : "Hitesh Mahto",
# "Namev" : "Hitesh",
# "Name11" : "Mahto",
# "Bankl" : "HDFC0000170",
# "Bankn" : "ac91201001898261",
# "Koinh" : "2001",
# "Bkref" : "UTIB0019191",
# "Banka" : "AXIS BANK LTD.",
# "Xezer" : "",
# "Refno" : "VMS/000001",
# "Vedno" : "",
# "Zmsg" : ""
# }
    
    
#Below is the important one
    # data =  {
    # "Bukrs": company_code,
    # "Ekorg": purchase_organization_code,
    # "Ktokk": account_group_name,
    # "Title": "",
    # "Name1": vendor_name,
    # "Name2": "",
    # "Sort1": search_term,
    # "Street": office_address_line_1,
    # "StrSuppl1": office_address_line_1,
    # "StrSuppl2": "",
    # "StrSuppl3": "",
    # "PostCode1": pincode,
    # "City1": city,
    # "Country": country,
    # "J1kftind": "",
    # "Region": state_name,
    # "TelNumber": "",
    # "MobNumber": mobile_number,
    # "SmtpAddr": office_email_primary,
    # "SmtpAddr1": office_email_secondary,
    # "Zuawa": "",
    # "Akont": reconciliation_number,
    # "Waers": currency_code,
    # "Zterm": terms,
    # "Inco1": incoterm_name,
    # "Inco2": incoterms2,
    # "Kalsk": "",
    # "Ekgrp": purchase_group_name,
    # "Xzemp": "X",
    # "Reprf": "X",
    # "Webre": "X",
    # "Lebre": "",
    # "Stcd3": gst_number,
    # "J1ivtyp": vendor_type_name,
    # "J1ipanno": pan_number,
    # "J1ipanref": "Hitesh Mahto",
    # "Namev": "Hitesh",
    # "Name11": "Mahto",
    # "Bankl": bank_name,
    # "Bankn": account_number,
    # "Bkref": "2001",
    # "Banka": "UTIB0019191",
    # "Xezer": "",
    # "Refno": "VMS/368b008a78/0101",
    # "Vedno": "",
    # "Zmsg": ""

    #     }






    # url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
    # headers = {
    # 'X-CSRF-TOKEN': 'Fetch',
    #  'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ=',
    #  'Content-Type': 'application/json'
    # }
    # auth = HTTPBasicAuth('WF-BATCH ', 'M@wb#$%2024')
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     print("******GET CSRF TOKEN*********")
    #     csrf_token = response.headers.get('x-csrf-token')
    #     key1 = response.cookies.get('SAP_SESSIONID_BHD_200')
    #     key2 = response.cookies.get('sap-usercontext')
    #     send_detail(csrf_token, data, key1, key2, name)
    #     print("*******************KEYYYYY********", key1)
    #     print(key2)

    #     print(csrf_token)
    #     print(response.headers.get('x-csrf-token'))
    #     return data
  
        
    #    # return csrf_token
    # else:
    #     print("Error:", response.status_code)
    #    # return "Error: " + str(response.status_code)
    #     #send_detail("*************************",csrf_token)





#******************************* SAP PUSH  ************************************************************


# @frappe.whitelist(allow_guest=True)
# def send_detail(csrf_token, data, key1, key2, name):

   
#     url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
#     key1 = key1
#     key2 = key2
#     name = name
#     #pdb.set_trace()
#     headers = {

#         'X-CSRF-TOKEN': csrf_token,
#         'Content-Type': 'application/json;charset=utf-8',
#         'Accept': 'application/json',
#         'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ=',
#         'Cookie': f"SAP_SESSIONID_BHD_200={key1}; sap-usercontext={key2}"

#         #'Cookie': "SAP_SESSIONID_BHD_700=wHpHljfZ0I1z-tzSV5pxUO4ejeojGxHvgjQADTo-At8%3d; sap-usercontext=sap-client=700"
#     }
#     auth = HTTPBasicAuth('WF-BATCH ', 'M@wb#$%2024')
#     #print("***********************************************" ,requests.headers)
    
#     try:
#         response = requests.post(url, headers=headers, auth=auth ,json=data)
#         print("**************************POST here*********************", response.json(), response.status_code)
#         #return response.json()
#         vendor_sap_code = response.json()
#         vendor_code = vendor_sap_code['d']['Vedno']
#         print("^&%^%^%^*&%%^^^^^^^^^^^^^^^^^^^^^^^^^^", vendor_code)
        
#         print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",name)

#         frappe.db.sql(""" UPDATE `tabVendor Master` SET vendor_code=%s where name=%s """, (vendor_code, name))
#         frappe.db.commit()
        
#         #return response.json()
#     except ValueError:
#         print("**************************POSTsdfsdf here*********************", response.json())

    
#     if response.status_code == 201:  
#         print("*****************************************")
#         print("Vendor details posted successfully.")
#         # vendor_sap_code = response.json()
#         # vendor_code = vendor_sap_code['d']['Vedno']
#         # print("^&%^%^%^*&%%^^^^^^^^^^^^^^^^^^^^^^^^^^", vendor_code)
#         return response.json()

        
#     else:
#         print("******************************************")
#         print("Error in POST request:", response.status_code)

#************SAP DATA Push Closed**********************************************************************************************************************



#*********************** Onboarding Link ************************************************************************************

# @frappe.whitelist()
# def generate_onboarding_link(data, method):

#     random_uuid = str(uuid.uuid4())
#     # name = data.get('name')
#     # frappe.db.sql(""" UPDATE `tabVendor Master` SET uuid=%s WHERE name=%s """, (random_uuid, name))
#     # frappe.db.commit()
#     return "random: ", random_uuid


#************************** Onboarding Link Closed **************************************************************************

# @frappe.whitelist()
# def sap_fetch_token(data, method):


    # company_code = frappe.db.get_value("Company Master", filters={'name': data.get('company_name')}, fieldname='company_code')
    # purchase_organization = frappe.db.get_value("Company Master", filters={'name': data.get('purchase_organization')}, fieldname='company_name')
    # pincode = frappe.db.get_value("Pincode Master", filters={'name': data.get('pincode')}, fieldname='pincode')
    # city = frappe.db.get_value("City Master", filters={'name': data.get('city')}, fieldname='city_name')
    # country = frappe.db.get_value("Country Master", filters={'name': data.get('country')}, fieldname='country_name')
    # state = frappe.db.get_value("State Master", filters={'name': data.get('state')}, fieldname='state_name')
    # currency = frappe.db.get_value("Currency Master", filters={'name': data.get('order_currency')}, fieldname='currency_name')
    # #terms_of_payment = frappe.db.get_value("Terms Of Payment Master", filters={'name': data.get('terms_of_payment')}, fieldname='terms_of_payment')
    # #incoterms = frappe.db.get_value("Incoterm Master", filters={'name': data.get('incoterm')}, fieldname='incoterm_name')
    # #purchase_group = frappe.db.get_value("Purchase Group Master", filters={'name': data.get('purchase_group')}, fieldname='purchase_group_name')
    # vendor_type = frappe.db.get_value("Vendor Type Master", filters={'name': data.get('vendor_type')}, fieldname='vendor_type_name')


#     vendor_details = {
#     "Bukrs": company_code,
#     "Ekorg": purchase_organization,
#     "Ktokk": "",
#     "Title": "",
#     "Name1": "",
#     "Name2": "",
#     "Sort1": data.get('search_term'),
#     "Street": data.get('office_address_line_1'),
#     "StrSuppl1": data.get('office_address_line_2'),
#     "StrSuppl2": data.get('office_address_line_3'),
#     "StrSuppl3": data.get('office_address_line_4'),
#     "PostCode1": pincode,
#     "City1": city,
#     "Country": country,
#     "J1kftind": data.get('type_of_business'),
#     "Region": state,
#     "TelNumber": data.get('telephone_number'),
#     "MobNumber": data.get('mobile_number'),
#     "SmtpAddr": data.get('office_email_primary'),
#     "SmtpAddr1": data.get('office_email_secondary'),
#     "Zuawa": "",
#     "Akont": "",
#     "Waers": currency,
#     "Zterm": "",
#     "Inco1": "",
#     "Inco2": "",
#     "Kalsk": "",
#     "Ekgrp": "",
#     # "Xzemp": data.get('payee_in_document'),
#     # "Reprf": data.get('check_double_invoice'),
#     # "Webre": data.get('gr_based_inv_ver'),
#     # "Lebre": data.get('service_based_inv_ver'),
#     "Xzemp": "",
#     "Reprf": "",
#     "Webre": "",
#     "Lebre": "",
#     "Stcd3": "",
#     "J1ivtyp": vendor_type,
#     "J1ipanno": "",
#     "J1ipanref": "",
#     "Namev": "",
#     "Name11": "",
#     "Bankl": "",
#     "Bankn": "",
#     "Bkref": "",
#     "Banka": "",
#     "Xezer": "",
#     "Refno": data.get('name')
# }

#     url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
#     #print(vendor_details)
#     headers = {
#     'X-CSRF-TOKEN': 'Fetch'
#     }
#     auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
#     response = requests.get(url, headers=headers, auth=auth, json=vendor_details)

#         #print(response)
#     if response.status_code == 200:
#         csrf_token = response.headers.get('x-csrf-token')
#         send_detail(data, vendor_details ,method, csrf_token)
#         print("********************  Token ****************************************")
#         print("x-csrf-token:", csrf_token)
#         print(vendor_details)
#         return csrf_token
#     else:
#         print("Error:", response.status_code)
#         return "Error: " + str(response.status_code)
#     send_detail("*************************",csrf_token)



#     #*******************************************************************************

#     # headers = {
#     #     'X-CSRF-Token': csrf_token,
#     #     'Content-Type': 'application/json'
#     # }
#     # auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
#     # #print("***********************************************")
    
    
#     # response = requests.post(url, headers=headers, auth=auth, json=vendor_details)
#     # print("***********************************************", response.status_code)
    
    
#     # if response.status_code == 200:  
#     #    # print("*****************************************")
#     #     print("Vendor details posted successfully.")
#     #     #return "************************Vendor details posted successfully.******************************"
#     # else:
#     #     print("Error in POST request:", response.status_code)
#     #     return "Error in POST request: " + str(response.status_code)


# @frappe.whitelist()
# def send_detail(csrf_token, vendor_details ,data, method):
#     url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
#     print("*************************************")
#     print(type(csrf_token))
#     csrf_token_str = str(csrf_token)


#     headers = {
#         'X-CSRF-TOKEN': csrf_token_str,
#         'Content-Type': 'application/json',
#         'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ='
#     }
#     auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
#     #print("***********************************************")
    
    
#     response = requests.post(url, headers=headers, auth=auth, json=vendor_details)
#     print("***********************************************", response.status_code)
    
    
#     if response.status_code == 200:  
#        # print("*****************************************")
#         print("Vendor details posted successfully.")
#         #return "************************Vendor details posted successfully.******************************"
#     else:
#         print("Error in POST request:", response.status_code)
#         return "Error in POST request: " + str(response.status_code)



# @frappe.whitelist()
# def sap_fetch_token(data, method):


#     company_code = frappe.db.get_value("Company Master", filters={'name': data.get('company_name')}, fieldname='company_code')
#   #  purchase_organization = frappe.db.get_value("Company Master", filters={'name': data.get('purchase_organization')}, fieldname='company_name')
#     pincode = frappe.db.get_value("Pincode Master", filters={'name': data.get('pincode')}, fieldname='pincode')
#     city = frappe.db.get_value("City Master", filters={'name': data.get('city')}, fieldname='city_name')
#     country = frappe.db.get_value("Country Master", filters={'name': data.get('country')}, fieldname='country_name')
#     state = frappe.db.get_value("State Master", filters={'name': data.get('state')}, fieldname='state_name')
#     currency = frappe.db.get_value("Currency Master", filters={'name': data.get('order_currency')}, fieldname='currency_name')
#     #terms_of_payment = frappe.db.get_value("Terms Of Payment Master", filters={'name': data.get('terms_of_payment')}, fieldname='terms_of_payment')
#     #incoterms = frappe.db.get_value("Incoterm Master", filters={'name': data.get('incoterm')}, fieldname='incoterm_name')
#     #purchase_group = frappe.db.get_value("Purchase Group Master", filters={'name': data.get('purchase_group')}, fieldname='purchase_group_name')
#     vendor_type = frappe.db.get_value("Vendor Type Master", filters={'name': data.get('vendor_type')}, fieldname='vendor_type_name')


#     vendor_details = {
#     "Bukrs": company_code,
#     "Ekorg": data.get("purchase_organization"),
#     "Ktokk": "",
#     "Title": "",
#     "Name1": "",
#     "Name2": "",
#     "Sort1": data.get('search_term'),
#     "Street": data.get('office_address_line_1'),
#     "StrSuppl1": data.get('office_address_line_2'),
#     "StrSuppl2": data.get('office_address_line_3'),
#     "StrSuppl3": data.get('office_address_line_4'),
#     "PostCode1": pincode,
#     "City1": city,
#     "Country": country,
#     "J1kftind": data.get('type_of_business'),
#     "Region": state,
#     "TelNumber": data.get('telephone_number'),
#     "MobNumber": data.get('mobile_number'),
#     "SmtpAddr": data.get('office_email_primary'),
#     "SmtpAddr1": data.get('office_email_secondary'),
#     "Zuawa": "",
#     "Akont": "",
#     "Waers": currency,
#     "Zterm": "",
#     "Inco1": "",
#     "Inco2": "",
#     "Kalsk": "",
#     "Ekgrp": "",
#     "Xzemp": data.get('payee_in_document'),
#     "Reprf": data.get('check_double_invoice'),
#     "Webre": data.get('gr_based_inv_ver'),
#     "Lebre": data.get('service_based_inv_ver'),
#     "Stcd3": "",
#     "J1ivtyp": vendor_type,
#     "J1ipanno": "",
#     "J1ipanref": "",
#     "Namev": "",
#     "Name11": "",
#     "Bankl": "",
#     "Bankn": "",
#     "Bkref": "",
#     "Banka": "",
#     "Xezer": "",
#     "Refno": data.get('name')
# }


#     vendor_details = {
#     "Bukrs": "1000",
#     "Ekorg": "2000",
#     "Ktokk": "",
#     "Title": "NULL",
#     "Name1": "",
#     "Name2": "",
#     "Sort1": "None",
#     "Street": "ADLY2",
#     "StrSuppl1": "ADLY4",
#     "StrSuppl2": "ADLY5",
#     "StrSuppl3": "ADLY6",
#     "PostCode1": "123",
#     "City1": "City 1",
#     "Country": "Country 1",
#     "J1kftind": "Type 1",
#     "Region": "State 3",
#     "TelNumber": "65237486",
#     "MobNumber": "8989143666",
#     "SmtpAddr": "subodh.barche@merillife.com",
#     "SmtpAddr1": "None",
#     "Zuawa": "",
#     "Akont": "",
#     "Waers": "Currency1",
#     "Zterm": "",
#     "Inco1": "",
#     "Inco2": "",
#     "Kalsk": "",
#     "Ekgrp": "",
#     "Xzemp": "",
#     "Reprf": "",
#     "Webre": "",
#     "Lebre": "",
#     "Stcd3": "",
#     "J1ivtyp": "Vendor Type 2",
#     "J1ipanno": "",
#     "J1ipanref": "",
#     "Namev": "",
#     "Name11": "",
#     "Bankl": "",
#     "Bankn": "",
#     "Bkref": "",
#     "Banka": "",
#     "Xezer": "",
#     "Refno": "VMS/368b008a78/0101"
# }

#     url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
#     #print(vendor_details)
#     headers = {
#     'X-CSRF-TOKEN': 'Fetch'
#     }
#     auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
#     response = requests.get(url, headers=headers, auth=auth)

#         #print(response)
#     if response.status_code == 200:
#         csrf_token = response.headers.get('x-csrf-token')
#         send_detail(csrf_token, vendor_details ,data, method)
#         #print("********************  Token ****************************************")
#         #print("x-csrf-token:", csrf_token)
#         print(vendor_details)
#         return csrf_token
#     else:
#         print("Error:", response.status_code)
#         return "Error: " + str(response.status_code)
#     send_detail("*************************",csrf_token)



#     #*******************************************************************************

#     # headers = {
#     #     'X-CSRF-Token': csrf_token,
#     #     'Content-Type': 'application/json'
#     # }
#     # auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
#     # #print("***********************************************")
    
    
#     # response = requests.post(url, headers=headers, auth=auth, json=vendor_details)
#     # print("***********************************************", response.status_code)
    
    
#     # if response.status_code == 200:  
#     #    # print("*****************************************")
#     #     print("Vendor details posted successfully.")
#     #     #return "************************Vendor details posted successfully.******************************"
#     # else:
#     #     print("Error in POST request:", response.status_code)
#     #     return "Error in POST request: " + str(response.status_code)


# @frappe.whitelist()
# def send_detail(csrf_token, vendor_details ,data, method):
#     url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
#     print("*************************************")
#     print(csrf_token)
#     csrf_token_str = str(csrf_token)
#     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", csrf_token)


#     headers = {
#         'X-CSRF-TOKEN': "722gVEt7-nV-J3R_vjRSJg==",
#         'Content-Type': 'application/json',
#         'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ='
#     }
#     auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
#     #print("***********************************************")
    
    
#     response = requests.post(url, headers=headers, auth=auth, json=vendor_details)
#     print("***********************************************", response.status_code)
    
    
#     if response.status_code == 200:  
#        # print("*****************************************")
#         print("Vendor details posted successfully.")
#         #return "************************Vendor details posted successfully.******************************"
#     else:
#         print("Error in POST request:", response.status_code)
#         return "Error in POST request: " + str(response.status_code)







# #********************************************FROM GITHUB  *************************************************************

# def create_sap_so_from_po(data, method):
#     sap_user_data = frappe.cache.get_value("sap_user_data")

#     if not sap_user_data:
#         sap_user_data = get_token_from_sap()
#         frappe.cache.set_value("sap_user_data", sap_user_data,
#                                expires_in_sec=14*60*60)  # 14 mins

#     # purchase_order_items = frappe.get_list(
#     #     "Purchase Order Item", filters={"purchase_order": po_name})
#     # purchase_order = frappe.get_doc("Purchase Order", po_name)
#     # distributor = frappe.get_doc(
#     #     "Distributor Master", purchase_order.get("distributor"))
#     # company = frappe.get_doc("Company Master", purchase_order.get("company"))

#     payload_data = {
#         "ZTPA_REF_NO": "ODATATEST01",
#         "HeadItem": []
#     }
#     data = {
#     "Bukrs": "9000",
#     "Ekorg": "2000",
#     "Ktokk": "",
#     "Title": "NULL",
#     "Name1": "",
#     "Name2": "",
#     "Sort1": "None",
#     "Street": "ADLY2",
#     "StrSuppl1": "ADLY4",
#     "StrSuppl2": "ADLY5",
#     "StrSuppl3": "ADLY6",
#     "PostCode1": "123",
#     "City1": "City 1",
#     "Country": "Country 1",
#     "J1kftind": "Type 1",
#     "Region": "State 4",
#     "TelNumber": "65237486",
#     "MobNumber": "8989143666",
#     "SmtpAddr": "subodh.barche@merillife.com",
#     "SmtpAddr1": "None",
#     "Zuawa": "",
#     "Akont": "",
#     "Waers": "Currency1",
#     "Zterm": "",
#     "Inco1": "",
#     "Inco2": "",
#     "Kalsk": "",
#     "Ekgrp": "",
#     "Xzemp": "",
#     "Reprf": "",
#     "Webre": "",
#     "Lebre": "",
#     "Stcd3": "",
#     "J1ivtyp": "Vendor Type 233333333",
#     "J1ipanno": "",
#     "J1ipanref": "",
#     "Namev": "",
#     "Name11": "",
#     "Bankl": "",
#     "Bankn": "",
#     "Bkref": "",
#     "Banka": "",
#     "Xezer": "",
#     "Refno": "VMS/368b008a78/0101"
#     }
#     payload_data["HeadItem"].append(data)
#    # sr_no_counter += 1
#     url = f"{SAP_BASE_URL}/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
#     headers = {
#         "Content-Type": "application/json;charset=utf-8",
#         "Accept": "application/json",
#         "X-CSRF-TOKEN": data.get("X-CSRF-TOKEN")
#         }

#     auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
#     sales_order_data = send_request(url, payload=payload_data, headers=headers, auth=auth, method="POST")
#     #sales_order_data = requests.post(url, headers=headers, auth=auth, json=data)
#         #return sales_order_data





#**********************************************************************************************************************



@frappe.whitelist()
def validate_aadhar_number():
    pass




    #*******************************************************************************


    # try:
    #     response = requests.post(url, data=vendor_details)
    #     response.raise_for_status()  
    #     print("POST request successful")
    # except requests.RequestException as e:
    #     print(f"Failed to make POST request: {e}")



@frappe.whitelist()
def create_po(**kwargs):
    pass









# SELECT DISTINCT
    # vm.name AS name,
    # status AS status,
    # vendor_name AS vendor_name,
    # vm.company_name AS company_id, 
    # cm.company_name AS company_name, 
    # dm.department_name AS department_id, 
    # dt.district_name AS district_name,
    # ct.city_name AS city_name,
    # st.state_name AS state_name
# FROM 
#     `tabVendor Master` vm 
# LEFT JOIN 
#     `tabCompany Master` cm ON vm.company_name = cm.name 
# LEFT JOIN 
#     `tabDepartment Master` dm ON vm.department = dm.name 
# LEFT JOIN 
#     `tabDistrict Master` dt ON dt.district_name = dt.district_name
# LEFT JOIN 
#     `tabCity Master` ct ON ct.city_name = ct.city_name
# LEFT JOIN 
#     `tabState Master` st ON st.state_name = st.state_name


@frappe.whitelist()
def vendor_onboarding(**kwargs):
    pass




@frappe.whitelist()
def show_vendor(data, method):

    name = data.get("name")
    values = frappe.db.sql(""" select * from `tabVendor Onboarding` where name=%s """,(name),as_dict=1)
    return values



