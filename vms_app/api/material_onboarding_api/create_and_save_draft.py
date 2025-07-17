import frappe
from frappe import _
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from frappe.utils import get_fullname

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
    onboarding = None
    try:
        if not requestor.material_master_ref_no and not requestor.material_onboarding_ref_no:
            print("Material Master and Onboarding do not exist. Creating new ones...")

            material = frappe.new_doc("Material Master")
            material.update(mat_data)
            material.insert()
            print("Material Master created:", material.name)

            onb_data.update({
                "material_master_ref_no": material.name,
                "material_code_latest": form_dict.get("material_code")
            })

            onboarding = frappe.new_doc("Material Onboarding")
            onboarding.update(onb_data)
            onboarding.insert()
            print("Material Onboarding created:", onboarding.name)

            material.material_onboarding_ref_no = onboarding.name
            material.save()

            requestor.material_master_ref_no = material.name
            requestor.material_onboarding_ref_no = onboarding.name
            requestor.approval_status = "Sent to SAP"
            requestor.save()
            print("Requestor Master updated with new references.")
        else:
            print("Material Master or Onboarding already exists. Updating existing records...")

            material = frappe.get_doc("Material Master", requestor.material_master_ref_no)
            material.update(mat_data)
            material.save()
            print("Updated Material Master:", material.name)

            onboarding = frappe.get_doc("Material Onboarding", requestor.material_onboarding_ref_no)
            onb_data.update({
                "material_master_ref_no": material.name,
                "material_code_latest": form_dict.get("material_code")
            })
            onboarding.update(onb_data)
            onboarding.save()
            print("Updated Material Onboarding:", onboarding.name)

            requestor.material_master_ref_no = material.name
            requestor.material_onboarding_ref_no = onboarding.name
            requestor.approval_status = "Updated by CP"
            requestor.save()
            print("Requestor Master updated.")

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

@frappe.whitelist()
def save_material_onboarding_draft():
    print("=== SAVE AS DRAFT: Material Onboarding ===")
    form_dict = dict(frappe.form_dict)

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
    
    def map_fields(mapping):
        return {
            doc_field: form_dict.get(form_key)
            for doc_field, form_key in mapping.items()
            if form_dict.get(form_key) is not None
        }

    mat_data = map_fields(MATERIAL_FIELDS)
    onb_data = map_fields(ONBOARDING_FIELDS)

    for checkbox_field in ["incoming_inspection_01", "incoming_inspection_09"]:
        onb_data[checkbox_field] = 1 if form_dict.get(checkbox_field) in ["on", "1", 1, True, "true", "True"] else 0

    req_name = form_dict.get("requestor_ref_no") or form_dict.get("requestor_name")
    if not req_name:
        frappe.throw("Requestor reference missing!")

    requestor = frappe.get_doc("Requestor Master", req_name)

    mat_data.update({
        "requestor_ref_no": req_name,
        "basic_data_ref_no": req_name
    })

    onb_data.update({
        "requestor_ref_no": req_name
    })

    try:
        if not requestor.material_master_ref_no:
            material = frappe.new_doc("Material Master")
            material.update(mat_data)
            material.insert()
            print("Material Master draft created:", material.name)
        else:
            material = frappe.get_doc("Material Master", requestor.material_master_ref_no)
            material.update(mat_data)
            material.save()
            print("Material Master draft updated:", material.name)

        if not requestor.material_onboarding_ref_no:
            onb_data.update({
                "material_master_ref_no": material.name,
                "material_code_latest": form_dict.get("material_code"),
                "approval_status": "Draft"
            })
            onboarding = frappe.new_doc("Material Onboarding")
            onboarding.update(onb_data)
            onboarding.insert()
            print("Material Onboarding draft created:", onboarding.name)
        else:
            onboarding = frappe.get_doc("Material Onboarding", requestor.material_onboarding_ref_no)
            onb_data.update({
                "material_master_ref_no": material.name,
                "material_code_latest": form_dict.get("material_code"),
                "approval_status": "Draft"
            })
            onboarding.update(onb_data)
            onboarding.save()
            print("Material Onboarding draft updated:", onboarding.name)

        requestor.material_master_ref_no = material.name
        requestor.material_onboarding_ref_no = onboarding.name
        requestor.approval_status = "Draft"
        requestor.save()

        frappe.db.commit()

        return {
            "status": "draft_saved",
            "material_master": material.name,
            "material_onboarding": onboarding.name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Save Draft Error")
        return {"status": "fail", "message": str(e)}