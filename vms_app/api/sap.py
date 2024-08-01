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
# import pandas as pd


@frappe.whitelist(allow_guest=True)
#def sap_fetch_token(data, method):
def sap_fetch_token(name):

    name = name
    company_id = frappe.db.get_value("Vendor Master", filters={"name": name}, fieldname=['company_name'])
    sap_code = frappe.db.get_value("Company Master", filters={"name": company_id}, fieldname=['sap_client_code'])
    print("*************This is name in the starting of the SAP Fetch Token********************", name, sap_code)
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

    termsid = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['terms_of_payment'])
    terms = frappe.db.get_value("Terms Of Payment Master", filters={'name': termsid}, fieldname=['terms_of_payment_code'])
    print("****************%%%%%%%%%%%TERMS%%%%%%%%%%%%%%%%%***************************", terms, termsid)
   # email_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary'])
    reconcileid = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['reconciliation_account'])
    reconciliation_number = frappe.get_value("Reconciliation Account", filters={'name': reconcileid}, fieldname=['num'])
    #company_code = vendor[0].get('company_code') if vendor else None
    company_id = frappe.db.get_value("Vendor Master", filters={"name": name}, fieldname=['company_name'])
    company_code = frappe.db.get_value("Company Master", filters={"name": company_id}, fieldname=['company_code'])
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
    print("*************************************ID%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", incokey)
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
    bank = frappe.db.get_value("Bank Master", filters={'name': bank_id}, fieldname=['bank_name', 'ifsc_code', 'bank_code', 'account_number'])   
    account_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['account_group'])
    account_code = frappe.db.get_value("Account Group Master", filters={'name': account_id}, fieldname=['acccount_group_code'])
    purchase_id = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['purchase_groupm'])
    purchase_code = frappe.db.get_value("Purchase Group Master", filters={'name': purchase_id}, fieldname=['purchase_group_code'])
    flname = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['first_name', 'last_name'])
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", reconcileid,reconciliation_number, company_code, country_name, bank, state_name)
    json_data = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['payee', 'gr_based_inv_ver', 'service_based_inv_ver', 'check_double_invoice'])
    print("##############################2345666666666666666666666############", json_data)
    payee_in_document, gr_based_inv_ver, service_based_inv_ver, check_double_invoice = json_data
    payee = 'X' if payee_in_document == 1 else ''
    gr_based_inv_ver = 'X' if gr_based_inv_ver == 1 else ''
    service_based_inv_ver = 'X' if service_based_inv_ver == 1 else ''
    check_double_invoice = 'X' if check_double_invoice == 1 else ''
    print(f"Payee: {payee}, GR Based Invoice Verification: {gr_based_inv_ver}, Service Based Invoice Verification: {service_based_inv_ver}, Check Double Invoice: {check_double_invoice}")
    mylist = [payee, gr_based_inv_ver, service_based_inv_ver, check_double_invoice]
    print("***********MYLIST & Name***********", mylist, name)
    val = frappe.db.get_value("Vendor Onboarding", filters={'ref_no': name}, fieldname=['city', 'state', 'pincode', 'gst_number', 'company_pan_number', 'account_number'])
    pincode_no = frappe.db.get_value("Pincode Master", filters={'name': val[2] }, fieldname=['pincode'])
    

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
            "Bankl": bank[2],
            "Bankn": val[5],
            "Bkref": bank[0],
            "Banka": bank[1],
            "koinh": bank[3],
            "Xezer": "",
            "Refno": name,
            "Vedno": "",
            "Zmsg": ""

                }
        
            url = f"http://10.10.103.133:8000/sap/opu/odata/sap/ZMM_VENDOR_SRV/VENDORSet?sap-client={sap_code}"
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
                key1 = response.cookies.get(f'SAP_SESSIONID_BHD_{sap_code}')
                key2 = response.cookies.get('sap-usercontext')
                
                # Sending details to SAP
                send_detail(csrf_token, data, key1, key2, name, sap_code)
                print("*******************KEYYYYY********", key1)
                print(key2)
                print(csrf_token)
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
        # 'Cookie': f"SAP_SESSIONID_BHD_200={key1}; sap-usercontext={key2}"
        'Cookie': f"SAP_SESSIONID_BHD_{sap_code}={key1}; sap-usercontext={key2}"

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
        print("********** Here is the Vendor Code ****************", vendor_code)
        
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

#**********************************************************************************************************************
