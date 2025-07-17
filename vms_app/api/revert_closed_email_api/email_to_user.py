import frappe
from frappe import _
from frappe.utils import get_fullname
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@frappe.whitelist()
def send_email_to_user(doc_name):
    try:
        print("+++++++Approval Status is Ticket Closed++++++")

        requestor_doc = frappe.get_doc("Requestor Master", doc_name)
        requestor_doc.approval_status = "Use Existing Code"
        requestor_doc.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"Set approval_status to 'Ticket Closed' for {doc_name}")

        to_address = requestor_doc.contact_information_email

        if not to_address:
            raise Exception("No contact_email found in Requestor Master")

        from_address = frappe.session.user
        if from_address == "Guest":
            raise Exception("Guest user cannot send email")
        from_full_email = f"{get_fullname(from_address)} <{from_address}>"

        employee_doc = frappe.get_doc("Employee Master", requestor_doc.immediate_reporting_head)
        cc_address = ""
        if employee_doc:
            # reporting_manager = frappe.get_doc("Employee", employee_doc.reporting_to)
            cc_address = employee_doc.email or ""

        if not requestor_doc.material_request:
            raise Exception("No material_requests found in the document")

        item = requestor_doc.material_request[0]
        revised_code = item.material_code_revised or "N/A"
        material_description = item.material_name_description or "N/A"
        subject = f"Ticket Closed: Material Code Exists"
        body = (
            f"The material code <b>{revised_code}</b> for material description "
            f"<b>{material_description}</b> already exists.<br><br>"
            f"Therefore, closing the following ticket for <b>{doc_name}</b>.<br><br>"
            f"Regards,<br>"
            f"{get_fullname(from_address)}"
        )
        bcc_address = "rishi.hingad@merillife.com"
        msg = MIMEMultipart()
        msg["From"] = from_full_email
        msg["To"] = to_address
        msg["Subject"] = subject
        msg["Cc"] = cc_address
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "html"))

        smtp_conf = frappe.conf
        with smtplib.SMTP(smtp_conf.get("smtp_server"), smtp_conf.get("smtp_port")) as server:
            server.starttls()
            server.login(smtp_conf.get("smtp_user"), smtp_conf.get("smtp_password"))
            server.sendmail(from_address, [to_address, cc_address, bcc_address], msg.as_string())
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
            'to_email': to_address if 'to_address' in locals() else '',
            'from_email': from_address if 'from_address' in locals() else '',
            'message': str(e),
            'status': f"Failed: {e}",
            'screen': "Material Onboarding",
            'created_by': from_address if 'from_address' in locals() else 'System'
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error(frappe.get_traceback(), "send_email_to_user Error")

        return {"status": "fail", "message": _("Failed to send email.")}
    
@frappe.whitelist()
def send_email_to_user_on_revert(doc_name, remark):
    try:
        print("+++++++Approval Status is Re-open due to Revert++++++")

        requestor_doc = frappe.get_doc("Requestor Master", doc_name)
        requestor_doc.approval_status = "Re-Opened by CP"
        requestor_doc.revert_remark = remark
        requestor_doc.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"Set approval_status to 'Re-open' and revert_remark for {doc_name}")

        to_address = requestor_doc.contact_information_email

        if not to_address:
            raise Exception("No contact_email found in Requestor Master")

        from_address = frappe.session.user
        if from_address == "Guest":
            raise Exception("Guest user cannot send email")

        from_full_email = f"{get_fullname(from_address)} <{from_address}>"

        employee_doc = frappe.get_doc("Employee Master", requestor_doc.immediate_reporting_head)
        cc_address = employee_doc.email or "" if employee_doc else ""

        item = requestor_doc.material_request[0] if requestor_doc.material_request else None
        revised_code = item.material_code_revised if item else "N/A"
        material_description = item.material_name_description if item else "N/A"

        subject = f"Ticket Re-opened: Action Required on Material Code"
        body = (
            f"The ticket <b>{doc_name}</b> has been <b>re-opened</b> by the CP/Store team.<br><br>"
            f"<b>Material Code:</b> {revised_code}<br>"
            f"<b>Material Description:</b> {material_description}<br><br>"
            f"<b>Revert Remark:</b> {remark}<br><br>"
            f"Please take necessary action.<br><br>"
            f"Regards,<br>"
            f"{get_fullname(from_address)}"
        )

        bcc_address = "rishi.hingad@merillife.com"

        msg = MIMEMultipart()
        msg["From"] = from_full_email
        msg["To"] = to_address
        msg["Subject"] = subject
        msg["Cc"] = cc_address
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "html"))

        smtp_conf = frappe.conf
        with smtplib.SMTP(smtp_conf.get("smtp_server"), smtp_conf.get("smtp_port")) as server:
            server.starttls()
            server.login(smtp_conf.get("smtp_user"), smtp_conf.get("smtp_password"))
            server.sendmail(from_address, [to_address, cc_address, bcc_address], msg.as_string())
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
            'to_email': to_address if 'to_address' in locals() else '',
            'from_email': from_address if 'from_address' in locals() else '',
            'message': str(e),
            'status': f"Failed: {e}",
            'screen': "Material Onboarding",
            'created_by': from_address if 'from_address' in locals() else 'System'
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error(frappe.get_traceback(), "send_email_to_user_on_revert Error")

        return {"status": "fail", "message": _("Failed to send email.")}