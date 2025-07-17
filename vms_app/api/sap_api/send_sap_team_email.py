import frappe
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from frappe import _
from frappe.utils import getdate


ERP_TO_SAP_FIELD_MAP = {
    "material_code_revised": "Matnr",
    "material_name_description": "Maktx",
    "purchase_uom": "Bstme",
    "issue_unit": "Ausme",
    "availability_check": "Mtvfp",
    "batch_requirements_yn": "Xchpf",
    "lead_time": "Plifz",
    "mrp_type": "Dismm",
    "mrp_group": "Disgr",
    "mrp_controller_revised": "Dispo",
    "lot_size_key": "Disls",
    "procurement_type": "Beskz",
    "scheduling_margin_key": "Fhori",
    "purchase_order_text": "Purcom",
    "purchasing_group": "Ekgrp",
    "gr_processing_time": "Webaz",
    "purchasing_value_key": "Ekwsl",
    "minimum_remaining_shell_life": "Mhdrz",
    "total_shell_life": "Mhdhb",
    "expiration_date": "Iprkz",
    "inspection_interval": "Prfrq",
    "incoming_inspection_01": "Qminst",
    "incoming_inspection_09": "Qminst1",
    "valuation_class": "Bklas",
    "profit_center": "Prctr",
    "price_control": "Vprsv",
    "do_not_cost": "Ncost",
    "comment_by_store": "Storecom",
    "inspection_require": "Qmatv",
    "class_type": "Class",
    "class_number": "Klart",
    "serial_number_profile": "Sernp",
    "serialization_level": "Serlv",
    "storage_location": "Lgort",
    "division": "Spart",
}



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
    

def get_changed_fields(old_doc, sap_payload_dict, fields_to_check):
    changes = []

    for erp_field in fields_to_check:
        sap_field = ERP_TO_SAP_FIELD_MAP.get(erp_field)
        if not sap_field:
            continue

        old_val = get_mapped_erp_value(old_doc, erp_field)
        new_val = str(sap_payload_dict.get(sap_field, "") or "").strip()
        print(f"Checking field: {erp_field}, ERP: '{old_val}', SAP: '{new_val}'")

        if old_val != new_val:
            changes.append((erp_field, old_val, new_val))

    return changes


def get_mapped_erp_value(doc, field):
    raw = str(getattr(doc, field, "") or "").strip()

    if field == "purchasing_group":
        return frappe.get_value("Purchase Group Master", {"name": raw}, "purchase_group_code") or raw
    elif field == "storage_location":
        return frappe.get_value("Storage Location Master", {"name": raw}, "storage_location") or raw
    elif field == "division":
        return frappe.get_value("Division Master", {"name": raw}, "division_code") or raw
    elif field == "valuation_class":
        return frappe.get_value("Valuation Class Master", {"name": raw}, "valuation_class_code") or raw
    elif field == "mrp_controller_revised":
        return frappe.get_value("MRP Controller Master", {"name": raw}, "mrp_controller") or raw
    elif field in ["batch_requirements_yn", "inspection_require"]:
        return "X" if raw == "Yes" else ""
    elif field in ["incoming_inspection_01", "incoming_inspection_09"]:
        return "X" if raw else ""
    elif field == "serial_number_profile":
        return "" if raw == "No" else raw
    else:
        return raw


def prettify_field_name(field_name):
    return field_name.replace("_", " ").title()


@frappe.whitelist()
def send_sap_duplicate_change_email(doc_name, changed_fields):
    print("*******SAP TEAM DUPLICATE CHANGE EMAIL HIT********", doc_name)
    requestor = frappe.get_doc("Requestor Master", doc_name)
    mo_doc_name = requestor.material_onboarding_ref_no
    mo_details = frappe.get_doc("Material Onboarding", mo_doc_name)

    request_id = requestor.request_id
    cp_team = mo_details.approved_by_name
    cp_email = frappe.get_value("Employee Master", {"name": cp_team}, "email")
    email = requestor.contact_information_email
    cc_2 = requestor.immediate_reporting_head
    cc_email2 = frappe.get_value("Employee Master", {"name": cc_2}, "email")

    sap_email = frappe.get_value("Employee Master", {"role": "SAP"}, "email")

    from_address = "roreply@merillife.com"
    cc_list = list(filter(None, [email, cp_email, cc_email2]))
    bcc_address = "rishi.hingad@merillife.com"

    changes_html = "".join(
        f"<li><strong>{prettify_field_name(f)}:</strong> '{o}' ➜ '{n}'</li>"
        for f, o, n in changed_fields
    )

    subject = f"🔄 Changes Detected for Existing Material Request - {request_id}"
    message = f"""
        <p>Dear SAP Team,</p>
        <p>The request <strong>{request_id}</strong> was already found in SAP.</p>
        <p>However, the following changes were detected in the latest update:</p>
        <ul>{changes_html}</ul>
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

    conf = frappe.conf
    server = smtplib.SMTP(conf.smtp_server, conf.smtp_port)
    server.starttls()
    server.login(conf.smtp_user, conf.smtp_password)
    server.sendmail(conf.smtp_user, recipients, msg.as_string())
    server.quit()

    # Optional: Add Email Log
    frappe.get_doc({
        'doctype': 'Email Log',
        'to_email': sap_email,
        'from_email': conf.smtp_user,
        'message': message,
        'status': "Sent - Duplicate Record Update",
        'screen': "Material Onboarding",
        'created_by': conf.smtp_user
    }).insert(ignore_permissions=True)
    frappe.db.commit()
