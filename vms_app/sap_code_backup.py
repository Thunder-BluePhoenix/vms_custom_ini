@frappe.whitelist(allow_guest=True)
def sap_fetch_token(data, method):

    #*******************************Send Email*************************
    name = data.get("name")
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
    current_user_email = frappe.db.get_value("User", filters={'full_name': current_user}, fieldname='email')
    print(current_user_email)
    frappe.db.sql(" update `tabVendor Master` set registered_by=%s ",(current_user_email))
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
    body = "You have been Successfully Registered on the VMS Portal. Please complete the Onboarding process on this link http://localhost:3000/onboarding?Refno=" + str(name)

    #body = "You have been Successfully Registered on the VMS Portal. Please complete the On boarding process on this link http://localhost:3000/onboarding/{}".format(name)
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



#***************************Send Email Close*********************************************************************************


    company_code = frappe.db.get_value("Company Master", filters={'name': data.get('company_name')}, fieldname='company_code')
    purchase_organization = frappe.db.get_value("Company Master", filters={'name': data.get('purchase_organization')}, fieldname='company_code')
    account_group = frappe.db.get_value("Account Group Master", filters={'name': data.get('account_group')}, fieldname='account_group_name')
    pincode = frappe.db.get_value("Pincode Master", filters={'name': data.get('pincode')}, fieldname='pincode')
    city = frappe.db.get_value("City Master", filters={'name': data.get('city_name')}, fieldname='city_name')
    country = frappe.db.get_value("Country Master", filters={'name': data.get('country')}, fieldname='country_code')
    state = frappe.db.get_value("State Master", filters={'name': data.get('state')}, fieldname='state_code')
    currency = frappe.db.get_value("Currency Master", filters={'name': data.get('order_currency')}, fieldname='currency_code')
    terms_of_payment = frappe.db.get_value("Terms Of Payment Master", filters={'name': data.get('terms_of_payment')}, fieldname='terms_of_payment_name')
    incoterms1 = frappe.db.get_value("Incoterm Master", filters={'name': data.get('incoterm_name')}, fieldname='incoterm_name')
    incoterms2 = frappe.db.get_value("Incoterm Master", filters={'name': data.get('incoterm_name')}, fieldname='incoterm_name')
    purchase_group = frappe.db.get_value("Purchase Group Master", filters={'name': data.get('purchase_group')}, fieldname='purchase_group_name')


    vendor_type = frappe.db.get_value("Vendor Type Master", filters={'name': data.get('vendor_type')}, fieldname='vendor_type_name')
    # purchasing_group = frappe.db.get_value("Purchase Group Master", filters={'name': data.get('Ekgrp')},fieldname='' )
    bank1 = frappe.db.get_value("Bank Master", filters={'name': data.get('bank1')}, fieldname='bank_name')
    name = data.get('name')
    print("********************", bank1)
    # bank2 = frappe.db.get_value("Bank Master", filters={'name': data.get('bank_name')}, fieldname='bank_name')

    data =  {
    "Bukrs": company_code,
    "Ekorg": purchase_organization,
    "Ktokk": account_group,
    "Title": "",
    "Name1": data.get('vendor_name'),
    "Name2": "",
    "Sort1": data.get('search_term'),
    "Street": data.get('office_address_line_1'),
    "StrSuppl1": data.get('office_address_line_1'),
    "StrSuppl2": "",
    "StrSuppl3": "",
    "PostCode1": pincode,
    "City1": city,
    "Country": country,
    "J1kftind": "",
    "Region": "6",
    "TelNumber": "",
    "MobNumber": data.get('mobile_number'),
    "SmtpAddr": data.get('office_email_primary'),
    "SmtpAddr1": data.get('office_email_secondary'),
    "Zuawa": "",
    "Akont": "16101020",
    "Waers": currency,
    "Zterm": "Z072",
    "Inco1": incoterms1,
    "Inco2": incoterms2,
    "Kalsk": "",
    "Ekgrp": purchase_group,
    "Xzemp": "X",
    "Reprf": "X",
    "Webre": "X",
    "Lebre": "",
    "Stcd3": data.get('get_number'),
    "J1ivtyp": data.get('vendor_type'),
    "J1ipanno": data.get('pan_number'),
    "J1ipanref": "Hitesh Mahto",
    "Namev": "Hitesh",
    "Name11": "Mahto",
    "Bankl": bank1,
    "Bankn": data.get("account_number"),
    "Bkref": "2001",
    "Banka": "UTIB0019191",
    "Xezer": "",
    "Refno": "VMS/368b008a78/0101",
    "Vedno": "",
    "Zmsg": ""

        }






#     data =  {
#     "Bukrs": "2000",
#     "Ekorg": "2000",
#     "Ktokk": "ZDOM",
#     "Title": "NULL",
#     "Name1": "MERIL-API12",
#     "Name2": "",
#     "Sort1": "Harin",
#     "Street": "test",
#     "StrSuppl1": "test",
#     "StrSuppl2": "",
#     "StrSuppl3": "",
#     "PostCode1": "151617",
#     "City1": "test",
#     "Country": "IN",
#     "J1kftind": "",
#     "Region": "6",
#     "TelNumber": "",
#     "MobNumber": "1256651",
#     "SmtpAddr": "hitesh.mahto@merillife.com",
#     "SmtpAddr1": "hitesh@gmail.com",
#     "Zuawa": "",
#     "Akont": "16101020",
#     "Waers": "INR",
#     "Zterm": "Z072",
#     "Inco1": "CFR",
#     "Inco2": "CFR Costs and freight",
#     "Kalsk": "",
#     "Ekgrp": "P02",
#     "Xzemp": "X",
#     "Reprf": "X",
#     "Webre": "X",
#     "Lebre": "",
#     "Stcd3": "GST12345",
#     "J1ivtyp": "0",
#     "J1ipanno": "PAN11010",
#     "J1ipanref": "Hitesh Mahto",
#     "Namev": "Hitesh",
#     "Name11": "Mahto",
#     "Bankl": "HDFC0000170",
#     "Bankn": "ac91201001898261",
#     "Bkref": "2001",
#     "Banka": "UTIB0019191",
#     "Xezer": "",
#     "Refno": "VMS/368b008a78/0101",
#     "Vedno": "",
#     "Zmsg": ""
# }




















#     data = {
#     "company_": company_code,
#     "Ekorg": data.get("purchase_organization"),
#     "Ktokk": data.get("ZDOM"),
#     "Title": "",
#     "Name1": data.get('Name1'),
#     "Name2": "",
#     "Sort1": data.get('Sort1'),
#     "Street": data.get('office_address_line_1'),
#     "StrSuppl1": data.get('StrSuppl1'),
#     "StrSuppl2": data.get('StrSuppl2'),
#     "StrSuppl3": data.get('StrSuppl3'),
#     "PostCode1": pincode,
#     "City1": city,
#     "Country": "",
#     "J1kftind": data.get('J1kftind'),
#     "Region": state,
#     "TelNumber": data.get('TelNumber'),
#     "MobNumber": data.get('MobNumber'),
#     "SmtpAddr": data.get('SmtpAddr'),
#     "SmtpAddr1": data.get('SmtpAddr1'),
#     "Zuawa": "",
#     "Akont": "",
#     "Waers": data.get('Waers'),
#     "Zterm": data.get('Zterm'),
#     "Inco1": "",
#     "Inco2": "",
#     "Kalsk": "",
#     "Ekgrp": "",
#     "Xzemp": data.get('Xzemp'),
#     "Reprf": data.get('Reprf'),
#     "Webre": data.get('Webre'),
#     "Lebre": data.get('Lebre'),
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
#     "Refno": data.get('Refno'),
#     "Vedno": "",
#     "Zmsg": ""
# }




    # "Ekorg": data.get("purchase_organization"),
    # "Ktokk": "ZDOM",
    # "Title": data.get("ZDOM"),
    # "Name1": data.get('Name1'),
    # "Name2": "",
    # "Sort1": data.get('Sort1'),
    # "Street": data.get('Street'),
    # "StrSuppl1": data.get('StrSuppl1'),
    # "StrSuppl2": data.get('StrSuppl2'),
    # "StrSuppl3": data.get('StrSuppl3'),
    # "PostCode1": pincode,
    # "City1": city,
    # "Country": country,
    # "J1kftind": "",
    # "Region": state,
    # "TelNumber": "",
    # "MobNumber": "1256651",
    # "SmtpAddr": "hitesh.mahto@merillife.com",
    # "SmtpAddr1": "hitesh@gmail.com",
    # "Zuawa": "",
    # "Akont": "16101020",
    # "Waers": currency,
    # "Zterm": terms_of_payment,
    # "Inco1": incoterms1,
    # "Inco2": incoterms2,
    # "Kalsk": "",
    # "Ekgrp": purchasing_group,
    # "Xzemp": "X",
    # "Reprf": "X",
    # "Webre": "X",
    # "Lebre": "",
    # "Stcd3": "GST12345",
    # "J1ivtyp": vendor_type,
    # "J1ipanno": data.get('J1ipanno'),
    # "J1ipanref": "Hitesh Mahto",
    # "Namev": "Hitesh",
    # "Name11": "Mahto",
    # "Bankl": "HDFC0000170",
    # "Bankn": "ac91201001898261",
    # "Bkref": "2001",
    # "Banka": "UTIB0019191",
    # "Xezer": "",
    # "Refno": "VMS/368b008a78/0101",
    # "Vedno": "",
    # "Zmsg": ""
# }








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
  
        
       # return csrf_token
    else:
        print("Error:", response.status_code)
       # return "Error: " + str(response.status_code)
        send_detail("*************************",csrf_token)





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

#************SAP DATA Push Closed******************************************************
