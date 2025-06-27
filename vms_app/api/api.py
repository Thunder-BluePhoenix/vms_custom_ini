from __future__ import unicode_literals
import frappe
from datetime import datetime, timedelta
from frappe.auth import clear_sessions
from frappe.utils.file_manager import save_url
# from numpy import convolve
import requests # type: ignore
import json
from frappe.utils.background_jobs import enqueue
from frappe import _
from frappe.utils.file_manager import get_file_url
from frappe.utils import get_url
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
from requests.auth import HTTPBasicAuth # type: ignore
# from cryptography.fernet import Fernet
import base64
from vms_app.api.config.api import SAP_BASE_URL
from vms_app.utils.utils import get_token_from_sap, send_request
import uuid
from frappe.utils.file_manager import save_file
from frappe.utils.password import get_decrypted_password
import random
import string
import os, pdb
# import psycopg2
# from werkzeug.utils import secure_filename
import pandas as pd # type: ignore
from frappe.exceptions import DoesNotExistError
import logging
import mimetypes

@frappe.whitelist()
def show_single_purchase_order_vendor(**kwargs):
    print("Parameters")
    # pdb.set_trace()
    name = kwargs.get("name",None)
    vendor_code = kwargs.get("vendor_code", None)
    po_number = kwargs.get("po_number", None)

    if not (name or vendor_code or po_number):
        return {"error": "At least one of 'name', 'vendor_code', or 'po_number' is required."}

    # Check if vendor_code is null or zero
    # if vendor_code in [None, '', 0]:
    #     return []

    if name:
        purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` WHERE name=%s """, (name,), as_dict=1)
    elif po_number:
        purchase_detail = frappe.db.sql("""SELECT * FROM `tabPurchase Order` WHERE po_number=%s """, (po_number,), as_dict=1)
    elif vendor_code:
        purchase_detail = frappe.db.sql("""SELECT * FROM `tabPurchase Order` WHERE vendor_code=%s""", (vendor_code,), as_dict=1)    
    else:
        purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order`""", as_dict=1)

    for detail in purchase_detail:
        purchase_items = frappe.db.sql(""" SELECT * FROM `tabPurchase Order Item` WHERE parent=%s """, (detail['name'],), as_dict=1)
        detail['items'] = purchase_items

        if detail.get('vendor_code'):
            onboarding_ref_no = frappe.db.get_value("Vendor Master", detail['vendor_code'], "onboarding_ref_no")
            if onboarding_ref_no:
                vendor_onboarding_details = frappe.db.sql("""SELECT * FROM `tabVendor Onboarding` WHERE name=%s""", (onboarding_ref_no,), as_dict=1)
                detail['vendor_onboarding_details'] = vendor_onboarding_details
      
        # if detail.get('material_code'):
        #     material_name = frappe.db.get_value("Material Master", detail['material_code'], "material_name")
        #     detail['material_code'] = material_name
        # if detail.get('product_code'):
        #     product_name = frappe.db.get_value("Product Master", detail['product_code'], "product_name")
        #     detail['product_code'] = product_name
        if detail.get('purchase_group'):
            purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
            detail['purchase_group'] = purchase_group_name
        if detail.get('company_code'):
            company_name = frappe.db.get_value("Company Master", detail['company_code'], "company_name")
            detail['company_code'] = company_name
        # if detail.get('product_category'):
        #     product_category_name = frappe.db.get_value("Product Category Master", detail['product_category'], "product_category_name")
        #     detail['product_category'] = product_category_name
        # if detail.get('material_category'):
        #     material_category_name = frappe.db.get_value("Material Category Master", detail['material_category'], "material_category_name")
        #     detail['material_category'] = material_category_name
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
        if detail.get('terms_of_payment'):
            terms_of_payment_name = frappe.db.get_value("Terms Of Payment Master", detail['terms_of_payment'], "terms_of_payment_name")
            detail['terms_of_payment'] = terms_of_payment_name

       
        for item in purchase_items:
            if item.get('material_code'):
                material_name = frappe.db.get_value("Old Material Master", item['material_code'], "material_name")
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

@frappe.whitelist(allow_guest=True)
def get_file_with_token(file_name, token):
    user_api_key = frappe.db.get_value("User", {"api_key": token}, "name")

    if not user_api_key:
        frappe.throw(_("Invalid or expired token"))
    
    file = frappe.get_doc("File", {"file_url": file_name, "is_private": 1})
    if file:
        file_url = get_url(file.file_url)
        return {"file_url": file_url}
    else:
        frappe.throw(_("File not found"))


@frappe.whitelist()
def fetch_delivery_date_changes(**kwargs):
    vendor_code = kwargs.get('vendor_code')
    print("Vendor Code for Delivery Date Changes:", vendor_code)

    delivery_date_changes = frappe.db.sql("""
        SELECT 
            ddc.name AS name,
            ddc.vendor_code,
            ddc.purchase_num,
            ddc.meril_email_address,
            ddc.old_po_date,
            ddc.new_po_date,
            ddc.remarks,
            ddc.vendor_remark,
            ddc.modified_by,
            ddc.modified,
            ddc.status,
            po.bill_to_company,
            po.ship_to_company,
            po.total_value_of_po__so,
            po.status AS po_status,
            vm.vendor_name
        FROM 
            `tabDelivery Date Change` ddc
        LEFT JOIN 
            `tabPurchase Order` po ON ddc.purchase_num = po.name
        LEFT JOIN
            `tabCompany Master` cm ON po.bill_to_company = cm.company_name
        LEFT JOIN
            `tabVendor Master` vm ON ddc.vendor_code = vm.vendor_code
        WHERE 
            (%(vendor_code)s IS NULL OR ddc.vendor_code = %(vendor_code)s)
    """, {'vendor_code': vendor_code}, as_dict=1)

    return delivery_date_changes



@frappe.whitelist()
def show_po_count_vendor(**kwargs):
    vendor_code = kwargs.get('vendor_code')
    print("Vendor Code for PO Count:", vendor_code)  

    if vendor_code:
        po_counts = frappe.db.sql("""
            SELECT 
                COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_count,
                COUNT(CASE WHEN status IN ('Pending', 'Shipped') THEN 1 END) AS pending_shipped_count,
                COUNT(*) AS total_count
            FROM 
                `tabPurchase Order` 
            WHERE 
                vendor_code = %s
        """, (vendor_code,), as_dict=1)
    else:
        po_counts = frappe.db.sql("""
            SELECT 
                COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_count,
                COUNT(CASE WHEN status IN ('Pending', 'Shipped') THEN 1 END) AS pending_shipped_count,
                COUNT(*) AS total_count
            FROM 
                `tabPurchase Order` 
            WHERE 
                vendor_code IS NULL OR vendor_code = ''
        """, as_dict=1)

    return po_counts

@frappe.whitelist()
def show_purchase_order(**kwargs):
    rfq_number = kwargs.get("rfq_number")
    rfq = show_rfq_detail(rfq_number)
    purchase_detail = frappe.db.sql("""SELECT * FROM `tabPurchase Order` WHERE rfq_code=%s""", (rfq_number), as_dict=1)
    parent = frappe.db.get_value("Purchase Order", filters={'rfq_code': rfq_number}, fieldname=["name"])
    purchase_items = frappe.db.sql("""SELECT * FROM `tabPurchase Order Item` WHERE parent=%s""", (parent), as_dict=1)

    
    for detail in purchase_detail:
        if detail.get('material_code'):
            material_code = frappe.db.get_value("Old Material Master", detail['material_code'], "material_code")
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
            material_code = frappe.db.get_value("Old Material Master", item['material_code'], "material_code")
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


@frappe.whitelist()
def send_email_on_vendor_po_status(**kwargs):
    import smtplib
    from email.mime.text import MIMEText

    name = kwargs.get("name")
    po_number = kwargs.get("po_number")

    if name:
        purchase_detail = frappe.db.sql("""SELECT * FROM `tabPurchase Order` WHERE name=%s""", (name,), as_dict=1)
    elif po_number:
        purchase_detail = frappe.db.sql("""SELECT * FROM `tabPurchase Order` WHERE po_number=%s""", (po_number,), as_dict=1)
    else:
        purchase_detail = frappe.db.sql("""SELECT * FROM `tabPurchase Order`""", as_dict=1)

    if not purchase_detail:
        frappe.throw("No purchase details found.")

    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    from_address = "noreply@merillife.com"
    bcc_address = "rishi.hingad@merillife.com"

    for po in purchase_detail:
        vendor_status = po.get("vendor_status")
        vendor_code = po.get("vendor_code")

        vendor_email = frappe.db.get_value("Vendor Master", {"vendor_code": vendor_code}, "office_email_primary")
        vendor_name = frappe.db.get_value("Vendor Master", {"vendor_code": vendor_code}, "vendor_name")
        registered_email = frappe.db.get_value("Vendor Master", {"vendor_code": vendor_code}, "registered_by")
        if not vendor_email:
            frappe.throw(f"Vendor email is missing for Purchase Order {po.get('name')}.")

        if vendor_status == "Rejected":
            vendors_reason_to_reject = po.get("vendors_reason_to_reject")
            subject = f"Purchase Order {po.get('name')} Rejected by {vendor_name}"
            message = f"""
                Dear Team,

                Your purchase order {po.get('po_number')} has been rejected by {vendor_name}.
                Reason for rejection: {vendors_reason_to_reject}.

                Regards,
                {vendor_name}
            """
        elif vendor_status == "Accepted":
            vendors_tentative_delivery_date = po.get("vendors_tentative_delivery_date")
            subject = f"Purchase Order {po.get('name')} Accepted by {vendor_name}"
            message = f"""
                Dear Team,

                Your purchase order {po.get('po_number')} has been accepted by {vendor_name}.
                Tentative delivery date: {vendors_tentative_delivery_date}.

                Regards,
                {vendor_name}
            """
        else:
            continue

        msg = MIMEText(message, "plain")
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = registered_email
        msg["Bcc"] = bcc_address

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [registered_email, bcc_address], msg.as_string())
                print("Email sent successfully!")
            # Log Email
            doc = frappe.get_doc({
                "doctype": "Email Log",
                "ref_no": po.get("po_number"),
                "to_email": registered_email,
                "from_email": from_address,
                "message": message,
                "status": "Successfully Sent",
                "screen": "PO Status Successfully Sent",
                "created_by": from_address,
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

        except Exception as e:
            # Log Failed Email
            doc = frappe.get_doc({
                "doctype": "Email Log",
                "ref_no": po.get("po_number"),
                "to_email": registered_email,
                "from_email": from_address,
                "message": message,
                "status": f"Failed to send email: {e}",
                "screen": "PO Status Send Failed",
                "created_by": from_address,
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            frappe.throw(f"Failed to send email to {vendor_email}. Error: {str(e)}")

    frappe.msgprint("Emails sent successfully.")


@frappe.whitelist(allow_guest=True)
def get_purchase_order_data():
    purchase_orders = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` """, as_dict=1)

    for po in purchase_orders:
        purchase_items = frappe.db.sql(""" SELECT * FROM `tabPurchase Order Item` WHERE parent=%s """, (po['name'],), as_dict=1)

        po['items'] = purchase_items
        if po.get('purchase_group'):
            purchase_group_desc = frappe.db.get_value("Purchase Group Master", po['purchase_group'], "description")
            po['purchase_group_description'] = purchase_group_desc if purchase_group_desc else ""
        vendor_code = po.get('vendor_code')
        # print(f"Vendor Code: {vendor_code}")

        if vendor_code:

            vendor_details = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=["name", "vendor_name", "company_name", "registered_by"], as_dict=True)

            # print(f"Vendor Details: {vendor_details}")

            if vendor_details:
                po.update(vendor_details)
                frappe.logger().info(f"Vendor details found: {vendor_details}")
                parent_name = vendor_details.get("name")

                registered_by = vendor_details.get("registered_by")
                if registered_by:
                    team_name = frappe.db.get_value("User", {"name": registered_by}, "team")
                    po["registered_by_team"] = team_name if team_name else None
                    frappe.logger().info(f"Team found for {registered_by}: {team_name}")

                multiple_company_data = frappe.db.sql(""" 
                    SELECT * FROM `tabMultiple Company Data` 
                    WHERE parent=%s 
                """, (parent_name,), as_dict=1)

                if multiple_company_data:
                    po['multiple_company_data'] = multiple_company_data
                else:
                    vendor_company_name = vendor_details.get("company_name")
                    if vendor_company_name:
                        vendor_company_code = frappe.db.get_value("Company Master", {"name": vendor_company_name}, "company_name")
                        po["vendor_company_code"] = vendor_company_code if vendor_company_code else None

            else:
                frappe.logger().warning(f"No vendor details found for: {vendor_code}")

    return purchase_orders

# ======================= NEW METHOD ================
@frappe.whitelist(allow_guest=True)
def show_single_purchase_order(**kwargs):
    name = kwargs.get("name")
    po_number = kwargs.get("po_number")

    if name:
        purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` WHERE name=%s """, (name,), as_dict=1)
    elif po_number:
        purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order` WHERE po_number=%s """, (po_number,),as_dict=1)
    else:
        purchase_detail = frappe.db.sql(""" SELECT * FROM `tabPurchase Order`""", as_dict=1)

    for detail in purchase_detail:
        purchase_items = frappe.db.sql(""" SELECT * FROM `tabPurchase Order Item` WHERE parent=%s """, (detail['name'],), as_dict=1)        
        detail['items'] = purchase_items

    if detail.get('terms_of_payment'):
        print(f"Terms of Payment for {detail['name']}: {detail['terms_of_payment']}")

    if detail.get('terms_of_payment'):
        detail['terms_of_payment'] = detail['terms_of_payment'] 
        terms_of_payment_name = frappe.db.get_value("Terms Of Payment Master", detail['terms_of_payment'], "terms_of_payment_name")
        detail['terms_of_payment'] = terms_of_payment_name
    else:
        print(f"Terms of Payment is null for {detail['name']}")

    for item in purchase_items:
        if item.get('product_code'):
            item['product_code'] = item['product_code']
    
        if detail.get('vendor_code'):
            print(f"Found vendor_code: {detail['vendor_code']}")


        vendor_master_details = frappe.db.sql("""SELECT * FROM `tabVendor Master` WHERE vendor_code=%s""", (detail['vendor_code'],), as_dict=1)
        # print(f"onboarding_ref_no query result for vendor_code {detail['vendor_code']}: {vendor_master_details}")
        
        if vendor_master_details:
            vendor_master_detail = vendor_master_details[0]
            detail['vendor_name'] = vendor_master_detail.get('vendor_name')
            detail['registered_by'] = vendor_master_detail.get('registered_by')
            detail['vendor_email'] = vendor_master_detail.get('office_email_primary')
            
            onboarding_ref_no = vendor_master_detail.get('onboarding_ref_no')
            print(f"Extracted onboarding_ref_no: {onboarding_ref_no}")
            
            incoterms = vendor_master_detail.get('incoterms')
            if incoterms:
                incoterm_name = frappe.db.get_value(
                    "Incoterm Master", 
                    {"name": incoterms}, 
                    "incoterm_name"
                )
                if incoterm_name:
                    print(f"Incoterm Name: {incoterm_name}")
                    detail['incoterm_name'] = incoterm_name
                else:
                    print(f"No incoterm_name found for incoterm: {incoterms}")
            else:
                print("No incoterms found in Vendor Master")
            
            if onboarding_ref_no:
                vendor_onboarding_details = frappe.db.sql(
                    """ SELECT * FROM `tabVendor Onboarding` WHERE name=%s """, 
                    (onboarding_ref_no,), 
                    as_dict=1
                )
                if vendor_onboarding_details:
                    detail['vendor_onboarding_details'] = vendor_onboarding_details
                else:
                    print(f"No Vendor Onboarding Details found for onboarding_ref_no: {onboarding_ref_no}")
            else:
                print(f"onboarding_ref_no is None for vendor_code: {detail['vendor_code']}")
        else:
            detail['vendor_name'] = None
            detail['registered_by'] = None
            print(f"No Vendor Master details found for vendor_code: {detail.get('vendor_code')}")

        # if detail.get('material_code'):
        #     material_name = frappe.db.get_value("Material Master", detail['material_code'], "material_name")
        #     detail['material_code'] = material_name
        # if detail.get('product_code'):
        #     product_name = frappe.db.get_value("Product Master", detail['product_code'], "product_name")
        #     detail['product_code'] = product_name
        if detail.get('purchase_group'):
            purchase_group_name = frappe.db.get_value("Purchase Group Master", detail['purchase_group'], "purchase_group_name")
            detail['purchase_group'] = purchase_group_name
        if detail.get('company_code'):
            company_name = frappe.db.get_value("Company Master", detail['company_code'], "company_name")
            detail['company_code'] = company_name
        # if detail.get('product_category'):
        #     product_category_name = frappe.db.get_value("Product Category Master", detail['product_category'], "product_category_name")
        #     detail['product_category'] = product_category_name
        # if detail.get('material_category'):
        #     material_category_name = frappe.db.get_value("Material Category Master", detail['material_category'], "material_category_name")
        #     detail['material_category'] = material_category_name
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
                material_name = frappe.db.get_value("Old Material Master", item['material_code'], "material_name")
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
            print("**************", status, message, resp)
            
            # Add country name to the response
            resp["countryName"] = "India"
            return {"status": status, "resp": resp}
        else:
            frappe.throw(f"API request failed with status code {response.status_code}")
    
    except Exception as e:
        frappe.throw(f"An error occurred while making the API request: {str(e)}")

#*******************************************GST NUMBER VERIFICATION API CLOSED ************************************************

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
            LEFT JOIN `tabOld Material Master` mm ON pd.material_type = mm.name
            LEFT JOIN `tabCountry Master` cm ON pd.country_of_origin = cm.name
            LEFT JOIN `tabOld Material Master` mm2 ON pd.material_used = mm2.name
    """

    if name:
        query += " WHERE pd.name=%s"
        product = frappe.db.sql(query, (name,), as_dict=1)
    else:
        product = frappe.db.sql(query, as_dict=1)

    return product

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


@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    frappe.logger("login").error("Login Method----")

    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.local.response["message"] = {
            "success_key": 0,
            "message": "Authentication Error!"
        }
        return

    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)

    # Fetch additional details
    user_designation_id = frappe.db.get_value("User", {'email': user.email}, 'designation')
    user_name = frappe.db.get_value("User", {'email': user.email}, 'full_name')
    user_designation_name = frappe.db.get_value("Designation Master", {'name': user_designation_id}, 'designation_name')
    refno = frappe.db.get_value("Vendor Master", {'office_email_primary': user.email}, 'name')
    vendor_code = frappe.db.get_value("Vendor Master", {'office_email_primary': user.email}, 'vendor_code')
    company_code = frappe.db.get_value("User", {'email': user.email}, 'user_company')
    company_name = frappe.db.get_value("Company Master", {'name': company_code}, 'company_name')
    company_short = frappe.db.get_value("Company Master", {'name': company_code}, 'short_form')

    frappe.response["message"] = {
        "success_key": 1,
        "message": "Authentication success",
        "sid": frappe.session.sid,
        # "api_key": api_generate.get('api_key'),
        # "api_secret": api_generate.get('api_secret'),
        "designation_name": user_designation_name,
        "username": user.username,
        "email": user.email,
        "refno": refno,
        "vendor_code": vendor_code,
        "full_name": user_name,
        "company_code": company_code,
        "user_company": company_name,
        "company_short_form": company_short
    }

    # frappe.local.response["cookies"] = {
    #     "sid": {"value": frappe.session.sid, "httponly": True},
    #     "api_key": {"value": api_generate.get("api_key"), "httponly": True},
    # }

def generate_keys(user):
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)
    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
    else:
        api_key = user_details.api_key
    user_details.api_secret = api_secret
    user_details.save()

    return {
        "api_key": api_key,
        "api_secret": api_secret
    }

@frappe.whitelist(allow_guest=True)
def clear_last_active_session(usr):
    """Clear the last active session ID when the user chooses to log out from previous session"""
    frappe.db.set_value("User", usr, "last_active_sid", None)
    frappe.db.commit()

    return {"success": True, "message": "Previous session logged out. Please try logging in again."}


@frappe.whitelist(allow_guest=True)
def logout():
    frappe.local.login_manager.logout()

    # Set response correctly
    frappe.response["message"] = "Logged out successfully"
    frappe.response["type"] = "json"
    frappe.response["cookies"] = {
        "sid": {"value": "", "expires": 0, "httponly": True}
    }

    return frappe.response

@frappe.whitelist(allow_guest=True)
def verify_otp(user_name, entered_otp):
    stored_otp = frappe.db.get_value('Vendor Master', {'office_email_primary': user_name}, 'otp')
    otp_expiry_time_str = frappe.db.get_value('Vendor Master', {'office_email_primary': user_name}, 'otp_expiry_time')
   
    otp_expiry_time = datetime.fromisoformat(otp_expiry_time_str)
    
    if datetime.now() > otp_expiry_time:
        return "OTP expired."
    
    if stored_otp == entered_otp:
        return "OTP correct. Access granted."
    else:
        return "Wrong OTP."
    

@frappe.whitelist(allow_guest=True)
def send_otp(**kwargs):
    reciever_email = kwargs.get('email')

    try:
        user = frappe.get_doc("User", reciever_email)
        
        otp = ''.join(random.choices(string.digits, k=6))
        expiry_time = datetime.now() + timedelta(minutes=5)

        vendor_name = frappe.db.get_value("Vendor Master", filters={'office_email_primary': reciever_email}, fieldname=['vendor_name'])
        
        frappe.db.set_value('Vendor Master', {'office_email_primary': reciever_email}, 'otp', otp)
        frappe.db.set_value('Vendor Master', {'office_email_primary': reciever_email}, 'otp_expiry_time', expiry_time)
    
        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        from_address = 'noreply@merillife.com'
        to_address = reciever_email
        subject = "One Time Password for Password Reset"
        body = f"""
        Dear {vendor_name},
        Your One-Time Password for the Vendor Management System (VMS) Portal is {otp}.
        """
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
                doc = frappe.get_doc({
                    'doctype': 'Email Log',        
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Forgot Password",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

            return {
                "status": "success",
                "message": _("OTP sent successfully.")
            }

        except Exception as e:
            print(f"Failed to send email: {e}")
            msge = f"Failed to send email: {e}"
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "Forgot Password",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

            return {
                "status": "fail",
                "message": _("Failed to send email.")
            }

    except DoesNotExistError:
        user_message = f"User {reciever_email} does not exists."
        frappe.log_error(user_message, _("User not found"))
        server_message = frappe.as_json([{
            "message": user_message,
            "title": "Message",
            "indicator": "red",
            "raise_exception": 1
        }])
        return {
            "status": "fail",
            "message": user_message,
            "_server_messages": server_message
        }

@frappe.whitelist(allow_guest=True)
def send_material_onboarding_otp(**kwargs):
    reciever_email = kwargs.get('email')

    reciever_name = frappe.db.get_value("Employee Master", {'email': reciever_email}, 'full_name')

    if not reciever_name:
        return {
            "status": "fail",
            "message": f"Employee with email {reciever_email} does not exist in Employee Master."
        }

    otp = ''.join(random.choices(string.digits, k=6))
    expiry_time = datetime.now() + timedelta(minutes=5)

    frappe.db.set_value("Employee Master", {'email': reciever_email}, "otp", otp)
    frappe.db.set_value("Employee Master", {'email': reciever_email}, "otp_expiry_time", expiry_time)

    from_address = 'noreply@merillife.com'
    to_address = reciever_email
    bcc_address = 'rishi.hingad@merillife.com'
    subject = "One Time Password for Material Onboarding"
    body = f"""
    Dear {reciever_name},

    Your OTP for accessing the Vendor Management System (VMS) Portal for material onboarding is: {otp}.

    This OTP is valid for 5 minutes.

    Regards,  
    Meril VMS Team
    """

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "plain"))

    try:
        conf = frappe.conf
        with smtplib.SMTP(conf.get("smtp_server"), conf.get("smtp_port")) as server:
            server.starttls()
            server.login(conf.get("smtp_user"), conf.get("smtp_password"))
            server.sendmail(from_address, [to_address, bcc_address], msg.as_string())

        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': "Successfully Sent",
            'screen': "Material Onboarding",
            'created_by': from_address
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "success", "message": _("OTP sent successfully.")}

    except Exception as e:
        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': f"Failed: {e}",
            'screen': "Material Onboarding",
            'created_by': from_address
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "fail", "message": _("Failed to send OTP email.")}

from frappe.auth import LoginManager

# @frappe.whitelist(allow_guest=True)
# def verify_material_onboarding_otp(user_name, entered_otp):
#     stored_otp = frappe.db.get_value('Employee Master', {'email': user_name}, 'otp')
#     otp_expiry_time_str = frappe.db.get_value('Employee Master', {'email': user_name}, 'otp_expiry_time')

#     if not stored_otp or not otp_expiry_time_str:
#         return {"status": "fail", "message": "OTP not found. Please request again."}

#     otp_expiry_time = datetime.fromisoformat(otp_expiry_time_str)

#     if datetime.now() > otp_expiry_time:
#         return {"status": "fail", "message": "OTP expired. Please request a new one."}

#     if stored_otp == entered_otp:
#         frappe.set_user("Guest")
#         frappe.local.login_manager = LoginManager()
#         frappe.local.login_manager.login_as(user_name)

#         user = frappe.get_doc('Employee Master', user_name)
#         user_role_id = frappe.db.get_value("Employee Master", {'email': user.email}, 'role')
#         user_name_full = frappe.db.get_value("Employee Master", {'email': user.email}, 'full_name')
#         # user_designation_name = frappe.db.get_value("Designation Master", {'name': user_designation_id}, 'designation_name')
#         # refno = frappe.db.get_value("Vendor Master", {'office_email_primary': user.email}, 'name')
#         vendor_code = frappe.db.get_value("Vendor Master", {'office_email_primary': user.email}, 'vendor_code')
#         company_code = frappe.db.get_value("Employee Master", {'email': user.email}, 'company')
#         company_name = frappe.db.get_value("Company Master", {'name': company_code}, 'company_name')
#         company_short = frappe.db.get_value("Company Master", {'name': company_code}, 'short_form')

#         return {
#             "status": "success",
#             "message": "OTP verified. Access granted.",
#             "email": user.email,
#             "full_name": user_name_full,
#             "role": user_role_id,
#             "vendor_code": vendor_code,
#             "company_code": company_code,
#             "user_company": company_name,
#             "company_short_form": company_short,
#             "sid": frappe.session.sid,
#         }

#     return {"status": "fail", "message": "Invalid OTP"}


@frappe.whitelist(allow_guest=True)
def verify_material_onboarding_otp(user_name, entered_otp):
    stored_otp = frappe.db.get_value('Employee Master', {'email': user_name}, 'otp')
    otp_expiry_time_str = frappe.db.get_value('Employee Master', {'email': user_name}, 'otp_expiry_time')

    if not stored_otp or not otp_expiry_time_str:
        return {"status": "fail", "message": "OTP not found. Please request again."}

    otp_expiry_time = datetime.fromisoformat(otp_expiry_time_str)

    if datetime.now() > otp_expiry_time:
        return {"status": "fail", "message": "OTP expired. Please request a new one."}

    if stored_otp != entered_otp:
        return {"status": "fail", "message": "Invalid OTP"}

    if not frappe.db.exists("User", user_name):
        full_name = frappe.db.get_value("Employee Master", {"email": user_name}, "full_name") or "Guest"
        new_user = frappe.get_doc({
            "doctype": "User",
            "email": user_name,
            "first_name": full_name,
            "enabled": 1,
            "new_password": frappe.generate_hash(user_name),
            "send_welcome_email": 0,
            "roles": [{
                "role": "System Manager",
                "apply_user_permissions": 1
            }]
        })
        new_user.flags.ignore_permissions = True
        new_user.insert(ignore_permissions=True)

    frappe.set_user("Guest")
    frappe.local.login_manager = LoginManager()
    frappe.local.login_manager.login_as(user_name)

    user = frappe.get_doc('Employee Master', {'email': user_name})
    user_role_id = user.role
    user_name_full = user.full_name
    vendor_code = frappe.db.get_value("Vendor Master", {'office_email_primary': user.email}, 'vendor_code')
    company_code = user.company
    company_name = frappe.db.get_value("Company Master", {'name': company_code}, 'company_name')
    company_short = frappe.db.get_value("Company Master", {'name': company_code}, 'short_form')

    return {
        "status": "success",
        "message": "OTP verified. Access granted.",
        "email": user.email,
        "full_name": user_name_full,
        "role": user_role_id,
        "vendor_code": vendor_code,
        "company_code": company_code,
        "user_company": company_name,
        "company_short_form": company_short,
        "sid": frappe.session.sid,
    }


@frappe.whitelist(allow_guest=True)
def employee_login_abc(data):
    usr = data.get("usr")
    pwd = data.get("pwd")
    if not usr.endswith("@merillife.com"):
        return {"status": "fail", "message": "Only @merillife.com emails are allowed."}

    employee = frappe.db.get("Employee Master", {"email": usr})
    if not employee:
        return {"status": "fail", "message": "User not found in Employee Master."}

    if not frappe.db.exists("User", usr):
        new_user = frappe.get_doc({
            "doctype": "User",
            "email": usr,
            "first_name": employee.full_name,
            "enabled": 1,
            "new_password": pwd,
            "send_welcome_email": 0,
            "roles": [{"role": "System Manager"}]
        })
        new_user.flags.ignore_permissions = True
        new_user.insert(ignore_permissions=True)

    # Login using Frappe LoginManager
    try:
        frappe.local.login_manager = LoginManager()
        frappe.local.login_manager.authenticate(usr, pwd)
        frappe.local.login_manager.post_login()
    except frappe.AuthenticationError:
        return {"status": "fail", "message": "Invalid username or password."}

    company_code = employee.company
    company_name = frappe.db.get_value("Company Master", {'name': company_code}, 'company_name')
    company_short = frappe.db.get_value("Company Master", {'name': company_code}, 'short_form')

    return {
        "status": "success",
        "message": "Logged in",
        "sid": frappe.session.sid,
        "email": usr,
        "full_name": employee.full_name,
        "role": employee.role,
        "company_code": company_code,
        "user_company": company_name,
        "company_short_form": company_short
    }


# @frappe.whitelist()
# def get_all_material_type_master_details():
#     try:
#         material_type_masters = frappe.get_all(
#             "Material Type Master",
#             fields=["*"],
#         )

#         result = []

#         for mt in material_type_masters:
#             doc = frappe.get_doc("Material Type Master", mt.name)

#             valuation_rows = []
#             for row in doc.valuation_and_profit:
#                 valuation_rows.append({
#                     "valuation_class": row.valuation_class,
#                     "profit_center": row.profit_center,
#                     "division": row.division,
#                 })

#             result.append({
#                 "name": doc.name,
#                 "material_type_name": doc.material_type_name,
#                 "description": doc.description,
#                 "company": doc.company,
#                 "valuation_and_profit": valuation_rows
#             })

#         return result

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "get_all_material_type_master_details_error")
#         return frappe.throw(_("Failed to fetch Material Type Master details: {0}").format(str(e)))

@frappe.whitelist()
def get_all_material_type_master_details():
    try:
        material_type_masters = frappe.get_all(
            "Material Type Master",
            fields=["*"],
        )

        result = []

        for mt in material_type_masters:
            doc = frappe.get_doc("Material Type Master", mt.name)

            valuation_rows = []
            for row in doc.valuation_and_profit:
                valuation_class_description = ""
                if row.valuation_class:
                    vc = frappe.get_value("Valuation Class Master",row.valuation_class,"valuation_class_name")
                    valuation_class_description = vc or ""
                
                profit_center_description = ""
                if row.profit_center:
                    pc = frappe.get_value("Profit Center Master",row.profit_center,"description")
                    profit_center_description = pc or ""

                valuation_rows.append({
                    "valuation_class": row.valuation_class,
                    "valuation_class_description": valuation_class_description,
                    "profit_center": row.profit_center,
                    "profit_center_description": profit_center_description,
                    "division": row.division,
                })

            result.append({
                "name": doc.name,
                "material_type_name": doc.material_type_name,
                "description": doc.description,
                "company": doc.company,
                "valuation_and_profit": valuation_rows
            })

        return result

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_all_material_type_master_details_error")
        return frappe.throw(_("Failed to fetch Material Type Master details: {0}").format(str(e)))
    

@frappe.whitelist()
def erp_to_sap_material_code(doc_name):
    print("****Calling ERP TO SAP API******",doc_name)
    try:
        requestor = frappe.get_doc("Requestor Master", doc_name)
        material_master = frappe.get_doc("Material Master", requestor.material_master_ref_no)
        onboarding = frappe.get_doc("Material Onboarding", requestor.material_onboarding_ref_no)
        sap_settings = frappe.get_doc("SAP Settings")

        sap_client_code = ""
        material_items = []
        for item in requestor.material_request:
            material_items.append({
                "material_name_description": item.material_name_description or "",
                "material_code_revised": item.material_code_revised or "",
                "company_code": item.company_name or "",
                "plant_name": item.plant_name or "",
                "material_category": item.material_category or "",
                "material_type": item.material_type or "",
                "base_unit_of_measure": item.base_unit_of_measure or "",
                "comment_by_user": item.comment_by_user or "",
                "material_specifications": item.material_specifications or ""
            })
        if not sap_client_code and item.company_name:
            try:
                company_code = item.company_name
                company_doc = frappe.get_doc("Company Master", company_code)
                sap_client_code = company_doc.sap_client_code or ""
            except Exception as e:
                frappe.log_error(f"Company Master fetch failed for {item.company_name}", str(e))
        print("SAP CLIENT CODE--->",sap_client_code)
        company_code = ""
        if requestor.material_request:
            company_code = requestor.material_request[0].company_name

        if not company_code:
            frappe.throw("Company Code is missing from material request item.")

        last_request_id = frappe.db.sql("""
            SELECT request_id FROM `tabRequestor Master`
            WHERE request_id LIKE %s AND LENGTH(request_id) = 7
            ORDER BY request_id DESC LIMIT 1
        """, (f"{company_code}%",), as_dict=True)

        if last_request_id:
            last_number = int(last_request_id[0]['request_id'][-3:])
            new_suffix = f"{last_number + 1:03d}"
        else:
            new_suffix = "001"

        request_id = f"{company_code}{new_suffix}"
        requestor.request_id = request_id
        print("Request ID--->",request_id)
        requestor.save(ignore_permissions=True)

        bukrs = material_items[0]["company_code"] if material_items else ""
        batch_value = material_master.batch_requirements_yn
        batch_management_indicator = "X" if batch_value == "Yes" else ""
        inspection_1 = onboarding.inspection_require
        inspection_sap = "X" if inspection_1 == "Yes" else ""
        inspection_01 = "X" if onboarding.incoming_inspection_01 else ""
        inspection_09 = "X" if onboarding.incoming_inspection_09 else ""
        serial_number = "" if material_master.serial_number_profile == "No" else material_master.serial_number_profile or ""
        material_type_code = frappe.get_value("Material Type Master", {"name": material_items[0]["material_type"]}, "material_type")
        plant_code = frappe.get_value("Plant Master", {"name": material_items[0]["plant_name"]}, "plant_code")
        category_code = frappe.get_value("Material Category Master", {"name": material_items[0]["material_category"]}, "material_category_name")
        storage_code = frappe.get_value("Storage Location Master", {"name": material_master.storage_location}, "storage_location")
        purchase_group_code = frappe.get_value("Purchase Group Master", {"name": material_master.purchasing_group}, "purchase_group_code")
        division_code = frappe.get_value("Division Master", {"name": material_master.division}, "division_code")
        material_group_code = frappe.get_value("Material Group", {"name": material_master.material_group}, "material_group_name")
        mrp_code = frappe.get_value("MRP Type Master", {"name": material_master.mrp_type}, "mrp_code")
        valuation_class_code = frappe.get_value("Valuation Class Master", {"name": onboarding.valuation_class}, "valuation_class_code")

        data_list = {
            "Reqno": "",
            "Matnr": "",
            "Maktx": "",
            "Zmsg": "",
            "Ztext": "",
            "ZMATSet": []
        }
        data = {
            "Reqno": request_id,
            "Bukrs": bukrs,
            "Matnr" : material_items[0]["material_code_revised"] or "",
            "Adrnr": "",
            "Matkey": "",
            "Mat": category_code or "",
            "Mtart": material_type_code or "",
            "Mbrsh": "P",
            "Werks": plant_code or "",
            "Lgort": storage_code or "",
            "Maktx": material_items[0]["material_name_description"] or "",
            "Meins": material_items[0]["base_unit_of_measure"] or "",
            "Matkl": material_group_code or "",
            "Spart": division_code or "",
            "Brgew": "",
            "Ntgew": "",
            "Gewei": "",
            "Bmatnr": "",
            "Xchpf": batch_management_indicator,
            "Mtvfp": material_master.availability_check or "",
            "Ekgrp": purchase_group_code or "",
            "Bstme": material_master.purchase_uom or "",
            "Umrez": material_master.numerator_purchase_uom or "",
            "Umren": material_master.denominator_purchase_uom or "",
            "Webaz": material_master.gr_processing_time or "",
            "Dismm": mrp_code or "",
            "Dispo": material_master.mrp_controller_revised or "",
            "Disls": material_master.lot_size_key or "",
            "Bstma": "",
            "Mabst": "",
            "Beskz": material_master.procurement_type or "",
            "Lgortep": "",
            "Plifz": material_master.lead_time or "",
            "Fhori": material_master.scheduling_margin_key or "",
            "Eisbe": "",
            "Mhdrz": onboarding.minimum_remaining_shell_life or "",
            "Mhdhb": onboarding.total_shell_life or "",
            "Iprkz": onboarding.expiration_date or "",
            "Prctr": onboarding.profit_center or "",
            "Ausme": material_master.issue_unit or "",
            "Umren1": material_master.numerator_issue_uom or "",
            "Umrez1": material_master.denominator_issue_uom or "",
            "Qmatv": inspection_sap,
            "Qminst": inspection_01,
            "Qminst1": inspection_09,
            "Prfrq": onboarding.inspection_interval or "",
            "Bklas": valuation_class_code or "",
            "Vprsv": onboarding.price_control or "",
            "Ncost": onboarding.do_not_cost or "",
            "Ekalr": "X",
            "Hkmat": "X",
            "Oldmat": material_master.old_material_code or "",
            "Sernp": serial_number,
            "Taxim": "1",
            "Steuc": "",
            "Aedat": "",
            "Aezet": "",
            "Aenam": "",
            "Emailid": "",
            "Storecom": onboarding.comment_by_store or "",
            "Purcom": material_master.purchase_order_text or "",
            "Taxcom": "",
            "Div": "",
            "Ygroup": "",
            "Sgroup": "",
            "Tcode": "", 
            "Ekwsl": material_master.purchasing_value_key or "",
            "Mstcom": "",
            "Qacom": "",
            "Class": material_master.class_type or "",
            "Klart": material_master.class_number or "",
            "Disgr": material_master.mrp_group or "",
            "Lgpro": "",
            "Serlv": ""
        }

        data_list["ZMATSet"].append(data)
        # if debug:
        #     return {
        #         "status": "debug",
        #         "data": data,
        #         "data_list": data_list
        #     }

        # Send to SAP
        url = f"{sap_settings.url}{sap_client_code}"
        headers = {
            'x-csrf-token': 'fetch',
            'Authorization': f"{sap_settings.authorization_type} {sap_settings.authorization_key}",
            'Content-Type': 'application/json'
        }
        auth = HTTPBasicAuth(sap_settings.auth_user_name, sap_settings.auth_user_pass)
        response = requests.get(url, headers=headers, auth=auth)

        if response.status_code == 200:
            csrf_token = response.headers.get('x-csrf-token')
            key1 = response.cookies.get(f'SAP_SESSIONID_BHD_{sap_client_code}')
            key2 = response.cookies.get('sap-usercontext')

            # Send data
            send_material_detail(csrf_token, data_list, key1, key2, sap_client_code, doc_name)
            return {"status": "success", "data_sent": data_list}
        else:
            frappe.log_error(f"Failed to fetch CSRF token: {response.status_code}", "ERP to SAP Material Code")
            return {"status": "fail", "error": "Could not fetch CSRF token"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "ERP to SAP Material Code Error")
        return {"status": "error", "message": str(e)}

def safe_get(obj, list_name, index, attr, default=""):
    try:
        return getattr(getattr(obj, list_name)[index], attr) or default
    except (AttributeError, IndexError, TypeError):
        return default

@frappe.whitelist(allow_guest=True)
def send_material_detail(csrf_token, data_list, key1, key2, sap_client_code, doc_name):
    print("************* Entered send_material_detail *************")
    try:
        sap_settings = frappe.get_doc("SAP Settings")
        erp_to_sap_pr_url = sap_settings.url
        url = f"{erp_to_sap_pr_url}{sap_client_code}"
        header_auth_type = sap_settings.authorization_type
        header_auth_key = sap_settings.authorization_key
        user = sap_settings.auth_user_name
        password = sap_settings.auth_user_pass

        headers = {
            'X-CSRF-TOKEN': csrf_token,
            'Authorization': f"{header_auth_type} {header_auth_key}",
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json',
            'Cookie': f"SAP_SESSIONID_BHD_{sap_client_code}={key1}; sap-usercontext={key2}"
        }

        auth = HTTPBasicAuth(user, password)
        print("Sending payload to SAP...")
        print("Headers:", headers)
        print("Payload:", json.dumps(data_list, indent=2))
        print("*************")
        
        response = requests.post(url, headers=headers, auth=auth, json=data_list)
        print("Response received from SAP")

        try:
            mo_sap_code = response.json()
        except Exception as parse_error:
            print("Failed to parse SAP response as JSON:", parse_error)
            mo_sap_code = response.text

        print("SAP Response Content:", mo_sap_code)

        sap_log = frappe.new_doc("Material SAP Logs")
        sap_log.requestor_ref_no = doc_name
        sap_log.erp_to_sap_data = json.dumps(data_list, indent=2)
        sap_log.sap_response = response.text
        sap_log.save(ignore_permissions=True)
        frappe.db.commit()

        if response.status_code == 201:
            print("Material Onboarding posted successfully.")
            frappe.db.set_value("Requestor Master", doc_name, "approval_status", "Sent to SAP")
            frappe.db.commit()
            send_sap_team_email(doc_name)
        else:
            print(f"SAP POST returned status: {response.status_code}")

        return mo_sap_code

    except Exception as e:
        traceback_str = frappe.get_traceback()
        print("Exception in send_material_detail:")
        print(traceback_str)
        frappe.log_error(traceback_str, "SAP Sync Error")

        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def send_sap_team_email(doc_name):
    print("*******SAP TEAM EMAIL HIT********",doc_name)
    try:
        requestor = frappe.get_doc("Requestor Master", doc_name)
        print("Reqeustor--->",requestor)
        requestor_name = requestor.requested_by
        request_id = requestor.request_id
        email = requestor.contact_information_email
        cc_2 = requestor.immediate_reporting_head
        print("CP TEam--->",cc_2)
        sap_email = frappe.get_value("Employee Master", {"role": "SAP"}, "email")
        mo_doc_name = requestor.material_onboarding_ref_no
        mo_details = frappe.get_doc("Material Onboarding", mo_doc_name)
        cc_team = mo_details.approved_by_name
        print("CP TEam--->",cc_team)
        cc_email = frappe.get_value("Employee Master", {"name": cc_team}, "email")
        print("CP TEam--->",cc_email)
        cp_name = frappe.get_value("Employee Master", {"name": cc_team}, "full_name")
        print("CP Team FUll Name--->",cp_name)
        cc_email2 = frappe.get_value("Employee Master", {"name": cc_2}, "email")

        from_address = "roreply@merillife.com"
        cc_list = list(filter(None, [email, cc_email, cc_email2]))
        bcc_address = "rishi.hingad@merillife.com"

        if not requestor.material_request:
            frappe.throw("No material items found in the request.")
            print("No Material Reqeust Child table.")

        material_row = requestor.material_request[0]
        company_code = material_row.company_name or "-"
        company_name = frappe.get_value("Company Master",{"name": company_code}, "company_name")

        plant_name = material_row.plant_name or "-"
        material_type = material_row.material_type or "-"
        material_description = material_row.material_name_description or "-"

        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")

        if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
            frappe.log_error("SMTP settings missing in site_config", "SAP Email Error")
            return {"status": "fail", "message": _("SMTP settings are not configured.")}

        subject = f"Request for Creating New Material Code in {company_code}-{company_name}"
        message = f"""
            <p>Dear SAP Team,</p>
            <p>The following request to generate or create a new material code has been submitted by <strong>{cp_name}</strong>, which was initially requested by <strong>{requestor_name}</strong>.</p>
            <ul>
                <li><strong>Request ID:</strong> {request_id}</li>
                <li><strong>Company:</strong>{company_code} - {company_name}</li>
                <li><strong>Plant:</strong> {plant_name}</li>
                <li><strong>Material Type:</strong> {material_type}</li>
                <li><strong>Material Description:</strong> {material_description}</li>
            </ul>
            <p>Regards,<br>ERP System</p>
        """

        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = sap_email
        msg['Subject'] = subject
        msg['Cc'] = ", ".join(cc_list)
        msg['Bcc'] = bcc_address
        msg.attach(MIMEText(message, 'html'))

        recipients = [sap_email] + cc_list + [bcc_address]

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipients, msg.as_string())
        server.quit()
        print("Email Sent Successfully")

        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': sap_email,
            'from_email': smtp_user,
            'message': message,
            'status': "Successfully Sent",
            'screen': "Material Onboarding",
            'created_by': smtp_user
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "success", "message": _("Email sent successfully.")}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "SAP Email Send Failed")
        try:
            frappe.get_doc({
                'doctype': 'Email Log',
                'to_email': sap_email if 'sap_email' in locals() else "",
                'from_email': smtp_user if 'smtp_user' in locals() else "",
                'message': f"Error: {str(e)}",
                'status': f"Failed: {e}",
                'screen': "Material Onboarding",
                'created_by': smtp_user if 'smtp_user' in locals() else ""
            }).insert(ignore_permissions=True)
            frappe.db.commit()
        except:
            pass
        return {"status": "fail", "message": _("Failed to send email.")}


@frappe.whitelist(allow_guest = True)
def get_material_code_from_sap():
    print("--------------------API GOT HIT IN SAP---------------")
    try:
        data = frappe.request.get_json()
        # print("SAP Data=====>",data)
        if not data:
            return {"status": "fail", "message": "No JSON body received"}

        reqno = data.get("Reqno")
        matnr = data.get("Matnr")
        maktx = data.get("Maktx")
        zmsg = data.get("Zmsg")
        ztext = data.get("Ztext")

        if not reqno or not matnr:
            return {"status": "fail", "message": "Reqno and Matnr are required fields"}

        requestor_doc = frappe.get_doc("Requestor Master", {"request_id": reqno})
        if not requestor_doc:
            return {"status": "fail", "message": f"No Requestor Master found for request_id: {reqno}"}

        material_master_name = requestor_doc.material_master_ref_no
        material_doc = frappe.get_doc("Material Master", material_master_name)

        material_doc.material_code = matnr
        material_doc.save(ignore_permissions=True)

        requestor_doc.db_set("zmsg", zmsg or "")
        requestor_doc.db_set("ztext", ztext or "")
        requestor_doc.db_set("maktx", maktx or "")
        requestor_doc.db_set("approval_status", "Code Generated by SAP")
        requestor_doc.save(ignore_permissions=True)

        log = frappe.new_doc("Material SAP Logs")
        log.requestor_ref_no = requestor_doc.name
        log.erp_to_sap_data = "NA"
        log.sap_response = json.dumps(data, indent=2)
        log.direction = "SAP to ERP"
        log.save(ignore_permissions=True)

        frappe.db.commit()
        send_email_from_sap(requestor_doc, matnr, maktx, zmsg, ztext)

        return {
            "status": "success",
            "updated_material_code": matnr,
            "material_master": material_master_name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "SAP Material Code Update Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def send_email_from_sap(requestor_doc, matnr, maktx, zmsg, ztext):
    try:
        print("Email Function Hit")

        to_email = requestor_doc.contact_information_email
        if not to_email:
            frappe.log_error("No recipient email found", f"Requestor: {requestor_doc.name}")
            return

        bcc_email = "rishi.hingad@merillife.com"
        cc_email = ""
        from_email = "noreply@merillife.com"

        reporting_to_id = requestor_doc.immediate_reporting_head
        user_name = frappe.get_value("Employee Master", filters={"name": requestor_doc.requested_by}, fieldname=["full_name"])
        if reporting_to_id:
            employee_doc = frappe.get_doc("Employee Master", reporting_to_id)
            cc_email = employee_doc.email or ""

        subject = f"Material Code Created for Request ID {requestor_doc.request_id}"
        message = f"""
        <p>Dear {user_name or 'User'},</p>
        <p>SAP has successfully created a material for your request.</p>
        <p><strong>Details:</strong></p>
        <ul>
            <li><b>Request ID:</b> {requestor_doc.request_id}</li>
            <li><b>Material Code:</b> {matnr}</li>
            <li><b>Description:</b> {maktx}</li>
            <li><b>Message:</b> {zmsg}</li>
            <li><b>Details:</b> {ztext}</li>
        </ul>
        <p>Thank you,<br/></p>
        """

        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")

        if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
            frappe.log_error("SMTP settings missing in site_config", "SAP Email Error")
            return
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        if cc_email:
            msg['Cc'] = cc_email
        msg.attach(MIMEText(message, 'html'))

        recipients = [to_email] + ([cc_email] if cc_email else []) + [bcc_email]

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipients, msg.as_string())
        server.quit()

        print("Email sent successfully.")

        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_email,
            'from_email': from_email,
            'message': message,
            'status': "Successfully Sent",
            'screen': "Material Onboarding",
            'created_by': from_email
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "success", "message": _("Email sent successfully.")}

    except Exception as e:
        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_email,
            'from_email': from_email,
            'message': message,
            'status': f"Failed: {e}",
            'screen': "Material Onboarding",
            'created_by': from_email
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "fail", "message": _("Failed to send email.")}

@frappe.whitelist()
def create_requestor_details():
    print("=== START create_requestor_details ===")

    form_dict = frappe.form_dict.copy()
    print("Received form_dict keys:", list(form_dict.keys()))

    REQUESTOR_FIELDS = {
        "request_date": "request_date",
        "contact_information_email": "contact_information_email",
        "contact_information_phone": "contact_information_phone",
        "requested_by": "requested_by",
        "requestor_department": "requestor_department",
        "requestor_hod": "requestor_hod",
        "sub-department": "sub_department",
        "immediate_reporting_head": "immediate_reporting_head",
        "requestor_company": "requestor_company",
        "requested_by_place": "requested_by_place"
    }

    def map_data(form, mapping):
        return {doc_field: form[form_key] for doc_field, form_key in mapping.items() if form_key in form}

    try:
        req_data = map_data(form_dict, REQUESTOR_FIELDS)
        requestor_doc = frappe.new_doc("Requestor Master")
        requestor_doc.update(req_data)
        requestor_doc.approval_status = "Pending by CP"

        material_json = form_dict.get("material_request")
        print("material_request raw value:", material_json)

        if material_json:
            try:
                material_list = json.loads(material_json)
                print("Parsed material_request JSON:", material_list)
                for entry in material_list:
                    requestor_doc.append("material_request", {
                        "material_name_description": entry.get("material_name_description"),
                        # "material_code_revised": entry.get("material_code_revised"),
                        "company_name": entry.get("material_company_code"),
                        "plant_name": entry.get("plant_name"),
                        "material_category":entry.get("material_category"),
                        "material_group": entry.get("material_group"),
                        "material_type": entry.get("material_type"),
                        "base_unit_of_measure": entry.get("base_unit_of_measure"),
                        "comment_by_user": entry.get("comment_by_user", ""),
                        "material_specifications": entry.get("material_specifications",""),
                        "is_revised_code_new": entry.get("is_revised_code_new","")
                    })
            except Exception as parse_err:
                frappe.log_error(frappe.get_traceback(), "Material JSON Parsing Failed")
                return {"status": "error", "message": "Invalid material_request JSON"}

        requestor_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        send_email_on_requestor_creation(requestor_doc.name)

        print("=== END create_requestor_details ===")
        return {"status": "success", "message": "Requestor Master created", "name": requestor_doc.name}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Requestor Master Creation Failed")
        return {"status": "error", "message": "Something went wrong while saving"}


@frappe.whitelist()
def send_email_on_requestor_creation(requestor_name):
    # Email to Reporting Head keeping Store and CP in CC
    print("=== START send_email_on_requestor_creation ===", requestor_name)
    try:
        requestor_doc = frappe.get_doc("Requestor Master", requestor_name)
    except Exception as e:
        print("Error fetching Requestor Master:", str(e))
        return {"status": "fail", "message": "Could not fetch Requestor Master"}
    requestor_email = requestor_doc.contact_information_email
    requestor_person = requestor_doc.requested_by
    child_records = requestor_doc.get("material_request")
    if not requestor_email:
        print("No email found in requestor doc")
        frappe.throw("Requestor email not found.")
    requestor_emps_cp = frappe.get_all("Employee Master", filters={"role": "CP"}, fields=["email", "full_name"])
    requestor_emps_store = frappe.get_all("Employee Master", filters={"role": "Store"}, fields=["email", "full_name"])
    unique_emps = {}
    for emp in requestor_emps_cp + requestor_emps_store:
        if emp["email"]:
            unique_emps[emp["email"]] = emp["full_name"]
    table_rows = ""
    for row in child_records:
        table_rows += f"""
            <tr>
                <td style="border: 1px solid #ccc; padding: 8px;">{row.company_name}</td>
                <td style="border: 1px solid #ccc; padding: 8px;">{row.plant_name}</td>
                <td style="border: 1px solid #ccc; padding: 8px;">{row.material_category}</td>
                <td style="border: 1px solid #ccc; padding: 8px;">{row.material_type}</td>
                <td style="border: 1px solid #ccc; padding: 8px;">{row.material_code_revised}</td>
                <td style="border: 1px solid #ccc; padding: 8px;">{row.material_name_description}</td>
                <td style="border: 1px solid #ccc; padding: 8px;">{row.base_unit_of_measure}</td>
                <td style="border: 1px solid #ccc; padding: 8px;">{row.comment_by_user}</td>
            </tr>
        """
    table_html = f"""
        <table style="border-collapse: collapse; width: 100%; margin-top: 10px;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid #ccc; padding: 8px;">Company Name</th>
                    <th style="border: 1px solid #ccc; padding: 8px;">Plant Name</th>
                    <th style="border: 1px solid #ccc; padding: 8px;">Material Category</th>
                    <th style="border: 1px solid #ccc; padding: 8px;">Material Type</th>
                    <th style="border: 1px solid #ccc; padding: 8px;">Material Code (Revised)</th>
                    <th style="border: 1px solid #ccc; padding: 8px;">Material Description</th>
                    <th style="border: 1px solid #ccc; padding: 8px;">Base UOM</th>
                    <th style="border: 1px solid #ccc; padding: 8px;">Comment</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    """
    recipient_emails = list(unique_emps.keys())
    recipient_names = ", ".join(unique_emps.values())
    print("Final Recipient Emails:", recipient_emails)
    print("Final Recipient Names:", recipient_names)
    requestor_head = frappe.get_value("Employee Master", requestor_person, "reporting_head")
    requestor_head_email = frappe.get_value("Employee Master", requestor_head, "email")
    requestor_head_name = frappe.get_value("Employee Master", requestor_head, "full_name")
    bcc_address = 'rishi.hingad@merillife.com'
    subject = "Request to Generate New Material Code Submitted"
    body = f"""
    <p>Dear {requestor_head_name},</p>

    <p>
        A request to generate a new material code "<strong>{requestor_name}</strong>" has been successfully submitted by <strong>{requestor_person}</strong>.
    </p>

    <p>Preview the details:</p>
    {table_html}
    <p>Regards,<br>
    Meril VMS Team</p>
    """
    msg = MIMEMultipart()
    msg["From"] = requestor_email
    msg["To"] = requestor_head_email or ""
    msg["Subject"] = subject
    msg["Cc"] = ", ".join(recipient_emails)
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "html"))

    try:
        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        all_recipients = recipient_emails + [bcc_address]
        if requestor_head_email:
            all_recipients.append(requestor_head_email)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(requestor_email, all_recipients, msg.as_string())
            print("Email sent successfully!")

        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': ", ".join(recipient_emails),
            'from_email': requestor_email,
            'message': body,
            'status': "Successfully Sent",
            'screen': "Requestor Master",
            'created_by': requestor_email
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "success", "message": _("Email sent successfully.")}

    except Exception as e:
        print("EMAIL SEND ERROR:", str(e))

        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': ", ".join(recipient_emails),
            'from_email': requestor_email,
            'message': body,
            'status': f"Failed: {e}",
            'screen': "Requestor Master",
            'created_by': requestor_email
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        print("Email failure log saved.")
        return {"status": "fail", "message": _("Failed to send email.")}


@frappe.whitelist()
def create_material_onboarding():
    print("=== START create_material_onboarding ===")

    files = frappe.request.files
    form_dict = dict(frappe.form_dict)
    print("Form data:", form_dict.keys())

    if "material_information" in files:
        file = files["material_information"]
        if file and getattr(file, "filename", None) and file.filename != "undefined":
            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": file.filename,
                "content": file.read(),
                "is_private": 1
            }).save()
            form_dict["material_information"] = file_doc.file_url
            print("Uploaded:", file_doc.file_url)

    def map_fields(mapping):
        return {
            doc_field: form_dict.get(form_key)
            for doc_field, form_key in mapping.items()
            if form_dict.get(form_key) is not None
        }

    MATERIAL_FIELDS = {
        "storage_location": "storage_location",
        "division": "division",
        "old_material_code": "old_material_code",
        "material_group": "material_group",
        "batch_requirements_yn": "batch_requirements_yn",
        "brand_make": "brand_make",
        "availability_check": "availability_check",
        "class_type": "class_type",
        "class_number": "class_number",
        "serial_number_profile": "serial_number_profile",
        "serialization_level": "serialization_level",
        "purchase_uom": "purchase_uom",
        "numerator_purchase_uom": "numerator_purchase_uom",
        "denominator_purchase_uom": "denominator_purchase_uom",
        "lead_time": "lead_time",
        "mrp_type": "mrp_type",
        "mrp_group": "mrp_group",
        "mrp_controller_revised": "mrp_controller_revised",
        "lot_size_key": "lot_size_key",
        "procurement_type": "procurement_type",
        "scheduling_margin_key": "scheduling_margin_key",
        "issue_unit": "issue_unit",
        "numerator_issue_uom": "numerator_issue_uom",
        "denominator_issue_uom": "denominator_issue_uom",
        "material_code_revised": "material_code_revised",
        "material_code": "material_code",
        "industry": "industry",
        "purchase_order_text": "purchase_order_text",
        "purchasing_group": "purchasing_group",
        "gr_processing_time": "gr_processing_time",
        "purchasing_value_key": "purchasing_value_key",
        "min_lot_size": "min_lot_size",
        
    }

    ONBOARDING_FIELDS = {
        "material_information": "material_information",
        "minimum_remaining_shell_life": "minimum_remaining_shell_life",
        "total_shell_life": "total_shell_life",
        "expiration_date": "expiration_date",
        "inspection_interval": "inspection_interval",
        "incoming_inspection_01": "incoming_inspection_01",
        "incoming_inspection_09": "incoming_inspection_09",
        "material_specifications": "material_specifications",
        "valuation_class": "valuation_class",
        "profit_center": "profit_center",
        "price_control": "price_control",
        "hsn_code": "hsn_code",
        "do_not_cost": "do_not_cost",
        "comment_by_store": "comment_by_store",
        "intended_usage_application": "intended_usage_application",
        "storage_requirements": "storage_requirements",
        "hazardous_material": "hazardous_material",
        "inspection_require": "inspection_require",
        "approval_date": "approval_date",
        "approval_status": "approval_status",
        "requested_by_name": "requested_by_name",
        "requested_by_place": "requested_by_place",
        "approved_by_name": "approved_by_name",
        "approved_by_place": "approved_by_place",
        "hsn_status": "hsn_status",
        "special_instructionsnotes": "special_instructionsnotes",
        "lot_size": "lot_size",
        "lead_time": "lead_time",
        "purchase_order_text": "purchase_order_text"
    }

    mat_data = map_fields(MATERIAL_FIELDS)
    onb_data = map_fields(ONBOARDING_FIELDS)
    for checkbox_field in ["incoming_inspection_01", "incoming_inspection_09"]:
        onb_data[checkbox_field] = 1 if form_dict.get(checkbox_field) in ["on", "1", 1, True, "true", "True"] else 0

    req_name = form_dict.get("requestor_ref_no") or form_dict.get("requestor_name")
    requestor = frappe.get_doc("Requestor Master", req_name)
    print("Approval value",requestor.approval_status)

    mat_data.update({
        "requestor_ref_no": req_name,
        "basic_data_ref_no": req_name
    })
    onb_data.update({
        "requestor_ref_no": req_name
    })
    try:
        if (form_dict.get("approval_status") or "").strip().lower() == "updated by cp":
            print("Form approval_status is 'Updated by CP'. Updating existing Material Master and Onboarding.")
            material = frappe.get_doc("Material Master", requestor.material_master_ref_no)
            material.update(mat_data)
            material.save()
            print("Updated existing Material Master:", material.name)

            onboarding = frappe.get_doc("Material Onboarding", requestor.material_onboarding_ref_no)
            onb_data.update({
                "material_master_ref_no": material.name,
                "material_code_latest": form_dict.get("material_code")
            })
            onboarding.update(onb_data)
            onboarding.save()
            print("Updated existing Material Onboarding:", onboarding.name)

            requestor.approval_status = "Updated by CP"
            requestor.material_master_ref_no = material.name
            requestor.material_onboarding_ref_no = onboarding.name
            requestor.save()
            print("Updated Requestor Master approval_status to 'Updated by CP'.")
        else:
            if not requestor.material_master_ref_no and not requestor.material_onboarding_ref_no:
                print("Material Master and Onboarding do not exist for requestor. Creating new ones...")

                material = frappe.new_doc("Material Master")
                material.update(mat_data)
                material.insert()
                print("Material Master created:", material.name)

                onb_data.update({
                    "material_master_ref_no": material.name,
                    "material_code_latest": form_dict.get("material_code"),
                })

                onboarding = frappe.new_doc("Material Onboarding")
                onboarding.update(onb_data)
                onboarding.insert()
                print("Material Onboarding created:", onboarding.name)

                material.material_onboarding_ref_no = onboarding.name
                material.save()
                print("Updated Material Master with onboarding ref:", onboarding.name)

                requestor.material_master_ref_no = material.name
                requestor.material_onboarding_ref_no = onboarding.name
                requestor.approval_status = "Sent to SAP"
                requestor.save()
                print("Updated Requestor Master with references and approval status.")
            else:
                print("Material Master or Onboarding already exists. Skipping creation.")
                onboarding = None 

    except Exception as e:
        frappe.log_error(f"Failed to update Requestor Master '{req_name}'", str(e))

    if onboarding:
        send_email_on_material_onboarding(onboarding.name)
        print("Email sent on material onboarding.")
        return {"status": "created", "name": onboarding.name}
    else:
        return {"status": "skipped", "message": "Material Master or Onboarding already existed"}


@frappe.whitelist(allow_guest=True)
def send_email_on_material_onboarding(onboarding_doc):
    print("***************send_email_on_material_onboarding***************", onboarding_doc)

    try:
        onboarding_doc = frappe.get_doc("Material Onboarding", onboarding_doc)
    except Exception as e:
        frappe.throw(f"Failed to fetch Material Onboarding doc: {str(e)}")

    print("***************requestor_ref_no***************", onboarding_doc.requestor_ref_no)

    if onboarding_doc.requestor_ref_no:
        requestor_email = frappe.db.get_value(
            "Requestor Master",
            {"name": onboarding_doc.requestor_ref_no},
            "contact_information_email"
        )
    else:
        frappe.throw("Requestor Reference Number is missing from Material Onboarding.")

    if not requestor_email:
        frappe.throw("Requestor email not found in Requestor Master.")

    cp_emails = frappe.get_all("Employee Master", filters={"role": "CP"}, fields=["email"])
    cp_addresses = ", ".join([emp["email"] for emp in cp_emails if emp["email"]])

    reciever_name = frappe.db.get_value("Employee Master", {'email': requestor_email}, 'full_name')
    reporting_manager = frappe.db.get_value("Employee Master", {'email': requestor_email}, 'reporting_head')
    reporting_manager_email = frappe.db.get_value("Employee Master", {'name': reporting_manager}, 'email')
    reporting_manager_name = frappe.db.get_value("Employee Master", {'name': reporting_manager}, 'full_name')

    if not reciever_name:
        return {
            "status": "fail",
            "message": f"Employee with email {requestor_email} does not exist in Employee Master."
        }

    latest_material_docname = frappe.db.get_value(
        "Material Onboarding",
        {'requestor_ref_no': onboarding_doc.requestor_ref_no},
        'name',
        order_by="creation desc"
    )

    from_address = requestor_email
    to_address = cp_addresses
    cc_address = reporting_manager_email
    bcc_address = 'rishi.hingad@merillife.com'
    subject = "New Material Onboarding Request Submitted"
    body = f"""
    Dear {reporting_manager_name},

    A new material onboarding request "{latest_material_docname}" has been submitted by {reciever_name} ({requestor_email}).
    Please review the request at your earliest convenience.

    Regards,  
    Meril VMS Team
    """

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Cc"] = cc_address
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "plain"))

    try:
        conf = frappe.conf
        with smtplib.SMTP(conf.get("smtp_server"), conf.get("smtp_port")) as server:
            server.starttls()
            server.login(conf.get("smtp_user"), conf.get("smtp_password"))
            server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
            print("Email sent successfully!")

        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': "Successfully Sent",
            'screen': "Material Onboarding",
            'created_by': from_address
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "success", "message": _("Email sent successfully.")}

    except Exception as e:
        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': f"Failed: {e}",
            'screen': "Material Onboarding",
            'created_by': from_address
        }).insert(ignore_permissions=True)

        frappe.db.commit()
        return {"status": "fail", "message": _("Failed to send email.")}

# @frappe.whitelist()
# def update_material_onboarding():
#     print("=== START update_material_onboarding ===")
#     files     = frappe.request.files
#     form_dict = dict(frappe.form_dict)

#     form_dict["name"] = form_dict.get("name") or form_dict.get("material_onboarding_ref_no")
#     if not form_dict["name"]:
#         frappe.throw("Parameter 'name' (Material Onboarding docname) is required.")

#     onboarding_doc = frappe.get_doc("Material Onboarding", form_dict["name"])
#     material_doc   = frappe.get_doc("Material Master",  onboarding_doc.material_master_ref_no)
#     requestor_doc  = frappe.get_doc("Requestor Master", onboarding_doc.requestor_ref_no)

#     if "material_information" in files:
#         f = files["material_information"]
#         if f and getattr(f, "filename", None) and f.filename != "undefined":
#             file_doc = frappe.get_doc({
#                 "doctype": "File",
#                 "file_name": f.filename,
#                 "content":   f.read(),
#                 "is_private": 1,
#             }).insert()
#             form_dict["material_information"] = file_doc.file_url

#     def map_data(src, mapping):
#         return {dfield: src[fkey] for dfield, fkey in mapping.items() if fkey in src}

#     REQUESTOR_FIELDS = {
#         "request_date": "request_date",
#         "contact_information_email": "contact_information_email",
#         "contact_information_phone": "contact_information_phone",
#         "requested_by": "requested_by",
#         "requestor_department": "requestor_department",
#         "requestor_hod": "requestor_hod",
#         "sub-department": "sub_department",
#         "immediate_reporting_head": "immediate_reporting_head",
#         "requestor_company": "requestor_company",
#     }

#     MATERIAL_FIELDS = {
#         "material_information": "material_information",
#         "plant_code": "plant_code",
#         "price_control": "price_control",
#         "material_company_code": "material_company_code",
#         "division": "division",
#         "material_type": "material_type",
#         "material_group": "material_group",
#         "material_sub_group": "material_sub_group",
#         "material_name_description": "material_name_description",
#         "brand_make": "brand_make",
#         "batch_requirements_yn": "batch_requirements_yn",
#         "base_unit_of_measure": "base_unit_of_measure",
#         "industry": "industry",
#         "profit_center": "profit_center",
#         "mrp_type": "mrp_type",
#         "availability_check": "availability_check",
#         "mrp_group": "mrp_group",
#         "mrp_controller_revised": "mrp_controller_revised",
#         "storage_location": "storage_location",
#         "production_storage_location": "production_storage_location",
#         "valuation_category": "valuation_category",
#         "storage_location_for_ep": "storage_location_for_ep",
#         "class_number": "class_number",
#         "class_type": "class_type",
#         "gr_processing_time": "gr_processing_time",
#         "purchasing_group": "purchasing_group",
#         "valuation_class": "valuation_class",
#         "minimum_remaining_shelf_life": "minimum_remaining_shelf_life",
#         "expiration_date": "expiration_date",
#         "serial_number_profile": "serial_number_profile",
#         "purchase_uom": "purchase_uom",
#         "do_not_cost": "do_not_cost",
#         "inspection_type": "inspection_type",
#         "issue_unit": "issue_unit",
#         "total_shelf_life": "total_shelf_life",
#         "scheduling_margin_key": "scheduling_margin_key",
#         "serialization_level": "serialization_level",
#         "material_code_revised":"material_code_revised",
#         "valuation_class_material":"valuation_class_material",
#         "material_code":"material_code"
#     }

#     ONBOARDING_FIELDS = {
#         "material_specifications": "material_specifications",
#         "purchase_order_text": "purchase_order_text",
#         "intended_usage_application": "intended_usage_application",
#         "hazardous_material": "hazardous_material",
#         "storage_requirements": "storage_requirements",
#         "procurement_type": "procurement_type",
#         "valuation_class": "valuation_class",
#         "lot_size": "lot_size",
#         "lead_time": "lead_time",
#         "hsn_code": "hsn_code",
#         "hsn_status": "hsn_status",
#         "special_instructionsnotes": "special_instructionsnotes",
#         "requested_by_name": "requested_by_name",
#         "approved_by_name": "approved_by_name",
#         "requested_by_place": "requested_by_place",
#         "approved_by_place": "approved_by_place",
#         "approval_date": "approval_date",
#         "approval_status": "approval_status",
#     }

#     requestor_doc.update(map_data(form_dict, REQUESTOR_FIELDS))
#     material_doc.update( map_data(form_dict, MATERIAL_FIELDS))
#     onboarding_doc.update(map_data(form_dict, ONBOARDING_FIELDS))

#     requestor_doc.save()
#     material_doc.save()
#     onboarding_doc.save()

#     send_email_on_material_approval(onboarding_doc.name)

#     print("=== END update_material_onboarding ===")
#     return {"status": "updated", "name": onboarding_doc.name}

@frappe.whitelist()
def send_email_on_material_approval(onboarding_doc, method=None):
    print("***************send_email_on_material_approval***************", onboarding_doc)
    onboarding_doc = frappe.get_doc("Material Onboarding", onboarding_doc)
    docname = onboarding_doc.name

    requestor_email = frappe.db.get_value("Requestor Master", {"name": onboarding_doc.requestor_ref_no}, "contact_information_email")
    if not requestor_email:
        frappe.throw("Requestor email not found in Requestor Master")

    requestor_name = frappe.db.get_value("Employee Master", {'email': requestor_email}, 'full_name')

    reciever_email = frappe.session.user
    reciever_name = frappe.db.get_value("Employee Master", {'email': reciever_email}, 'full_name')
    reciever_role = frappe.db.get_value("Employee Master", {'email': reciever_email}, 'role')

    reporting_manager = frappe.db.get_value("Employee Master", {'email': requestor_email}, 'reporting_head')
    reporting_manager_email = frappe.db.get_value("Employee Master", {'name': reporting_manager}, 'email')
    reporting_manager_name = frappe.db.get_value("Employee Master", {'name': reporting_manager}, 'full_name')

    if not reciever_name:
        return {"status": "fail", "message": f"Employee with email {reciever_email} does not exist in Employee Master."}

    from_address = reciever_email
    bcc_address = 'rishi.hingad@merillife.com'

    cp_emails = frappe.get_all("Employee Master", filters={"role": "CP"}, fields=["email"])
    cp_addresses = [emp["email"] for emp in cp_emails if emp["email"]]

    if reciever_role == "CP":
        to_address = requestor_email
        cc_address = ", ".join(filter(None, [reporting_manager_email]))
        subject = "New Material Onboarding Request Approved"
        body = f"""
        Dear {requestor_name},

        Your material onboarding request (Document: {docname}) has been approved by {reciever_name} ({reciever_email}).
        
        Regards,  
        Meril VMS Team
        """

    elif reciever_role == "Purchase":
        material_data = frappe.db.get_value("Material Onboarding", {"name": docname},
                                            ["hsn_code", "lot_size", "procurement_type"], as_dict=True)

        hsn_code = material_data.hsn_code if material_data else "N/A"
        lot_size = material_data.lot_size if material_data else "N/A"
        procurement_type = material_data.procurement_type if material_data else "N/A"

        gst_emails = frappe.get_all("Employee Master", filters={"role": "GST"}, fields=["email"])
        to_address = ", ".join([emp["email"] for emp in gst_emails if emp["email"]])
        cc_list = list(filter(None, [requestor_email, reporting_manager_email] + cp_addresses))
        cc_address = ", ".join(cc_list)
        subject = f"""Verify the HSN Code for New Material - {docname}"""
        body = f"""
        Dear GST Team,

        A new material code has been generated. The Material onboarding request has been approved by {reciever_name} ({reciever_email}).
        
        Below are the details:
        Document Name: {docname}
        HSN Code: {hsn_code}
        Lot Size: {lot_size}
        Procurement Type: {procurement_type}

        Kindly verify the HSN Code and proceed with next steps.

        Regards,  
        Meril VMS Team
        """
    elif reciever_role == "GST":
        material_data = frappe.db.get_value("Material Onboarding", {"name": docname},
                                            ["hsn_code", "lot_size", "procurement_type"], as_dict=True)

        hsn_code = material_data.hsn_code if material_data else "N/A"
        lot_size = material_data.lot_size if material_data else "N/A"
        procurement_type = material_data.procurement_type if material_data else "N/A"
        to_address = ", ".join(cp_addresses)

        purchase_emails = frappe.get_all("Employee Master", filters={"role": "Purchase"}, fields=["email"])
        cc_list = [emp["email"] for emp in purchase_emails if emp["email"]]
        cc_address = ", ".join(cc_list)

        subject = f"""HSN Code Verified by GST Team - {docname}"""
        body = f"""
        Dear CP Team,

        The HSN Code for the Material Onboarding request (Document: {docname}) has been verified by the GST team ({reciever_name} - {reciever_email}).

        Below are the details:
        HSN Code: {hsn_code}
        Lot Size: {lot_size}
        Procurement Type: {procurement_type}
        
        Please proceed with the next steps in the onboarding workflow.

        Regards,  
        Meril VMS Team
        """

    elif reciever_role == "SAP":
        material_data = frappe.db.get_value("Material Master", {"material_onboarding_ref_no": docname},
                                            ["material_code", "material_code_revised"], as_dict=True)

        material_code = material_data.material_code if material_data else "N/A"
        material_code_revised = material_data.material_code_revised if material_data else "N/A"

        purchase_emails = frappe.get_all("Employee Master", filters={"role": "Purchase Team"}, fields=["email"])
        to_address = ", ".join([emp["email"] for emp in purchase_emails if emp["email"]])
        cc_list = list(filter(None, [requestor_email, reporting_manager_email] + cp_addresses))
        cc_address = ", ".join(cc_list)
        subject = f"""Material Code Generated for New Material- {docname}"""
        body = f"""
        Dear Purchase Team,

        A material onboarding request has been processed by {reciever_name} ({reciever_email}).

        Document Name: {docname}
        Revised Material Code: {material_code_revised}
        Final Material Code: {material_code}

        Please add the HSN Code, Lead Time, Lot Size, Capacity etc. for the following Material Request.

        Regards,  
        Meril VMS Team
        """

    else:
        return {"status": "fail", "message": "Role not authorized for this action."}

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Cc"] = cc_address
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "plain"))

    try:
        conf = frappe.conf
        with smtplib.SMTP(conf.get("smtp_server"), conf.get("smtp_port")) as server:
            server.starttls()
            server.login(conf.get("smtp_user"), conf.get("smtp_password"))
            server.sendmail(from_address, to_address.split(",") + cc_address.split(",") + [bcc_address], msg.as_string())
            print("Email sent successfully!")

        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': "Successfully Sent",
            'screen': "Material Onboarding",
            'created_by': from_address
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "success", "message": _("Email sent successfully.")}

    except Exception as e:
        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': f"Failed: {e}",
            'screen': "Material Onboarding",
            'created_by': from_address
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "fail", "message": _("Failed to send email.")}


@frappe.whitelist()
def create_notification(user, message, reference_doctype, reference_name, subject="New Notification"):
    """
    Create a notification entry and send it to the specified user.
    
    :param user: The recipient user ID (user email or username).
    :param message: The notification message.
    :param reference_doctype: The doctype related to the notification.
    :param reference_name: The document name related to the notification.
    :param subject: The subject of the notification (default is 'New Notification').
    """
    try:
        notification_doc = frappe.get_doc({
            "doctype": "Notification Log",
            "for_user": user,
            "type": "Alert",
            "subject": subject,
            "email_content": message,
            "document_type": reference_doctype,
            "document_name": reference_name,
            "from_user": frappe.session.user,
            "read": 0,
        })

        notification_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        frappe.publish_realtime(event='realtime_notification', message={
            "type": "Alert",
            "message": message,
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "from_user": frappe.session.user
        }, user=user)

    except Exception as e:
        frappe.log_error(message=str(e), title="Notification Creation Failed")
        frappe.throw(_("Could not create notification due to an internal error. Please try again later."))

@frappe.whitelist()
def send_password_change_email(email):
    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password") 
    from_address = 'noreply@merillife.com'
    bcc_address = 'rishi.hingad@merillife.com'
    to_address = email
    subject = "Password Changed Successfully"
    body = """
        <html>
        <body>
            <p>Your password for the VMS Portal has been changed successfully.</p>
            <p>If you did not request this change, please contact support immediately.</p>
            <br/>
            <p>Regards,<br/>
            VMS Team</p>
        </body>
        </html>
    """

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(smtp_user, smtp_password)  
            server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
            print("Email sent successfully!")
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': "Successfully Sent",
                'screen': "Password Change Notification",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

    except Exception as e:
        print(f"Failed to send email: {e}")
        doc = frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': f"Failed to send email: {e}",
            'screen': "Password Change Notification",
            'created_by': from_address
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()


@frappe.whitelist(allow_guest=False)
def change_user_password(email, new_password):
    try:
        user = frappe.get_doc("User", email)
        if not user:
            return {"status": "fail", "message": _("User not found.")}

        user.new_password = new_password
        user.save(ignore_permissions=True)

        send_password_change_email(email)

        return {"status": "success", "message": _("Password changed successfully.")}
    
    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Password Change Failed")
        return {"status": "fail", "message": _("Something went wrong. Please try again later.")}


@frappe.whitelist()
def verify_current_password(email, current_password):
    from frappe.auth import LoginManager
    try:
        frappe.logger().info(f"Trying to authenticate: {email}")
        login_manager = LoginManager()
        login_manager.authenticate(user=email.strip(), pwd=current_password.strip())
        return {"success": True, "message": "Password verified"}
    except frappe.AuthenticationError:
        return {"success": False, "message": "Incorrect password"}
    except Exception as e:
        frappe.logger().error(f"Unexpected error: {e}")
        frappe.log_error(frappe.get_traceback(), "Password Verification Error")
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}"
        }

#======================================================================================================
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@frappe.whitelist(allow_guest=True)
def upload_file(docname, doctype, attachmentFieldName):
    file = frappe.request.files['file']
    # is_private = frappe.form_dict.is_private or 0
    is_private = 1
    saved_file = save_file(file.filename, file.stream.read(), doctype, docname, is_private=int(is_private))
    doc = frappe.get_doc(doctype, docname)
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
    elif(attachmentFieldName == 'msme_proof'): 
        doc.iec_proof =saved_file.file_url
    elif(attachmentFieldName == 'bank_proof_for_beneficiary_bank'): 
        doc.iec_proof =saved_file.file_url
    elif(attachmentFieldName == 'bank_proof_for_intermediate_bank'): 
        doc.iec_proof =saved_file.file_url
    elif(attachmentFieldName == 'pe_certificate'): 
        doc.iec_proof =saved_file.file_url
    elif(attachmentFieldName == 'form_10f_proof'): 
        doc.iec_proof =saved_file.file_url
    elif(attachmentFieldName == 'trc_certificate'): 
        doc.iec_proof =saved_file.file_url
    elif(attachmentFieldName == 'organisation_structure_document'): 
        doc.organisation_structure_document =saved_file.file_url
    elif(attachmentFieldName == 'certificate_attach'): 
        doc.certificate_attach =saved_file.file_url
    elif(attachmentFieldName == 'material_images'): 
        doc.material_images =saved_file.file_url
    elif(attachmentFieldName == 'tissue_supplier'):
        doc.tissue_supplier = saved_file.file_url
    elif(attachmentFieldName == 'technical_agreement_labs'):
        doc.technical_agreement_labs = saved_file.file_url
    elif(attachmentFieldName == 'new_supplier'):
        doc.new_supplier = saved_file.file_url
    elif(attachmentFieldName == 'amendment_existing_supplier'):
        doc.amendment_existing_supplier = saved_file.file_url
    elif(attachmentFieldName == 'qa_attachment'):
        doc.qa_attachment = saved_file.file_url
    else:
        logger.info("No matching field for attachmentFieldName: %s", attachmentFieldName)

    doc.save()

    return {
        'file_url': saved_file.file_url,
        'file_name': saved_file.name
    }

@frappe.whitelist()
def get_team_master_details(name):
    if not name:
        frappe.throw("Team Master name is required")

    team_master = frappe.get_doc("Team Master", name)
    purchase_group_details = []
    for row in team_master.get("purchase_group_multiselect", []):
        purchase_group_doc = frappe.get_doc("Purchase Group Master", row.pur_grp_name)
        purchase_group_details.append({
            "purchase_group": row.pur_grp_name,
            "purchase_group_name": purchase_group_doc.purchase_group_name,
            "description": purchase_group_doc.description
        })

    team_master_details = team_master.as_dict()
    # team_master_details["purchase_group_details"] = purchase_group_details

    return team_master_details


@frappe.whitelist()
def send_email_on_vendor_register(data, method):
    name = data.get("name")
    # print("&^$$#$%^&*(*&^%$^&*()*&^%$#^&*())", name)
    # load_dotenv(dotenv_path='/home/rishi_hingad/frappe-bench/.env')
    # onboarding_link = os.getenv('ONBOARDING_LINK')

    print("**** Send Email on vendor register *****", name)
    frappe.db.sql(""" update `tabVendor Master` set purchase_team_approval='In Process' where name=%s """, (name))
    frappe.db.commit()
    frappe.db.sql(""" update `tabVendor Master` set purchase_head_approval='In Process' where name=%s """, (name) )
    frappe.db.commit()
    frappe.db.sql(""" update `tabVendor Master` set accounts_team_approval='In Process' where name=%s """, (name) )
    frappe.db.commit()
    frappe.db.sql(""" update `tabVendor Master` set status='In Process' where name=%s """, (name) )
    frappe.db.commit()
    frappe.db.sql(""" update `tabVendor Master` set onboarding_form_status='In Process' where name=%s """, (name) )
    frappe.db.commit()
    # print(frappe.session.user)
    current_user = frappe.session.user
    print("***********()()(T&^%@#$%^&*(**CURRENT USER*****", current_user)
    current_user_email = frappe.db.get_value("User", filters={'full_name': current_user}, fieldname=['email'])
    current_user_team = frappe.db.get_value("User", filters={'email': current_user}, fieldname=['team'])
    cc_address_email = frappe.db.get_value("Team Master", filters={'name': current_user_team}, fieldname=['reporting_head'])
    # current_user_company = frappe.get_all("Users Company",{"parent":current_user_email},"name")
    current_user_designation = frappe.db.get_value("User", filters={'email': current_user}, fieldname=['designation'])
    # Fetch BCC email based on company and designation
    # bcc_email = frappe.db.get_value("User", filters={["Users Company",'company',current_user_company], current_user_designation}, fieldname='email')    
    print(current_user_designation)
    frappe.db.sql(""" UPDATE `tabVendor Master` SET registered_by=%s WHERE name=%s """,(current_user, name))
    frappe.db.commit()
    vendor_name = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['vendor_name'])
    company_code = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['company_name'])
    company_name = frappe.db.get_value("Company Master", filters={'company_code': company_code}, fieldname=['company_name'])
    purchase_team_name = frappe.db.get_value("User", filters={'email': current_user}, fieldname=['full_name'])
    reciever_email = data.get("office_email_primary")
    print("****************EMAIL******************", current_user, reciever_email)
    # print("*******************ONBOARDING LINK*********************", onboarding_link)
    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    server_url = conf.get("server_url")

    from_address = current_user
    to_address = reciever_email  
    bcc_address = "rishi.hingad@merillife.com"
    cc_address = cc_address_email
    print(f"From: {from_address}")
    print(f"To: {to_address}")
    print(f"Bcc: {bcc_address}")
    print(f"Cc: {cc_address}")
    # bcc_address = [bcc_email, "rishi.hingad@merillife.com"]
    subject = f"""New Vendor Appointment for {company_name} - {vendor_name} - VMS Ref #: {name}"""
    body = f"""
        Dear Sir/Madam,
        {vendor_name}

        Greetings of the Day!

        You have been added by {purchase_team_name} to onboard as a Vendor/Supplier for {company_name}.

        Founded in 2006, Meril Life Sciences Private Limited is an India-based, global medical device company. We design, manufacture, and distribute clinically relevant, state-of-the-art, and best-in-class devices to alleviate human suffering. At Meril Life Sciences, we champion the need to accelerate positive change in medtech solutions with a wide range of efficient and accessible medical devices, perfected to ensure every product is patient-centric. We are committed to advancing healthcare solutions, so more patients may live longer and healthier lives. We share a strong commitment to R&D in providing med-tech solutions and adhere to the best quality standards in manufacturing, clinical and scientific research, and education of our stakeholders.

        We are a family of 3000+ Vendors/Sub-Vendors across India.

        Please find the link below to fill in your details:

        {server_url}/onboarding?Refno={name}

        Thank you,
        Meril Team
        """
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Bcc"] = bcc_address
    msg["CC"] = cc_address
    msg.attach(MIMEText(body, "html"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(smtp_user, smtp_password)  
            server.sendmail(from_address, [to_address, bcc_address, cc_address], msg.as_string()) 
            print("Email sent successfully!")
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': name,
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': "Successfully Sent",
                'screen': "Onboarding Link sent successfully.",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

    except Exception as e:
        print(f"Failed to send email: {e}")
        doc = frappe.get_doc({
            'doctype': 'Email Log',
            'ref_no': name,
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': f"Failed to send email: {e}",
            'screen': "Onboarding Link send failed",
            'created_by': from_address
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

@frappe.whitelist()
def get_all_material_descriptions_and_codes():
    results = []

    material_master_entries = frappe.get_all(
        "Material Master",
        fields=["material_name_description", "material_code_revised","name"]
    )
    for entry in material_master_entries:
        results.append({
            "source": "Material Master",
            "name": entry.name,
            "material_name_description": entry.material_name_description,
            "material_code_revised": entry.material_code_revised
        })

    requestor_names = frappe.get_all("Requestor Master", fields=["name"])
    for item in requestor_names:
        doc = frappe.get_doc("Requestor Master", item.name)
        for child in doc.material_request:
            results.append({
                "source": "Requestor Master",
                "name": doc.name,
                "material_name_description": child.material_name_description,
                "material_code_revised": child.material_code_revised
            })

    return results

@frappe.whitelist(allow_guest=True)
def get_all_material_codes():
    try:
        materials = frappe.get_all(
            "Material Code Master",
            fields=["name", "material_description", "material_type", "material_group", "plant", "company_code"]
        )
        frappe.response["type"] = "json"
        frappe.response["data"] = materials
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Material Code Fetch Error")
        frappe.response["http_status_code"] = 500
        frappe.response["data"] = {"error": str(e)}


@frappe.whitelist()
def show_requestor_master_list():
    requestor_master_list = []

    requestor_names = frappe.get_all(
        "Requestor Master",
        fields=["name"],
        order_by="request_date DESC, creation DESC"
    )

    for item in requestor_names:
        doc = frappe.get_doc("Requestor Master", item.name)
        doc_dict = doc.as_dict()

        if "material_request" in doc_dict:
            del doc_dict["material_request"]

        material_request_items = []
        for child in doc.material_request:
            company_name = frappe.db.get_value("Company Master", child.company_name, "company_name") if child.company_name else ""

            material_request_items.append({
                "child_name": child.name,
                "company_code": child.company_name,
                "company_name": company_name,
                "plant_name": child.plant_name,
                "material_description": child.material_name_description,
                "material_type": child.material_type,
                "comment_by_user": child.comment_by_user,
            })

        doc_dict["material_request_items"] = material_request_items

        requestor_master_list.append(doc_dict)

    return requestor_master_list

@frappe.whitelist()
def show_material_onboarding_list():
    material_onboarding_list = []

    requestors = frappe.get_all(
        "Requestor Master",
        fields=["name"],
        order_by="request_date DESC, creation DESC"
    )

    for requestor in requestors:
        requestor_doc = frappe.get_doc("Requestor Master", requestor.name)

        for material in requestor_doc.material_request:
            entry = {
                "requestor_ref_no": requestor_doc.name,
                "child_table_row_id": material.name,
                "material_name_description": material.material_name_description,
                "material_company_code": material.company_name,
                "material_company_name": frappe.db.get_value("Company Master", material.company_name, "company_name") if material.company_name else None,
                "plant_name": material.plant_name,
                "material_type": material.material_type,
                "base_unit_of_measure": material.base_unit_of_measure,
                "comment_by_user": material.comment_by_user,
                "requested_by": requestor_doc.requested_by,
                "request_date": requestor_doc.request_date,
                "requestor_company": requestor_doc.company,
                "contact_information_email": requestor_doc.contact_information_email, 
                "approval_status": requestor_doc.approval_status,  
            }

            material_onboarding_list.append(entry)

    return material_onboarding_list


@frappe.whitelist()
def get_material_onboarding_details(name, material_name):
    if not name:
        frappe.throw("Requestor Master document name is required")

    try:
        requestor_doc = frappe.get_doc("Requestor Master", name)
    except frappe.DoesNotExistError:
        frappe.throw(f"Requestor Master with name '{name}' not found")

    requestor_dict = requestor_doc.as_dict()

    if requestor_doc.requestor_company:
        requestor_dict["requestor_company_name"] = frappe.db.get_value(
            "Company Master", requestor_doc.requestor_company, "company_name"
        )

    selected_row = next(
        (row for row in requestor_doc.material_request if row.name == material_name),
        None
    )
    # Fetch Material Master (with children)
    material_master_data = {}
    mm_ref = requestor_doc.get("material_master_ref_no")
    if mm_ref:
        try:
            # material_master_data = frappe.get_doc("Material Master", mm_ref).as_dict()
            material_doc = frappe.get_doc("Material Master", mm_ref)
            material_master_data = material_doc.as_dict()
            material_master_data["children"] = [d.as_dict() for d in material_doc.get_all_children()]

        except Exception as e:
            frappe.log_error(f"Failed to get Material Master '{mm_ref}'", str(e))

    # Fetch Material Onboarding (with children)
    material_onboarding_data = {}
    mo_ref = requestor_doc.get("material_onboarding_ref_no")
    if mo_ref:
        try:
            # mo_doc = frappe.get_doc("Material Onboarding", mo_ref)
            mo_doc = frappe.get_doc("Material Onboarding", mo_ref)
            material_onboarding_data = mo_doc.as_dict()
            material_onboarding_data["children"] = [d.as_dict() for d in mo_doc.get_all_children()]
            material_onboarding_data = mo_doc.as_dict()
            if mo_doc.company:
                material_onboarding_data["company_name"] = frappe.db.get_value(
                    "Company Master", mo_doc.company, "company_name"
                )
        except Exception as e:
            frappe.log_error(f"Failed to get Material Onboarding '{mo_ref}'", str(e))

    return {
        "requestor_master": requestor_dict,
        "material_request_item": selected_row.as_dict() if selected_row else {},
        "material_master": material_master_data,
        "material_onboarding": material_onboarding_data
    }


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


@frappe.whitelist()
def send_vendor_code_email(name):
    vendor = frappe.db.get_value("Vendor Master", name, ["vendor_code", "office_email_primary", "company_name"], as_dict=True)
    
    if not vendor:
        frappe.throw("Vendor not found")
    
    vendor_code = vendor.vendor_code,
    reciever_email = vendor.office_email_primary,
    company_name = vendor.company_name,
    current_user = frappe.session.user
    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    from_address = "noreply@merillife.com"
    to_address = reciever_email
    subject = "Vendor Code Generated"
    body = f"Dear {company_name},\n\nYour vendor code is {vendor_code}. Your username will be {reciever_email}. The username will be activated in 24 hours. After 24 hours, you will receive an email with the password.\n\nThank you."
    
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
def set_changed_delivery_date_status(data, method):
    print("*********** Change Delivery Date ***********")
    print("Received Data:", data)

    if not data:
        print("Error: No data received.")
        return

    vendor_code = data.get('vendor_code') 
    if not vendor_code:
        print("Error: 'vendor code' is missing or empty in the data.")
        return

    print("Received vendor code:", vendor_code)
    refno = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=['name'])
    vendor_name = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=['vendor_name'])
    office_email_primary = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=['office_email_primary'])
    designation_name1 = frappe.db.get_value("User", filters={'email': office_email_primary}, fieldname=['designation'])
    print("Designation name1 ------>", designation_name1)

    if not office_email_primary:
        print(f"Error: No record found in 'Vendor Master' for Vendor Code: {vendor_code}")
        return

    print("%%%%%%% Office Email Primary %%%%%%%%%%", office_email_primary)
    docname = data.get('name')
    purchase_number = data.get('purchase_num')
    new_delivery_date = data.get('new_po_date') 
    status = data.get('status')
    print("%%%%%%% Purchase Number (date change) %%%%%%%%%%", purchase_number, status)

    purchase_order = frappe.get_doc("Purchase Order", {"name": purchase_number})
    old_delivery_date = frappe.db.get_value('Purchase Order', filters={'name': purchase_number}, fieldname=['delivery_date'])

    if purchase_order:
        purchase_order.delivery_date = new_delivery_date
        purchase_order.save()
        frappe.db.commit()
        print(f"Updated Delivery Date for Purchase Order {purchase_number}.")
        
        meril_email_address = frappe.db.get_value("Delivery Date Change", filters={'name': docname}, fieldname=['meril_email_address'])
        print("Meril Email Address--->",meril_email_address)
        designation_name = frappe.db.get_value("User", filters={'email': meril_email_address}, fieldname=['designation'])
        print("Designation Name from cookies:", designation_name)
        vendor_remarks = frappe.db.get_value("Delivery Date Change", filters={'name': docname}, fieldname=['vendor_remark'])
    
        if designation_name == "Purchase Team" and status == "Pending":
            subject = f"Change in Delivery Date for Purchase Number: {purchase_number}"
            body = f"""
            Dear {vendor_name},

            The delivery date for Purchase Order {purchase_number} has been changed.

            Below are the details:
            Old Delivery Date: {old_delivery_date}
            New Delivery Date: {new_delivery_date}
            Remarks: {data.get('remarks')}
            Contact Person: {meril_email_address}
            
            For any query, mail on above email address or click the link below:

            Thanks
            """
            to_address = office_email_primary
            from_address = meril_email_address
        elif designation_name1 == "Vendor" and status == "Accepted":
            subject = f"Vendor Accepted Delivery Date Change for PO: {purchase_number}"
            body = f"""
            Dear Team,

            The vendor has accepted the changes made to the delivery date for Purchase Order {purchase_number}.

            Below are the details:
            Old Delivery Date: {old_delivery_date}
            New Delivery Date: {new_delivery_date}
            Vendor Remarks: {vendor_remarks}

            Regards,
            {vendor_name}
            """
            to_address = meril_email_address
            from_address = office_email_primary
        elif designation_name1 == "Vendor" and status == "Rejected":
            subject = f"Vendor Rejected Delivery Date Change for PO: {purchase_number}"
            body = f"""
            Dear Team,

            The vendor has rejected the proposed changes to the delivery date for Purchase Order {purchase_number}.

            Below are the details:
            Old Delivery Date: {old_delivery_date}
            Proposed New Delivery Date: {new_delivery_date}
            Vendor Remarks: {vendor_remarks}

            Please reach out to the vendor for further discussion.

            Regards,
            {vendor_name}
            """
            to_address = meril_email_address
            from_address = office_email_primary
        else:
            print(f"Unrecognized designation or status: {designation_name}, {status}")
            return

        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        bcc_address = "rishi.hingad@merillife.com"

        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_address,bcc_address], msg.as_string())
                print("Email sent successfully!")

                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': refno,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Delivery Date Change Notification.",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            msge = f"Failed to send email to {to_address}: {e}"
            print(msge)
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': refno,
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "Delivery Date Change Notification.",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
    else:
        print(f"Error: Purchase Order with number {purchase_number} not found.")

@frappe.whitelist()
def send_email_on_onboarding(data, method):
    print("*********** Checking Onboarding Submission Status ***********")
    print("Received Data:", data)
    
    if not data:
        print("Error: No data received.")
        return

    refno = data.get('ref_no')
    if not refno:
        print("Error: 'Refno' is missing or empty in the data.")
        return
    
    print("Received Refno:", refno)

    onboarding_form_status = frappe.db.get_value("Vendor Onboarding", {"ref_no": refno}, "onboarding_form_status")
    qms_form_status = frappe.db.get_value("Supplier QMS Assessment Form", {"ref_no": refno}, "qms_form_status")

    print(f"Onboarding Form Status: {onboarding_form_status}, QMS Form Status: {qms_form_status}")

    if onboarding_form_status != "Submitted" or qms_form_status != "Submitted":
        print("Skipping email: Onboarding or QMS form is not submitted.")
        return
    
    print("*********** Onboarding Details Filled ***********")
    
    office_email_primary = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname='office_email_primary')
    if not office_email_primary:
            print(f"Error: No record found in 'Vendor Master' for Refno: {refno}")
            return
        
    print("%%%%%%% Office Email Primary %%%%%%%%%%", office_email_primary)

    name = office_email_primary
    print("%%%%%%% Onboarding Detail Name %%%%%%%%%%", name)
    conf = frappe.conf
    server_url = conf.get("server_url")
    refnumber = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['name'])
    vendor_name = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['vendor_name'])
    onboardingrefno = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': refno}, fieldname=['name'])
    frappe.db.sql("""UPDATE `tabVendor Onboarding` SET ref_no=%s WHERE office_email_primary=%s""", (refno, name))
    frappe.db.commit()
    frappe.db.sql("""UPDATE `tabVendor Master` SET onboarding_ref_no=%s WHERE office_email_primary=%s""", (onboardingrefno, name))
    frappe.db.commit()

    meril_company = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
    company_name = frappe.db.get_value("Company Master", filters={'company_code': meril_company}, fieldname='company_name')
    print("***** This Meril Company Name (without Child table) ****", meril_company, company_name)

    company_data = frappe.get_all("Multiple Company Data", filters={"parent": refno}, fields=["company_name_mt"])
    company_codes = []
    for company_entry in company_data:
        company_name_mt = company_entry.get("company_name_mt")
        if company_name_mt:
            company_code = frappe.db.get_value("Company Master", filters={'company_name': company_name_mt}, fieldname='company_code')
            if company_code:
                company_codes.append(company_code)

    if any(code in ['2000', '7000'] for code in company_codes):
        onboarding_form_status = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': refno}, fieldname=['onboarding_form_status'])
        qms_form_status = frappe.db.get_value("Supplier QMS Assessment Form", filters={'ref_no': refno}, fieldname=['qms_form_status'])

        if onboarding_form_status == "Submitted" and qms_form_status == "Submitted":
            current_user_email = name
            print("Email for onboarding:", current_user_email)
            reciever_email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['registered_by'])
            print("Receiver email:", reciever_email)
            base_link = f"{server_url}/vendor-details/{name}"
            links = []
            if company_codes:
                for company_code in company_codes:
                    links.append(f"{base_link}&{company_code}")
            else:
                if meril_company:
                    links.append(f"{base_link}&{meril_company}")

            final_links = "\n".join(links)
            print("******* Final Link in Body ******", final_links)
            body = f"Vendor has successfully submitted its details in the onboarding form on the VMS Portal. Please check the details on these links:\n{final_links}"

            conf = frappe.conf
            smtp_server = conf.get("smtp_server")
            smtp_port = conf.get("smtp_port")
            smtp_user = conf.get("smtp_user")
            smtp_password = conf.get("smtp_password")
            from_address = current_user_email
            to_address = reciever_email
            bcc_address = "rishi.hingad@merillife.com"
            subject = "Vendor Onboarding Submission Confirmation."
            msg = MIMEMultipart()
            msg["From"] = from_address
            msg["To"] = to_address
            msg["Subject"] = subject
            msg["Bcc"] = bcc_address
            msg.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
                    print("Email sent successfully!")

                    doc = frappe.get_doc({
                        'doctype': 'Email Log',
                        'ref_no': refno,
                        'to_email': to_address,
                        'from_email': from_address,
                        'message': body,
                        'status': "Successfully Sent",
                        'screen': "Onboarding form submitted.",
                        'created_by': from_address
                    })
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()

            except Exception as e:
                msge = f"Failed to send email to {to_address}: {e}"
                print(msge)
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': refno,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': msge,
                    'screen': "Onboarding form submitted.",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        else:
            print("Onboarding form or QMS form is not submitted, skipping email.")
    else:
        onboarding_form_status = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': refno}, fieldname=['onboarding_form_status'])
        if onboarding_form_status == 'Submitted':
            current_user_email = name
            print("Email for onboarding:", current_user_email)
            meril_company = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
            company_name = frappe.db.get_value("Company Master", filters={'company_name': meril_company}, fieldname='company_code')
            print(company_name)
            reciever_email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['registered_by'])
            print("Receiver email:", reciever_email)
            base_link = f"{server_url}/vendor-details/{name}"
            links = []
            multiple_company_data = frappe.get_all(
                "Multiple Company Data",
                filters={"parent": refno},
                fields=["company_name_mt"]
            )
            if multiple_company_data:
                print("Found multiple company data:", multiple_company_data)
                for company_entry in multiple_company_data:
                    company_name_mt = company_entry.get("company_name_mt")
                    if company_name_mt:
                        company_code = frappe.db.get_value("Company Master", filters={'company_name': company_name_mt}, fieldname='company_code')
                        if company_code:
                            links.append(f"{base_link}&{company_code}")
            else:
                if meril_company:
                    links.append(f"{base_link}&{meril_company}")

            final_links = "\n".join(links)
            print("******* Final Link in Body ******", final_links)
            body = f"Vendor has successfully submitted its details in the onboarding form on the VMS Portal. Please check the details on these links:\n{final_links}"

            conf = frappe.conf
            smtp_server = conf.get("smtp_server")
            smtp_port = conf.get("smtp_port")
            smtp_user = conf.get("smtp_user")
            smtp_password = conf.get("smtp_password")
            from_address = current_user_email
            to_address = reciever_email
            bcc_address = "rishi.hingad@merillife.com"
            subject = "Vendor Onboarding Submission Confirmation."
            msg = MIMEMultipart()
            msg["From"] = from_address
            msg["To"] = to_address
            msg["Subject"] = subject
            msg["Bcc"]= bcc_address
            msg.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.sendmail(from_address, [to_address,bcc_address], msg.as_string())
                    print("Email sent successfully!")

                    doc = frappe.get_doc({
                        'doctype': 'Email Log',
                        'ref_no': refno,
                        'to_email': to_address,
                        'from_email': from_address,
                        'message': body,
                        'status': "Successfully Sent",
                        'screen': "Onboarding form submitted.",
                        'created_by': from_address
                    })
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()

            except Exception as e:
                msge = f"Failed to send email to {to_address}: {e}"
                print(msge)
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': refno,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': msge,
                    'screen': "Onboarding form submitted.",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()


@frappe.whitelist()
def hit():
    print("****************Hi there!*******************")
    purchase_head_key = frappe.db.get_value("Designation Master", {"designation_name": "Purchase Head"}, "name")
    accounts_team_key = frappe.db.get_value("Designation Master", {"designation_name": "Accounts Team"}, "name")
    purchase_head_users = frappe.db.get_list("User", filters={"designation": purchase_head_key}, fields=["email"])
    accounts_team_users = frappe.db.get_list("User", filters={"designation": accounts_team_key}, fields=["email"])
    all_emails = [user["email"] for user in accounts_team_users] + [user["email"] for user in purchase_head_users]
    print(all_emails)
    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password") 
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


@frappe.whitelist()
def show_dispatch_order_detail_vendor(**kwargs):
    vendor_code = kwargs.get('vendor_code')

    if not vendor_code:
        return {'error': 'Vendor code is not provided or invalid'}

    dispatch_details = frappe.db.sql("""
        SELECT * FROM `tabDispatch Item`
        WHERE vendor_code = %s
    """, (vendor_code,), as_dict=1)

    if not dispatch_details:
        return {'error': 'No dispatch details found for the given vendor code'}

    purchase_numbers = list(set(d['purchase_number'] for d in dispatch_details if d.get('purchase_number')))
    purchase_orders = frappe.get_all("Purchase Order", filters={"name": ["in", purchase_numbers]}, fields=["name", "po_number", "ship_to_company"])
    
    po_details = {po['name']: po for po in purchase_orders}
    company_ids = list(set(po.get('ship_to_company') for po in po_details.values() if po.get('ship_to_company')))
    company_names = frappe.get_all("Company Master", filters={"name": ["in", company_ids]}, fields=["name", "company_name"])
    company_details = {company['name']: company['company_name'] for company in company_names}

    for detail in dispatch_details:
        detail['dispatch_order_item'] = frappe.db.sql("""
            SELECT * FROM `tabDispatch Order Items`
            WHERE parent = %s
        """, (detail['name'],), as_dict=1)

        po_info = po_details.get(detail.get('purchase_number'))
        if po_info:
            detail['po_number'] = po_info.get('po_number')
            ship_to_company_id = po_info.get('ship_to_company')
            detail['ship_to_company'] = company_details.get(ship_to_company_id, ship_to_company_id)

        for item in detail.get('dispatch_order_item', []):
            if item.get('uom'):
                item['uom'] = frappe.db.get_value("UOM Master", item['uom'], "uom")
            if item.get('product_code'):
                item['product_code'] = frappe.db.get_value("Product Master", item['product_code'], "product_code")
            if item.get('product_name'):
                item['product_name'] = frappe.db.get_value("Product Master", item['product_name'], "product_name")

    return dispatch_details


@frappe.whitelist()
def show_dispatch_order_detail(**kwargs):
    pno = kwargs.get('pno')

    vendor_name = None
    po_number = None
    bill_to_company = None
    ship_to_company = None
    registered_by = None
    purchase_numbers_list = []

    if pno:
        vendor_code = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname='vendor_code')
        vendor_name = frappe.db.get_value("Vendor Master", vendor_code, "vendor_name") if vendor_code else "Unknown Vendor"
        registered_by = frappe.db.get_value("Vendor Master", vendor_code, "registered_by") if vendor_code else "Unknown Vendor"
        po_number = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname='po_number') or "Not Available"
        bill_to_company = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname='bill_to_company')
        ship_to_company = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname='ship_to_company')
        
        dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item` WHERE purchase_number=%s""", (pno,), as_dict=1)
    else:
        dispatch_detail = frappe.db.sql("""SELECT * FROM `tabDispatch Item`""", as_dict=1)

    for detail in dispatch_detail:
        dispatch_order_item = frappe.db.sql("""SELECT * FROM `tabDispatch Order Items` WHERE parent=%s""", (detail['name'],), as_dict=1)
        detail['dispatch_order_item'] = dispatch_order_item

        if not pno:
            purchase_numbers = frappe.db.sql("""
                SELECT purchase_number 
                FROM `tabDispatch Purchase No Group` 
                WHERE parent=%s
            """, (detail['name'],), as_dict=1)

            for purchase in purchase_numbers:
                if purchase.get('purchase_number'):
                    purchase_numbers_list.append(purchase['purchase_number'])

            if purchase_numbers_list:
                purchase_number = purchase_numbers_list[0]
                print("**** Extracted Purchase Number ****", purchase_number)

                vendor_code = frappe.db.get_value("Purchase Order", filters={"name": purchase_number}, fieldname=['vendor_code'])
                vendor_name = frappe.db.get_value("Vendor Master", filters={"vendor_code": vendor_code}, fieldname=["vendor_name"]) if vendor_code else "Unknown Vendor"
                registered_by = frappe.db.get_value("Vendor Master", filters={"vendor_code": vendor_code}, fieldname=["registered_by"]) if vendor_code else "Unknown Vendor"
                po_number = frappe.db.get_value("Purchase Order", filters={"name": purchase_number}, fieldname='po_number') or "Not Available"
                bill_to_company_code = frappe.db.get_value("Purchase Order", filters={"name": purchase_number}, fieldname='bill_to_company')
                bill_to_company = frappe.db.get_value("Company Master", bill_to_company_code, "company_name") if bill_to_company_code else None
                ship_to_company_code = frappe.db.get_value("Purchase Order", filters={"name": purchase_number}, fieldname='ship_to_company')
                ship_to_company = frappe.db.get_value("Company Master", ship_to_company_code, "company_name") if ship_to_company_code else None
                print("Registered_by---->",vendor_code,vendor_name,registered_by)
        detail['vendor_name'] = vendor_name
        detail['registered_by'] = registered_by
        detail['po_number'] = po_number
        detail['bill_to_company'] = bill_to_company
        detail['ship_to_company'] = ship_to_company

        for item in dispatch_order_item:
            if item.get('uom'):
                item['uom'] = frappe.db.get_value("UOM Master", item['uom'], "uom")
            if item.get('product_code'):
                item['product_code'] = frappe.db.get_value("Product Master", item['product_code'], "product_code")
            if item.get('product_name'):
                item['product_name'] = frappe.db.get_value("Product Master", item['product_name'], "product_name")

    return dispatch_detail


@frappe.whitelist()
def total_number_of_dispatch_details(vendor_code):
    if not vendor_code:
        print("Vendor code is empty or None.")
        return 0

    try:
        print(f"Vendor Code received: {vendor_code}")
        count_result = frappe.db.sql("""
            SELECT COUNT(*) AS count
            FROM 
                `tabDispatch Item`
            WHERE vendor_code = %s
        """, (vendor_code,), as_dict=True)

        count = count_result[0]['count'] if count_result else 0

        return count
    except Exception as e:
        return 0


@frappe.whitelist()
def send_email_on_dispatch(data, method):
    ccurrent_user = frappe.session.user
    try:
        name = data.get('name')
        print("************ Email on Dispatch Order ********",data)
        print("**** Doctype Name/ID *****",name)
        
        dispatch_item_doc = frappe.get_doc("Dispatch Item", name)
        print(f"Dispatch Items Data: {dispatch_item_doc.items}")

        purchase_numbers = [
            row.purchase_number for row in dispatch_item_doc.get("purchase_number") if row.purchase_number
        ]
        print(f"Extracted Purchase Numbers: {purchase_numbers}")

        for pno in purchase_numbers:
            purchase_order_doc = frappe.get_doc("Purchase Order", pno)
            print("Purchase Order details----->",purchase_order_doc)
            print(f"Purchase Order Data: {purchase_order_doc.po_items}")

        purchase_order_doc.status = "Shipped"

        for item in purchase_order_doc.po_items:
            if item.pending_qty is None or item.pending_qty == "":
                print(f"Setting Pending Qty to 0 for Product: {item.product_name}")
                item.pending_qty = 0.0
            else:
                item.pending_qty = float(item.pending_qty)

            if item.dispatch_qty is None or item.dispatch_qty == "":
                print(f"Setting Dispatch Qty to 0 for Product: {item.product_name}")
                item.dispatch_qty = 0.0
            else:
                item.dispatch_qty = float(item.dispatch_qty)

            print(f"Initial: Product Code: {item.product_name}, Pending Qty: {item.pending_qty}, Dispatch Qty: {item.dispatch_qty}")

        for item in purchase_order_doc.po_items:
            print(f"Processing item: {item.product_name}")
            print(f"Dispatch Item Data: {[row.product_name for row in dispatch_item_doc.items]}")
            matching_dispatch_items = [row for row in dispatch_item_doc.items if row.product_name.strip() == item.product_name.strip()]
            print(f"Matching Dispatch Items for {item.product_name}: {matching_dispatch_items}")

            if matching_dispatch_items:
                for dispatch_item_row in matching_dispatch_items:
                    print(f"Matching Dispatch Item Found: {dispatch_item_row.product_name} - Dispatch Qty: {dispatch_item_row.dispatch_qty} - Pending Qty: {dispatch_item_row.pending_qty}")
                    
                    print(f"Updating {item.product_name}: Pending Qty (before): {item.pending_qty}, Dispatch Qty (before): {item.dispatch_qty}")
                    item.pending_qty = dispatch_item_row.pending_qty
                    item.dispatch_qty += dispatch_item_row.dispatch_qty

                    print(f"Updated: Product Name: {item.product_name}, Pending Qty: {item.pending_qty}, Dispatch Qty: {item.dispatch_qty}")

                    item._dirty = True
                    item.save()
            else:
                print(f"No matching dispatch item found for product_name: {item.product_name} in Dispatch Items")
                continue

        frappe.db.commit()

        for item in purchase_order_doc.po_items:
            matching_dispatch_items = [row for row in dispatch_item_doc.items if row.product_name.strip() == item.product_name.strip()]
            
            if matching_dispatch_items:
                for dispatch_item_row in matching_dispatch_items:
                    new_dispatch_qty = dispatch_item_row.dispatch_qty
                    new_pending_qty = dispatch_item_row.pending_qty

                    print(f"Updating {item.product_name}: Pending Qty (before): {item.pending_qty}, Dispatch Qty (before): {item.dispatch_qty}")
                    
                    if item.pending_qty > 0:
                        item.pending_qty = max(0, item.pending_qty - new_pending_qty)
                    
                    item.dispatch_qty += new_dispatch_qty

                    print(f"Updated: Product Name: {item.product_name}, Pending Qty: {item.pending_qty}, Dispatch Qty: {item.dispatch_qty}")

                    item._dirty = True
                    item.save()
        frappe.db.commit()

        print(f"Updated Purchase Order: {purchase_order_doc.name}")
        print(f"Updated PO Items After Commit: {[f'{item.product_name}: Pending Qty={item.pending_qty}, Dispatch Qty={item.dispatch_qty}' for item in purchase_order_doc.po_items]}")

        for pno in purchase_numbers:
            vendor_code = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname="vendor_code")
            print(f"Vendor Code for Purchase Number {pno}: {vendor_code}")

        if pno:
            vendor_code = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname=['vendor_code'])
            vendor_name = frappe.db.get_value("Vendor Master", filters={"vendor_code":vendor_code}, fieldname=["vendor_name"]) if vendor_code else None
            po_number = frappe.db.get_value("Purchase Order", filters={"name": pno}, fieldname='po_number')
            bill_to_company_code = frappe.db.get_value("Purchase Order", filters={"name": po_number}, fieldname='bill_to_company')
            bill_to_company = frappe.db.get_value("Company Master", filters={"name":bill_to_company_code}, fieldname=["company_name"])
            ship_to_company_code = frappe.db.get_value("Purchase Order", filters={"name": po_number}, fieldname='ship_to_company')
            ship_to_company = frappe.db.get_value("Company Master", filters={"name":ship_to_company_code}, fieldname=["company_name"])
            invoice_number = frappe.db.get_value("Dispatch Item", filters={"purchase_number":pno}, fieldname=['invoice_number'])
            invoice_amount = frappe.db.get_value("Dispatch Item", filters={"purchase_number":pno}, fieldname=['invoice_amount'])
            invoice_date = frappe.db.get_value("Dispatch Item", filters={"purchase_number":pno}, fieldname=['invoice_date'])
            courier_name = frappe.db.get_value("Dispatch Item", filters={"purchase_number":pno}, fieldname=['courier_name'])
            dispatch_date = frappe.db.get_value("Dispatch Item", filters={"purchase_number":pno}, fieldname=['dispatch_date'])

            print("1st details of dispatched_order---->",vendor_code, vendor_name, po_number, bill_to_company, ship_to_company, courier_name, dispatch_date)

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
                bill_to_company_code = frappe.db.get_value("Purchase Order", filters={"name": detail['purchase_number']}, fieldname='bill_to_company')
                bill_to_company = frappe.db.get_value("Company Master", bill_to_company_code, "company_name") if bill_to_company_code else None
                ship_to_company_code = frappe.db.get_value("Purchase Order", filters={"name": detail['purchase_number']}, fieldname='ship_to_company')
                ship_to_company = frappe.db.get_value("Company Master", ship_to_company_code, "company_name") if ship_to_company_code else None

            detail['vendor_name'] = vendor_name
            detail['po_number'] = po_number
            detail['bill_to_company'] = bill_to_company
            detail['ship_to_company'] = ship_to_company

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

        vendor_email = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=['registered_by'])
        vendor_name = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=['vendor_name'])
        from_address = ccurrent_user
        to_address = vendor_email
        bcc_address = "rishi.hingad@merillife.com"
        subject = f"Dispatch Order dispatched - PO Number: {po_number}"
        html_body = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Table Example</title>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    border: 1px solid black;
                }}

                td, th {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }}

                th {{
                    background-color: #f2f2f2;
                }}

                .header-table td {{
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>

        <table>
            <tr class="header-table">
                <td>Company</td>
                <td>{bill_to_company}</td>
            </tr>
            <tr class="header-table">
                <td>Po. No.</td>
                <td>{po_number}</td>
            </tr>
            <tr>
                <th>Invoice Number</th>
                <th>Invoice Amount</th>
                <th>Invoice Date</th>
                <th>Dispatch Date</th>
                <th>Courier Name</th>
            </tr>
            <tr>
                <td>{invoice_number}</td>
                <td>{invoice_amount}</td>
                <td>{invoice_date}</td>
                <td>{dispatch_date}</td>
                <td>{courier_name}</td>
            </tr>
        </table>

        </body>
        </html>
        """
        body = f"""
        Dear {bill_to_company},
        
        Please find the dispatch details for your purchase order {po_number}.
        Dispatch Details: {html_body}
        
        Best Regards,
        {vendor_name}
        """
        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
                print("Email sent successfully!")

                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': po_number,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Dispatch Order",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email: {e}")
            msge = f"Failed to send email: {e}"
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': po_number,
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "Dispatch Order",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

        return "Dispatch Order Email Sent Successfully."

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "send_email_on_dispatch Error")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def hitt(data, method):
    
    list_of_names = data.get('list', [])
    name = data.get('name')
    rfq_number = data.get('name')
    print("************************************", name, list_of_names)
    call = frappe.db.sql(""" UPDATE `tabRequest For Quotation` SET vendor_list=%s WHERE name=%s  """,(list_of_names, name))
    email_id_of_rfq_creator = frappe.session.user
    frappe.db.sql("UPDATE `tabRequest For Quotation` SET raised_by=%s",(email_id_of_rfq_creator))
    frappe.db.commit()
    
    all_office_emails = []
    print("**********************((((((((()))))))))", name)
    
    for name in list_of_names:
        vendors = frappe.db.sql("""
            SELECT office_email_primary 
            FROM `tabVendor Master` 
            WHERE name = %s
        """, (name,), as_dict=True)
        
        office_emails = [vendor.get('office_email_primary') for vendor in vendors]
        
        all_office_emails.extend(office_emails)
    
    print("List of office_email_primary:", all_office_emails)

    email_id_of_rfq_creator = frappe.session.user
    print("Email ID of RFQ Creator:", email_id_of_rfq_creator)

    rfq_type = frappe.db.get_value("Request for Quotation", filters={'name':name}, fieldname=['select_services'])
   
    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    server_url = conf.get("server_url")
    print("Server URL:", server_url)
    from_address = "noreply@merillife.com"
    subject = "RFQ Generated"

    if rfq_type == "Logistics Vendor":
        country = frappe.db.get_value("Request for Quotation", filters={'name':name}, fieldname=['country'])
        pod = frappe.db.get_value("Request for Quotation", filters={'name':name}, fieldname=['destination_port'])
        company_id = frappe.db.get_value("Request for Quotation", filters={'name': name}, fieldname=['company_name'])
        company = frappe.db.get_value("Company Master", filters={'name':company_id}, fieldname=['company_name'])
        Shipper_Mode = frappe.db.get_value("Request for Quotation", filters={'name': name}, fieldname=['mode_of_shipment'])
        shipment_date = frappe.db.get_value("Request for Quotaion", filters={'name':name}, fieldname=['shipment_date'])
        boxes = frappe.db.get_value("Request for Quotaion", filters={'name':name}, fieldname=['no_of_pkg_units'])
        actual_weight = frappe.db.get_value("Request for Quotaion", filters={'name':name}, fieldname=['actual_weight'])
        vol_weight = frappe.db.get_value("Request for Quotaion", filters={'name':name}, fieldname=['vol_weight'])
        product_id = frappe.db.get_value("Request for Quotation", filters={'name':name}, fieldname=['product_category'])
        product_category = frappe.db.get_value("Product Category Master", filters={'name':product_id}, fieldname=['product_category_name'])
        shipment_id = frappe.db.get_value("Request for Quotation", filters={'name':name}, fieldname=["shipment_type"])
        shipment_name = frappe.db.get_value("Request for Quotation", filters={'name': shipment_id}, fieldname=['shipment_type_name'])
        rfq_cutoff_date = frappe.db.get_value("Request for Quotation", filters={'name':name}, fieldname=['rfq_cutoff_date'])
        remarks = frappe.db.get_value("Reqeust for Quotation", filters={'name':name}, fieldname=['remarks'])
        raised_by = frappe.db.get_value("Request for Quotation", filters={'name':name}, fieldname=['raised_by'])
        raised_by_name = frappe.db.get_value("User", filters={'name':raised_by}, fieldname=['full_name'])

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vendor Details</title>
    </head>
    <body>
        <h2>Example Table</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tbody>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">RFQ Reference Number:</td>
                    <td style="border: 1px solid black; padding: 8px;" >{name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Origin Country:</td>
                    <td style="border: 1px solid black; padding: 8px;">{country}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">POD:</td>
                    <td style="border: 1px solid black; padding: 8px;" >{pod}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Shipper Name:</td>
                    <td style="border: 1px solid black; padding: 8px;">{company}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Shipper Mode</td>
                    <td style="border: 1px solid black; padding: 8px;" >{Shipper_Mode}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Expected Date of Arrival:</td>
                    <td style="border: 1px solid black; padding: 8px;">{shipment_date}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Number of Boxes</td>
                    <td style="border: 1px solid black; padding: 8px;" >{boxes}</td>
                    </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Vol. Weight(KG)</td>
                    <td style="border: 1px solid black; padding: 8px;">{vol_weight}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Actual Weight(KG)</td>
                    <td style="border: 1px solid black; padding: 8px;" >{actual_weight}</td>
                    </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Product Category</td>
                    <td style="border: 1px solid black; padding: 8px;">{product_category}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Shipment Type</td>
                    <td style="border: 1px solid black; padding: 8px;" >{shipment_name}</td>
                    </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">RFQ Cut Off Date & Time:</td>
                    <td style="border: 1px solid black; padding: 8px;">{rfq_cutoff_date}</td>
                </tr>
                 <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Remarks</td>
                    <td style="border: 1px solid black; padding: 8px;" colspan="3">{remarks}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Meril Contact Person</td>
                    <td style="border: 1px solid black; padding: 8px;" colspan="3">{raised_by_name}</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """
    link = f"""{server_url}/vendor/dashboard/quotation?RFQno={rfq_number}"""
    body = f"""
    Dear Sir/Madam,

    Please find the below given shipment details that needs to be imported. Kindly go through the following particulars and provide your best competitive rate for the same.<br/>
    {html_body}<br/>

    Please click the link here below to submit your quote.
    <a href={link}>Click Here!</a>

    """
    
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
                doc = frappe.get_doc({

                    'doctype': 'Email Log',
                    'ref_no': rfq_number,
                    'to_email': to_address,
                    'from_email': 'from_address',
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Raise RFQ",
                    'created_by': email_id_of_rfq_creator


                    })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()
        except Exception as e:
            msge = f"Failed to send email to {to_address}: {e}"
            print(f"Failed to send email to {to_address}: {e}")
            doc = frappe.get_doc({

                    'doctype': 'Email Log',
                    'ref_no': rfq_number,
                    'to_email': to_address,
                    'from_email': 'from_address',
                    'message': body,
                    'status': msge,
                    'screen': "Raise RFQ",
                    'created_by': email_id_of_rfq_creator


                    })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()


def set_rfq_raisers_name(data, method):

    email_id_of_rfq_creator = frappe.session.user
    frappe.db.sql("update `tabRequest For Quotation` SET raised_by=%s",(email_id_of_rfq_creator))
    frappe.db.commit()

@frappe.whitelist()
def send_email_on_quotation_creation(data, method):

    rfq_number = data.get('rfq_number')
    name = data.get('name')
    reciever_address = frappe.db.get_value("Request For Quotation", filters={'name': rfq_number}, fieldname=['raised_by'])
    sender_address = frappe.session.user
    print(reciever_address, sender_address)
    print(rfq_number)
    print("******************************************************")
    subject = "Hi there from SendEmail Class ...!"
    #obj.send_email(reciever_address, sender_address, subject)
    #test_send_email()
    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password") 
    from_address = sender_address 
    to_address = reciever_address
    subject = "Quotation from Vendor"
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
            doc = frappe.get_doc({

                    'doctype': 'Email Log',
                    'ref_no': name,
                    'to_email': to_address,
                    'from_email': 'from_address',
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Create Quotation",
                    'created_by': from_address


                    })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
    except Exception as e:
        print(f"Failed to send email: {e}")
        msge = f"Failed to send email: {e}"
        doc = frappe.get_doc({

                    'doctype': 'Email Log',
                    'ref_no': name,
                    'to_email': to_address,
                    'from_email': 'from_address',
                    'message': body,
                    'status': msge,
                    'screen': "Create Quotation",
                    'created_by': from_address
                    })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()


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
            qo.rfq_number AS rfq_number,
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
            tocr.currency_name AS to_currency_name,
            qo.fuel_surcharge AS fuel_surcharge,
            qo.sc AS sc,
            qo.xray AS xray,
            qo.pickuporigin AS pickuporigin,
            qo.ex_works AS ex_works,
            qo.transit_days AS transit_days,
            qo.total_freight AS total_freight,
            qo.exchange_rate AS exchange_rate,
            qo.total_freightinr AS total_freightinr,
            qo.destination_charge AS destination_charge,
            qo.shipping_line_charge AS shipping_line_charge,
            qo.cfs_charge AS cfs_charge,
            qo.total_landing_price AS total_landing_price,
            qo.remarks AS remarks

        FROM
            `tabQuotation` qo
            LEFT JOIN `tabRequest For Quotation` rfq ON qo.rfq_number = rfq.name
            LEFT JOIN `tabCompany Master` co ON qo.company_name = co.name
            LEFT JOIN `tabVendor Master` vm ON qo.vendor_code = vm.name
            LEFT JOIN `tabProduct Master` pm ON qo.product_code = pm.name
            LEFT JOIN `tabProduct Category Master` pc ON qo.product_category = pc.name
            LEFT JOIN `tabOld Material Master` mm ON qo.material_code = mm.name
            LEFT JOIN `tabMaterial Category Master` mcm ON qo.material_category = mcm.name
            LEFT JOIN `tabOld Material Master` m ON qo.material_name = m.name
            LEFT JOIN `tabCurrency Master` frmcr ON qo.from_currency = frmcr.name
            LEFT JOIN `tabCurrency Master` tocr ON qo.to_currency = tocr.name
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
            LEFT JOIN `tabOld Material Master` mm ON qo.material_code = mm.name
            LEFT JOIN `tabMaterial Category Master` mcm ON qo.material_category = mcm.name
            LEFT JOIN `tabOld Material Master` m ON qo.material_name = m.name
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
    register_email = frappe.db.get_value("Vendor Master", filters={'name': vendor_code}, fieldname=['registered_by'])
    print("********************************************")
    print(po_creator, vendor_email, vendor_code)
    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password") 
    server_url = conf.get("server_url")
    from_address = po_creator
    to_address = vendor_email
    cc_address = register_email
    bcc_address = "rishi.hingad@merillife.com"
    subject = "Purchase Order (PO) Generated."
    body = f"Purchase Order has been created. Please check on the VMS Portal for more details.{server_url}/vendor/dashboard/purchase-order?POName=" + str(name)
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["CC"] = cc_address
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(smtp_user, smtp_password)  
            server.sendmail(from_address, [to_address, bcc_address], cc_address, msg.as_string()) 
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
def generate_custom_random_string():

    uppercase_letters = random.choices(string.ascii_uppercase, k=2)
 
    lowercase_letters = random.choices(string.ascii_lowercase, k=3)

    digits = random.choices(string.digits, k=3)

    special_characters = random.choices('!@#$', k=2)
    
    combined_list = uppercase_letters + lowercase_letters + digits + special_characters
    random.shuffle(combined_list)
    
    random_string = ''.join(combined_list)
    return random_string


@frappe.whitelist()
def create_new_user(email_address, password, full_name ,first_name, designation, role, last_name=None):
    user = frappe.new_doc("User")
    user.email = email_address
    user.full_name = full_name
    user.first_name = first_name
    user.designation = designation
    print("**************From create_new_user ************************", email_address, password,first_name, designation)

    if last_name:
        user.last_name = last_name

    user.enabled = 1
    user.new_password = password
    user.send_welcome_email = False

    if role:
        user.add_roles(role)
    else:
        frappe.throw("Role must be provided.")

    user.save(ignore_permissions=True)
    return user


@frappe.whitelist()
def send_email_on_new_added_product(**kwargs):
    name = kwargs.get("name")
    print("***** This is current User for new product ****", name)
    refno = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['ref_no'])
    vendor_name = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['vendor_name'])
    email = frappe.db.get_value("Vendor Master", filters={'name':refno},fieldname=['office_email_primary'])
    registered_by = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['registered_by'])
    meril_name = frappe.db.get_value("User", filters={'email': registered_by}, fieldname=['full_name'])
    vendor_onboarding_details = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['first_name', 'last_name', 'state', 'city', 'district', 'country', 'pincode', 'address_line_1', 'address_line_2', 'vendor_type', 'size_of_company', 'company_name','purchase_team_remarks','purchase_head_remark'])
    supplied_products = frappe.get_all(
        "Supplied",
        filters={'parent': name},
        fields=['material_description']
    )

    supplied_products.sort(key=lambda x: x['creation'], reverse=True)
    new_product_names = [product['material_description'] for product in supplied_products if product['creation'] >= frappe.utils.now_datetime() - timedelta(days=1)]
    all_product_names = [product['material_description'] for product in supplied_products]
    
    new_product_names_str = ", ".join(new_product_names)
    all_product_names_str = ", ".join(all_product_names)
    
    multiple_company_data = frappe.get_all("Multiple Company Data", filters={'parent': refno}, fields=['company_name_mt'])
    company_codes = [company['company_name_mt'] for company in multiple_company_data]

    if not company_codes:
        company_code = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname='company_name')
        company_codes.append(company_code)

    company_codes_str = ", ".join(company_codes)

    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password") 
    server_url = conf.get("server_url")
    from_address = "noreply@merillife.com"
    to_address = registered_by
    bcc_address = "rishi.hingad@merillife.com"
    subject = F""" New Product added by {vendor_name}"""
    body = f"""
        Dear {meril_name},

        {vendor_name} has added the following new product(s) to its product list:
        {new_product_names_str}

        Complete product list:
        {all_product_names_str}

        To view more about the details, click the link below:
        {server_url}/vendor-details/{email}&{company_codes_str}
        
        Regards,
        VMS Team
        Meril Life Sciences Pvt. Ltd.

    """
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(smtp_user, smtp_password)  
            server.sendmail(from_address, [to_address,bcc_address], msg.as_string()) 
            print("Email sent successfully!")
            doc = frappe.get_doc({
            'doctype': 'Email Log',
            'ref_no': name,
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': "Successfully Sent",
            'screen': "New Product Added",
            'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return 200 ,'ok'
    except Exception as e:
        print(f"Failed to send email: {e}")
        msge = f"Failed to send email: {e}"
        doc = frappe.get_doc({

            'doctype': 'Email Log',
            'ref_no': name,
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': f"Failed to send email: {e}",
            'screen': "New Product Added",
            'created_by': from_address
            })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return 500

@frappe.whitelist()
def send_email_on_deleted_product(**kwargs):
    name = kwargs.get("name")
    print("***** This is current User for deleted product ****", name)
    
    refno = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['ref_no'])
    if not refno:
        return 400, "Reference number not found"
    
    vendor_name = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['vendor_name'])
    email = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['office_email_primary'])
    registered_by = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['registered_by'])
    meril_name = frappe.db.get_value("User", filters={'email': registered_by}, fieldname=['full_name'])

    current_supplied_products = frappe.get_all(
        "Supplied",
        filters={'parent': name},
        fields=['material_description']
    )
    current_product_names = [product['material_description'] for product in current_supplied_products]

    previous_product_names = kwargs.get("previous_products", [])

    deleted_product_names = list(set(previous_product_names) - set(current_product_names))
    deleted_product_names_str = ", ".join(deleted_product_names)
    all_product_names_str = ", ".join(current_product_names)

    multiple_company_data = frappe.get_all("Multiple Company Data", filters={'parent': refno}, fields=['company_name_mt'])
    company_codes = [company['company_name_mt'] for company in multiple_company_data]

    if not company_codes:
        company_code = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['company_name'])
        company_codes.append(company_code)

    company_codes_str = ", ".join(company_codes)

    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    server_url = conf.get("server_url")
    from_address = "noreply@merillife.com"
    to_address = registered_by
    bcc_address = "rishi.hingad@merillife.com"
    subject = f""" Deleted Products Notification by {vendor_name}"""
    body = f"""
        Dear {meril_name},

        {vendor_name} has deleted the following product(s) from its product list:
        {deleted_product_names_str}

        Current product list:
        {all_product_names_str}

        To view more about the details, click the link below:
        {server_url}/vendor-details/{email}&{company_codes_str}

        Regards,
        VMS Team
        Meril Life Sciences Pvt. Ltd.
    """
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
            print("Email sent successfully!")
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': name,
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': "Successfully Sent",
                'screen': "Deleted Products Notification",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return 200, 'ok'
    except Exception as e:
        print(f"Failed to send email: {e}")
        doc = frappe.get_doc({
            'doctype': 'Email Log',
            'ref_no': name,
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': f"Failed to send email: {e}",
            'screen': "Deleted Products Notification",
            'created_by': from_address
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return 500

@frappe.whitelist()
def send_email_on_brochure_update(**kwargs):
    name = kwargs.get("name")
    print("***** This is current User for brochure update ****", name)
    
    refno = frappe.db.get_value("Vendor Onboarding", filters={'name': name}, fieldname=['ref_no'])
    if not refno:
        return 400, "Reference number not found"
    
    vendor_name = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['vendor_name'])
    email = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['office_email_primary'])
    registered_by = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['registered_by'])
    meril_name = frappe.db.get_value("User", filters={'email': registered_by}, fieldname=['full_name'])

    multiple_company_data = frappe.get_all("Multiple Company Data", filters={'parent': refno}, fields=['company_name_mt'])
    company_codes = [company['company_name_mt'] for company in multiple_company_data]

    if not company_codes:
        company_code = frappe.db.get_value("Vendor Master", filters={'name': refno}, fieldname=['company_name'])
        company_codes.append(company_code)

    company_codes_str = ", ".join(company_codes)

    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    server_url = conf.get("server_url")
    from_address = "noreply@merillife.com"
    to_address = registered_by
    bcc_address = "rishi.hingad@merillife.com"
    subject = f""" New Brochure Uploaded by {vendor_name}"""
    body = f"""
        Dear {meril_name},

        {vendor_name} has uploaded a new brochure.

        To view the brochure, click the link below:
        {server_url}/vendor-details/{email}&{company_codes_str}

        Regards,
        VMS Team

    """
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
            print("Email sent successfully!")
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': name,
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': "Successfully Sent",
                'screen': "Brochure Upload Notification",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return 200, 'ok'
    except Exception as e:
        print(f"Failed to send email: {e}")
        doc = frappe.get_doc({
            'doctype': 'Email Log',
            'ref_no': name,
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': f"Failed to send email: {e}",
            'screen': "Brochure Upload Notification",
            'created_by': from_address
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return 500


@frappe.whitelist()
def set_vendor_onboarding_status(**kwargs):
    name = kwargs.get("name")
    current_user = frappe.session.user
    print("**** This is Current User ****",current_user)
    current_user_designation_key = frappe.db.get_value("User", filters={'email': current_user}, fieldname=['designation'])
    current_user_name = frappe.db.get_value("User", filters={'email': current_user}, fieldname=['full_name'])
    current_user_designation_name = frappe.db.get_value("Designation Master", filters={'name': current_user_designation_key}, fieldname=['designation_name'])
    print("********* Current User Designation Name *********************",current_user_designation_name)
    vendor_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary'])
    length = 10
    print(vendor_email)
    print(name)
    
    if current_user_designation_name == "Account Team":
        print("*****If Account Team current user desgination*****", current_user_designation_name)
        frappe.db.sql(""" UPDATE `tabVendor Master` set accounts_team_approval='Approved' where office_email_primary=%s """,(vendor_email) )
        frappe.db.commit()
        frappe.db.sql(""" UPDATE `tabVendor Master` SET approved_by_accounts_team = %s WHERE name = %s """, (current_user_name, name))
        frappe.db.commit()
        print("*** Set Vendor Onboarding Current User--->", current_user)
        frappe.db.sql(""" UPDATE `tabVendor Onboarding` set accounts_t_approval='Approved' where office_email_primary=%s """,(vendor_email))
        frappe.db.commit()
        print("()()()()((()(()()()())))", "above Count method")
        if  check_approval_and_send_mail_on_all_3_approvals(name) == 1:
            print("All approvals completed.")
            frappe.db.sql("""UPDATE `tabVendor Master`SET status = 'Onboarded' WHERE name = %s""", (name,))
            frappe.db.commit()
            print("Vendor status updated to Onboarded.")
            print("()()()()((()(()()()())))", "from Count method")
            sap_fetch_token(name)
            vendor_details = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['vendor_name'])
            designation_key = frappe.db.get_value("Designation Master", filters={'designation_name': "Vendor"}, fieldname=['name'])
            print("***************Vendor First Name***************", vendor_details)
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            role = "System Manager"
            create_new_user(vendor_email, password, vendor_details ,vendor_details, designation_key, role)
            registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')
            vendor_detail = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['vendor_code', 'vendor_name'])
            vendor_name = vendor_detail[1]
            vendor_code = vendor_detail[0]
            if not vendor_code:
                print(f"Vendor Code not found for Vendor Master with name: {name}. Ensure the vendor code is generated before sending the email.")
                frappe.throw("Vendor Code not Generated. Email not sent.")
            vendor_city= frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['city'])
            vendor_state= frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['state'])
            vendor_company = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['company_name'])
            multiple_company_data = frappe.db.get_all("Multiple Company Data", filters={'parent': name}, fields=['company_name_mt'])

            company_codes = []
            company_names = []

            for company in multiple_company_data:
                company_name_mt = company['company_name_mt']
                company_code = frappe.db.get_value("Company Master", filters={'company_name': company_name_mt}, fieldname=['company_code'])

                if company_code:
                    company_codes.append(company_code)
                if company_name_mt:
                    company_names.append(company_name_mt)

            if not multiple_company_data:
                company_code = vendor_company
                company_name = frappe.db.get_value("Company Master", filters={'name': vendor_company}, fieldname=['company_name'])

                if company_code:
                    company_codes.append(company_code)
                if company_name:
                    company_names.append(company_name)

            company_codes_str = ", ".join(company_codes)
            company_names_str = ", ".join(company_names)

            print(f"Company Codes of AT: {company_codes_str}")
            print(f"Company Names of AT: {company_names_str}")

            # company_code = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['company_name'])
            # company_name = frappe.db.get_value("Company Master", filters={'company_code': company_code}, fieldname=['company_name'])

            conf = frappe.conf
            smtp_server = conf.get("smtp_server")
            smtp_port = conf.get("smtp_port")
            smtp_user = conf.get("smtp_user")
            smtp_password = conf.get("smtp_password")
            server_url = conf.get("server_url")
            from_address = current_user
            to_address = vendor_email
            bcc_address = "rishi.hingad@merillife.com"
            subject = F""" Welcome to Meril : New Vendor Appointment for {company_names_str} – {vendor_name} - {vendor_state},{vendor_city} - VMS Ref # : {name} """
            body = f"""
    To, 
    {vendor_name}

    Greetings for the Day!

    Dear Sir/Madam,

    We are happy to welcome you in the Meril Family and now you are our business associate and extended arm of {company_names_str}.

    Vendor Code is {vendor_code} for {company_names_str}. This is your uniquew Code in Meril records.

    We are confident with your support and rapport we will surely establish {company_names_str} business in your assigned area in fruitful ways.

    We wish you Best of Luck & fruitful association.

    Below is the link of the Portal and Login Credentials.
    {server_url}/Login_page
    Username: {vendor_email}
    Password: {password}

    Please revert us for any query.
    Regards,
    Purchase Team"""

            msg = MIMEMultipart()
            msg["From"] = from_address
            msg["To"] = to_address
            msg["Subject"] = subject
            msg["Bcc"] = bcc_address
            msg.attach(MIMEText(body, "plain"))
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()  
                    server.login(smtp_user, smtp_password)  
                    server.sendmail(from_address, [to_address,bcc_address], msg.as_string()) 
                    print("Email sent successfully!")
                    doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': name,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Account Team Approval",
                    'created_by': from_address
                    })
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.sql(""" UPDATE `tabVendor Master` SET status='Onboarded' WHERE name=%s """, (name,))
                    frappe.db.commit()
                    frappe.db.sql(""" UPDATE `tabVendor Onboarding` SET onboarding_form_status='Onboarded' WHERE office_email_primary=%s """, (vendor_email,))
                    frappe.db.commit()
                    return 200 ,'ok'
            except Exception as e:
                print(f"Failed to send email: {e}")
                msge = f"Failed to send email: {e}"
                doc = frappe.get_doc({

                    'doctype': 'Email Log',
                    'ref_no': name,
                    'to_email': to_address,
                    'from_email': 'from_address',
                    'message': body,
                    'status': f"Failed to send email: {e}",
                    'screen': "Account Team Approval",
                    'created_by': from_address
                    })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()
                return 500
            
            
    vendor_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary'])
    vendorname = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['vendor_name'])
    rejectcomment = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['rejection_comment'])

    print("Vendor email:", vendor_email, vendorname)
    
    purchase_head_email = frappe.db.get_value("User", filters={'designation': "Purchase Head"}, fieldname=['email'])
    print("Purchase Head email:", purchase_head_email)
    status = frappe.db.get_value('Vendor Master',filters={'name':name}, fieldname=['status'])
    print("Status before Rejection Method---->", status)
    
    if current_user_designation_name == "Purchase Team" and status == "Rejected":
        print("*****If Purchase Team current user desgination*****", current_user_designation_name)
        frappe.db.sql(""" UPDATE `tabVendor Master` SET approved_by_purchase_team = %s WHERE name = %s """, (current_user_name, name))
        frappe.db.commit()

        frappe.db.sql(""" UPDATE `tabVendor Onboarding` set onboarding_form_status='Rejected' where ref_no=%s """, (name,))
        frappe.db.commit()
        
        print("Vendor Onboarding status updated to Rejected.")
        
        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        from_address = current_user 
        bcc_address = "rishi.hingad@merillife.com"
        
        subject = f"Vendor Onboarding Rejected - {vendorname}"
        vendorbody = f"""
        <html>
        <body>
            <p>Dear {vendorname},</p>

            <p>We regret to inform you that your onboarding process has been rejected due to the following reason <strong>"{rejectcomment}"</strong>. Please contact us if you have any questions or need further assistance.</p>

            <p>Regards,<br>
            {current_user_name}<br>
            Purchase Team</p>
        </body>
        </html>
        """
        
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = vendor_email
        msg["Subject"] = subject
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(vendorbody, "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(smtp_user, smtp_password)  
                server.sendmail(from_address, [vendor_email,bcc_address], msg.as_string()) 
                print("Rejection email sent to vendor successfully!")
                
                # Log the email sent to the vendor
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': name,
                    'to_email': vendor_email,
                    'from_email': from_address,
                    'message': vendorbody,
                    'status': "Successfully Sent",
                    'screen': "Account Team Approval",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email to vendor: {e}")
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': name,
                'to_email': vendor_email,
                'from_email': from_address,
                'message': vendorbody,
                'status': f"Failed to send email: {e}",
                'screen': "Account Team Approval",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
        
        purchase_head_subject = f"Vendor Onboarding Rejected - {vendorname}"
        purchase_head_body = f"""
        <html>
        <body>
            <p>Dear Purchase Head,</p>
            <p>The vendor onboarding process for <strong>{vendorname}</strong> has been rejected due to the following reason: 
            <strong>{rejectcomment}</strong>. Please take the necessary actions.</p>
            <br>
            <br>
            <br>
            <p>Regards,<br>
            {current_user_name}<br>
            Purchase Team</p>
        </body>
        </html>
        """
        purchase_head_msg = MIMEMultipart()
        purchase_head_msg["From"] = from_address
        purchase_head_msg["To"] = purchase_head_email
        purchase_head_msg["Subject"] = purchase_head_subject
        purchase_head_msg["Bcc"] = bcc_address
        purchase_head_msg.attach(MIMEText(purchase_head_body, "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(smtp_user, smtp_password)  
                server.sendmail(from_address, [purchase_head_email,bcc_address], msg.as_string()) 
                print("Rejection email sent to Purchase Head successfully!")
                
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': name,
                    'to_email': purchase_head_email,
                    'from_email': from_address,
                    'message': purchase_head_body,
                    'status': "Successfully Sent",
                    'screen': "Account Team Approval",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email to Purchase Head: {e}")
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': name,
                'to_email': purchase_head_email,
                'from_email': from_address,
                'message': purchase_head_body,
                'status': f"Failed to send email: {e}",
                'screen': "Account Team Approval",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

        return 200, 'Rejection emails sent successfully'
    
    if current_user_designation_name == "Purchase Team":
        print("*****If Purchase Team current user desgination*****", current_user_designation_name)
        frappe.db.sql(""" UPDATE `tabVendor Master` set purchase_team_approval='Approved' where name=%s """, (name) )
        frappe.db.commit()
        frappe.db.sql(""" UPDATE `tabVendor Master` SET approved_by_purchase_team = %s WHERE name = %s """, (current_user_name, name))
        frappe.db.commit()
        frappe.db.sql(""" UPDATE `tabVendor Onboarding` set purchase_t_approval='Approved' where office_email_primary=%s """,(vendor_email))
        frappe.db.commit()
        registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')
        vendor_code = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['vendor_code'])
        print("******Purchase Team is designation*******",registered_by_email)
        send_email_on_purchase_team_approval(name)
        print("**Purchase Team desgination email****",name)
        return 200 ,'ok'

    if current_user_designation_name == "Purchase Head":
        print("*****If Purchase Head current user desgination*****", current_user_designation_name)
        frappe.db.sql(""" UPDATE `tabVendor Master` set purchase_head_approval='Approved' where office_email_primary=%s """,(vendor_email) )
        frappe.db.commit()
        frappe.db.sql(""" UPDATE `tabVendor Master` SET approved_by_purchase_head = %s WHERE name = %s """, (current_user_name, name))
        frappe.db.commit()
        frappe.db.sql(""" UPDATE `tabVendor Onboarding` set purchase_h_approval='Approved' where office_email_primary=%s """,(vendor_email))
        frappe.db.commit()
        registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')
        vendor_code = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['vendor_code'])
        print("***Purchase Head desgination PT Email***",registered_by_email)
        send_email_on_purchase_head_approval(name)
        print("**************",name)
        return 200 ,'ok'

@frappe.whitelist()
def send_email_on_purchase_team_approval(name):
    frappe.logger("api").exception("+++")
    email_id = frappe.session.user

    # purchase_head_key = frappe.db.get_value("Designation Master", filters={'designation_name': "Purchase Head"}, fieldname='name')
    # purchase_head_emails = frappe.db.get_all("User", filters={'designation': purchase_head_key}, fields=['email'])
    # account_team_key = frappe.db.get_value("Designation Master", filters={'designation_name': "Account Team"}, fieldname='name')
    # account_team_emails = frappe.db.get_all("User", filters={'designation': account_team_key}, fields=['email'])

    teamname = frappe.db.get_all("User", filters={'email': email }, fieldname=['team'])
    purchase_head_email = frappe.db.get_all("Team Master", filters={'name': teamname}, fields=['reporting_head'])
    
    print("Purchase Head Email from Team Master--->",purchase_head_email)
    vendor_detail = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['vendor_code', 'vendor_name','office_email_primary','registered_by'])
    vendor_company = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['company_name'])
    register_name = frappe.db.get_value("User", filters={'email':vendor_detail[3]}, fieldname=['full_name'])
    print(f"Vendor Detail: {vendor_detail}")  # Add this line to see what you get
    purchase_org = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_organization'])
    purchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name':purchase_org}, fieldname=['purchase_organization_name'])
    email = vendor_detail[2] if vendor_detail and len(vendor_detail) > 2 else None
    vendor_onboarding_details = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['first_name', 'last_name', 'state', 'city', 'district', 'country', 'pincode', 'telephone_number', 'address_line_2', 'vendor_type', 'size_of_company', 'company_name','purchase_team_remarks'])
    # purchase_team_remarks = vendor_onboarding_details[12]
    purchase_team_approval = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_team_approval'])
    # vertical = frappe.db.get_value("Company Master", filters={'name': vendor_onboarding_details[11]}, fieldname=['company_name'])
    vendor_type = frappe.db.get_value("Vendor Type Master", filters={'name': vendor_onboarding_details[9]}, fieldname=['vendor_type_name'])
    city = frappe.db.get_value("City Master", filters={'name': vendor_onboarding_details[3]}, fieldname=['city_name'])
    district = frappe.db.get_value("District Master", filters={'name': vendor_onboarding_details[4]}, fieldname=['district_name'])
    state = frappe.db.get_value("State Master", filters={'name': vendor_onboarding_details[2]}, fieldname=['state_name'])
    country = frappe.db.get_value("Country Master", filters={'name': vendor_onboarding_details[5]}, fieldname=['country_name'])
    pincode = frappe.db.get_value("Pincode Master", filters={'name': vendor_onboarding_details[6]}, fieldname=['pincode'])

    multiple_company_data = frappe.db.get_all("Multiple Company Data", filters={'parent': name}, fields=['company_name_mt'])

    company_codes = []
    company_names = []

    for company in multiple_company_data:
        company_name_mt = company['company_name_mt']
        company_code = frappe.db.get_value("Company Master", filters={'company_name': company_name_mt}, fieldname=['company_code'])

        if company_code:
            company_codes.append(company_code)
        if company_name_mt:
            company_names.append(company_name_mt)

    if not multiple_company_data:
        company_code = vendor_company
        company_name = frappe.db.get_value("Company Master", filters={'name': vendor_company}, fieldname=['company_name'])

        if company_code:
            company_codes.append(company_code)
        if company_name:
            company_names.append(company_name)

    company_codes_str = ", ".join(company_codes)
    company_names_str = ", ".join(company_names)

    print(f"Company Codes of PT: {company_codes_str}")
    print(f"Company Names of PT: {company_names_str}")

    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    server_url = conf.get("server_url")
    from_address = email_id
    # to_addresses = ", ".join([email['email'] for email in purchase_head_emails])
    to_addresses = purchase_head_email
    bcc_address = "rishi.hingad@merillife.com"

    subject = f"""Request for Appointment of New Vendor for {company_names_str}."""

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vendor Details</title>
    </head>
    <body>
        <h2>Vendor Details Table</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tbody>
                 <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Purchase Team Approval</td>
                    <td style="border: 1px solid black; padding: 8px;" colspan="3">{purchase_team_approval}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Registered By:</td>
                    <td style="border: 1px solid black; padding: 8px;" >{register_name}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Vendor Name</td>
                    <td style="border: 1px solid black; padding: 8px;">{vendor_detail[1]}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Company Code:</td>
                    <td style="border: 1px solid black; padding: 8px;" >{company_codes_str}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Company Name:</td>
                    <td style="border: 1px solid black; padding: 8px;">{company_names_str}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Purchase Organisation</td>
                    <td style="border: 1px solid black; padding: 8px;" colspan="3">{purchase_org} - {purchase_org_name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">City</td>
                    <td style="border: 1px solid black; padding: 8px;" >{city}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">District</td>
                    <td style="border: 1px solid black; padding: 8px;">{district}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">State</td>
                    <td style="border: 1px solid black; padding: 8px;" >{state}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Country</td>
                    <td style="border: 1px solid black; padding: 8px;">{country}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Pincode</td>
                    <td style="border: 1px solid black; padding: 8px;" >{pincode}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Vendor Type</td>
                    <td style="border: 1px solid black; padding: 8px;">{vendor_type}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Contact Person</td>
                    <td style="border: 1px solid black; padding: 8px;" >{vendor_onboarding_details[0]}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Contact Number</td>
                    <td style="border: 1px solid black; padding: 8px;">{vendor_onboarding_details[7]}</td>
                </tr>
                
            </tbody>
        </table>
    </body>
    </html>
    """

    purchase_head_link = f"""{server_url}/vendor-details/{email}&{company_codes_str}"""

    def send_email_and_log(to_addresses, purchase_head_link, category):
        body = f"""
        Dear Sir,<br>

        Greetings for the Day!<br>

        There is a request for appointment of new Vendor for {company_names_str}.<br>
        {html_body}<br>

        <p>For further details, please use the following link:<br />
            <a href="{purchase_head_link}">Click Here.</a>
        </p>
        """
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_addresses
        msg["Subject"] = subject
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_addresses,bcc_address], msg.as_string())
                print(f"Email sent successfully!")
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': name,
                    'to_email': to_addresses,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Purchase Team Approval - " + category,
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email: {e}")
            msge = f"Failed to send email: {e}"
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': name,
                'to_email': to_addresses,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "Purchase Team Approval - " + category,
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

    send_email_and_log(to_addresses, purchase_head_link, "Purchase Head")
    # send_email_and_log([d.email for d in account_team_emails], account_team_link, "Account Team")

    return to_addresses


@frappe.whitelist()
def send_email_on_purchase_head_approval(name):
    email_id = frappe.session.user
    # purchase_head_key = frappe.db.get_value("Designation Master", filters={'designation_name': "Purchase Head"}, fieldname='name')
    # purchase_head_emails = frappe.db.get_all("User", filters={'designation': purchase_head_key}, fields=['email'])

    vendor_detail = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['vendor_code', 'vendor_name','office_email_primary','registered_by'])
    register_name = frappe.db.get_value("User", filters={'email':vendor_detail[3]}, fieldname=['full_name'])
    register_email = vendor_detail[3]

    print(f"Vendor Detail: {vendor_detail}")  # Add this line to see what you get
    purchase_org = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_organization'])
    purchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name':purchase_org}, fieldname=['purchase_organization_name'])
    email = vendor_detail[2] if vendor_detail and len(vendor_detail) > 2 else None
    vendor_onboarding_details = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['first_name', 'last_name', 'state', 'city', 'district', 'country', 'pincode', 'address_line_1', 'address_line_2', 'vendor_type', 'size_of_company', 'company_name','purchase_team_remarks','purchase_head_remark'])
    purchase_team_remarks = vendor_onboarding_details[12]
    purchase_head_remarks = vendor_onboarding_details[13]
    vendor_company = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['company_name'])
    purchase_team_approval = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_team_approval'])
    purchase_head_approval = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_head_approval'])
    # vertical = frappe.db.get_value("Company Master", filters={'name': vendor_onboarding_details[11]}, fieldname=['company_name'])
    vendor_type = frappe.db.get_value("Vendor Type Master", filters={'name': vendor_onboarding_details[9]}, fieldname=['vendor_type_name'])

    city = frappe.db.get_value("City Master", filters={'name': vendor_onboarding_details[3]}, fieldname=['city_name'])
    district = frappe.db.get_value("District Master", filters={'name': vendor_onboarding_details[4]}, fieldname=['district_name'])
    state = frappe.db.get_value("State Master", filters={'name': vendor_onboarding_details[2]}, fieldname=['state_name'])
    country = frappe.db.get_value("Country Master", filters={'name': vendor_onboarding_details[5]}, fieldname=['country_name'])
    pincode = frappe.db.get_value("Pincode Master", filters={'name': vendor_onboarding_details[6]}, fieldname=['pincode'])

    multiple_company_data = frappe.db.get_all("Multiple Company Data", filters={'parent': name}, fields=['company_name_mt'])

    company_codes = []
    company_names = []

    for company in multiple_company_data:
        company_name_mt = company['company_name_mt']
        company_code = frappe.db.get_value("Company Master", filters={'company_name': company_name_mt}, fieldname=['company_code'])

        if company_code:
            company_codes.append(company_code)
        if company_name_mt:
            company_names.append(company_name_mt)

    if not multiple_company_data:
        company_code = vendor_company
        company_name = frappe.db.get_value("Company Master", filters={'name': vendor_company}, fieldname=['company_name'])

        if company_code:
            company_codes.append(company_code)
        if company_name:
            company_names.append(company_name)


    company_codes_str = ", ".join(company_codes)
    company_names_str = ", ".join(company_names)

    print(f"Company Codes of PH: {company_codes_str}")
    print(f"Company Names of PH: {company_names_str}")

    # account_team_key = frappe.db.get_value("Designation Master", filters={'designation_name': "Account Team"}, fieldname='name')
    # account_team_emails = frappe.db.get_all("User", filters={'designation': account_team_key}, fields=['email'])

    for company_code, company_name in zip(company_codes, company_names):
        print(f"Looking for users with company_name: {company_name} and designation: Account Team")

    account_team_users = frappe.db.get_list("User", filters={"user_company": company_code, "designation": "Account Team"}, fields=["email"])
    print(f"Filter account team users---> {account_team_users}")
    account_team_emails = [user['email'] for user in account_team_users] if account_team_users else []
    print(f"Account Team Emails for {company_name} (Code: {company_code}): {account_team_emails}")

    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    server_url = conf.get("server_url")
    from_address = email_id
    # to_addresses = ", ".join([email['email'] for email in account_team_emails])
    to_addresses = account_team_emails
    cc_addresses = register_email
    bcc_address = "rishi.hingad@merillife.com"

    subject = f"""Request for Appointment of New Vendor for {company_names_str}."""

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vendor Details</title>
    </head>
    <body>
        <h2>Vendor Details Table</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tbody>
                 <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Purchase Team Approval</td>
                    <td style="border: 1px solid black; padding: 8px;" colspan="3">{purchase_team_approval}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Purchase Head Approval</td>
                    <td style="border: 1px solid black; padding: 8px;" colspan="3">{purchase_head_approval}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Registered By</td>
                    <td style="border: 1px solid black; padding: 8px;" >{register_name}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Vendor Name</td>
                    <td style="border: 1px solid black; padding: 8px;">{vendor_detail[1]}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Company Code:</td>
                    <td style="border: 1px solid black; padding: 8px;" >{company_codes_str}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Company Name:</td>
                    <td style="border: 1px solid black; padding: 8px;">{company_names_str}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Purchase Organisation</td>
                    <td style="border: 1px solid black; padding: 8px;" colspan="3">{purchase_org} - {purchase_org_name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">City</td>
                    <td style="border: 1px solid black; padding: 8px;" >{city}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">District</td>
                    <td style="border: 1px solid black; padding: 8px;">{district}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">State</td>
                    <td style="border: 1px solid black; padding: 8px;" >{state}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Country</td>
                    <td style="border: 1px solid black; padding: 8px;">{country}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Pincode</td>
                    <td style="border: 1px solid black; padding: 8px;" >{pincode}</td>
                    <<td style="border: 1px solid black; padding: 8px;" width="100px">Vendor Type</td>
                    <td style="border: 1px solid black; padding: 8px;">{vendor_type}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Contact Person</td>
                    <td style="border: 1px solid black; padding: 8px;" >{vendor_onboarding_details[0]}</td>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Contact Number</td>
                    <td style="border: 1px solid black; padding: 8px;">{vendor_onboarding_details[7]}</td>
                </tr>
                
            </tbody>
        </table>
    </body>
    </html>
    """

    account_team_link = f"""{server_url}/account-team/vendor-detail/{email}&{company_code}"""

    def send_email_and_log(to_addresses, cc_addresses, account_team_link):
        body = f"""
        Dear Sir,<br>

        Greetings for the Day!<br>

        There is a request for appointment of new Vendor for {company_name}.<br>
        {html_body}<br>

        <p>For further details, please use the following link:<br />
            <a href="{account_team_link}">Click Here.</a>
        </p>
        """
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_addresses
        msg["Subject"] = subject
        msg["CC"] = cc_addresses
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_addresses,bcc_address], msg.as_string())
                print(f"Email sent successfully!")
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': name,
                    'to_email': to_addresses,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Purchase Head Approval - ",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email: {e}")
            msge = f"Failed to send email: {e}"
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': name,
                'to_email': to_addresses,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "Purchase Head Approval - ",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

    # send_email_and_log([d.email for d in purchase_head_emails], purchase_head_link, "Purchase Head")
    send_email_and_log(", ".join(to_addresses) if isinstance(to_addresses, list) else to_addresses, cc_addresses, account_team_link)

    return to_addresses


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
        url = f'http://10.120.140.7/api/resource/User/{email}'
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
            ) """,(rfq_number, vendor_code, rfq_number, vendor_code),as_dict=1)
    quotation = quotation[0]
    product_code = frappe.db.get_value("Product Master", filters={"name": quotation.product_code}, fieldname="product_code")
    quotation["product_code"] = product_code
    company_name = frappe.db.get_value("Company Master", filters={"name": quotation.company_name}, fieldname="company_name")
    quotation["company_name"] = company_name
    product_category_name = frappe.db.get_value("Product Category Master", filters={"name": quotation.product_category}, fieldname="product_category_name")
    quotation["product_category"] = product_category_name
    material_code = frappe.db.get_value("Old Material Master", filters={"name": quotation.material_code}, fieldname="material_code")
    quotation["material_code"] = material_code
    material_category_name = frappe.db.get_value("Material Category Master", filters={"name": quotation.material_category}, fieldname="material_category_name")
    quotation["material_category"] = material_category_name
    material_name = frappe.db.get_value("Old Material Master", filters={"name": quotation.material_name}, fieldname="material_name")
    quotation["material_name"] = material_name
    return quotation


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

        material_code = frappe.db.get_value("Old Material Master", filters={"name": quotation.material_code}, fieldname="material_code")
        quotation["material_code"] = material_code

        material_category_name = frappe.db.get_value("Material Category Master", filters={"name": quotation.material_category}, fieldname="material_category_name")
        quotation["material_category"] = material_category_name

        material_name = frappe.db.get_value("Old Material Master", filters={"name": quotation.material_name}, fieldname="material_name")
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

        material_code = frappe.db.get_value("Old Material Master", filters={"name": quotation.material_code}, fieldname="material_code")
        quotation["material_code"] = material_code

        material_category_name = frappe.db.get_value("Material Category Master", filters={"name": quotation.material_category}, fieldname="material_category_name")
        quotation["material_category"] = material_category_name

        material_name = frappe.db.get_value("Old Material Master", filters={"name": quotation.material_name}, fieldname="material_name")
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
def total_vendors_team():
    total_vendors = frappe.db.sql("""
        SELECT 
            ud.team, 
            COUNT(vm.name) AS total_vendors 
        FROM 
            `tabVendor Master` vm
        LEFT JOIN 
            `tabUser` ud ON vm.registered_by = ud.name
        GROUP BY ud.team
    """, as_dict=True)

    return total_vendors


@frappe.whitelist()
def total_in_process_vendors_team():
    total_in_process_vendors = frappe.db.sql("""
        SELECT 
            ud.team, 
            COUNT(vm.name) AS total_in_process_vendors
        FROM 
            `tabVendor Master` vm
        LEFT JOIN 
            `tabUser` ud ON vm.registered_by = ud.name
        WHERE 
            vm.status = 'In Process'
        GROUP BY 
            ud.team
    """, as_dict=True)

    return total_in_process_vendors

@frappe.whitelist()
def total_in_process_vendors():
    
    total_in_process_vendors = frappe.db.sql(""" select count(*) from `tabVendor Master` where status='In Process' """,as_dict=1)
    return total_in_process_vendors

@frappe.whitelist()
def inprocess_vendor_detail():
    
    inprocess_vendor_detail = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.status AS status,
            vm.onboarding_form_status AS onboarding_form_status,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.office_email_primary AS office_email_primary,
            vm.vendor_name AS vendor_name,
            cm.company_name AS company_name,
            cm.company_code AS company_code,
            vm.name AS ref_no,
            vm.registered_by AS registered_by,
            u.full_name AS registered_by_name
        FROM 
            "tabVendor Master" vm 
        LEFT JOIN 
            "tabCompany Master" cm ON vm.company_name = cm.name
        LEFT JOIN 
            "tabUser" u ON vm.registered_by = u.name
        WHERE 
            status='In Process' """,as_dict=1)
    
    for vendor in inprocess_vendor_detail:
        multiple_company_data = frappe.db.sql("""
            SELECT 
                mcd.company_name_mt, 
                cm.company_name
            FROM 
                "tabMultiple Company Data" mcd 
            LEFT JOIN 
                "tabCompany Master" cm ON mcd.company_name_mt = cm.name
            WHERE 
                mcd.parent = %s
        """, (vendor['name'],), as_dict=1)

        vendor_types = frappe.db.sql("""
            SELECT
                vt.vendor_type       
            FROM
                "tabVendor Type Group" vt
            WHERE
                vt.parent = %s
        """, (vendor['name'],), as_dict=1)
        
        vendor['multiple_company_data'] = multiple_company_data
        vendor['vendor_types'] = vendor_types

    return inprocess_vendor_detail

@frappe.whitelist()
def inprocess_vendor_detail_team():
    inprocess_vendor_detail = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.status AS status,
            vm.onboarding_form_status AS onboarding_form_status,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.office_email_primary AS office_email_primary,
            vm.vendor_name AS vendor_name,
            cm.company_name AS company_name,
            cm.company_code AS company_code,
            vm.name AS ref_no,
            vm.registered_by AS registered_by,
            ud.team AS team,
            u.full_name AS registered_by_name
        FROM 
            `tabVendor Master` vm 
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name
        LEFT JOIN 
            `tabUser` ud ON vm.registered_by = ud.name
        LEFT JOIN 
            "tabUser" u ON vm.registered_by = u.name
        WHERE 
            vm.status = 'In Process'
    """, as_dict=1)
    
    vendor_data = []
    for vendor in inprocess_vendor_detail:
        multiple_company_data = frappe.db.sql("""
            SELECT 
                mcd.company_name_mt, 
                cm.company_name
            FROM 
                `tabMultiple Company Data` mcd 
            LEFT JOIN 
                `tabCompany Master` cm ON mcd.company_name_mt = cm.name
            WHERE 
                mcd.parent = %s
        """, (vendor['name'],), as_dict=1)

        vendor_types = frappe.db.sql("""
            SELECT
                vt.vendor_type       
            FROM
                `tabVendor Type Group` vt
            WHERE
                vt.parent = %s
        """, (vendor['name'],), as_dict=1)
        
        vendor_data.append({
            "team": vendor.get("team") or "Unassigned",
            "vendor_details": {
                "name": vendor["name"],
                "status": vendor["status"],
                "onboarding_form_status": vendor["onboarding_form_status"],
                "purchase_team_approval": vendor["purchase_team_approval"],
                "purchase_head_approval": vendor["purchase_head_approval"],
                "accounts_team_approval": vendor["accounts_team_approval"],
                "office_email_primary": vendor["office_email_primary"],
                "vendor_name": vendor["vendor_name"],
                "company_name": vendor["company_name"],
                "company_code": vendor["company_code"],
                "ref_no": vendor["ref_no"],
                "registered_by": vendor["registered_by"],
                "registered_by_name": vendor["registered_by_name"],
                "multiple_company_data": multiple_company_data,
                "vendor_types": vendor_types,
            }
        })

    grouped_vendors = {}
    for entry in vendor_data:
        team = entry["team"]
        if team not in grouped_vendors:
            grouped_vendors[team] = []
        grouped_vendors[team].append(entry["vendor_details"])

    return [{"team": team, "vendors": vendors} for team, vendors in grouped_vendors.items()]


@frappe.whitelist()
def inprocess_vendor_detail_qa():
    
    inprocess_vendor_detail_qa = frappe.db.sql(""" 
        SELECT
            vm.*,
            cmm.company_name as company_name,
            cmm.company_code AS company_code
                                             
    FROM
        `tabVendor Master` vm
    LEFT JOIN
        `tabCompany Master` cmm on vm.company_name = cmm.name
    WHERE 
        status='In Process'
        AND cmm.company_code IN ('2000', '7000')
     """,as_dict=1)
    return inprocess_vendor_detail_qa


@frappe.whitelist()
def total_onboarded_vendors():

    total_in_process_vendors = frappe.db.sql(""" select count(*) from `tabVendor Master` where status='Onboarded' """,as_dict=1)
    return total_in_process_vendors

@frappe.whitelist()
def total_onboarded_vendors_team():
    total_onboarded_vendors = frappe.db.sql("""
        SELECT 
            ud.team, 
            COUNT(vm.name) AS total_onboarded_vendors 
        FROM 
            `tabVendor Master` vm
        LEFT JOIN 
            `tabUser` ud ON vm.registered_by = ud.name
        WHERE 
            vm.status = 'Onboarded'
        GROUP BY 
            ud.team
    """, as_dict=True)

    return total_onboarded_vendors


@frappe.whitelist()
def total_rfq():

    total_rfq = frappe.db.sql(""" select count(*) from `tabRequest For Quotation` """, as_dict=1)
    return total_rfq


# @frappe.whitelist()
# def total_number_of_quotation():

#     count = frappe.db.sql(""" select count(*) from `tabQuotation` """,as_dict=1)
#     return count

@frappe.whitelist()
def total_number_of_quotation(vendor_code):
    count = frappe.db.sql("""
        SELECT COUNT(*)
        FROM `tabQuotation`
        WHERE vendor_code = %s
        """, (vendor_code,), as_dict=1)
    return count

@frappe.whitelist()
def total_number_of_quotation_by_rfq():
    count = frappe.db.sql("""
        SELECT rfq_number, COUNT(*) AS quotation_count
        FROM `tabQuotation`
        GROUP BY rfq_number
    """, as_dict=True)
    return count

@frappe.whitelist()
def total_vendors_registerd_in_month():

    current_month = datetime.now.strftime("%B")
    current_year = datetime.now.year
    return current_month, current_year

@frappe.whitelist()
def all_rfq_detail():
    #  RFQ details
    all_rfq = frappe.db.sql("""  
        SELECT 
            rfq.*,
            rtm.rfq_name AS rfq_name,
            mm.material_name,
            cmm.company_name AS company_name
                            
        FROM 
            `tabRequest For Quotation` rfq
        LEFT JOIN
            `tabRFQ Type Master` rtm ON rfq.rfq_type = rtm.name
        LEFT JOIN
            `tabOld Material Master` mm ON rfq.material = mm.name
        LEFT JOIN
            `tabCompany Master` cmm ON rfq.company_code = cmm.name
    """, as_dict=1)

    quotation_counts = frappe.db.sql("""
        SELECT rfq_number, COUNT(*) AS quotation_count
        FROM `tabQuotation`
        GROUP BY rfq_number
    """, as_dict=True)

    quotation_count_map = {item['rfq_number']: item['quotation_count'] for item in quotation_counts}

    for rfq in all_rfq:
        rfq['total_quotation'] = quotation_count_map.get(rfq['name'], 0)

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
def show_all_payment_request():
    records = frappe.db.sql("""
        SELECT 
            pr.*, 
            cm.currency_name AS currency_name,
            top.company_code AS company_code,
            cmp.company_name AS company_name,
            vm.vendor_name AS vendor_name,
            vm.registered_by AS registered_by                       
                            
        FROM 
            `tabPayment Request` pr
        LEFT JOIN 
            `tabCurrency Master` cm ON pr.currency = cm.name
        LEFT JOIN
            `tabTerms Of Payment Master` top ON pr.terms_of_payment = top.name
        LEFT JOIN
            `tabCompany Master` cmp ON top.company_code = cmp.company_code
        LEFT JOIN
            `tabVendor Master` vm ON pr.vendor_code = vm.vendor_code
                            
    """, as_dict=1)

    count = len(records)

    return {
        "records": records,
        "count": count
    }


@frappe.whitelist()
def show_payment_request(**kwargs):

    po_no = kwargs.get('po_number')
    record = frappe.db.sql("""
        SELECT 
            pr.*, 
            cm.currency_name AS currency_name
        FROM 
            `tabPayment Request` pr
        LEFT JOIN 
            `tabCurrency Master` cm 
        ON 
            pr.currency = cm.name
        WHERE 
            pr.po_number=%s
    """, (po_no,), as_dict=1)
    return record


@frappe.whitelist()
def show_payment_request_vendor(**kwargs):

    vendor_code = kwargs.get('vendor_code')
    record = frappe.db.sql("""
        SELECT 
            pr.*, 
            cm.currency_name AS currency_name,
            po.bill_to_company AS bill_to_company
                           
        FROM 
            `tabPayment Request` pr
        LEFT JOIN 
            `tabCurrency Master` cm ON pr.currency = cm.name
        LEFT JOIN 
            `tabPurchase Order` po ON pr.po_number = po.name
        WHERE 
            pr.vendor_code=%s
        ORDER BY 
            pr.creation DESC
    """, (vendor_code), as_dict=1)
    return record

@frappe.whitelist()
def show_all_payment_requisition_details():
    query = """
        SELECT 
            pr.*,
            cm.company_name AS company_name
            
        FROM 
            `tabPayment Requisition` pr
        LEFT JOIN
            `tabCompany Master` cm ON pr.company = cm.name
        
        ORDER BY 
            pr.creation DESC
    """
    
    records = frappe.db.sql(query, as_dict=True)
    
    count = len(records)
    
    return {
        "records": records,
        "count": count
    }


@frappe.whitelist()
def get_dispatch_items_by_vendor(vendor_code):
    if not vendor_code:
        frappe.throw("Vendor code is required")

    dispatch_items = frappe.get_all(
        "Dispatch Item",
        filters={"vendor_code": vendor_code},
        fields=["*"]
    )

    if not dispatch_items:
        return []

    for item in dispatch_items:
        item["items"] = frappe.get_all(
            "Dispatch Order Items",
            filters={"parent": item.get("name")},
            fields="*"
        )

        purchase_no_group = frappe.get_all(
            "Dispatch Purchase No Group",
            filters={"parent": item.get("name")},
            fields=["purchase_number"]
        )

        item["purchase_numbers"] = [
            frappe.get_doc("Purchase Order", row["purchase_number"])
            for row in purchase_no_group if row.get("purchase_number")
        ]

    return dispatch_items

@frappe.whitelist()
def get_payment_request_details_by_po_invoice_number(**kwargs):
    print("Request Args:", frappe.local.request.args)

    po_number = frappe.local.request.args.get('po_number')
    invoice_number = frappe.local.request.args.get('invoice_number', None)

    print("po_number------->", po_number, invoice_number)

    if not po_number:
        frappe.throw("Purchase Order number is required")

    print(f"Received po_number: {po_number}")
    if invoice_number:
        print(f"Received invoice_number: {invoice_number}")

    filters = {"po_number": po_number}
    if invoice_number:
        filters["invoice_number"] = invoice_number
        
    print(f"Combined Filters: {filters}")

    payment_requests = frappe.get_all("Payment Request", filters=filters, fields=["*"])

    print(f"Payment requests fetched: {payment_requests}")

    if not payment_requests:
        print("No payment requests found.")
        return []

    for request in payment_requests:
        if request.get("po_number"):
            print(f"Fetching Purchase Order details for: {request['po_number']}")
            try:
                request["purchase_order_details"] = frappe.get_doc("Purchase Order", request["po_number"])
            except frappe.DoesNotExistError:
                print(f"No Purchase Order found for po_number: {request['po_number']}")
                request["purchase_order_details"] = None

    print(f"Final enriched payment requests: {payment_requests}")
    return payment_requests


@frappe.whitelist()
def get_grn_details_of_grn_number(grn_number):
    
    if not grn_number:
        frappe.throw("GRN number is required")

    grn = frappe.get_all(
        "GRN",
        filters={"grn_no": grn_number},
        fields=["*"]
    )

    if not grn:
        return []

    for record in grn:
        record["grn_items"] = frappe.get_all(
            "GRN Items",
            filters={"parent": record.get("name")},
            fields=["*"]
        )

    return grn

@frappe.whitelist()
def get_purchase_requisition_details(pr_number):
    if not pr_number:
        frappe.throw("Purchase Requisition number is required")
    purchase_requisition = frappe.get_all(
        "Purchase Requisition",
        filters={"purchase_requisition_number": pr_number},
        fields=["*"]
    )

    if not purchase_requisition:
        return []

    for record in purchase_requisition:
        record["pr_items"] = frappe.get_all(
            "Purchase Requisition Item",
            filters={"parent": record.get("name")},
            fields=["*"]
        )

    return purchase_requisition

@frappe.whitelist()
def get_dispatch_items_by_invoice(invoice_number):
    if not invoice_number:
        frappe.throw("Invoice number is required")

    dispatch_items = frappe.get_all(
        "Dispatch Item",
        filters={"invoice_number": invoice_number},
        fields=["*"]
    )

    if not dispatch_items:
        return []

    for item in dispatch_items:
        item["order_items"] = frappe.get_all(
            "Dispatch Order Items",
            filters={"parent": item.get("name")},
            fields=["*"]
        )

        purchase_no_group = frappe.get_all(
            "Dispatch Purchase No Group",
            filters={"parent": item.get("name")},
            fields=["purchase_number"]
        )

        item["purchase_numbers"] = [
            frappe.get_doc("Purchase Order", row["purchase_number"])
            for row in purchase_no_group if row.get("purchase_number")
        ]

    return dispatch_items

@frappe.whitelist()
def get_all_grn_details():
    try:
        print("Fetching all GRN records...")
        grn_list = frappe.get_all(
            "GRN",
            fields="*",
            filters={},
        )
        print(f"Fetched GRN records: {len(grn_list)}")

        for grn in grn_list:
            print(f"Fetching child items for GRN: {grn['name']}")
            grn_items = frappe.get_all(
                "GRN Items",
                fields="*",
                filters={"parent": grn["name"]},
            )
            print(f"Fetched {len(grn_items)} items for GRN: {grn['name']}")
            grn["grn_items"] = grn_items

        if grn_items:
                po_number = grn_items[0].get("po_no")
                if po_number:
                    print(f"Fetching Purchase Order details for PO No.: {po_number}")
                    purchase_order = frappe.get_doc("Purchase Order", po_number)

                    purchase_group = purchase_order.get("purchase_group")
                    if purchase_group:
                        print(f"Fetching Purchase Group details for: {purchase_group}")
                        purchase_group_doc = frappe.get_doc("Purchase Group Master", purchase_group)

                        team_value = purchase_group_doc.get("team")
                        print(f"Team value fetched for Purchase Group {purchase_group}: {team_value}")

                        grn["team"] = team_value

        print("Completed fetching all GRN details.")
        return grn_list

    except Exception as e:
        error_message = str(e)
        print(f"Error occurred: {error_message}")
        frappe.log_error(message=error_message, title="Error in fetching GRN details")
        frappe.throw(_("An error occurred while fetching GRN details. Please check the logs for more details."))


@frappe.whitelist()
def get_all_purchase_requisition_details():
    try:
        print("Fetching all Purchase Requisition records...")
        pr_list = frappe.get_all(
            "Purchase Requisition",
            fields="*",
            filters={},
        )
        print(f"Fetched Purchase Requisition records: {len(pr_list)}")

        for pr in pr_list:
            print(f"Fetching child items for Purchase Requisition: {pr['name']}")
            pr_items = frappe.get_all(
                "Purchase Requisition Item",
                fields="*",
                filters={"parent": pr["name"]},
            )
            print(f"Fetched {len(pr_items)} items for Purchase Requisition: {pr['name']}")
            pr["pr_items"] = pr_items

            if pr_items:
                first_item = pr_items[0]
                purchase_group = first_item.get("purchase_group")
                
                if purchase_group:
                    print(f"Fetching Purchase Group details for: {purchase_group}")
                    purchase_group_doc = frappe.get_doc("Purchase Group Master", purchase_group)

                    team_value = purchase_group_doc.get("team")
                    print(f"Team value fetched for Purchase Group {purchase_group}: {team_value}")

                    pr["team"] = team_value

        print("Completed fetching all Purchase Requisition details.")
        return pr_list

    except Exception as e:
        error_message = str(e)
        print(f"Error occurred: {error_message}")
        frappe.log_error(message=error_message, title="Error in fetching Purchase Requisition details")
        frappe.throw(_("An error occurred while fetching Purchase Requisition details. Please check the logs for more details."))

@frappe.whitelist()
def send_email_on_payment_request(data, method):
    vendor_code = data.get('vendor_code')
    receiver_email = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=['registered_by'])
    vendor_name = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=['vendor_name'])
    from_add = frappe.db.get_value("Vendor Master", filters={'vendor_code': vendor_code}, fieldname=['office_email_primary'])
    
    payment_request = frappe.db.get_all("Payment Request", filters={'vendor_code': vendor_code}, fields=['*'], order_by="modified desc")

    if payment_request:
        latest_pr = payment_request[0]

        purchase_number = latest_pr.get('po_number')
        request_type = latest_pr.get('request_type')

        if request_type == "Normal":
            invoice_number = latest_pr.get('invoice_number')
            invoice_amount = latest_pr.get('invoice_amount')
            terms_of_payment = latest_pr.get('terms_of_payment')
            invoice_date = latest_pr.get('invoice_date')

            accounts_team_emails = [email[0] for email in frappe.db.sql("SELECT email FROM `tabUser` WHERE designation='Account Team'")]

            recipient_emails = receiver_email + accounts_team_emails

            html_body = f"""
                <table style="border-collapse: collapse; width: 100%;">
                    <tr class="header-table" style="border: 1px solid black;">
                        <td style="border: 1px solid black; padding: 8px;">Invoice Number</td>
                        <td style="border: 1px solid black; padding: 8px;">{invoice_number}</td>
                    </tr>
                    <tr class="header-table" style="border: 1px solid black;">
                        <td style="border: 1px solid black; padding: 8px;">Invoice Amount</td>
                        <td style="border: 1px solid black; padding: 8px;">{invoice_amount}</td>
                    </tr>
                    <tr class="header-table" style="border: 1px solid black;">
                        <td style="border: 1px solid black; padding: 8px;">Terms of Payment</td>
                        <td style="border: 1px solid black; padding: 8px;">{terms_of_payment}</td>
                    </tr>
                    <tr class="header-table" style="border: 1px solid black;">
                        <td style="border: 1px solid black; padding: 8px;">Invoice Date</td>
                        <td style="border: 1px solid black; padding: 8px;">{invoice_date}</td>
                    </tr>
                </table>
            """
        elif request_type == "Advance":
            proforma_invoice_number = latest_pr.get('proforma_invoice_number')
            proforma_invoice_amount = latest_pr.get('proforma_invoice_amount')
            terms_of_payment = latest_pr.get('terms_of_payment')
            proforma_invoice_date = latest_pr.get('proforma_invoice_date')

            html_body = f"""
                <table style="border-collapse: collapse; width: 100%;">
                    <tr class="header-table" style="border: 1px solid black;">
                        <td style="border: 1px solid black; padding: 8px;">Terms of Payment</td>
                        <td style="border: 1px solid black; padding: 8px;">{terms_of_payment}</td>
                    </tr>
                    <tr class="header-table" style="border: 1px solid black;">
                        <td style="border: 1px solid black; padding: 8px;">Proforma Invoice Number</td>
                        <td style="border: 1px solid black; padding: 8px;">{proforma_invoice_number}</td>
                    </tr>
                    <tr class="header-table" style="border: 1px solid black;">
                        <td style="border: 1px solid black; padding: 8px;">Proforma Invoice Amount</td>
                        <td style="border: 1px solid black; padding: 8px;">{proforma_invoice_amount}</td>
                    </tr>
                    <tr class="header-table" style="border: 1px solid black;">
                        <td style="border: 1px solid black; padding: 8px;">Proforma Invoice Date</td>
                        <td style="border: 1px solid black; padding: 8px;">{proforma_invoice_date}</td>
                    </tr>
                </table>
            """
        else:
            html_body = "<p>No relevant request type found.</p>"
        
        recipient_emails = receiver_email
        print("***** Tuple of Purchase Team Email*****",recipient_emails)

    else:
        html_body = "<p>No payment requisition found for this vendor.</p>"
        recipient_emails = []

    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    from_address = "noreply@merillife.com"
    bcc_address = "rishi.hingad@merillife.com"
    subject = f"Request for Payment from Vendor {vendor_name}"

    body = f"""
    Dear Team,<br/>
    <br/>
    {vendor_name} has requested for payment against Purchase Number: {purchase_number}.<br/>
    Below are the details:
    {html_body}<br/>
    
    Regards
    """

    for to_address in recipient_emails:
        # to_address = recipient_emails
        # to_address = receiver_email
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
                print(f"Email sent successfully to {to_address}!")

                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Send Payment Request Email",
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()
        except Exception as e:
            msge = f"Failed to send email to {to_address}: {e}"
            print(msge)
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "Send Payment Request Email",
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

    print("*************************", recipient_emails)

@frappe.whitelist()
def send_email_payment_requisition(data, method):
    """
    Function to handle email notifications for payment requisitions based on user designation.
    """
    try:
        current_user = frappe.session.user
        current_user_designation_key = frappe.db.get_value("User", {"email": current_user}, "designation")
        current_user_name = frappe.db.get_value("User", {"email": current_user}, "full_name")
        designation_name = frappe.db.get_value("Designation Master", {"name": current_user_designation_key}, "designation_name")
        
        vendor_code = data.get('vendor_code')
        if not vendor_code:
            frappe.throw("Vendor code is missing in the request data.")
        
        vendor_details = frappe.db.get_value("Vendor Master", {"vendor_code": vendor_code}, 
                                             ["registered_by", "vendor_name", "office_email_primary"], as_dict=True)
        
        if not vendor_details:
            frappe.throw(f"No vendor found for vendor code: {vendor_code}")

        receiver_email = vendor_details.registered_by
        vendor_name = vendor_details.vendor_name
        from_add = vendor_details.office_email_primary

        reporting_head = frappe.db.get_value("User", {"email": receiver_email}, "reporting_head")
        reporting_name = frappe.db.get_value("User", {"email": reporting_head}, "full_name") if reporting_head else None

        payment_requisition = frappe.db.get_all(
            "Payment Requisition", 
            filters={"vendor_code": vendor_code}, 
            fields=["*"], 
            order_by="modified desc", 
            limit_page_length=1
        )

        purchase_number = company = favoring_of = currency = amount = "N/A"
        request_type = None
        terms_of_payment = "N/A"

        if payment_requisition:
            latest_pr = payment_requisition[0]
            purchase_number = latest_pr.get("powo_no", "N/A")
            request_type = latest_pr.get("request_type", "N/A")
            invoice_number = latest_pr.get("invoice_no", "N/A")
            terms_key = latest_pr.get("special_remarks")
            terms_of_payment = frappe.db.get_value("Terms Of Payment Master", {"name": terms_key}, "terms_of_payment_name") or "N/A"
            company = latest_pr.get("company", "N/A")
            favoring_of = latest_pr.get("favoring_of", "N/A")
            currency = latest_pr.get("currency", "N/A")
            amount = latest_pr.get("amount", "N/A")

        email_content = generate_email_content(vendor_code, vendor_name, purchase_number, invoice_number, 
                                               currency, amount, company, terms_of_payment)

        if designation_name == "Account Team":
            handle_account_team_email(from_add, vendor_name, email_content, purchase_number)

        elif designation_name == "Purchase Team":
            handle_purchase_team_email(reporting_head, reporting_name, vendor_name, email_content, request_type, purchase_number)

        elif designation_name == "Purchase Head":
            handle_purchase_head_email(vendor_name, email_content)

        else:
            frappe.throw(f"Invalid designation name: {designation_name}")

    except Exception as e:
        frappe.log_error(f"Error in send_email_payment_requisition: {str(e)}", "Email Sending Error")
        frappe.throw(f"An error occurred: {str(e)}")


def generate_email_content(vendor_code, vendor_name, purchase_number, invoice_number, currency, amount, company, terms_of_payment):
    """
    Generate the HTML email content.
    """
    html_body = f"""
    <table>
        <tr><td>Company</td><td>{company}</td></tr>
        <tr><td>DP Request No.</td><td>{purchase_number}</td></tr>
        <tr><td>Terms of Payment</td><td>{terms_of_payment}</td></tr>
        <tr>
            <th>Vendor Code</th>
            <th>Vendor Name</th>
            <th>PO No.</th>
            <th>Proforma Invoice No.</th>
            <th>Currency</th>
            <th>Proforma Amount</th>
        </tr>
        <tr>
            <td>{vendor_code}</td>
            <td>{vendor_name}</td>
            <td>{purchase_number}</td>
            <td>{invoice_number}</td>
            <td>{currency}</td>
            <td>{amount}</td>
        </tr>
    </table>
    """
    return html_body


def handle_account_team_email(from_add, vendor_name, email_content, purchase_number):
    """
    Handle email notifications for the account team.
    """
    subject = f"Down Payment Request - {purchase_number}"
    body = f"""
    Dear {vendor_name},<br/><br/>
    The payment has been processed and released as per the below details:<br/><br/>
    {email_content}<br/><br/>
    Regards,<br/>Account Team
    """
    send_payment_email(from_add, from_add, subject, body)


def handle_purchase_team_email(reporting_head, reporting_name, vendor_name, email_content, request_type, purchase_number):
    """
    Handle email notifications for the purchase team.
    """
    if request_type == "Advance":
        frappe.db.sql("""
        UPDATE `tabPayment Request`
        SET status = 'Pending'
        WHERE po_number = %s
        """, (purchase_number,))
    
    subject = f"Down Payment Request - {purchase_number}"
    body = f"""
    Dear {reporting_name},<br/><br/>
    Advance Down Payment Request has been generated for {vendor_name} as per the below details:<br/><br/>
    {email_content}<br/><br/>
    Kindly Approve the Advance Down Payment Request.<br/>Regards, Team
    """
    send_payment_email(reporting_head, reporting_head, subject, body)


def handle_purchase_head_email(vendor_name, email_content):
    """
    Handle email notifications for the purchase head.
    """
    account_team_emails = frappe.db.sql("""SELECT email FROM `tabUser` WHERE designation = 'Account Team'""", as_list=True)
    for email in account_team_emails:
        subject = "Advance Down Payment Request"
        body = f"""
        Dear Account Team,<br/><br/>
        The Advance Down Payment Request for {vendor_name} has been approved.<br/>
        Please process and release the payment as per the below details:<br/><br/>
        {email_content}<br/><br/>Regards,<br/>Purchase Head
        """
        send_payment_email(email[0], email[0], subject, body)

def send_payment_email(from_address, to_address, subject, body):
    """
    Send email using SMTP.
    """
    try:
        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        bcc_address = "rishi.hingad@merillife.com"
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_address, [to_address,bcc_address], msg.as_string())
        print(f"Email sent successfully to {to_address}!")

    except Exception as e:
        frappe.log_error(f"Failed to send email to {to_address}: {str(e)}", "Email Sending Error")
        raise
# ========================================================================

@frappe.whitelist()
def on_submit_raise_payment_form(doc, method):
    invoice_number = doc.get('invoice_number')
    po_number = doc.get('po_number')

    print(f"Submit - Invoice Number: {invoice_number}, PO Number: {po_number}")
    
    payment_request = None

    if invoice_number:
        payment_request = frappe.get_value("Payment Request", {"invoice_number": invoice_number}, "name")
        print(f"Submit - Payment Request found by invoice_number: {payment_request}")

    if not payment_request and po_number:
        payment_request = frappe.get_value("Payment Request", {"po_number": po_number}, "name")
        print(f"Submit - Payment Request found by po_number: {payment_request}")

    if payment_request:
        print(f"Submit - Updating Payment Request: {payment_request} to Pending")
        update_payment_request_status(payment_request, "Pending")
    else:
        print(f"Submit - No Payment Request found for Invoice: {invoice_number} or PO: {po_number}")


@frappe.whitelist()
def on_approve_raise_payment_form(doc, method):
    invoice_number = doc.get('invoice_number')
    po_number = doc.get('po_number')

    print(f"Approve - Invoice Number: {invoice_number}, PO Number: {po_number}")
    
    payment_request = None

    if invoice_number:
        payment_request = frappe.get_value("Payment Request", {"invoice_number": invoice_number}, "name")
        print(f"Approve - Payment Request found by invoice_number: {payment_request}")

    if not payment_request and po_number:
        payment_request = frappe.get_value("Payment Request", {"po_number": po_number}, "name")
        print(f"Approve - Payment Request found by po_number: {payment_request}")

    if payment_request:
        print(f"Approve - Updating Payment Request: {payment_request} to Approved")
        update_payment_request_status(payment_request, "Approved")
    else:
        print(f"Approve - No Payment Request found for Invoice: {invoice_number} or PO: {po_number}")


@frappe.whitelist()
def on_release_raise_payment_form(doc, method):
    invoice_number = doc.get('invoice_number')
    po_number = doc.get('po_number')

    print(f"Release - Invoice Number: {invoice_number}, PO Number: {po_number}")

    payment_request = None

    if invoice_number:
        payment_request = frappe.get_value("Payment Request", {"invoice_number": invoice_number}, "name")
        print(f"Release - Payment Request found by invoice_number: {payment_request}")

    if not payment_request and po_number:
        payment_request = frappe.get_value("Payment Request", {"po_number": po_number}, "name")
        print(f"Release - Payment Request found by po_number: {payment_request}")

    if payment_request:
        print(f"Release - Updating Payment Request: {payment_request} to Released")
        update_payment_request_status(payment_request, "Released")
    else:
        print(f"Release - No Payment Request found for Invoice: {invoice_number} or PO: {po_number}")

def update_payment_request_status(payment_request_name, status):
    try:
        print(f"Updating Status - Fetching Payment Request Doc: {payment_request_name}")
        payment_request_doc = frappe.get_doc("Payment Request", payment_request_name)
        print(f"Updating Status - Fetched Payment Request Doc: {payment_request_doc.name}")
        
        payment_request_doc.status = status
        payment_request_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        print(f"Updating Status - Payment Request {payment_request_name} status updated to {status}")
    except Exception as e:
        print(f"Error - Updating Payment Request {payment_request_name} to {status}: {str(e)}")

@frappe.whitelist()
def total_number_of_payment_request(vendor_code):
    if not vendor_code:
        return 0

    count_result = frappe.db.sql("""
        SELECT COUNT(*) AS count
        FROM 
            `tabPayment Request`
        WHERE 
            vendor_code = %s
    """, (vendor_code,), as_dict=True)
    
    count = count_result[0]['count'] if count_result else 0

    return count

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
            return values[0]
        else:
            return None
    else:
        values = frappe.db.sql("""
            SELECT rca.*, agm.account_group_name
            FROM `tabReconciliation Account` AS rca
            LEFT JOIN `tabAccount Group Master` AS agm ON rca.account_group = agm.name
        """, as_dict=1)
        
        return values

@frappe.whitelist()
def get_po_field_mappings(docname):
    doctype_name = frappe.db.get_value("SAP Mapper PR", filters={'doctype_name': 'Purchase Order'}, fieldname=['name'])
    print("********doctype_name:", doctype_name)
    mappings = frappe.get_all('SAP Mapper PR Item', filters={'parent': doctype_name}, fields=['sap_field', 'erp_field'])
    print(f"Field Mappings for {docname}: {mappings}")
    return {mapping['sap_field']: mapping['erp_field'] for mapping in mappings}

@frappe.whitelist()
def get_po():
    try:
        data = frappe.request.get_json()
        print(f"Received Data: {data}")
        first_item_lifnr = data['items'][0]['LIFNR']
        vendor_email = frappe.db.get_value("Vendor Master", filters={'vendor_code': first_item_lifnr}, fieldname=['office_email_primary'])
        register_email = frappe.db.get_value("Vendor Master", filters={'vendor_code': first_item_lifnr}, fieldname=['registered_by'])
        print("*********EMAIL*******", vendor_email, first_item_lifnr)

        if data and "items" in data:
            po_no = data.get("po_no", "")
            field_mappings = get_po_field_mappings('SAP Mapper PO')
            print(f"Field Mappings: {field_mappings}")
            if not field_mappings   :
                raise ValueError("No field mappings found for 'SAP Mapper PO'")

            po_doc = frappe.get_doc("Purchase Order", {"po_number": po_no}) if frappe.db.exists("Purchase Order", {"po_number": po_no}) else frappe.new_doc("Purchase Order")
            
            po_doc.po_number = po_no
            po_doc.po_items = []

            meta = frappe.get_meta("Purchase Order")
            if not meta or not meta.fields:
                return {"status": "error", "message": "Meta fields for 'Purchase Order' not found."}

            for item in data["items"]:
                try: 
                    po_item_data = {}
                    for sap_field, erp_field in field_mappings.items():
                        print("-----This SAP Field------",sap_field)
                        print("-----This ERP Field------",erp_field)
                        value = item.get(sap_field, "")
                        field = next((field for field in meta.fields if field.fieldname == erp_field), None)
                        if field and field.fieldtype == 'Date':
                            po_item_data[erp_field] = parse_date(value)
                        else:
                            po_item_data[erp_field] = value
                            
                    po_doc.vendor_code = po_item_data["vendor_code"]
                    po_doc.po_no = po_item_data["po_no"]
                    po_doc.po_date = po_item_data["po_date"]
                    po_doc.delivery_date = po_item_data["delivery_date"]
                    po_doc.total_value_of_po__so = po_item_data["total_gross_amount"]
                    po_doc.company_code = po_item_data["company_code"]

                    print(f"Item Data: {po_item_data}")  
                    print("PO DOC", po_doc.po_items)

                    if not hasattr(po_doc, "po_items"):
                        print("Error: 'po_items' field is not found in the 'Purchase Order' doctype")

                    po_doc.append("po_items", po_item_data)
                except Exception as e :
                    print("---------Error--------",e)
                    return "Error While submitting the PO"
                
            print(f"PO Items Before Save: {po_doc.po_items}")
            print(f"PO Doc Before Save: {po_doc.as_dict()}")


            if po_doc.is_new():
                po_doc.status = "Pending"
                po_doc.insert()
                conf = frappe.conf
                smtp_server = conf.get("smtp_server")
                smtp_port = conf.get("smtp_port")
                smtp_user = conf.get("smtp_user")
                smtp_password = conf.get("smtp_password") 
                from_address = 'noreply@merillife.com'
                to_address = vendor_email
                cc_address = register_email
                bcc_adress = "rishi.hingad@merillife.com"
                subject = f"""Purchase Order Created"""
                body = "body"
                msg = MIMEMultipart()
                msg["From"] = from_address
                msg["To"] = to_address
                msg["Subject"] = subject
                msg["Bcc"] = bcc_adress
                msg["CC"] = cc_address
                msg.attach(MIMEText(body, "plain"))
                try:
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()  
                        server.login(smtp_user, smtp_password)  
                        server.sendmail(from_address, [to_address, bcc_adress], cc_address, msg.as_string()) 
                        print("Email sent successfully!")
                        doc = frappe.get_doc({

                                'doctype': 'Email Log',
                                'ref_no': po_no,
                                'to_email': to_address,
                                'from_email': from_address,
                                'message': body,
                                'status': "Successfully Sent",
                                'screen': "Purchase Order Creation",
                                'created_by': from_address
                                })
                        doc.insert(ignore_permissions=True)
                        frappe.db.commit()

                except Exception as e:
                    print(f"Failed to send email: {e}")
                    msge = f"Failed to send email: {e}"
                    doc = frappe.get_doc({

                                'doctype': 'Email Log',
                                'ref_no': po_no,
                                'to_email': to_address,
                                'from_email': from_address,
                                'message': body,
                                'status': msge,
                                'screen': "Purchase Order Creation",
                                'created_by': from_address
                                })
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()
                return "Purchase Order Created Successfully."

            else:
                po_doc.save()
                conf = frappe.conf
                smtp_server = conf.get("smtp_server")
                smtp_port = conf.get("smtp_port")
                smtp_user = conf.get("smtp_user")
                smtp_password = conf.get("smtp_password")  
                from_address = 'noreply@merillife.com'
                to_address = vendor_email
                cc_address = register_email
                bcc_adress = "rishi.hingad@merillife.com"
                subject = f"""Purchase Order Created"""
                body = "body"
                msg = MIMEMultipart()
                msg["From"] = from_address
                msg["To"] = to_address
                msg["Subject"] = subject
                msg["CC"] = cc_address
                msg["Bcc"] = bcc_adress 
                msg.attach(MIMEText(body, "plain"))
                try:
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()  
                        server.login(smtp_user, smtp_password)  
                        server.sendmail(from_address, [to_address, bcc_adress], cc_address, msg.as_string()) 
                        print("Email sent successfully!")
                        doc = frappe.get_doc({

                                'doctype': 'Email Log',
                                'ref_no': po_no,
                                'to_email': to_address,
                                'from_email': from_address,
                                'message': body,
                                'status': "Successfully Sent",
                                'screen': "Purchase Order Creation",
                                'created_by': from_address


                                })
                        doc.insert(ignore_permissions=True)
                        frappe.db.commit()

                except Exception as e:
                    print(f"Failed to send email: {e}")
                    msge = f"Failed to send email: {e}"
                    doc = frappe.get_doc({

                                'doctype': 'Email Log',
                                'ref_no': po_no,
                                'to_email': to_address,
                                'from_email': from_address,
                                'message': body,
                                'status': msge,
                                'screen': "Purchase Order Creation",
                                'created_by': from_address


                                })
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()
                return "Purchase Order Updated Successfully."
        else:
            return "No valid data received or 'items' key not found."
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_po Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_all_product_master():
    try:
    
        product_master_details = frappe.get_all(
            "VMS Product Master", 
            fields=["*"]
        )
        
        for product in product_master_details:
            if product.get("product_image"):
                product["product_image_url"] = frappe.utils.get_url(product["product_image"])
        
        return  product_master_details
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_all_product_master")
        return {
            "status": "error",
            "message": str(e)
        }
    

@frappe.whitelist()
def get_purchase_enquiry_details():
    try:
        cart_details = frappe.get_all("Cart Details", fields=["*"], filters={"docstatus": ["<", 2]},)

        if not cart_details:
            return {"status": "error", "message": "No Cart Details found"}

        for cart in cart_details:
            cart_products = frappe.get_all(
                "Cart Master",
                fields=["product_name", "assest_code", "product_quantity"],
                filters={"parent": cart["name"]},
            )

            for product in cart_products:
                product_master_details = frappe.db.get_value(
                    "VMS Product Master",
                    {"name": product["product_name"]},
                    ["product_price", "lead_time", "product_image","category_type"],
                    as_dict=True,
                )

                if product_master_details:
                    product["price"] = product_master_details.get("product_price")
                    product["lead_time"] = product_master_details.get("lead_time")
                    product["product_image"] = product_master_details.get("product_image")
                    product["category_type"] = product_master_details.get("category_type")
                else:
                    product["price"] = None
                    product["lead_time"] = None
                    product["product_image"] = None
                    product["category_type"] = None

            cart["cart_products"] = cart_products

        return cart_details

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_purchase_enquiry_details")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def send_enquiry_email():
    try:
        data = frappe.request.get_json()
        cart_name = data.get("cart_name")

        if not cart_name:
            return {"status": "error", "message": "Cart name is required"}

        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        
        cart_details = frappe.get_all(
            "Cart Details",
            fields=["*"],
            filters={"name": cart_name, "enquirer_status": "Raised", "docstatus": ["<", 2]},
        )

        if not cart_details:
            return {"status": "error", "message": f"No raised Cart Details found for {cart_name}"}

        for cart in cart_details:
            enquirer_email = cart.get("user")
            receiver_email = cart.get("sender_email")
            enquirer_name = frappe.db.get_value("User", filters={'email': enquirer_email}, fieldname=['full_name'])
            receiver_name = frappe.db.get_value("User", filters={'email': receiver_email}, fieldname=['full_name'])
            po_no = cart.get("name")

            cart_products = frappe.get_all(
                "Cart Master",
                fields=["product_name", "assest_code", "product_quantity"],
                filters={"parent": cart_name},
            )

            for product in cart_products:
                product_master_details = frappe.db.get_value(
                    "VMS Product Master",
                    {"name": product["product_name"]},
                    ["product_price", "lead_time", "product_image","category_type"],
                    as_dict=True,
                )
                if product_master_details:
                    product.update(product_master_details)
                else:
                    product.update({"product_price": None, "lead_time": None, "product_image": None, "category_type": None})

            email_body = f"""
                <p>Dear {receiver_name},</p>
                <p>The following purchase enquiry has been raised by {enquirer_name}:</p>
                <table border='1' cellspacing='0' cellpadding='5'>
                    <tr>
                        <th>Product Name</th>
                        <th>Asset Code</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Lead Time</th>
                        <th>Category</th>
                    </tr>
                    {''.join([f'<tr><td>{p["product_name"]}</td><td>{p["assest_code"]}</td><td>{p["product_quantity"]}</td><td>{p["product_price"] or "N/A"}</td><td>{p["lead_time"] or "N/A"}</td><td>{p["category_type"] or "N/A"}</td></tr>' for p in cart_products])}
                </table>

                <p>Best Regards</p>
            """
            from_address = enquirer_email
            to_address = receiver_email
            subject = "Enquiry Raised - Cart Details"
            bcc_address = "rishi.hingad@merillife.com"
            msg = MIMEMultipart()
            msg["From"] = from_address
            msg["To"] = to_address
            msg["Subject"] = subject
            msg["Bcc"] = bcc_address
            msg.attach(MIMEText(email_body, "html"))

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
                    print("Email sent successfully!")
                    doc = frappe.get_doc({
                        'doctype': 'Email Log',
                        'ref_no': po_no,
                        'to_email': to_address,
                        'from_email': from_address,
                        'message': email_body,
                        'status': "Successfully Sent",
                        'screen': "Cart Details Enquiry",
                        'created_by': from_address
                    })
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()
            except Exception as e:
                print(f"Failed to send email: {e}")
                msge = f"Failed to send email: {e}"
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': po_no,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': email_body,
                    'status': msge,
                    'screen': "Cart Details Enquiry",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        return {"status": "success", "message": "Emails sent successfully"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in send_enquiry_email")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def send_email_on_approval_rejection_of_enquiry():
    try:
        print("Inside send_email_on_approval_rejection_of_enquiry function")

        data = frappe.request.get_json()

        designationname = data.get("designationname")
        cart_name = data.get("cart_name")
        reject_reason = data.get("rejection_reason")

        if not cart_name:
            print("Cart name is missing")
            return {"status": "error", "message": "Cart name is required"}

        # Fetch cart details
        cart_details = frappe.get_all(
            "Cart Details",
            fields=["*"],
            filters={"name": cart_name, "enquirer_status": "Raised", "docstatus": ["<", 2]},
        )

        if not cart_details:
            print(f"No raised Cart Details found for {cart_name}")
            return {"status": "error", "message": f"No raised Cart Details found for {cart_name}"}

        for cart in cart_details:
            enquirer_email = cart.get("user")
            receiver_email = cart.get("sender_email")
            enquirer_name = frappe.db.get_value("User", filters={'email': enquirer_email}, fieldname=['full_name'])
            receiver_name = frappe.db.get_value("User", filters={'email': receiver_email}, fieldname=['full_name'])
            reporting_email = frappe.db.get_value("User", filters={'email': receiver_email}, fieldname=['reporting_head'])
            po_no = cart.get("name")

            purchase_team_status = cart.get("purchase_team_status")
            representative_head_status = cart.get("representative_head_status")
            print(f"From: {receiver_email}, To: {reporting_email}, CC: {enquirer_email}, "
            f"Enquirer: {enquirer_name}, Receiver: {receiver_name}, PO: {po_no}, "
            f"Cart: {cart_name}, Status: {purchase_team_status}, Reason: {reject_reason}")


            if designationname == "Purchase Team":
                if purchase_team_status in ["Acknowledged", "Rejected"]:
                    print(f"Sending email for Purchase Team: {purchase_team_status}")
                    send_email_on_enquiry_status(
                        from_address=receiver_email, 
                        to_address=reporting_email, 
                        cc_address=enquirer_email, 
                        enquirer_name=enquirer_name, 
                        receiver_name=receiver_name, 
                        po_no=po_no, 
                        cart_name=cart_name, 
                        status=purchase_team_status,
                        reason=reject_reason
                    )
            elif designationname == "Purchase Head":
                if representative_head_status in ["Acknowledged", "Rejected"]:
                    print(f"Sending email for Purchase Head: {representative_head_status}")
                    send_email_on_enquiry_status(
                        from_address=reporting_email, 
                        to_address=receiver_email, 
                        cc_address=enquirer_email, 
                        enquirer_name=enquirer_name, 
                        receiver_name=receiver_name, 
                        po_no=po_no, 
                        cart_name=cart_name, 
                        status=representative_head_status,
                        reason=reject_reason
                    )

        return {"status": "success", "message": "Emails sent successfully"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in send_email_on_approval_rejection_of_enquiry")
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}

def send_email_on_enquiry_status(from_address, to_address, cc_address, enquirer_name, receiver_name, po_no, cart_name, status, reason):
    print("Inside send_email function")
    print(f"Preparing email for {to_address} (status: {status})")

    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    
    # Fetch cart products
    cart_products = frappe.get_all(
        "Cart Master",
        fields=["product_name", "assest_code", "product_quantity",],
        filters={"parent": cart_name},
    )
    email_body = f"""
    <p>Dear {receiver_name},</p>
    <p>The following purchase enquiry has been {status} by {enquirer_name}:</p>
    <table border='1' cellspacing='0' cellpadding='5'>
        <tr>
            <th>Product Name</th>
            <th>Asset Code</th>
            <th>Quantity</th>
        </tr>
        {''.join([f'<tr><td>{p["product_name"]}</td><td>{p["assest_code"]}</td><td>{p["product_quantity"]}</td></tr>' for p in cart_products])}
    </table>
    """

    # Add rejection reason if status is "Rejected"
    if status == "Rejected":
        email_body += f"""
            <p><strong>Rejection Reason:</strong> {reason}</p>
        """

    email_body += "<p>Best Regards</p>"

    
    subject = f"Enquiry {status} - Cart Details"
    bcc_address = "rishi.hingad@merillife.com"

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Bcc"] = bcc_address
    msg["CC"] = cc_address
    msg.attach(MIMEText(email_body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_address, [to_address, bcc_address, cc_address], msg.as_string())
            print("Email sent successfully!")
            # Log email in Frappe
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': po_no,
                'to_email': to_address,
                'from_email': from_address,
                'message': email_body,
                'status': "Successfully Sent",
                'screen': "Enquiry Status Change",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print("Email Log created successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")
        frappe.log_error(frappe.get_traceback(), "Email Sending Failed")
        # Log failure in Email Log
        doc = frappe.get_doc({
            'doctype': 'Email Log',
            'ref_no': po_no,
            'to_email': to_address,
            'from_email': from_address,
            'message': email_body,
            'status': f"Failed: {e}",
            'screen': "Enquiry Status Change",
            'created_by': from_address
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()



@frappe.whitelist(allow_guest=True)
def send_sub_head_email():
    if frappe.request.method != "POST":
        frappe.local.response.http_status_code = 405
        return {"error": "Method not allowed"}
    
    try:
        raw_data = frappe.request.data.decode('utf-8')
        # print("Raw Request Data--->", raw_data)
        try:
            data = frappe.parse_json(raw_data)
            # print("JSON Parsed Successfully:", data)
        except Exception as e:
            frappe.log_error(f"JSON Parsing Error: {str(e)}", "JSON Error")
            return {"error": "Invalid JSON format"}

        to_email = data.get("email")
        cart_details = data.get("cartDetails", {})
        cart_id = data.get("cartDetails", {}).get("name")
        
        if not to_email or not cart_details:
            print("Missing email or cartDetails data")
            return {"error": "Missing email or cartDetails data"}
        from_email = data.get("senderemail")
        print("From Email--->", from_email)
        print("To Email--->", to_email)

        try:
            frappe.db.set_value("Cart Details", cart_id, {
                "sub_head_email": to_email,
                "sub_head_transfer_status": "Transferred"
            })
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Failed to update Cart Details: {str(e)}", "Cart Update Error")
            return {"error": "Failed to update cart details."}

        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")
        bcc_address = "rishi.hingad@merillife.com"

        subject = f"Cart Details for {cart_details.get('name', 'Vendor')}"
        message = f"""
            <p>Hello,</p>
            <p>Here are the cart details:</p>
            <ul>
                <li><strong>Cart Date:</strong> {cart_details.get('cart_date')}</li>
                <li><strong>Remarks:</strong> {cart_details.get('remarks')}</li>
                <li><strong>Representative Head Status:</strong> {cart_details.get('representative_head_status')}</li>
            </ul>
            <p>Cart Products:</p>
            <ul>
        """
        cart_products = cart_details.get("cart_products", [])
        if cart_products:
            for product in cart_products:
                product_name = product.get("product_name", "Unknown Product")
                product_quantity = product.get("product_quantity", "Unknown Quantity")
                product_unit = product.get("unit", "Unknown Unit")

                message += f"<li>{product_name} - {product_quantity} {product_unit}</li>"
        else:
            message += "<li>No products available</li>"

        message += "</ul><p>Best Regards,<br>{from_email}</p>"
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(message, "html"))
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [to_email, bcc_address], msg.as_string())
                print("Email Sent Successfully!")
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': cart_details.get('name'),
                'to_email': to_email,
                'from_email': from_email,
                'message': message,
                'status': "Successfully Sent",
                'screen': "Cart Details Enquiry",
                'created_by': from_email
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

            return {"success": f"Email sent successfully to {to_email}"}
        
        except Exception as e:
            error_message = f"Failed to send email: {str(e)}"
            print(f"SMTP Error: {error_message}")
            frappe.log_error(error_message, "Email Sending Error")
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': cart_details.get('name'),
                'to_email': to_email,
                'from_email': from_email,
                'message': message,
                'status': error_message,
                'screen': "Cart Details Enquiry",
                'created_by': from_email
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

            return {"error": error_message}
    
    except Exception as e:
        frappe.log_error(f"Email sending failed: {str(e)}", "Email Error")
        print(f"General Exception: {str(e)}")
        return {"error": "Failed to send email. Please check logs."}


import uuid
from urllib.parse import urlparse, parse_qs

@frappe.whitelist(allow_guest=True)
def import_excel_to_doctype():
    try:
        file_data = frappe.request.files['file_data']
        print(f"Received file: {file_data.filename}")
        df = pd.read_excel(file_data)
        print(df.head(2))
        file_data = frappe.request.files['file_data']
        df = pd.read_excel(file_data)

        for _, row in df.iterrows():
            # file_url = None
            # product_image_path = row.get('product_image')  # Image path or URL

            # if product_image_path:
            #     try:
            #         # Normalize path if it's a local file path
            #         product_image_path = product_image_path.replace("\\", "/")
                    
            #         # Check if the product image is a URL
            #         if product_image_path.startswith("http"):  # URL
            #             response = requests.get(product_image_path, stream=True)
            #             response.raise_for_status()  # Ensure it is valid

            #             # Extract file name from the URL or generate a UUID
            #             file_name = os.path.basename(urlparse(product_image_path).path)
            #             if not file_name:
            #                 file_name = f"{uuid.uuid4()}.jpg"  # Generate a new filename

            #             # Save the image file to Frappe's file system
            #             file_doc = save_file(
            #                 file_name,                  # The image file name
            #                 response.content,           # Image content
            #                 "VMS Product Master",       # Attached to Doctype
            #                 None,                        # No specific document
            #                 is_private=0                 # Public access (set to 1 for private)
            #             )
            #             file_url = file_doc.file_url  # The URL of the uploaded file
            #         else:
            #             raise Exception(f"Invalid product_image path: {product_image_path}")
            #     except Exception as e:
            #         print(f"Failed to process image: {e}")
            #         continue  # Continue with other products even if an image fails
            specifications = row['specifications'] if pd.notna(row['specifications']) else 'NaN'
            product_name = row['product_name'] if pd.notna(row['product_name']) else 'Unknown Product'
            category_type = row['category_type'] if pd.notna(row['category_type']) else 'Uncategorized'
            product_price = row['product_price'] if pd.notna(row['product_price']) else 'N/A'
            lead_time = row['lead_time'] if pd.notna(row['lead_time']) else 'N/A'

            category_doc = frappe.get_all('Category Master', filters={'name': category_type})
            if not category_doc:
                new_category = frappe.get_doc({
                    'doctype': 'Category Master',
                    'category_name': category_type
                })
                new_category.insert()
                frappe.db.commit()

            doc = frappe.get_doc({
                'doctype': 'VMS Product Master',
                'product_name': product_name,
                'category_type': category_type,
                'product_price': product_price,
                'specifications': specifications,
                'lead_time': lead_time,
            })
            doc.insert(ignore_if_duplicate=True)

        frappe.db.commit()
        return {"success": "Data imported successfully "}
    
    except Exception as e:
        if 'file_data' not in frappe.request.files:
            return {"error": "No file data provided"}
        else:
            return {"error": f"Error importing data: {str(e)}"}


def parse_date(date_str):
    if isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            frappe.log_error(frappe.get_traceback(), f"Invalid date format: {date_str}")
    return None

@frappe.whitelist()
def get_field_mappings(docname):
    doctype_name = frappe.db.get_value("SAP Mapper PR", filters={'doctype_name': 'Purchase Requisition'}, fieldname=['name'])
    mappings = frappe.get_all('SAP Mapper PR Item', filters={'parent': doctype_name}, fields=['sap_field', 'erp_field'])
    print(f"Field Mappings: {mappings}", docname)
    return {mapping['sap_field']: mapping['erp_field'] for mapping in mappings}

@frappe.whitelist()
def get_pr():
    try:
        data = frappe.request.get_json()
        print(f"Received Data: {data}")

        if data and "items" in data:
            pr_no = data.get("pr_no", "")
            field_mappings = get_field_mappings('SAP Mapper PR')
            print(f"Field Mappings: {field_mappings}")

            pr_doc = frappe.get_doc("Purchase Requisition", {"purchase_requisition_number": pr_no}) if frappe.db.exists("Purchase Requisition", {"purchase_requisition_number": pr_no}) else frappe.new_doc("Purchase Requisition")
            
            pr_doc.purchase_requisition_number = pr_no
            pr_doc.pr_items = []

            meta = frappe.get_meta("Purchase Requisition")

            for item in data["items"]:
                pr_item_data = {}
                for sap_field, erp_field in field_mappings.items():
                    value = item.get(sap_field, "")
                   
                    field = next((field for field in meta.fields if field.fieldname == erp_field), None)
                    if field and field.fieldtype == 'Date':
                        pr_item_data[erp_field] = parse_date(value)  
                    else:
                        pr_item_data[erp_field] = value
                
                print(f"Item Data: {pr_item_data}")  
                pr_doc.append("pr_items", pr_item_data)

                if pr_plant_value is None and "plant" in item:
                    pr_plant_value = item.get("plant")
                
            if pr_plant_value:
                pr_doc.pr_plant = pr_plant_value
                
            print(f"PR Items Before Save: {pr_doc.pr_items}")  

            pr_doc.save()

            if pr_doc.is_new():
                pr_doc.insert()
                return "Purchase Requisition Created Successfully."
            else:
                return "Purchase Requisition Updated Successfully."
        else:
            return "No valid data received or 'items' key not found."
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_purchase_requisition Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_grn_field_mappings(docname):
    doctype_name = frappe.db.get_value("SAP Mapper PR", filters={'doctype_name': 'GRN'}, fieldname=['name'])
    mappings = frappe.get_all('SAP Mapper PR Item', filters={'parent': doctype_name}, fields=['sap_field', 'erp_field'])
    print(f"Field Mappings: {mappings}", docname)
    return {mapping['sap_field']: mapping['erp_field'] for mapping in mappings}

@frappe.whitelist()
def get_grn():
    try:
        data = frappe.request.get_json()
        print(f"Received Data: {data}")

        if data and "items" in data:
            grn_no = data.get("grn_no", "")
            field_mappings = get_grn_field_mappings('SAP Mapper PR')
            print(f"Field Mappings: {field_mappings}")

            grn_doc = frappe.get_doc("GRN", {"grn_no": grn_no}) if frappe.db.exists("GRN", {"grn_no": grn_no}) else frappe.new_doc("GRN")
            
            grn_doc.grn_no = grn_no
            grn_doc.grn_items_table = []

            meta = frappe.get_meta("GRN")

            for item in data["items"]:
                grn_item_data = {}
                for sap_field, erp_field in field_mappings.items():
                    value = item.get(sap_field, "")
                    
                    field = next((field for field in meta.fields if field.fieldname == erp_field), None)
                    if field and field.fieldtype == 'Date':
                        grn_item_data[erp_field] = parse_date(value)  
                    else:
                        grn_item_data[erp_field] = value
                
                grn_doc.grn_date = grn_item_data["grn_date"]

                grn_date = grn_doc.get('grn_date', frappe.utils.nowdate())
                
                print(f"Item Data: {grn_item_data}")  
                grn_doc.append("grn_items_table", grn_item_data)

            print(f"GRN Items Before Save: {grn_doc.grn_items_table}")  

            if grn_doc.is_new():
                grn_doc.insert()
            else:
                grn_doc.save()

            purchase_team_emails = frappe.db.get_all(
                "User",
                filters={"designation": "Purchase Team", "enabled": 1},
                fields=["email"],
            )
            email_list = [user["email"] for user in purchase_team_emails]
            print("Purchase Team Emails:", email_list)

            if email_list:
                conf = frappe.conf
                smtp_server = conf.get("smtp_server")
                smtp_port = conf.get("smtp_port")
                smtp_user = conf.get("smtp_user")
                smtp_password = conf.get("smtp_password")
                from_address = 'noreply@merillife.com'
                to_address = ", ".join(email_list)
                bcc_address = "rishi.hingad@merillife.com"
                subject = f"GRN Created: {grn_no}"
                body = f"""
                Dear Team,

                The GRN for {grn_no} is created on {grn_date}.

                Kindly view the details here:
                http://localhost:3000/grn-details

                Regards,
                VMS
                """
                msg = MIMEMultipart()
                msg["From"] = from_address
                msg["To"] = to_address
                msg["Subject"] = subject
                msg["Bcc"] = bcc_address
                msg.attach(MIMEText(body, "plain"))

                try:
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_user, smtp_password)
                        server.sendmail(from_address, [email_list, bcc_address], msg.as_string())
                        print("Email sent successfully!")
                        doc = frappe.get_doc({
                            'doctype': 'Email Log',
                            'ref_no': grn_no,
                            'to_email': to_address,
                            'from_email': from_address,
                            'message': body,
                            'status': "Successfully Sent",
                            'screen': "GRN Creation",
                            'created_by': from_address
                        })
                        doc.insert(ignore_permissions=True)
                        frappe.db.commit()

                except Exception as e:
                    print(f"Failed to send email: {e}")
                    msge = f"Failed to send email: {e}"
                    doc = frappe.get_doc({
                        'doctype': 'Email Log',
                        'ref_no': grn_no,
                        'to_email': to_address,
                        'from_email': from_address,
                        'message': body,
                        'status': msge,
                        'screen': "GRN Creation",
                        'created_by': from_address
                    })
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()

            if grn_doc.is_new():
                grn_doc.insert()
                return "Goods Receipt Note Created Successfully."
            else:
                return "Goods Receipt Note Updated Successfully."
        else:
            return "No valid data received or 'items' key not found."
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_goods_receipt_note Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def check_vendor_exists(email):
    """
    Check if a vendor already exists based on email or mobile number.
    """
    filters = {
        "email": email
    }

    vendor_exists = frappe.db.exists("Vendor Master", filters)

    if vendor_exists:
        return {"status": "error", "message": "Vendor already exists"}
    
    return {"status": "success", "message": "Vendor does not exist"}


@frappe.whitelist(allow_guest=True)
def check_vendor_gst(gst_number):
    """
    Check if a vendor already exists based on GST number.
    """
    filters = {
        "gst_number": gst_number
    }

    vendor_exists = frappe.db.exists("Vendor Onboarding", filters)

    if vendor_exists:
        return {"status": "error", "message": "Vendor with this GST already exists"}
    
    return {"status": "success", "message": "Vendor does not exist"}

@frappe.whitelist(allow_guest=True)
def send_email_on_gst_existing():
    try:
        data = frappe.request.get_json()
        gst_number = data.get("gst_number")
        vendoronboarding = frappe.get_value("Vendor Onboarding", {"gst_number": gst_number}, ["ref_no"])
        print("Ref No for Vendor Master--->",vendoronboarding)
        vendor = frappe.get_doc("Vendor Master", {"name":vendoronboarding})

        vendor_name = vendor.vendor_name
        from_address = "noreply@merillife.com"
        to_address = vendor.registered_by
        bcc_address = "rishi.hingad@merillife.com"
        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")

        if not from_address or not to_address:
            return {"status": "error", "message": "Vendor email details missing"}

        subject = "GST Number Exists"
        body = f"""
        <p>Dear Team,</p>

        <p>The GST Number <strong>{gst_number}</strong> for this <strong>{vendor_name}</strong> already exists in our system.</p>
        
        <p>Please check.</p>

        <p>Regards,<br> VMS Team</p>
        """

        msg = MIMEText(body,"html")
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Bcc"] = bcc_address

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
                print("Email sent successfully!")
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': vendoronboarding,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "GST Number Exists",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email: {e}")
            msge = f"Failed to send email: {e}"
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': vendoronboarding,
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "GST Number Exists",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

        return {"status": "success", "message": "Email sent successfully"}

    except Exception as e:
        frappe.log_error(f"Email Sending Error: {str(e)}", "GST Email Error")
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}


@frappe.whitelist(allow_guest=True)
def send_email_on_pan_existing():
    try:
        data = frappe.request.get_json()
        company_pan_number = data.get("company_pan_number")
        vendoronboarding = frappe.get_value("Vendor Onboarding", {"company_pan_number": company_pan_number}, ["ref_no"])
        print("Ref No for Vendor Master--->",vendoronboarding)
        vendor = frappe.get_doc("Vendor Master", {"name":vendoronboarding})

        vendor_name = vendor.vendor_name
        from_address = "noreply@merillife.com"
        to_address = vendor.registered_by
        bcc_address = "rishi.hingad@merillife.com"
        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")

        if not from_address or not to_address:
            return {"status": "error", "message": "Vendor email details missing"}

        subject = "Company PAN Number Exists"
        body = f"""
        <p>Dear Team,</p>

        <p>The PAN Number <strong>{company_pan_number}</strong> for this <strong>{vendor_name}</strong> already exists in our system.</p>
        
        <p>Please check.</p>

        <p>Regards,<br> VMS Team</p>
        """

        msg = MIMEText(body,"html")
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Bcc"] = bcc_address

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
                print("Email sent successfully!")
                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': vendoronboarding,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "PAN Number Exists",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email: {e}")
            msge = f"Failed to send email: {e}"
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': vendoronboarding,
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "PAN Number Exists",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

        return {"status": "success", "message": "Email sent successfully"}

    except Exception as e:
        frappe.log_error(f"Email Sending Error: {str(e)}", "GST Email Error")
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}


@frappe.whitelist(allow_guest=True)
def check_vendor_pan(company_pan_number):
    """
    Check if a vendor already exists based on Company PAN number.
    """
    filters = {
        "company_pan_number": company_pan_number
    }

    vendor_exists = frappe.db.exists("Vendor Onboarding", filters)

    if vendor_exists:
        return {"status": "error", "message": "Vendor with this PAN number already exists"}
    
    return {"status": "success", "message": "Vendor does not exist"}

@frappe.whitelist(allow_guest=True)
def send_email_on_click():
    try:
        data = frappe.request.get_json()
        print("My Data--->",data)
        vendor_name = data.get("vendor_name")
        bank_name = data.get("bank_name")
        account_number = data.get("account_number")
        ifsc_code = data.get("ifsc_code")
        branch_name = data.get("branch_name")
        registered_by = data.get("registered_by")

        from_address = "noreply@merillife.com"
        to_address = registered_by
        bcc_address = "rishi.hingad@merillife.com"

        if not from_address or not to_address:
            return {"status": "error", "message": "Vendor email details missing"}

        subject = "Bank Details Verification"
        body = f"""
        <p>Dear Team,</p>

        <p>Please find below the bank details for <strong>{vendor_name}</strong>:</p>

        <ul>
            <li><strong>Bank Name:</strong> {bank_name}</li>
            <li><strong>Account Number:</strong> {account_number}</li>
            <li><strong>IFSC Code:</strong> {ifsc_code}</li>
            <li><strong>Branch Name:</strong> {branch_name}</li>
        </ul>

        <p>Please verify and proceed accordingly.</p>

        <p>Regards,<br>VMS Team</p>
        """

        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")

        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Bcc"] = bcc_address

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_address, bcc_address], msg.as_string())
                print("Email sent successfully!")

                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Bank Details Verification",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email: {e}")
            msge = f"Failed to send email: {e}"
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "Bank Details Verification",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

        return {"status": "success", "message": "Email sent successfully"}

    except Exception as e:
        frappe.log_error(f"Email Sending Error: {str(e)}", "Bank Details Email Error")
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}


@frappe.whitelist(allow_guest=True)
def show_all_vendors():
    all_vendors = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.status AS status,
            vm.onboarding_form_status AS onboarding_form_status,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.office_email_primary AS office_email_primary,
            vm.vendor_name AS vendor_name,
            cm.company_name AS company_name,
            cm.company_code AS company_code,
            vm.name AS ref_no,
            vm.registered_by AS registered_by,
            u.full_name AS registered_by_name
        
        FROM 
            "tabVendor Master" vm 
        LEFT JOIN 
            "tabCompany Master" cm ON vm.company_name = cm.name
        LEFT JOIN 
            "tabUser" u ON vm.registered_by = u.name
        ORDER BY 
            vm.creation DESC, vm.modified DESC
    """, as_dict=1)

    for vendor in all_vendors:
        multiple_company_data = frappe.db.sql("""
            SELECT 
                mcd.company_name_mt, 
                cm.company_name
            FROM 
                "tabMultiple Company Data" mcd 
            LEFT JOIN 
                "tabCompany Master" cm ON mcd.company_name_mt = cm.name
            WHERE 
                mcd.parent = %s
        """, (vendor['name'],), as_dict=1)

        vendor_types = frappe.db.sql("""
            SELECT
                vt.vendor_type       
            FROM
                "tabVendor Type Group" vt
            WHERE
                vt.parent = %s
        """, (vendor['name'],), as_dict=1)
        
        vendor['multiple_company_data'] = multiple_company_data
        vendor['vendor_types'] = vendor_types

    return all_vendors

@frappe.whitelist(allow_guest=True)
def show_all_vendors_team():
    all_vendors = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.status AS status,
            vm.onboarding_form_status AS onboarding_form_status,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.office_email_primary AS office_email_primary,
            vm.vendor_name AS vendor_name,
            cm.company_name AS company_name,
            cm.company_code AS company_code,
            vm.name AS ref_no,
            vm.registered_by AS registered_by,
            ud.team AS team,
            u.full_name AS registered_by_name,
            vm.approved_by_accounts_team AS approved_by_accounts_team,
            vm.approved_by_purchase_team AS approved_by_purchase_team,
            vm.approved_by_purchase_head AS approved_by_purchase_head,
            ua.full_name AS approved_by_accounts_team_name,
            up.full_name AS approved_by_purchase_team_name,
            uh.full_name AS approved_by_purchase_head_name
        
        FROM 
            "tabVendor Master" vm 
        LEFT JOIN 
            "tabCompany Master" cm ON vm.company_name = cm.name
        LEFT JOIN 
            "tabUser" ud ON vm.registered_by = ud.name
        LEFT JOIN 
            "tabUser" u ON vm.registered_by = u.name
        LEFT JOIN 
            `tabUser` ua ON vm.approved_by_accounts_team = ua.name
        LEFT JOIN 
            `tabUser` up ON vm.approved_by_purchase_team = up.name
        LEFT JOIN 
            `tabUser` uh ON vm.approved_by_purchase_head = uh.name
        ORDER BY 
            vm.creation DESC, vm.modified DESC
    """, as_dict=1)

    vendor_data = []
    for vendor in all_vendors:
        multiple_company_data = frappe.db.sql("""
            SELECT 
                mcd.company_name_mt, 
                cm.company_name
            FROM 
                "tabMultiple Company Data" mcd 
            LEFT JOIN 
                "tabCompany Master" cm ON mcd.company_name_mt = cm.name
            WHERE 
                mcd.parent = %s
        """, (vendor['name'],), as_dict=1)

        vendor_types = frappe.db.sql("""
            SELECT
                vt.vendor_type       
            FROM
                "tabVendor Type Group" vt
            WHERE
                vt.parent = %s
        """, (vendor['name'],), as_dict=1)
        
        vendor_data.append({
            "team": vendor.get("team") or "Unassigned",
            "vendor_details": {
                "name": vendor["name"],
                "status": vendor["status"],
                "onboarding_form_status": vendor["onboarding_form_status"],
                "purchase_team_approval": vendor["purchase_team_approval"],
                "purchase_head_approval": vendor["purchase_head_approval"],
                "accounts_team_approval": vendor["accounts_team_approval"],
                "office_email_primary": vendor["office_email_primary"],
                "vendor_name": vendor["vendor_name"],
                "company_name": vendor["company_name"],
                "company_code": vendor["company_code"],
                "ref_no": vendor["ref_no"],
                "registered_by": vendor["registered_by"],
                "registered_by_name": vendor["registered_by_name"],
                "approved_by_accounts_team": vendor["approved_by_accounts_team"],
                "approved_by_purchase_team": vendor["approved_by_purchase_team"],
                "approved_by_purchase_head": vendor["approved_by_purchase_head"],
                "approved_by_accounts_team_name": vendor["approved_by_accounts_team_name"],
                "approved_by_purchase_team_name": vendor["approved_by_purchase_team_name"],
                "approved_by_purchase_head_name": vendor["approved_by_purchase_head_name"],
                "multiple_company_data": multiple_company_data,
                "vendor_types": vendor_types
                
            }
        })

    grouped_vendors = {}
    for entry in vendor_data:
        team = entry["team"]
        if team not in grouped_vendors:
            grouped_vendors[team] = []
        grouped_vendors[team].append(entry["vendor_details"])

    return [{"team": team, "vendors": vendors} for team, vendors in grouped_vendors.items()]


@frappe.whitelist(allow_guest=True)
def show_all_vendors_qa():
    all_vendors = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.status AS status,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.office_email_primary AS office_email_primary,
            vm.vendor_name AS vendor_name,
            cm.company_name AS company_name,
            cm.company_code AS company_code,
            vm.name AS ref_no
        FROM 
            `tabVendor Master` vm 
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name
        WHERE 
            cm.company_code IN ('2000', '7000')
        ORDER BY 
            vm.creation DESC, vm.modified DESC
    """, as_dict=True)

    return all_vendors


@frappe.whitelist(allow_guest=True)
def show_all_vendor_details(status=None):
    if not status:
        return {"error": "Status is required."}

    vendor_details = frappe.db.sql("""
        SELECT
            vm.name AS vendor_master_name,
            vm.status AS status,
            vm.office_email_primary AS office_email_primary,
            vm.vendor_name AS vendor_name,
            vm.vendor_code AS vendor_code,
            cm.company_name AS company_name,
            cm.company_code AS company_code,
            vo.ref_no AS ref_no,
            vo.first_name AS first_name,
            vo.email AS email,
            vo.contact_number AS contact_number,
            vo.city AS city,
            vo.state AS state,
            vo.country AS country,
            vo.pincode AS pincode,
            vo.gst_number AS gst_number,
            vo.company_pan_number AS company_pan_number,
            vo.enterprise_registration_number AS enterprise_registration_number,
            vo.iec AS iec,
            vo.msme_enterprise_type AS msme_enterprise_type,
            vo.udyam_number AS udyam_number,
            vo.name_on_udyam_certificate AS name_on_udyam_certificate,
            vo.trc_certificate_no AS trc_certificate_no,
            bm.bank_name AS bank_name,
            vo.ifsc_code AS ifsc_code,
            vo.beneficiary_name AS beneficiary_name,
            bkm.bank_name AS beneficiary_bank_name,
            vo.beneficiary_bank_swift_code AS beneficiary_bank_swift_code,
            vo.beneficiary_bank_address AS beneficiary_bank_address,
            bnkm.bank_name AS intermediate_bank_name,
            vo.intermediate_bank_swift_code AS intermediate_bank_swift_code,
            vo.intermediate_bank_address AS intermediate_bank_address,
            vo.vendor_type AS vendor_type,
            vo.corporate_identification_number AS corporate_identification_number,
            cnm.company_nature_name AS company_nature_name,
            bnm.business_nature_name AS business_nature_name,
            vo.cin_date AS cin_date,
            cur.currency_code AS beneficiary_currency,
            curr.currency_code AS intermediate_currency,
            vm.registered_by AS registered_by
                                   
        FROM 
            `tabVendor Master` vm
        LEFT JOIN
            `tabVendor Onboarding` vo ON vm.name = vo.ref_no
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name
        LEFT JOIN
            `tabCompany Nature Master` cnm ON vo.nature_of_company = cnm.name
        LEFT JOIN
            `tabBusiness Nature Master` bnm ON vo.nature_of_business = bnm.name
        LEFT JOIN
            `tabBank Master` bm ON vo.bank_name = bm.name
        LEFT JOIN
            `tabBank Master` bkm ON vo.beneficiary_bank_name = bkm.name
        LEFT JOIN
            `tabBank Master` bnkm ON vo.intermediate_bank_name = bnkm.name
        LEFT JOIN
            `tabCurrency Master` cur ON vo.beneficiary_currency = cur.name
        LEFT JOIN
            `tabCurrency Master` curr ON vo.intermediate_currency = curr.name
        WHERE
            vm.status = %s
        ORDER BY 
            vm.creation DESC, vm.modified DESC
    """, status, as_dict=1)

    return vendor_details


@frappe.whitelist(allow_guest=True)
def show_all_vendors_current_month():
    current_month_start = datetime.now().strftime('%Y-%m-01 00:00:00')
    current_month_end = datetime.now().strftime('%Y-%m-%d 23:59:59')

    all_vendors = frappe.db.sql(f"""
        SELECT
            vm.name AS name,
            status AS status,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.office_email_primary AS office_email_primary,
            co.country_name AS country_name,
            vm.vendor_name AS vendor_name,
            cm.company_name AS company_name,
            vm.creation AS creation,
            vo.registered_office_number AS registered_office_number,
            vo.gst_number AS gst_number,
            vm.registered_by AS registered_by,
            vo.ref_no AS ref_no
                                
        FROM 
            `tabVendor Master` vm 
        LEFT JOIN 
            `tabVendor Onboarding` vo ON vo.ref_no = vm.name
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name
        LEFT JOIN
            `tabCountry Master` co ON vm.country = co.name
        WHERE
            vm.creation BETWEEN '{current_month_start}' AND '{current_month_end}'
    """, as_dict=1)

    return all_vendors


@frappe.whitelist(allow_guest=True)
def show_all_vendors_current_month_qa():
    current_month_start = datetime.now().strftime('%Y-%m-01 00:00:00')
    current_month_end = datetime.now().strftime('%Y-%m-%d 23:59:59')

    all_vendors = frappe.db.sql(f"""
        SELECT
            vm.name AS name,
            vm.status AS status,
            vm.purchase_team_approval AS purchase_team_approval,
            vm.purchase_head_approval AS purchase_head_approval,
            vm.accounts_team_approval AS accounts_team_approval,
            vm.office_email_primary AS office_email_primary,
            co.country_name AS country_name,
            vm.vendor_name AS vendor_name,
            COALESCE(cm.company_name, cm_mt.company_name) AS company_name,
            cm.company_code AS company_code,
            mcd.company_name_mt AS company_name_mt,
            vm.creation AS creation,
            vo.registered_office_number AS registered_office_number,
            vo.gst_number AS gst_number,
            vo.ref_no AS ref_no
                                
        FROM 
            `tabVendor Master` vm 
        LEFT JOIN 
            `tabVendor Onboarding` vo ON vo.ref_no = vm.name
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name
        LEFT JOIN
            `tabCountry Master` co ON vm.country = co.name
        LEFT JOIN
            `tabMultiple Company Data` mcd ON mcd.parent = vm.name
        LEFT JOIN
            `tabCompany Master` cm_mt ON cm_mt.company_code = mcd.company_name_mt
        WHERE
            vm.creation BETWEEN '{current_month_start}' AND '{current_month_end}'
            AND (cm.company_code IN ('2000', '7000')
            OR mcd.company_name_mt IN ('2000', '7000'))
    """, as_dict=1)

    return all_vendors


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
        tocr.currency_name AS to_currency_name,
        qo.fuel_surcharge AS fuel_surcharge,
        qo.sc AS sc,
        qo.xray AS xray,
        qo.pickuporigin AS pickuporigin,
        qo.ex_works AS ex_works,
        qo.transit_days AS transit_days,
        qo.total_freight AS total_freight,
        qo.exchange_rate AS exchange_rate,
        qo.total_freightinr AS total_freightinr,
        qo.destination_charge AS destination_charge,
        qo.shipping_line_charge AS shipping_line_charge,
        qo.cfs_charge AS cfs_charge,
        qo.total_landing_price AS total_landing_price,
        qo.remarks AS remarks

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
        `tabOld Material Master` mm ON qo.material_code = mm.name
        LEFT JOIN
        `tabMaterial Category Master` mcm ON qo.material_category = mcm.name
        LEFT JOIN
        `tabOld Material Master` m ON qo.material_name = m.name
        LEFT JOIN
        `tabCurrency Master` frmcr ON qo.from_currency = frmcr.name
        LEFT JOIN
        `tabCurrency Master` tocr ON qo.to_currency = tocr.name

        where qo.name=%s

     """,(name),as_dict=1)
    return quotation


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

    rfq_number = frappe.db.get_value("Quotation", filters={'name': name}, fieldname=['rfq_number'])
    raised_by = frappe.db.get_value("Request for Quotation", filters={'name': name}, fieldname=['raised_by'])
    raiser_name = frappe.db.get_value('User', filters={'name': raised_by}, fieldname=['full_name'])
    if rfq_number:

        frappe.db.sql("""UPDATE `tabQuotation` SET `status` = 'Rejected' WHERE `rfq_number` = %s AND `name` != %s""", (rfq_number, name))

        frappe.db.sql("""UPDATE `tabRequest For Quotation` SET `status` = 'Closed' WHERE `name` = %s""", (rfq_number,))

        frappe.db.set_value('Quotation', name, 'status', 'Approved')

        frappe.db.commit()
        vendor_name = frappe.db.get_value("Quotation", filters={'name': name}, fieldname=['vendor_code'])
        vendor_id = frappe.db.get_value("Vendor Master", filters={'vendor_code'}, fieldname=['name'])
        rfq_type = frappe.db.get_value("Request for Quotation", filters={'name': rfq_number}, fieldname=['select_service'] )        
        reciever_email = frappe.db.get_value("Vendor Master",filters={'name': vendor_name}, fieldname='office_email_primary')
        sender_address = "noreply@merillife.com" 
        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")  
        from_address = sender_address
        to_address = reciever_email
        bcc_address = "rishi.hingad@merillife.com"
        subject = f"""Congratulations"""

        if rfq_type == "Logistics Vendor":
            destination_country = frappe.db.get_value("Request for Quotation", filters={'name': rfq_number}, fieldname=['destination_port'])
            airline = frappe.db.get_value("Request for Quotation", filters={'name': rfq_number}, fieldname=['airlinevessel_name'])
            pod = frappe.db.get_value("Request for Quotation", filters={'name': rfq_number}, fieldname=['destination_port'])
            shipper_name = frappe.db.get_value("Quotation",filters={'name': name},fieldname=['company_name'])
            boxes = frappe.db.get_value("Request for Quotation", filters={'name': rfq_number}, fieldname=['no_of_pkg_units'])
            vol_weight = frappe.db.get_value("Request for Quotation", filters={'name': rfq_number}, fieldname=['vol_weight'])
            chargeable_weight = frappe.db.get_value("Quotation", filters={'name': name}, fieldname=['chargeable_weight'])
            freight = frappe.db.get_value("Quotation", filters={'name': name}, fieldname=['total_freight'])
            delivery_date = frappe.db.get_value("Quotation", filters={'name': name}, fieldname=['delivery_date'])

        html_body = f""" 
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vendor Details</title>
    </head>
    <body>
        <h2>Example Table</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tbody>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">RFQ Reference Number</td>
                    <td style="border: 1px solid black; padding: 8px;" >{rfq_number}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Quotation Reference Number</td>
                    <td style="border: 1px solid black; padding: 8px;" >{name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Destination Country :</td>
                    <td style="border: 1px solid black; padding: 8px;" >{destination_country}</td>
                    </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Name of the Airline :</td>
                    <td style="border: 1px solid black; padding: 8px;">{airline}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">POD :</td>
                    <td style="border: 1px solid black; padding: 8px;" >{pod}</td>
                    </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Shipper Name :</td>
                    <td style="border: 1px solid black; padding: 8px;">{shipper_name}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Number of Boxes :</td>
                    <td style="border: 1px solid black; padding: 8px;" >{boxes}</td>
                    </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Gross Weight (Kg)/Actual Weight (Kg) :</td>
                    <td style="border: 1px solid black; padding: 8px;">{vol_weight}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Chargeable Weight (Kg) :</td>
                    <td style="border: 1px solid black; padding: 8px;" >{chargeable_weight}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Total Freight Amount :</td>
                    <td style="border: 1px solid black; padding: 8px;">{freight}</td>
                </tr>
                 <tr>
                    <td style="border: 1px solid black; padding: 8px;" width="100px">Delivery Date :</td>
                    <td style="border: 1px solid black; padding: 8px;" colspan="3">{delivery_date}</td>
                </tr>
                
            </tbody>
        </table>
    </body>
    </html>
        """
        body = f"""
        Dear Sir/Madam,

        We thank you very much for providing your quote against our enquiry {rfq_number} and pleased to inform you that, your quote bearing RFQ reference Number {rfq_number} has been shortlisted for the logistics of this shipment.
        Our representative will be in touch with you to take it forward.<br/>
        {html_body}<br/>
        
        For {shipper_name}
        {raiser_name}
        """
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "plain"))
        print("*********", from_address, to_address, subject,body)
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  
                server.login(smtp_user, smtp_password)  
                server.sendmail(from_address, [to_address, bcc_address], msg.as_string()) 
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
        # print("*****vendorname and email*****",vendor_name,reciever_email, naammee)
        # obj.send_email(reciever_email, sender_address, subject, body)
        return "Quotation approved successfully and others rejected"
    else:
        return "RFQ number not found for the quotation"
    
    
@frappe.whitelist()
def show_me(**kwargs):
    name = kwargs.get('name')

    record_exists = frappe.db.exists("Vendor Onboarding", {'office_email_primary': name})
    if not record_exists:
        return {"message": "Record does not exist"}
    
    vendor = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.onboarding_form_status AS onboarding_form_status,
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
            vm.gst_date AS gst_date,
            --vm.cind As cind,
            vm.company_pan_number AS company_pan_number,
            vm.name_on_company_pan AS name_on_company_pan,
            vm.enterprise_registration_number AS enterprise_registration_number,
            vm.iec As iec,
            vm.rtgs AS rtgs,
            vm.neft AS neft,
            gst.registration_ven_name AS registration_ven_name,
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
            vm.third_f_name AS third_f_name,
            vm.third_l_name AS third_l_name,
            vm.third_dnation AS third_dnation,
            vm.third_mail AS third_mail,
            vm.third_cnot AS third_cnot,
            vm.fourth_f_name AS fourth_f_name,
            vm.fourth_l_name AS fourth_l_name,
            vm.fourth_dnation AS fourth_dnation,
            vm.fourth_mail AS fourth_mail,
            vm.fourth_cnot AS fourth_cnot,
            vm.fifth_f_name AS fifth_f_name,
            vm.fifth_l_name AS fifth_l_name,
            vm.fifth_dnation AS fifth_dnation,
            vm.fifth_mail AS fifth_mail,
            vm.fifth_cnot AS fifth_cnot,
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
            --vm.enterprise AS enterprise,
            vm.reconciliation_account AS reconciliation_account,
            vm.accounts_team_remark AS accounts_team_remark,
            vm.ref_no AS ref_no,
            vm.company_name AS company_name,
            cm.vendor_title AS vendor_title,
            vm.msme_enterprise_type AS msme_enterprise_type,
            vm.udyam_number AS udyam_number,
            vm.name_on_udyam_certificate AS name_on_udyam_certificate,
            vm.msme_proof AS msme_proof,
            vm.form_10f_proof AS form_10f_proof,
            vm.trc_certificate_no AS trc_certificate_no,
            vm.trc_certificate AS trc_certificate,
            vm.pe_certificate AS pe_certificate,
            bbk.bank_name AS beneficiary_bank_name,
            vm.beneficiary_account_no AS beneficiary_account_no,
            vm.beneficiary_name AS beneficiary_name,
            vm.beneficiary_iban_no AS beneficiary_iban_no,
            vm.beneficiary_bank_swift_code AS beneficiary_bank_swift_code,
            vm.bank_proof_for_beneficiary_bank AS bank_proof_for_beneficiary_bank,
            vm.beneficiary_ach_no AS beneficiary_ach_no,
            vm.beneficiary_aba_no AS beneficiary_aba_no,
            vm.beneficiary_routing_no AS beneficiary_routing_no,
            vm.beneficiary_bank_address AS beneficiary_bank_address,
            curren.currency_name AS beneficiary_currency,
            ibk.bank_name AS intermediate_bank_name,
            curr.currency_name AS intermediate_currency,
            vm.intermediate_account_no AS intermediate_account_no,
            vm.intermediate_bank_swift_code AS intermediate_bank_swift_code,
            vm.intermediate_bank_address AS intermediate_bank_address,
            vm.intermediate_iban_no AS intermediate_iban_no,
            vm.intermediate_ach_no AS intermediate_ach_no,
            vm.intermediate_aba_no AS intermediate_aba_no,
            vm.intermediate_routing_no AS intermediate_routing_no,
            vm.bank_proof_for_intermediate_bank AS bank_proof_for_intermediate_bank,
            vm.add_intermediate_bank_details AS add_intermediate_bank_details,
            vm.total_godown AS total_godown,
            vm.cold_storage AS cold_storage,
            vm.brochure_proof AS brochure_proof,
            cm.status AS status,
            cm.qa_required AS qa_required,
            vm.multiple_locations AS multiple_locations,
            vm.whatsapp_number AS whatsapp_number,
            vm.msme_registered AS msme_registered,
            vm.first_department AS first_department,
            vm.second_department AS second_department,
            vm.third_department AS third_department,
            vm.fourth_department AS fourth_department,
            vm.fifth_department AS fifth_department
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
            `tabGST Registration Type Master` gst ON vm.gst_ven_type = gst.name
        LEFT JOIN
            `tabCertificate Master` crt ON vm.certificate_name = crt.name
        LEFT JOIN
            `tabReconciliation Account` rca ON vm.reconciliation_account = rca.name
        LEFT JOIN
            `tabBank Master` bbk on vm.beneficiary_bank_name = bbk.name
        LEFT JOIN
            `tabBank Master` ibk on vm.intermediate_bank_name = ibk.name
        LEFT JOIN
            `tabCurrency Master` curr on vm.intermediate_currency = curr.name
        LEFT JOIN
            `tabCurrency Master` curren on vm.beneficiary_currency = curren.name
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
    gst_details = frappe.db.sql(""" SELECT * FROM `tabGST Details Table` WHERE parent=%s """, (primary_key), as_dict=1)

    primary_key1 = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=["name"])
    
    multiple_company_data = frappe.db.sql(""" SELECT * FROM `tabMultiple Company Data` WHERE parent = %s """, (primary_key1), as_dict=1)
    vendor_types = frappe.db.sql(""" SELECT * FROM `tabVendor Type Group` WHERE parent = %s """, (primary_key1), as_dict=1)
    multiple_location_table = frappe.db.sql(""" SELECT * FROM `tabMultiple Address` WHERE parent=%s """, (primary_key), as_dict=1)

    xyz = frappe.db.get_value("Vendor Onboarding", filters={'name': primary_key}, fieldname=["office_email_primary"])
    gst_date = frappe.db.get_value("Vendor Onboarding", filters={'name': primary_key}, fieldname=['gst_date'])
    currency = frappe.db.get_value("Vendor Onboarding", filters={'name': primary_key}, fieldname=['currency'])
    paymentcurrency = frappe.db.get_value("Currency Master", filters={'name':currency}, fieldname=['currency_name'])
    email = frappe.db.get_value("Vendor Master", filters={'office_email_primary': xyz}, fieldname=["name"])
    ordercurrency = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['order_currency'])
    print("%%%%%%%%%%%%%%%%%((((((((((((((()))))))))))))))",xyz) #add
    currency_namee = frappe.db.get_value("Currency Master", filters={'name': ordercurrency}, fieldname=['currency_name'])
    term_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['terms_of_payment'])
    term_name = frappe.db.get_value("Terms Of Payment Master", filters={'name': term_id}, fieldname=['description']) #add
    inco_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['incoterms'])
    inco_name = frappe.db.get_value("Incoterm Master", filters={'name': inco_id}, fieldname=['incoterm_name']) #add
    payee = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['payee']) #add
    gr_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['gr_based_inv_ver']) #add
    check_double_invoice = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['check_double_invoice'])
    service_based_inv_ver = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['service_based_inv_ver']) #add
    purchase_group_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_groupm'])
    purchase_group_name = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_group_id}, fieldname=['purchase_group_name'])
    account_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
    account_name = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['account_group_name']) #add
    purchase_org_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['purchase_organization'])
    pruchase_org_name = frappe.db.get_value("Purchase Organization Master", filters={'name': purchase_org_id}, fieldname=['purchase_organization_name']) #add
    company_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['company_name'])
    company_name = frappe.db.get_value("Company Master", filters={'name': company_id}, fieldname=['company_name']) #add
    vendor_name = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['vendor_name'])
    vendor_id =frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['vendor_type'])
    vendor_type_name = frappe.db.get_value("Vendor Type Master", filters={'name': vendor_id}, fieldname=['vendor_type_name'])
    reconciled = frappe.db.get_value("Vendor Onboarding", filters={'name': primary_key}, fieldname=['reconciliation_account'])
    reconciliation_name = frappe.db.get_value("Reconciliation Account", filters={'name':reconciled}, fieldname=['reconcil_description'])
    accountgrp_id = frappe.db.get_value("Vendor Master", filters={'office_email_primary': name}, fieldname=['account_group'])
    account_group_description = frappe.db.get_value("Account Group Master", filters={'name': accountgrp_id}, fieldname=['description'])
    certificates = frappe.db.sql(""" SELECT * FROM `tabOnboarding Certificates` WHERE parent=%s """, (primary_key), as_dict=1)

    for cert in certificates:
        certificate_code = cert.get('certificate_code')
        
        try:
            certificate_doc = frappe.get_doc("Certificate Master", {'certificate_code': certificate_code})
            if certificate_doc:
                cert_name = certificate_doc.get('certificate_name')
                cert_code = certificate_doc.get('certificate_code')
                
                cert['certificate_name'] = cert_name
                cert['certificate_code'] = cert_code

                print(f"Updated certificate_name for {cert.get('name')} to {cert_name} with code {cert_code}")
            else:
                print(f"Certificate with code {certificate_code} not found in Certificate Master")
        except frappe.DoesNotExistError:
            print(f"Certificate with code {certificate_code} does not exist in Certificate Master")
        except Exception as e:
            print(f"An error occurred while processing certificate with code {certificate_code}: {str(e)}")

    if vendor:
        vendor[0].update({
            "banker_details": banker_details,
            "currency":paymentcurrency,
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
            "account_group_code": account_id,
            "account_name": account_name,
            "purchase_organization": pruchase_org_name,
            "purchase_organization_name": purchase_org_id,
            "reconciliation_account":reconciliation_name,
            "company": company_name,
            "vendor_name": vendor_name,
            "vendor_type": vendor_type_name,
            "gst_date": gst_date,
            "account_group_description": account_group_description,
            "certificates": certificates,
            "multiple_company_data": multiple_company_data,
            "vendor_types": vendor_types,
            "multiple_location_table":multiple_location_table,
            "gst_table": gst_details
        })

    return vendor

@frappe.whitelist()
def get_vendor_details_rfq():
    try:
        vendor_details = frappe.db.sql("""
            SELECT 
                vm.name,
                vm.vendor_name,
                vm.office_email_primary,
                vm.country,
                vm.vendor_code,
                vt.vendor_type
            FROM 
                `tabVendor Master` vm
            LEFT JOIN 
                `tabVendor Type Group` vt ON vt.parent = vm.name
        """, as_dict=True)

        grouped_vendors = {}
        for detail in vendor_details:
            vendor_name = detail["vendor_name"]
            if vendor_name not in grouped_vendors:
                grouped_vendors[vendor_name] = {
                    "ref_no": detail["name"],
                    "vendor_name": detail["vendor_name"],
                    "vendor_code": detail["vendor_code"],
                    "office_email_primary": detail["office_email_primary"],
                    "country": detail["country"],
                    "vendor_types": []
                }
            if detail["vendor_type"]:
                grouped_vendors[vendor_name]["vendor_types"].append({
                    "vendor_type": detail["vendor_type"]
                })

        vendors = list(grouped_vendors.values())

        return {
            "status": "success",
            "message": vendors
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_vendor_details")
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist()
def show_feedback_details(name):
    if not name:
        return {"error": _("Name is required")}

    feedback_entries = frappe.get_all(
        "FeedBack",
        filters={"feedback_raised_by": name},
        fields=["*"]
    )
    if not feedback_entries:
        return {"message": _("No feedback found for this Name")}

    for feedback in feedback_entries:
        feedback["feedback_chat"] = frappe.get_all(
            "Feedback Response Table",
            filters={"parent": feedback["name"]},
            fields=["*"]
        )
    return feedback_entries

@frappe.whitelist()
def show_all_feedback_details():
    feedback_entries = frappe.get_all(
        "FeedBack",
        fields=["*", "feedback_raised_by"]
    )

    if not feedback_entries:
        return {"message": _("No feedback found for this Name")}

    for feedback in feedback_entries:
        if feedback.get("feedback_raised_by"):
            vendor_details = frappe.get_value(
                "Vendor Master",
                feedback["feedback_raised_by"],
                "vendor_name"
            )
            feedback["vendor_name"] = vendor_details if vendor_details else "N/A"

        feedback["feedback_chat"] = frappe.get_all(
            "Feedback Response Table",
            filters={"parent": feedback["name"]},
            fields=["*"]
        )

    return feedback_entries

@frappe.whitelist(allow_guest=True)
def send_email_on_raising_complain(**kwargs):
    try:
        feedback_data = frappe._dict(kwargs)
        
        feedback_for = feedback_data.get("feedback_for")
        feedback_raised_by = feedback_data.get("feedback_raised_by")
        feedback_description = feedback_data.get("feedback_description")
        feedback_title = feedback_data.get("feedback_title")
        feedback_open_date = feedback_data.get("feedback_open_date")

        if not feedback_raised_by:
            return {"status": "error", "message": "Feedback raised by is required"}

        vendor_doc = frappe.get_value("Vendor Master", {"vendor_code": feedback_raised_by}, ["*"], as_dict=True)

        if not vendor_doc:
            return {"status": "error", "message": "Vendor not found"}

        vendor_name = vendor_doc.get("vendor_name")
        vendor_code = vendor_doc.get("vendor_code")
        vendor_email = vendor_doc.get("office_email_primary")
        registered_by = vendor_doc.get("registered_by")

        register_person = frappe.get_value("User Details", registered_by, ["team"])
        team_head = frappe.get_value("Team Master", register_person, ["reporting_head"])

        conf = frappe.conf
        smtp_server = conf.get("smtp_server")
        smtp_port = conf.get("smtp_port")
        smtp_user = conf.get("smtp_user")
        smtp_password = conf.get("smtp_password")

        from_address = "noreply@merillife.com"
        to_address = feedback_for
        cc_address = team_head
        bcc_address = "rishi.hingad@merillife.com"
        subject = f"New Complaint Raised: {feedback_title}"
        body = f"""
        Hello Team,

        A new complaint has been raised by {vendor_name} with {vendor_code}. Below are the details:

        - **Title**: {feedback_title}
        - **Description**: {feedback_description}
        - **Feedback For**: {feedback_for}
        - **Open Date**: {feedback_open_date}

        Regards,  
        Support Team
        """

        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg["CC"] = cc_address
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_address, [to_address, cc_address, bcc_address], msg.as_string())
                print("Email sent successfully!")

                doc = frappe.get_doc({
                    'doctype': 'Email Log',
                    'ref_no': feedback_raised_by,
                    'to_email': to_address,
                    'from_email': from_address,
                    'message': body,
                    'status': "Successfully Sent",
                    'screen': "Dispatch Order",
                    'created_by': from_address
                })
                doc.insert(ignore_permissions=True)
                frappe.db.commit()

        except Exception as e:
            print(f"Failed to send email: {e}")
            msge = f"Failed to send email: {e}"
            doc = frappe.get_doc({
                'doctype': 'Email Log',
                'ref_no': feedback_raised_by,
                'to_email': to_address,
                'from_email': from_address,
                'message': body,
                'status': msge,
                'screen': "Dispatch Order",
                'created_by': from_address
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

        return "Dispatch Order Email Sent Successfully."

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "send_email_on_dispatch Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_vendor_onboarding(ref_no):
    print("Get Vendor Onboarding Ref No-->",ref_no)
    if not frappe.has_permission("Vendor Onboarding", "read"):
        frappe.throw("Permission Denied")

    vendor_onboarding = frappe.get_all(
        'Vendor Onboarding',
        filters={'ref_no': ref_no},
        fields=['*']
    )

    # print("vendor_onboarding", vendor_onboarding)

    vendor_master = frappe.get_doc('Vendor Master', ref_no)
    company_name = ""
    vendor_types = []
    multiple_company_data = []

    if vendor_master:
        company_name = vendor_master.company_name

        vendor_types = [
            {
               "vendor_type" : row.vendor_type
            } for row in vendor_master.get("vendor_types", [])
        ]

        multiple_company_data = [
            {
                "company_name_mt": row.company_name_mt,
                "terms_of_payment_mt": row.terms_of_payment_mt,
                "purchase_group_mt": row.purchase_group_mt,
                "account_group_mt": row.account_group_mt,
                "purchase_organization_mt": row.purchase_organization_mt,
                "reconciliation_account_mt": row.reconciliation_account_mt
            } for row in vendor_master.get("multiple_company_data", [])
        ]

    if vendor_onboarding:
        number_of_employee = frappe.get_all(
            'Employee Number',
            filters={'parent': vendor_onboarding[0]['name']},
            fields=['*']
        )
        
        machinery_detail = frappe.get_all(
            'Machinery Detail',
            filters={'parent': vendor_onboarding[0]['name']},
            fields=['*']
        )
        
        banker_details = frappe.get_all(
            'Banker Details',
            filters={'parent': vendor_onboarding[0]['name']},
            fields=['*']
        )
        
        materials_supplied = frappe.get_all(
            'Supplied',
            filters={'parent': vendor_onboarding[0]['name']},
            fields=['*']
        )
        
        testing_detail = frappe.get_all(
            'Testing Facility',
            filters={'parent': vendor_onboarding[0]['name']},
            fields=['*']
        )
        
        reputed_partners = frappe.get_all(
            'Reputed Partners',
            filters={'parent': vendor_onboarding[0]['name']},
            fields=['*']
        )
        
        certificates = frappe.get_all(
            'Onboarding Certificates',
            filters={'parent': vendor_onboarding[0]['name']},
            fields=['*']
        )

        multiple_location_table = frappe.get_all(
            'Multiple Address',
            filters={'parent': vendor_onboarding[0]['name']},
            fields=['*']
        )
        
        vendor_onboarding[0]['number_of_employee'] = number_of_employee
        vendor_onboarding[0]['machinery_detail'] = machinery_detail
        vendor_onboarding[0]['banker_details'] = banker_details
        vendor_onboarding[0]['materials_supplied'] = materials_supplied
        vendor_onboarding[0]['testing_detail'] = testing_detail
        vendor_onboarding[0]['reputed_partners'] = reputed_partners
        vendor_onboarding[0]['certificates'] = certificates
        vendor_onboarding[0]['multiple_location_table'] = multiple_location_table
        vendor_onboarding = vendor_onboarding or [{}]
        vendor_onboarding[0]['company_name'] = company_name
        vendor_onboarding[0]['vendor_types'] = vendor_types
        vendor_onboarding[0]['multiple_company_data'] = multiple_company_data

        return vendor_onboarding
    else:
        return []


@frappe.whitelist(allow_guest=True)
def get_qms_form(ref_no):
    if not frappe.has_permission("Supplier QMS Assessment Form", "read"):
        frappe.throw("Permission Denied")

    qms_form = frappe.get_all(
        'Supplier QMS Assessment Form',
        filters={'ref_no': ref_no},
        fields=['*']
    )

    if qms_form:
        return qms_form
    else:
        return []

@frappe.whitelist()
def get_evaluation_form(vendor_ref_no):
    if not frappe.has_permission("Evaluation Form", "read"):
        frappe.throw("Permission Denied")

    evaluation_form = frappe.get_all('Evaluation Form', filters={'vendor_ref_no': vendor_ref_no}, fields=['*'])

    if evaluation_form:
        return evaluation_form
    else:
        return []


@frappe.whitelist(allow_guest=True)
def get_mlspl_assessment_form(vms_ref_no):
    if not frappe.has_permission("MLSPL Assessment Form", "read"):
        frappe.throw("Permission Denied")

    mlspl_form = frappe.get_all('MLSPL Assessment Form', filters={'vms_ref_no': vms_ref_no}, fields=['*'])

    if mlspl_form:
        return mlspl_form
    else:
        return []

@frappe.whitelist(allow_guest=True)
def get_diagno_approval_form(vms_ref_no):
    if not frappe.has_permission("Diagnostics Approval Form", "read"):
        frappe.throw("Permission Denied")

    diag_form = frappe.get_all('Diagnostics Approval Form', filters={'vms_ref_no': vms_ref_no}, fields=['*'])

    if diag_form:
        return diag_form
    else:
        return []

@frappe.whitelist()
def get_qms_counts():
    inprocess_qms_count = frappe.db.count("Supplier QMS Assessment Form", filters={'status': 'In Process'})
    approved_qms_count = frappe.db.count("Supplier QMS Assessment Form", filters={'status': 'Approved'})

    return {
        "inprocess_qms_count": inprocess_qms_count,
        "approved_qms_count": approved_qms_count
    }

@frappe.whitelist()
def fetch_vendor_and_qms_details(ref_no=None):
    vendor_query = """
        SELECT
            vm.name AS name,
            vm.website AS website,
            vm.office_email_primary AS office_email_primary,
            vm.first_name AS first_name,
            vm.last_name AS last_name,
            com.company_name AS company_name,
            com.company_code AS company_code,
            sm.state_name AS state_name,
            cnm.company_nature_name AS company_nature_name,
            bnm.business_nature_name AS business_nature_name,
            vt.vendor_type_name AS vendor_type_name,
            cn.country_name AS country_name,
            vm.type_of_business AS type_of_business,
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
            crt.certificate_name AS certificate_name,
            vm.valid_till AS valid_till,
            cm.status AS status,
            vm.ref_no AS ref_no,
            vm.vendor_name AS vendor_name,
            vm.telephone_number AS telephone_number
        FROM 
            `tabVendor Onboarding` vm 
        LEFT JOIN 
            `tabVendor Master` cm ON vm.ref_no = cm.name
        LEFT JOIN
            `tabCompany Master` com ON cm.company_name = com.name
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
            `tabCertificate Master` crt ON vm.certificate_name = crt.name
    """
    
    if ref_no:
        vendor_query += " WHERE vm.ref_no = %s"
        vendor = frappe.db.sql(vendor_query, ref_no, as_dict=1)
    else:
        vendor = frappe.db.sql(vendor_query, as_dict=1)

    qms_query = """
        SELECT * FROM `tabSupplier QMS Assessment Form`
    """

    if ref_no:
        qms_query += " WHERE ref_no = %s"
        qms_form = frappe.db.sql(qms_query, ref_no, as_dict=1)
    else:
        qms_form = frappe.db.sql(qms_query, as_dict=1)

    return {
        "vendor_details": vendor,
        "qms_form_details": qms_form
    }

@frappe.whitelist()
def check_email_exists(email):
    exists = frappe.db.exists("User", {"email": email})

    if exists:
        return {"exists": True, "message": "This email already exists."}
    
    verified_otp = frappe.db.get_value("OTP Verification", {"email": email, "is_verified": 1}, "otp")
    if verified_otp:
        return {"exists": False, "otp_sent": False, "message": "OTP is already verified for this email."}

    otp = random.randint(100000, 999999)
    otp_doc = frappe.get_doc({
        'doctype': 'OTP Verification',
        'email': email,
        'otp': otp,
        'is_verified': 0
    })
    otp_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    conf = frappe.conf
    smtp_server = conf.get("smtp_server")
    smtp_port = conf.get("smtp_port")
    smtp_user = conf.get("smtp_user")
    smtp_password = conf.get("smtp_password")
    from_address = "noreply@merillife.com"
    to_address = email
    bcc_address = "rishi.hingad@merillife.com"
    subject = "One-Time Password (OTP) for Email Verification"
    body = f"""
    <p>Dear User,</p>

    <p>Your One-Time Password (OTP) for Email Verification in Vendor Management System (VMS) Portal is: 
    <strong>{otp}</strong></p>

    <p>Please share this OTP to complete your email verification.</p>

    <p>Best regards,<br>VMS Team</p>
    """

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg["Bcc"] = bcc_address
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_address, [to_address,bcc_address], msg.as_string())
            print("Email Sent Successfully!!!")

        frappe.get_doc({
            'doctype': 'Email Log',
            'to_email': to_address,
            'from_email': from_address,
            'message': body,
            'status': "Successfully Sent",
            'screen': "Email Verification",
            'created_by': from_address
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        return {"exists": False, "otp_sent": True, "message": "OTP sent successfully."}

    except Exception as e:
        frappe.log_error(f"Failed to send OTP email: {e}")
        return {"exists": False, "otp_sent": False, "message": "Failed to send OTP."}


@frappe.whitelist()
def verify_email_otp(email, otp):
    """Verify OTP entered by the user"""
    otp_record = frappe.db.get_value("OTP Verification", {"email": email}, "otp")

    if otp_record and str(otp_record) == str(otp):
        frappe.db.delete("OTP Verification", {"email": email})
        frappe.db.commit()
        return {"verified": True, "message": "OTP verified successfully."}
    
    return {"verified": False, "message": "Invalid OTP, please try again."}


@frappe.whitelist()
def show_vendor_registration_details(**kwargs):
    name = kwargs.get('name')

    vendor = frappe.db.sql(
        """
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
            vm.purchase_organization AS purchase_organization,
            pom.purchase_organization_name AS purchase_organization_name,
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
            cmm.company_code AS company_code,
            vm.vendor_title AS vendor_title,
            vm.qa_required AS qa_required
        FROM
            `tabVendor Master` vm
        LEFT JOIN
            `tabVendor Type Master` vt ON vm.vendor_type = vt.name
        LEFT JOIN
            `tabAccount Group Master` at ON vm.account_group = at.name
        LEFT JOIN
            `tabDepartment Master` dp ON vm.department = dp.name
        LEFT JOIN
            `tabOld Material Master` mt ON vm.material_to_be_supplied = mt.name
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
            `tabCompany Master` cmm ON vm.company_name = cmm.name
        LEFT JOIN
            `tabCity Master` cty ON vm.city = cty.name
        LEFT JOIN
            `tabState Master` st ON vm.state = st.name
        LEFT JOIN
            `tabCountry Master` cnt ON vm.country = cnt.name
        LEFT JOIN
            `tabDistrict Master` dst ON vm.district = dst.name
        LEFT JOIN
            `tabPincode Master` pin ON vm.pincode = pin.name
        LEFT JOIN
            `tabPurchase Organization Master` pom ON vm.purchase_organization = pom.name
        WHERE
            vm.name = %s
        """,
        (name,), as_dict=1
    )

    multiple_company_data = frappe.db.sql(
        """
        SELECT
            mcd.name,
            mcd.company_name,
            mcd.purchase_organization,
            mcd.account_group,
            mcd.terms_of_payment,
            mcd.purchase_group,
            mcd.company_name_mt,
            mcd.purchase_organization_mt,
            mcd.account_group_mt,
            mcd.terms_of_payment_mt,
            mcd.purchase_group_mt
        FROM
            `tabMultiple Company Data` mcd
        WHERE
            mcd.parent = %s
        """, (name,), as_dict=True
    )

    for entry in multiple_company_data:
        if not entry.get("company_name"):
            entry["company_name"] = frappe.db.get_value(
                "Company Master", {"company_code": entry["company_name_mt"]}, "company_name"
            )
        if not entry.get("purchase_organization"):
            entry["purchase_organization"] = frappe.db.get_value(
                "Purchase Organization Master", {"purchase_organization_code": entry["purchase_organization_mt"]}, "purchase_organization_name"
            )
        if not entry.get("account_group"):
            entry["account_group"] = frappe.db.get_value(
                "Account Group Master", {"acccount_group_code": entry["account_group_mt"]}, "account_group_name"
            )
        if not entry.get("terms_of_payment"):
            entry["terms_of_payment"] = frappe.db.get_value(
                "Terms Of Payment Master", {"terms_of_payment_code": entry["terms_of_payment_mt"]}, "terms_of_payment_name"
            )
        if not entry.get("purchase_group"):
            entry["purchase_group"] = frappe.db.get_value(
                "Purchase Group Master", {"purchase_group_code": entry["purchase_group_mt"]}, "purchase_group_name"
            )

    vendor_types = frappe.db.sql(""" 
        SELECT * FROM `tabVendor Type Group` WHERE parent = %s 
    """, (name), as_dict=1)

    result = {
        'vendor_details': vendor,
        'multiple_company_data': multiple_company_data,
        'vendor_types': vendor_types
    }

    return result



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
        comp.company_name AS company_name,
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
            `tabOld Material Master` mm ON rfq.material = mm.name
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

@frappe.whitelist()
def show_rfq_detail(rfq_number):

    rfq = frappe.db.sql(""" 

        SELECT
        rfq.name AS rfq_number,
        prt4.port_name AS destination_port,
        rfq.meril_invoice_date AS meril_invoice_date,
        vt.vendor_type_name AS vendor_type_name,
        rfq.rfq_cutoff_date AS rfq_cutoff_date,
        comp.company_name AS company_name,
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
            `tabOld Material Master` mm ON rfq.material = mm.name
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

@frappe.whitelist()
def show_vendor_registration_details_filtered(**kwargs):
    status = kwargs.get('status')
    values_type = kwargs.get('values_type')

    if values_type == 'creation':
        order_by_clause = 'vm.creation DESC'
    elif values_type == 'modified':
        order_by_clause = 'vm.modified DESC'
    else:
        order_by_clause = 'vm.creation DESC'

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
        LEFT JOIN `tabOld Material Master` mt ON vm.material_to_be_supplied = mt.name
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
    vendor_code AS vendor_code,
    vendor_name AS vendor_name,
    office_email_primary AS office_email_primary,
    cm.company_name AS company_name,
    cm.company_code AS company_code,
    us.full_name AS registered_by_name,
    country AS country,
    search_term AS search_term,
    registered_by AS registered_by
                                
    FROM 
        `tabVendor Master` vm
    LEFT JOIN
        `tabUser` us ON vm.registered_by = us.email
    LEFT JOIN 
        `tabCompany Master` cm ON vm.company_name = cm.name 
    WHERE 
    status='Onboarded'
    ORDER BY 
        vm.modified DESC

    """, as_dict=1)

    for vendor in all_vendors:
        child_data = frappe.db.sql("""
            SELECT 
                mcd.company_name_mt, 
                cm.company_name 
            FROM 
                "tabMultiple Company Data" mcd 
            LEFT JOIN 
                "tabCompany Master" cm ON mcd.company_name_mt = cm.name
            WHERE 
                mcd.parent = %s
        """, (vendor['name'],), as_dict=1)

        vendor_types = frappe.db.sql("""
            SELECT
                vt.vendor_type       
            FROM
                "tabVendor Type Group" vt
            WHERE
                vt.parent = %s
        """, (vendor['name'],), as_dict=1)
        
        vendor['multiple_company_data'] = child_data
        vendor['vendor_types'] = vendor_types

    return all_vendors

@frappe.whitelist()
def onboarded_vendors_team():
    all_vendors = frappe.db.sql("""
        SELECT
            vm.name AS name,
            status AS status,
            vendor_code AS vendor_code,
            vendor_name AS vendor_name,
            office_email_primary AS office_email_primary,
            cm.company_name AS company_name,
            cm.company_code AS company_code,
            us.full_name AS registered_by_name,
            us.team AS team,
            country AS country,
            search_term AS search_term,
            registered_by AS registered_by
        FROM 
            `tabVendor Master` vm
        LEFT JOIN
            `tabUser` us ON vm.registered_by = us.email
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name 
        WHERE 
            status='Onboarded'
        ORDER BY 
            vm.modified DESC
    """, as_dict=1)

    for vendor in all_vendors:
        child_data = frappe.db.sql("""
            SELECT 
                mcd.company_name_mt, 
                cm.company_name 
            FROM 
                `tabMultiple Company Data` mcd 
            LEFT JOIN 
                `tabCompany Master` cm ON mcd.company_name_mt = cm.name
            WHERE 
                mcd.parent = %s
        """, (vendor['name'],), as_dict=1)

        vendor_types = frappe.db.sql("""
            SELECT
                vt.vendor_type       
            FROM
                `tabVendor Type Group` vt
            WHERE
                vt.parent = %s
        """, (vendor['name'],), as_dict=1)
        
        vendor['multiple_company_data'] = child_data
        vendor['vendor_types'] = vendor_types

    grouped_vendors = {}
    for vendor in all_vendors:
        team = vendor.get('team', 'Unknown')
        if team not in grouped_vendors:
            grouped_vendors[team] = {
                "team": team,
                "total_vendors": 0,
                "vendors": []
            }
        grouped_vendors[team]["total_vendors"] += 1
        grouped_vendors[team]["vendors"].append(vendor)

    return list(grouped_vendors.values())


@frappe.whitelist()
def onboarded_vendors_qa():

    all_vendors = frappe.db.sql(""" SELECT
    vm.name AS name,
    status AS status,
    vendor_code AS vendor_code,
    vendor_name AS vendor_name,
    office_email_primary AS office_email_primary,
    cm.company_name AS company_name,
    cm.company_code AS company_code,
    us.full_name AS registered_by,
    country AS country,
    search_term AS search_term
                                
    FROM 
        `tabVendor Master` vm
    LEFT JOIN
        `tabUser` us ON vm.registered_by = us.email
    LEFT JOIN 
        `tabCompany Master` cm ON vm.company_name = cm.name 
    WHERE 
    status='Onboarded'
    AND cm.company_code IN ('2000', '7000')
    ORDER BY 
        vm.modified DESC

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


@frappe.whitelist(allow_guest=True)
def sap_fetch_token(name):

    name = name
    print("*************This is name in the starting of the SAP Fetch Token********************", name)
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
        `tabOld Material Master` mt ON vm.material_to_be_supplied = mt.name
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

    termsid = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['terms_of_payment'])
    terms = frappe.db.get_value("Terms Of Payment Master", filters={'name': termsid}, fieldname=['terms_of_payment_code'])
    print("****************%%%%%%%%%%% TERMS %%%%%%%%%%%%%%%%%***************************", terms, termsid)
   # email_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary'])
    reconcileid = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['reconciliation_account'])
    reconciliation_number = frappe.get_value("Reconciliation Account", filters={'name': reconcileid}, fieldname=['num'])
    #company_code = vendor[0].get('company_code') if vendor else None
    company_id = frappe.db.get_value("Vendor Master", filters={"name": name}, fieldname=['company_name'])
    company_code = frappe.db.get_value("Company Master", filters={"name": company_id}, fieldname=['company_code'])
    sap_code = frappe.db.get_value("Company Master", filters={"name": company_id}, fieldname=['sap_client_code'])
    purchase_organization_code = vendor[0].get('purchase_organization_code') if vendor else None
    # account_group_name = vendor[0].get('account_group_name') if vendor else None
    vendor_name = vendor[0].get('vendor_name') if vendor else None
    search_term = vendor[0].get('search_term') if vendor else None
    # office_address_line_1 = vendor[0].get('office_address_line_1') if vendor else None
    pincode = vendor[0].get('pincode') if vendor else None
    city = vendor[0].get('city_name') if vendor else None
    #country_name = vendor[0].get('country_code') if vendor else None
    country_key = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['country'])
    country_name = frappe.db.get_value("Country Master", filters={'name': country_key}, fieldname=['country_code']) 
    state_key = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['state'])
    state_name = frappe.db.get_value("State Master", filters={'name': state_key}, fieldname=['sap_state_code']) 
    mobile_number = vendor[0].get('mobile_number') if vendor else None
    office_email_primary = vendor[0].get('office_email_primary') if vendor else None
    office_email_secondary = vendor[0].get('office_email_secondary') if vendor else None
    currency_code = vendor[0].get('currency_code') if vendor else None
    incokey = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['incoterms'])
    print("************************************* INCO TERMS AND SAP CODE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", incokey, sap_code)
    incoterms = frappe.db.get_value("Incoterm Master", filters={'name': incokey}, fieldname=['incoterm_code', 'incoterm_name'])
    purchase_group_name = vendor[0].get('purchase_group_name') if vendor else None
    gst_number = vendor[0].get('gst_number') if vendor else None
    vendor_type_name = vendor[0].get('vendor_type_name') if vendor else None
    pan_number = vendor[0].get('pan_number') if vendor else None
    bank_name = vendor[0].get('bank_name') if vendor else None
    account_number = vendor[0].get('account_number') if vendor else None
    # state_name = vendor[0].get('state_name') if vendor else None
    address = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['address_line_1', 'address_line_2'])
    #bank_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['bank1'])
    #bank_ifsc = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['ifsc_code', 'bank_name'])
    bank_id = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['bank_name'])
    # name_of_account_holder = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['name_of_account_holder'])
    bank = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['bank_name', 'ifsc_code', 'bank_code',])
    bankl_value = bank[2] if bank is not None and len(bank) > 2 else ""
    bkref_value = bank[0] if bank is not None and len(bank) > 2 else ""
    banka_value = bank[1] if bank is not None and len(bank) > 2 else ""
    # INTERNATIONAL BANK DETAILS ===================================================>
    benf_name = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_name']) or ""
    benf_bank_name = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_bank_name']) or ""
    benf_account_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_account_no']) or ""
    benf_swift_code = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_bank_swift_code']) or ""
    benf_ach_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_ach_no']) or ""
    benf_aba_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_aba_no']) or ""
    benf_iban_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_iban_no']) or ""
    benf_routing_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_routing_no']) or ""
    benf_add = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['beneficiary_bank_address']) or ""
    benf_bank_add = frappe.db.get_value("Country Master", filters={'name': benf_add}, fieldname=['country_code']) or ""
    # INTERMEDIATE BANK DETAILS ======================================================>
    intr_bank_name = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['intermediate_bank_name']) or ""
    intr_account_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['intermediate_account_no']) or ""
    intr_swift_code = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['intermediate_bank_swift_code']) or ""
    intr_ach_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['intermediate_ach_no']) or ""
    intr_aba_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['intermediate_aba_no']) or ""
    intr_iban_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['intermediate_iban_no']) or ""
    intr_routing_no = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['intermediate_routing_no']) or ""
    intr_add = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['intermediate_bank_address']) or ""
    intr_bank_add = frappe.db.get_value("Country Master", filters={'name': intr_add}, fieldname=['country_code']) or ""
    account_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['account_group'])
    account_code = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['acccount_group_code'])
    purchase_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_groupm'])
    purchase_code = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_id}, fieldname=['purchase_group_code'])
    flname = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['first_name', 'last_name'])
    print("&&&&&&&&&&&&&&& Reconciliation Number &&&&&&&&&&&&&&&&&&&&&&&&&&", reconcileid,reconciliation_number, company_code, country_name, bank, state_name)
    json_data = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['payee', 'gr_based_inv_ver', 'service_based_inv_ver', 'check_double_invoice'])
    print("############################## Checkbox Data ############", json_data)
    payee_in_document, gr_based_inv_ver, service_based_inv_ver, check_double_invoice = json_data
    payee = 'X' if payee_in_document == 1 else ''
    gr_based_inv_ver = 'X' if gr_based_inv_ver == 1 else ''
    service_based_inv_ver = 'X' if service_based_inv_ver == 1 else ''
    check_double_invoice = 'X' if check_double_invoice == 1 else ''
    print(f"Payee: {payee}, GR Based Invoice Verification: {gr_based_inv_ver}, Service Based Invoice Verification: {service_based_inv_ver}, Check Double Invoice: {check_double_invoice}")
    mylist = [payee, gr_based_inv_ver, service_based_inv_ver, check_double_invoice]
    print("*********** MYLIST & Name ***********", mylist, name)
    val = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['city', 'state', 'pincode', 'gst_number', 'company_pan_number', 'account_number'])
    bankn_value = val[5] if val is not None and len(val) > 2 else ""
    pincode_no = frappe.db.get_value("Pincode Master", filters={'name': val[2] }, fieldname=['pincode'])
    child_table_entries = frappe.get_all("Multiple Company Data", filters={'parent': name}, fields=['company_name_mt', 'account_group_mt', 'purchase_organization_mt', 'purchase_group_mt', 'reconciliation_account_mt', 'terms_of_payment_mt'])
    data_list = []
    if child_table_entries:
        for entry in child_table_entries:
            company_code_mt = frappe.db.get_value("Company Master", filters={'company_code': entry.get('company_name_mt')}, fieldname=['company_code'])
            sap_code_mt = frappe.db.get_value("Company Master", filters={'company_code': entry.get('company_name_mt')}, fieldname=['sap_client_code'])
            account_group_code_mt = frappe.db.get_value("Account Group Master", filters={'name': entry.get('account_group_mt')}, fieldname=['acccount_group_code'])
            reconciliation_account_mt = frappe.db.get_value("Reconciliation Account", filters={'name': entry.get('reconciliation_account_mt')}, fieldname=['num'])
            purchase_group_code_mt = frappe.db.get_value("Purchase Group Master", filters={'name': entry.get('purchase_group_mt')}, fieldname=['purchase_group_code'])
            purchase_org_code_mt = frappe.db.get_value("Purchase Organization Master", filters={'name': entry.get('purchase_organization_mt')}, fieldname=['purchase_organization_code'])
            terms_of_payment_mt = frappe.db.get_value("Terms Of Payment Master", filters={'name': entry.get('terms_of_payment_mt')}, fieldname=['terms_of_payment_code'])

        if sap_code_mt:
            data = {
                "Bukrs": company_code_mt,
                "Ekorg": purchase_org_code_mt,
                "Ktokk": account_group_code_mt,
                "Title": "",
                "Name1": vendor_name,
                "Name2": "",
                "Sort1": search_term,
                "Street": address[0],
                "StrSuppl1": address[1],
                "StrSuppl2": "",
                "StrSuppl3": "",
                "PostCode1": pincode_no,
                "City1": val[0],
                "Country": country_name,
                "J1kftind": "",
                "Region": state_name,
                "TelNumber": "",
                "MobNumber": mobile_number,
                "SmtpAddr": office_email_primary,
                "SmtpAddr1": office_email_secondary,
                "Zuawa": "",
                "Akont": reconciliation_account_mt,
                "Waers": currency_code,
                "Zterm": terms_of_payment_mt,
                "Inco1": incoterms[0],
                "Inco2": incoterms[1],
                "Kalsk": "",
                "Ekgrp": purchase_group_code_mt,
                "Xzemp": payee,
                "Reprf": check_double_invoice,
                "Webre": gr_based_inv_ver,
                "Lebre": service_based_inv_ver,
                "Stcd3": val[3],
                "J1ivtyp": vendor_type_name,
                "J1ipanno": val[4],
                "J1ipanref": vendor_name,
                "Namev": flname[0],
                "Name11": flname[1],
                "Bankl": bankl_value,
                "Bankn": val[5],
                "Bkref": bkref_value,
                "Banka": banka_value,
                "ZZBENF_NAME": benf_name,
                "ZZBEN_BANK_NM": benf_bank_name,
                "ZZBEN_ACCT_NO": benf_account_no,
                "ZZBENF_IBAN": benf_iban_no,
                "ZZBENF_BANKADDR": benf_bank_add,
                "ZZBENF_SHFTADDR": benf_swift_code,
                "ZZBENF_ACH_NO": benf_ach_no,
                "ZZBENF_ABA_NO": benf_aba_no,
                "ZZBENF_ROUTING": benf_routing_no,
                "ZZINTR_ACCT_NO": intr_account_no,
                "ZZINTR_IBAN": intr_iban_no,
                "ZZINTR_BANK_NM": intr_bank_name,
                "ZZINTR_BANKADDR": intr_bank_add,
                "ZZINTR_SHFTADDR": intr_swift_code,
                "ZZINTR_ACH_NO": intr_ach_no,
                "ZZINTR_ABA_NO": intr_aba_no,
                "ZZINTR_ROUTING": intr_routing_no,
                "Refno": name,
                "Vedno": "",
                "Zmsg": ""
            }
            data_list.append(data)
    else:
        if sap_code: 
            data =  {
            "Bukrs": company_code,
            "Ekorg": purchase_organization_code,
            "Ktokk": account_code,
            "Title": "",
            "Name1": vendor_name,
            "Name2": "",
            "Sort1": search_term,
            "Street": address[0],
            "StrSuppl1": address[1],
            "StrSuppl2": "",
            "StrSuppl3": "",
            "PostCode1": pincode_no,
            "City1": val[0],
            "Country": country_name,
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
            "Inco1": incoterms[0],
            "Inco2": incoterms[1],
            "Kalsk": "",
            "Ekgrp": purchase_code,
            "Xzemp": payee,
            "Reprf": check_double_invoice,
            "Webre": gr_based_inv_ver,
            "Lebre": service_based_inv_ver,
            "Stcd3": val[3],
            "J1ivtyp": vendor_type_name,
            "J1ipanno": val[4],
            "J1ipanref": vendor_name,
            "Namev": flname[0],
            "Name11": flname[1],
            "Bankl": bankl_value,
            "Bankn": val[5],
            "Bkref": bkref_value,
            "Banka": banka_value,
            # "koinh": name_of_account_holder,
            "Xezer": "",
            "ZZBENF_NAME" : benf_name,
            "ZZBEN_BANK_NM" : benf_bank_name,
            "ZZBEN_ACCT_NO" : benf_account_no,
            "ZZBENF_IBAN" : benf_iban_no,
            "ZZBENF_BANKADDR" : benf_bank_add,
            "ZZBENF_SHFTADDR" : benf_swift_code,
            "ZZBENF_ACH_NO" : benf_ach_no,
            "ZZBENF_ABA_NO" : benf_aba_no,
            "ZZBENF_ROUTING" : benf_routing_no,
            "ZZINTR_ACCT_NO" : intr_account_no,
            "ZZINTR_IBAN" : intr_iban_no,
            "ZZINTR_BANK_NM" : intr_bank_name,
            "ZZINTR_BANKADDR" : intr_bank_add,
            "ZZINTR_SHFTADDR" : intr_swift_code,
            "ZZINTR_ACH_NO" : intr_ach_no,
            "ZZINTR_ABA_NO" : intr_aba_no,
            "ZZINTR_ROUTING" : intr_routing_no,
            "Refno": name,
            "Vedno": "",
            "Zmsg": ""
                }
            data_list.append(data)
            
            print("************** Before URL JSON DATA *****************", data)
            url = f"http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client={sap_code}"
            print("******************* First URL *************", url)
            headers = {
                'X-CSRF-TOKEN': 'Fetch',
                'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ=',
                'Content-Type': 'application/json'
                }
            auth = HTTPBasicAuth('WF-BATCH ', 'M@wb#$%2024')
            response = requests.get(url, headers=headers, auth=auth)
        
            if response.status_code == 200:
                print("****** GET CSRF TOKEN *********")
                csrf_token = response.headers.get('x-csrf-token')
                key1 = response.cookies.get(f'SAP_SESSIONID_BHD_{sap_code}')
                key2 = response.cookies.get('sap-usercontext')
                
                # Sending details to SAP
                send_detail(csrf_token, data, key1, key2, name, sap_code)
                print("*********** KEY1 ***********", key1)
                print("*********** KEY2 ***********", key2)
                print("$$$$$$$$$$$ CSRF TOKEN $$$$$$$$$$$$$$$$$$",csrf_token)
                print("*********** JSON DATA ************", data)
                print(response.headers.get('x-csrf-token'))
                return data
            else:
                frappe.log_error(f"Failed to fetch CSRF token from SAP: {response.status_code if response else 'No response'}")
                return None
        else:
            frappe.log_error(f"No company_code or sap_code found for company: {company_code}")
            return None

#******************************* SAP PUSH  ************************************************************

@frappe.whitelist(allow_guest=True)
def send_detail(csrf_token, data, key1, key2, name, sap_code):

    url = f"http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client={sap_code}"
    key1 = key1
    key2 = key2
    name = name
    #pdb.set_trace()
    headers = {

        'X-CSRF-TOKEN': csrf_token,
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json',
        'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ=',
        'Cookie': f"SAP_SESSIONID_BHD_{sap_code}={key1}; sap-usercontext={key2}"
    }
    auth = HTTPBasicAuth('WF-BATCH ', 'M@wb#$%2024')
    print("*************")
    
    try:
        response = requests.post(url, headers=headers, auth=auth ,json=data)
        print("****************** RESPONSE ************",response)
        print("********* STATUS CODE *****************", response.json(), response.status_code)
        #return response.json()
        vendor_sap_code = response.json()
        print("********** Here is the vendor_sap_code **********", vendor_sap_code)
        vendor_code = vendor_sap_code['d']['Vedno']
        print("********** Here is the Vendor Code ****************", vendor_code)
        
        print("**************** Name after Vendor Code **************",name)

        frappe.db.sql(""" UPDATE `tabVendor Master` SET vendor_code=%s where name=%s """, (vendor_code, name))
        frappe.db.commit()
        
        return response.json()
    except ValueError:
        print("************************** Response is here *********************", response.json())
    
    
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

#**********************************************************************************************************************
@frappe.whitelist()
def validate_aadhar_number():
    pass


@frappe.whitelist()
def create_po(**kwargs):
    pass

@frappe.whitelist()
def vendor_onboarding(**kwargs):
    pass

@frappe.whitelist()
def show_vendor(data, method):

    name = data.get("name")
    values = frappe.db.sql(""" select * from `tabVendor Onboarding` where name=%s """,(name),as_dict=1)
    return values






# echo 'ssh-ed25519-cert-v01@openssh.com AAAAIHNzaC1lZDI1NTE5LWNlcnQtdjAxQG9wZW5zc2guY29tAAAAINBktpfqe6qD4XwtAv0Cp1dH1I4l+004UXrKFStwIZeAAAAAIKwnllF0rPJjt/hlwAN8bZiF6j1XlfLesLKTfIA1ABWcAAAAAAAAABMAAAABAAAAFmNoaW5tYXlAaHlicm93bGFicy5jb20AAAAOAAAACmJlbmNoLTAwMTQAAAAAaEgJoAAAAABoSF5pAAAAAAAAABIAAAAKcGVybWl0LXB0eQAAAAAAAAAAAAACFwAAAAdzc2gtcnNhAAAAAwEAAQAAAgEA197ObD5rz9BhSDk9PjBOEO3WVwXOWvCvbsiZUK9nWgAx+qMba2INurMjiJhtuJtKFIY/WB2USVUdaDtEf9qM1ZD0fL9RUxSVXBRpKLZ8WXD9hRapOP4SSPAC6c7aHCH+Gzx3ihf3P3bwwCc5A1OJrTjoZtMmw1wiOlNtsAVtCaFLBp9IL+wrrUVXfINreKE8gKWIDTUYXyGe4hz+hTdA0vmWejjvXtzzLJcutIOrAmZGHGjQF/pya/+Cmbew8PLe9Z93PdzgSrU1YFW8FhUjHVh871w2cD2poxjwYvGMOE7waPIrfksDdqQHX0cJVxPPIH4RBOH5U3N1Oqw1oeadXTfTitcbzxWhX49g1jXLD9SAq022OT5CXy0F9ITTFYAtdMrKgVNOBN1YVR5HqsfuOHJEkz6thv+Hz9KcpyjwjWiWfASbA4G3R5wYR/cy9VkN0JTvKPV/aG6qI4p6gKQzzGew1OQooyBeP7xwws5Kb3LTyPX2Eb1sDjdXsDxKugMh8FEOtQV6JHCuHGmlK6M2On154vk6tXSfMk0VlZktYLe4oCkYHpolxX1oFO2iykeP3+++oEsgKupTQJnSvD5m5HQBFobBNr96hRfmZ6Xx0oX6Xi45bd01s0PavSW1n4Rb5hp+6ZX+jAl/RwUGkTgfWwsbepA4zGIg7rdZ7it+j28AAAIUAAAADHJzYS1zaGEyLTUxMgAAAgAjxsjgHLeJf6hWUlUKjw5RGPlHCZ85SmAU38JtBO7Pme0TIYO74TtGNmwYeWb68j/WTpyfSn3HPIUrNMIHsptN0mp1Tg4LdRKS8OuJi3521KyJwzEpH+CrmGOGWQCz7CsVCExQT+v9yEp4A0yxIn9ZYT8R0BAVLEOh8Gd3zPiWdY7GXajBnsiMy/UvbxMuCabCLvtyIzio1ush7wP+5EXhdUdbMjGgKchYWH+VVZX0yxa3txrcjv0FZGpdJBtRI6jeAXCZP4BcFuWfJ1VPEasfEVBs3b4EgzAOe21sjsMwmTC36ngN+F4M4vadq93kysOktA74cFhOUiirk+cOu+btXsDiON6lX0oR7hLU702cATusEzwI5pIgh/Pc+cnAj4tipAnsvNDU3Hpx0jj8TKAQPBezE5w0dvnMQPlG8L+SqQYB6bpSHctjgVeBSwEiNKVPgb5/x2MC0qJ/0FX7o7iCAbRouWeeTLsdy5mH0Ma3r/VO0e4HIhI8b3Bb5xea09/o9r2zUyclSf2zkh6TehXqLk0Ns+oLwjtVspDgw9uOccwHwE+OHKODocgsWQKxddiv2wcYJyBS6mJ+s3VJpJdgNfCwU1gUm1RZhebYRMMdsBqNdTKPPTNgU367lpvdZFId8ypFOzyu9uE2AiZEQUnouGA/j/Ge40LN0yWGx0pEuQ== 41504211+grawish@users.noreply.github.com' > ~/.ssh/id_ed25519-cert.pub




# ssh bench-0014-000057-f1-dev@n1-india.bilakhiagroup.com -p 2222