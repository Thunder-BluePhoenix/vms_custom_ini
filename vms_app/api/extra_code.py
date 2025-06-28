# import smtplib,frappe
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# @frappe.whitelist(allow_guest=True)
# def set_vendor_onboarding_status(**kwargs):
#     name = kwargs.get("name")
#     current_user = frappe.session.user
#     current_user_designation_key = frappe.db.get_value("User", filters={'email': current_user}, fieldname='designation')
#     current_user_designation_name = frappe.db.get_value("Designation Master", filters={'name': current_user_designation_key}, fieldname=['designation_name'])


#     vendor_email, registered_by_email = frappe.db.get_value("Vendor Master", filters={'name': name}, fieldname=['office_email_primary', 'registered_by'])

  
#     if current_user_designation_name in ["Accounts Team", "Purchase Team", "Purchase Head"]:
#         status_map = {
#             "Accounts Team": "Approved by Accounts Team",
#             "Purchase Team": "Approved by Purchase Team",
#             "Purchase Head": "Approved by Purchase Head"
#         }
#         status = status_map.get(current_user_designation_name)

       
#         frappe.db.sql("""UPDATE `tabVendor Master` SET status=%s WHERE name=%s""", (status, name))
#         frappe.db.commit()       
#         smtp_server = "smtp.transmail.co.in"
#         smtp_port = 587
#         smtp_user = "emailapikey"  
#         smtp_password = "PHtE6r1cF7jiim598RZVsPW9QMCkMN96/uNveQUTt4tGWPNRTk1U+tgokDO0rRx+UKZAHKPInos5tbqZtbiHdz6/Z2dED2qyqK3sx/VYSPOZsbq6x00as1wSc0TfUILscdds1CLfutnYNA=="  
#         from_address = registered_by_email 
#         to_address = vendor_email  
#         subject = "Test email"
#         body = f"Your request has been approved by {current_user_designation_name}."
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
#                 print("Email sent successfully!")
#         except Exception as e:
#             print(f"Failed to send email: {e}")

#         return registered_by_email





