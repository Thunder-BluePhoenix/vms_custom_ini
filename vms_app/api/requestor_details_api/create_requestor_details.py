import frappe
from frappe import _
from frappe.utils import get_fullname
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from frappe.utils import json


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
                        "material_code_revised": entry.get("material_code_revised"),
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
def update_requestor_details():
    print("=== START update_requestor_details ===")

    form_dict = frappe.form_dict.copy()
    requestor_name = form_dict.get("requestor_name")
    if not requestor_name:
        return {"status": "error", "message": "Missing requestor_name"}

    try:
        requestor_doc = frappe.get_doc("Requestor Master", requestor_name)
    except frappe.DoesNotExistError:
        return {"status": "error", "message": "Requestor not found"}

    REQUESTOR_FIELDS = {
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

    req_data = map_data(form_dict, REQUESTOR_FIELDS)
    requestor_doc.approval_status = "Pending by CP"
    requestor_doc.update(req_data)

    material_json = form_dict.get("material_request")
    if material_json:
        try:
            material_list = json.loads(material_json)
            requestor_doc.set("material_request", [])
            for entry in material_list:
                requestor_doc.append("material_request", {
                    "material_name_description": entry.get("material_name_description"),
                    "material_code_revised": entry.get("material_code_revised"),
                    "company_name": entry.get("material_company_code"),
                    "plant_name": entry.get("plant_name"),
                    "material_category": entry.get("material_category"),
                    "material_group": entry.get("material_group"),
                    "material_type": entry.get("material_type"),
                    "base_unit_of_measure": entry.get("base_unit_of_measure"),
                    "comment_by_user": entry.get("comment_by_user", ""),
                    "material_specifications": entry.get("material_specifications", ""),
                    "is_revised_code_new": entry.get("is_revised_code_new", "")
                })
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Material JSON Parsing Failed")
            return {"status": "error", "message": "Invalid material_request JSON"}

    requestor_doc.save(ignore_permissions=True)
    frappe.db.commit()

    send_email_on_requestor_update(requestor_doc.name)

    return {"status": "success", "message": "Requestor updated", "name": requestor_doc.name}

@frappe.whitelist()
def send_email_on_requestor_update(requestor_name):
    print("=== START send_email_on_requestor_update ===", requestor_name)
    try:
        requestor_doc = frappe.get_doc("Requestor Master", requestor_name)
    except Exception as e:
        print("Error fetching Requestor Master:", str(e))
        return {"status": "fail", "message": "Could not fetch Requestor Master"}

    requestor_email = requestor_doc.contact_information_email
    requestor_person = requestor_doc.requested_by
    child_records = requestor_doc.get("material_request")

    if not requestor_email:
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

    requestor_head = frappe.get_value("Employee Master", requestor_person, "reporting_head")
    requestor_head_email = frappe.get_value("Employee Master", requestor_head, "email")
    requestor_head_name = frappe.get_value("Employee Master", requestor_head, "full_name")

    bcc_address = 'rishi.hingad@merillife.com'
    subject = "Requestor Master Updated"
    body = f"""
    <p>Dear {requestor_head_name},</p>

    <p>
        The Requestor Master "<strong>{requestor_name}</strong>" has been <strong>updated</strong> by <strong>{requestor_person}</strong>.
    </p>

    <p>Here are the updated material request details:</p>
    {table_html}

    <p>Regards,<br>
    Meril VMS Team</p>
    """

    try:
        msg = MIMEMultipart()
        msg["From"] = requestor_email
        msg["To"] = requestor_head_email or ""
        msg["Subject"] = subject
        msg["Cc"] = ", ".join(recipient_emails)
        msg["Bcc"] = bcc_address
        msg.attach(MIMEText(body, "html"))

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
            print("Update email sent successfully.")

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

        return {"status": "success", "message": _("Update email sent successfully.")}

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

        return {"status": "fail", "message": _("Failed to send update email.")}
