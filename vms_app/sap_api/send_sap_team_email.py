import frappe
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from frappe import _
from frappe.utils import getdate


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