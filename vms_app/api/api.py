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





# @frappe.whitelist(allow_guest=True)
# def get_all(**kwargs):
#     all = frappe.db.sql(""" select * from s """,allow_guest=True)



@frappe.whitelist(allow_guest=True)
def token():
    print("*******************************************************")
    return frappe.local.session.data.csrf_token

@frappe.whitelist(allow_guest=True)
def is_user_logged_in(email):
    user_session = frappe.db.exists('User', {'email': email, 'last_login': ['!=', None]})
    if user_session:
        return {"message": "User is logged in"}
    else:
        return {"message": "User is not logged in"}




obj = SendEmail()



@frappe.whitelist(allow_guest=True)
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


@frappe.whitelist(allow_guest=True)
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

    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)
    print("***********************************************")
    user_designation_id = frappe.db.get_value("User", filters={'email': user.email}, fieldname='designation')
    print(user_designation_id)
    user_designation_name = frappe.db.get_value("Designation Master", filters={'name': user_designation_id}, fieldname='designation_name')
    print(user_designation_name)
    frappe.response["message"] = {

        "success_key":1,
        "message":"Authentication success",
        'designation_name': user_designation_name,
        "sid":frappe.session.sid,
        "api_key":user.api_key,
        "api_secret":api_generate,
        "username":user.username,
        "email":user.email

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
def send_email(data, method):
    frappe.db.sql(""" update `tabVendor Master` set purchase_team_approval='In Process' """ )
    frappe.db.commit()
    frappe.db.sql(""" update `tabVendor Master` set purchase_head_approval='In Process' """ )
    frappe.db.commit()
    frappe.db.sql(""" update `tabVendor Master` set accounts_team_approval='In Process' """ )
    frappe.db.commit()
    print("*********************Hi from Docevents*****************")
    print(frappe.session.user)
    current_user = frappe.session.user
    current_user_email = frappe.db.get_value("User", filters={'full_name': current_user}, fieldname='email')
    print(current_user_email)
    frappe.db.sql(" update `tabVendor Master` set registered_by=%s ",(current_user_email))
    frappe.db.commit()
    reciever_email = data.get("office_email_primary")
    print(reciever_email)
    smtp_server = "smtp.transmail.co.in"
    smtp_port = 587
    smtp_user = "emailapikey"  
    smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
    from_address = current_user_email 
    to_address = reciever_email  
    subject = "Test email"
    body = "You have been Successfully Registered on the VMS Portal. PLease complete the On boarding process ."
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
def send_email_on_onboarding(data, method):

    print("***********Details filled***********")
    current_user_email = data.get('office_email_primary')
    print(current_user_email)
    company_name = data.get('company_name')
    print(company_name)
    reciever_email = frappe.db.get_value("Vendor Master", filters={'company_name': company_name}, fieldname=['registered_by'])
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
    body = "This is a Test email ...!"
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





@frappe.whitelist(allow_guest=True)
def hitt(data, method):
    print("****************Hi there!*******************")
    vendor_type_id = data.get('select_service')
    vendors = frappe.db.sql(""" select office_email_primary from `tabVendor Onboarding` where vendor_type=%s """,(vendor_type_id))
    email_id_of_rfq_creator = frappe.session.user
    print("*******************************************************")
    print(email_id_of_rfq_creator)
    email_addresses = [vendor[0] for vendor in vendors]
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&",email_addresses)
    smtp_server = "smtp.transmail.co.in"
    smtp_port = 587
    smtp_user = "emailapikey"  
    smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
    from_address = "noreply@merillife.com" 
    subject = "Test email"
    body = "This is a Test email to Vendor regarding RFQ ...!"
    for to_address in email_addresses:
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





@frappe.whitelist(allow_guest=True)
def send_email_on_po_creation(data, method):

    po_creator = frappe.session.user
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
    body = "Purchase Order has been created please check on the VMS Portal for more details ."
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
def set_vendor_onboarding_status(**kwargs):
    name = kwargs.get("name")
    current_user = frappe.session.user
    current_user_designation_key = frappe.db.get_value("User", filters={'email': current_user}, fieldname='designation')
    current_user_designation_name = frappe.db.get_value("Designation Master", filters={'name': current_user_designation_key}, fieldname=['designation_name'])
    print("*******************************************")
    vendor_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='office_email_primary')
    print(vendor_email)
    
    if current_user_designation_name == "Accounts Team":
        frappe.db.sql(""" update `tabVendor Master` set accounts_team_approval='Approved' """ )
        frappe.db.commit()
        registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')
        smtp_server = "smtp.transmail.co.in"
        smtp_port = 587
        smtp_user = "emailapikey"  
        smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
        from_address = registered_by_email 
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
        except Exception as e:
            print(f"Failed to send email: {e}")

    if current_user_designation_name == "Purchase Team":
        frappe.db.sql(""" update `tabVendor Master` set purchase_team_approval='Approved' """ )
        frappe.db.commit()
        registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')
        smtp_server = "smtp.transmail.co.in"
        smtp_port = 587
        smtp_user = "emailapikey"  
        smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
        from_address = registered_by_email 
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
        except Exception as e:
            print(f"Failed to send email: {e}")

    if current_user_designation_name == "Purchase Head":
        frappe.db.sql(""" update `tabVendor Master` set purchase_head_approval='Approved' """ )
        frappe.db.commit()
        registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname='registered_by')
        smtp_server = "smtp.transmail.co.in"
        smtp_port = 587
        smtp_user = "emailapikey"  
        smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
        from_address = registered_by_email 
        to_address = vendor_email  
        subject = "Test email"
        body = "Yourequest has been approved Purchase Head ."
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

        return registered_by_email


@frappe.whitelist(allow_guest=True)
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


@frappe.whitelist(allow_guest=True)
def compare_quotation(**kwargs):

    rfq_number = kwargs.get("rfq_number")
    orderd_list = frappe.db.sql(""" SELECT * FROM `tabQuotation` WHERE rfq_number = %s AND creation IN (SELECT MAX(creation) FROM `tabQuotation` WHERE rfq_number = %s GROUP BY vendor_code) ORDER BY creation ASC""",(rfq_number, rfq_number), as_dict=True)
    for quotation in orderd_list:
        
        product_code = frappe.db.get_value("Product Master", filters={"name": quotation.product_code}, fieldname="product_code")
        
        quotation["product_code"] = product_code

    return orderd_list



@frappe.whitelist(allow_guest=True)
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


@frappe.whitelist(allow_guest=True)
def test_method(self, method):
    if self.file_name:
        file_doc = frappe.get_doc("File", {"file_url": self.file_name})
        frappe.msgprint(f"File URL: {file_doc.file_url}")
            


@frappe.whitelist(allow_guest=True)
def test_method(self, method):
    if self.file_name:
       
        file_path = frappe.get_site_path(self.file_name.lstrip("/"))

    
        if os.path.exists(file_path):
            frappe.msgprint("File exists.")
        else:
            frappe.msgprint("File does not exist.")

        
        file_doc = frappe.get_doc("File", {"file_url": self.file_name})
        frappe.msgprint(f"File URL: {file_doc.file_url}")



@frappe.whitelist(allow_guest=True)
def total_vendors():
    total_vendors = frappe.db.sql(""" select count(*) from `tabVendor Master` """,as_dict=1)
    return total_vendors

@frappe.whitelist(allow_guest=True)
def total_in_process_vendors():

    total_in_process_vendors = frappe.db.sql(""" select count(*) from `tabVendor Master` where status='In Process' """,as_dict=1)
    return total_in_process_vendors

@frappe.whitelist(allow_guest=True)
def inprocess_vendor_detail():
    total_in_process_vendors = frappe.db.sql(""" select * from `tabVendor Master` where status='In Process' """,as_dict=1)
    return total_in_process_vendors




@frappe.whitelist(allow_guest=True)
def total_onboarded_vendors():

    total_in_process_vendors = frappe.db.sql(""" select count(*) from `tabVendor Master` where status='Onboarded' """,as_dict=1)
    return total_in_process_vendors


@frappe.whitelist(allow_guest=True)
def total_rfq():

    total_rfq = frappe.db.sql(""" select count(*) from `tabRequest For Quotation` """, as_dict=1)
    return total_rfq


@frappe.whitelist(allow_guest=True)
def total_vendors_registerd_in_month():

    current_month = datetime.now.strftime("%B")
    current_year = datetime.now.year
    return current_month, current_year

@frappe.whitelist(allow_guest=True)
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


@frappe.whitelist(allow_guest=True)
def main_function(data, method):
    #time.sleep(3)
    print("*****************************Hi From Main**************************************")
    name = data.get("name")
    file = frappe.db.sql(""" select file_name from `tabImport Entry` where name=%s """,(name))
    print(file)
    with fitz.open(file) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        print(text)

@frappe.whitelist(allow_guest=True)
def extract_text_from_pdf(data, method):
    pdf_path = data.get("file_name")
    #pdf_path = frappe.request.files.get("file_name")
    
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
   

    lines = text.split('\n')
    resume_dict = {}

    current_section = None
    for line in lines:
        if line.strip() == "":
            continue
        if ":" in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
           
            if current_section is not None:
               
                if current_section not in resume_dict or isinstance(resume_dict[current_section], list):
                    resume_dict[current_section] = {}
                resume_dict[current_section][key] = value
            else:
                resume_dict[key] = value
        else:
           
            if current_section is None or isinstance(resume_dict.get(current_section, None), dict):
                current_section = line.strip()
              
                if current_section in resume_dict and isinstance(resume_dict[current_section], list):
                    continue
                else:
                    resume_dict[current_section] = []  
            else:
                resume_dict[current_section].append(line.strip())
   
    text = extract_text_from_pdf(pdf_path)
    resume_dict = parse_resume_text(text)
    for key, value in resume_dict.items():
        if isinstance(value, dict):
            print(f"{key}:")
        for sub_key, sub_value in value.items():
            print(f"  {sub_key}: {sub_value}")
        if isinstance(value, list):
            print(f"{key}:")
        for item in value:
            print(f"  - {item}")
    else:
        print(f"{key}: {value}")
    print()  
    print(type(resume_dict))


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



@frappe.whitelist(allow_guest=True)
def show_all_vendors():

    all_vendors = frappe.db.sql(""" SELECT
    vm.name AS name,
    status AS status,
    purchase_team_approval AS purchase_team_approval,
    purchase_head_approval AS purchase_head_approval,
    accounts_team_approval AS accounts_team_approval,
    office_email_primary AS office_email_primary,
    vendor_name AS vendor_name,
    cm.company_name AS company_name 
    
  

FROM 
    `tabVendor Master` vm 
LEFT JOIN 
    `tabCompany Master` cm ON vm.company_name = cm.name 


""", as_dict=1)

    return all_vendors



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


@frappe.whitelist(allow_guest=True)
def show_me(name):
    vendor = frappe.db.sql("""
        SELECT
            vm.name AS name,
            vm.office_email_primary AS office_email_primary,
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
            vm.valid_till AS valid_till


        FROM 
            `tabVendor Onboarding` vm 
        LEFT JOIN 
            `tabCompany Master` cm ON vm.company_name = cm.name 
        LEFT JOIN
            `tabState Master` sm ON vm.state = sm.name
        LEFT JOIN 
            `tabCompany Nature Master` cnm ON vm.nature_of_company = cnm.name
        LEFT JOIN
            `tabBusiness Nature Master` bnm ON vm.nature_of_business = bnm.name
        LEFT JOIN 
            `tabVendor Type Master` vt ON vm.vendor_type = vt.name
        LEFT JOIN
            `tabCountry Master` cn ON vm.country = cn.country_name
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
        WHERE 
            vm.office_email_primary=%s
    """, (name), as_dict=1)

    return vendor




    # value = frappe.get_doc("Vendor Onboarding", name)
    # nature_of_company = value.nature_of_company
    # return nature_of_company

@frappe.whitelist(allow_guest=True)
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

@frappe.whitelist(allow_guest=True)
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

@frappe.whitelist(allow_guest=True)
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




@frappe.whitelist(allow_guest=True)
def sap_fetch_token(data, method):


    company_code = frappe.db.get_value("Company Master", filters={'name': data.get('company_name')}, fieldname='company_code')
    purchase_organization = frappe.db.get_value("Company Master", filters={'name': data.get('purchase_organization')}, fieldname='company_name')
    pincode = frappe.db.get_value("Pincode Master", filters={'name': data.get('pincode')}, fieldname='pincode')
    city = frappe.db.get_value("City Master", filters={'name': data.get('city')}, fieldname='city_name')
    country = frappe.db.get_value("Country Master", filters={'name': data.get('country')}, fieldname='country_name')
    state = frappe.db.get_value("State Master", filters={'name': data.get('state')}, fieldname='state_name')
    currency = frappe.db.get_value("Currency Master", filters={'name': data.get('order_currency')}, fieldname='currency_name')
    #terms_of_payment = frappe.db.get_value("Terms Of Payment Master", filters={'name': data.get('terms_of_payment')}, fieldname='terms_of_payment')
    #incoterms = frappe.db.get_value("Incoterm Master", filters={'name': data.get('incoterm')}, fieldname='incoterm_name')
    #purchase_group = frappe.db.get_value("Purchase Group Master", filters={'name': data.get('purchase_group')}, fieldname='purchase_group_name')
    vendor_type = frappe.db.get_value("Vendor Type Master", filters={'name': data.get('vendor_type')}, fieldname='vendor_type_name')


    vendor_details = {
    "Bukrs": company_code,
    "Ekorg": purchase_organization,
    "Ktokk": "",
    "Title": "",
    "Name1": "",
    "Name2": "",
    "Sort1": data.get('search_term'),
    "Street": data.get('office_address_line_1'),
    "StrSuppl1": data.get('office_address_line_2'),
    "StrSuppl2": data.get('office_address_line_3'),
    "StrSuppl3": data.get('office_address_line_4'),
    "PostCode1": pincode,
    "City1": city,
    "Country": country,
    "J1kftind": data.get('type_of_business'),
    "Region": state,
    "TelNumber": data.get('telephone_number'),
    "MobNumber": data.get('mobile_number'),
    "SmtpAddr": data.get('office_email_primary'),
    "SmtpAddr1": data.get('office_email_secondary'),
    "Zuawa": "",
    "Akont": "",
    "Waers": currency,
    "Zterm": "",
    "Inco1": "",
    "Inco2": "",
    "Kalsk": "",
    "Ekgrp": "",
    "Xzemp": data.get('payee_in_document'),
    "Reprf": data.get('check_double_invoice'),
    "Webre": data.get('gr_based_inv_ver'),
    "Lebre": data.get('service_based_inv_ver'),
    "Stcd3": "",
    "J1ivtyp": vendor_type,
    "J1ipanno": "",
    "J1ipanref": "",
    "Namev": "",
    "Name11": "",
    "Bankl": "",
    "Bankn": "",
    "Bkref": "",
    "Banka": "",
    "Xezer": "",
    "Refno": data.get('name')
}

    url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
    #print(vendor_details)
    headers = {
    'X-CSRF-TOKEN': 'Fetch'
    }
    auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
    response = requests.get(url, headers=headers, auth=auth)

        #print(response)
    if response.status_code == 200:
        csrf_token = response.headers.get('x-csrf-token')
        send_detail(data, vendor_details ,method, csrf_token)
        #print("********************  Token ****************************************")
        #print("x-csrf-token:", csrf_token)
        print(vendor_details)
        return csrf_token
    else:
        print("Error:", response.status_code)
        return "Error: " + str(response.status_code)
    send_detail("*************************",csrf_token)



    #*******************************************************************************

    # headers = {
    #     'X-CSRF-Token': csrf_token,
    #     'Content-Type': 'application/json'
    # }
    # auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
    # #print("***********************************************")
    
    
    # response = requests.post(url, headers=headers, auth=auth, json=vendor_details)
    # print("***********************************************", response.status_code)
    
    
    # if response.status_code == 200:  
    #    # print("*****************************************")
    #     print("Vendor details posted successfully.")
    #     #return "************************Vendor details posted successfully.******************************"
    # else:
    #     print("Error in POST request:", response.status_code)
    #     return "Error in POST request: " + str(response.status_code)


@frappe.whitelist(allow_guest=True)
def send_detail(csrf_token, vendor_details ,data, method):
    url = "http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client=200"
    print("*************************************")
    print(type(csrf_token))
    csrf_token_str = str(csrf_token)


    headers = {
        'X-CSRF-TOKEN': csrf_token_str,
        'Content-Type': 'application/json',
        'Authorization': 'Basic V0YtQkFUQ0g6TUB3YiMkJTIwMjQ='
    }
    auth = HTTPBasicAuth('WF-BATCH', 'M@wb#$%2024')
    #print("***********************************************")
    
    
    response = requests.post(url, headers=headers, auth=auth, json=vendor_details)
    print("***********************************************", response.status_code)
    
    
    if response.status_code == 200:  
       # print("*****************************************")
        print("Vendor details posted successfully.")
        #return "************************Vendor details posted successfully.******************************"
    else:
        print("Error in POST request:", response.status_code)
        return "Error in POST request: " + str(response.status_code)


@frappe.whitelist(allow_guest=True)
def validate_aadhar_number():
    pass




    #*******************************************************************************


    # try:
    #     response = requests.post(url, data=vendor_details)
    #     response.raise_for_status()  
    #     print("POST request successful")
    # except requests.RequestException as e:
    #     print(f"Failed to make POST request: {e}")



@frappe.whitelist(allow_guest=True)
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


@frappe.whitelist(allow_guest=True)
def vendor_onboarding(**kwargs):
    pass




@frappe.whitelist(allow_guest=True)
def show_vendor(data, method):

    name = data.get("name")
    values = frappe.db.sql(""" select * from `tabVendor Onboarding` where name=%s """,(name),as_dict=1)
    return values