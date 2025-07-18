import frappe
import json
from frappe import _
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


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