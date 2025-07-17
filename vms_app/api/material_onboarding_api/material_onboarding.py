import frappe
from frappe import _

@frappe.whitelist()
def show_material_onboarding_lists():
    material_onboarding_list = []

    requestors = frappe.get_all("Requestor Master", fields=["*"], order_by="request_date DESC, creation DESC")

    for requestor in requestors:
        requestor_doc = frappe.get_doc("Requestor Master", requestor.name)

        for material in requestor_doc.material_request:
            entry = {
                "requestor_ref_no": requestor_doc.name,
                "child_table_row_id": material.name,
                "material_name_description": material.material_name_description,
                "material_company_code": material.company_name,
                "material_company_name": frappe.db.get_value("Company Master", material.company_name, "company_name") if material.company_name else None,
                "plant_name": material.plant_name,
                "material_type": material.material_type,
                "base_unit_of_measure": material.base_unit_of_measure,
                "comment_by_user": material.comment_by_user,
                "requested_by": requestor_doc.requested_by,
                "request_date": requestor_doc.request_date,
                "requestor_company": requestor_doc.requestor_company,
                "contact_information_email": requestor_doc.contact_information_email, 
                "approval_status": requestor_doc.approval_status,  
            }

            material_onboarding_list.append(entry)

    return material_onboarding_list


@frappe.whitelist()
def get_material_onboarding_details(name, material_name):
    if not name:
        frappe.throw("Requestor Master document name is required")

    try:
        requestor_doc = frappe.get_doc("Requestor Master", name)
    except frappe.DoesNotExistError:
        frappe.throw(f"Requestor Master with name '{name}' not found")

    requestor_dict = requestor_doc.as_dict()
    # Patch material_type_name in each row of material_request
    for row in requestor_dict.get("material_request", []):
        if row.get("material_type"):
            row["material_type_name"] = frappe.db.get_value("Material Type Master",row["material_type"],"material_type") or ""

    if requestor_doc.requestor_company:
        requestor_dict["requestor_company_name"] = frappe.db.get_value("Company Master", requestor_doc.requestor_company, "company_name")

    selected_row = next((row for row in requestor_doc.material_request if row.name == material_name), None)

    material_type_name = ""
    if selected_row and selected_row.material_type:
        material_type_name = frappe.db.get_value("Material Type Master",selected_row.material_type,"material_type") or ""

    material_request_item = selected_row.as_dict() if selected_row else {}
    if material_type_name:
        material_request_item["material_type_name"] = material_type_name

    # Fetch Material Master (with children)
    material_master_data = {}
    mm_ref = requestor_doc.get("material_master_ref_no")
    if mm_ref:
        try:
            material_doc = frappe.get_doc("Material Master", mm_ref)
            material_master_data = material_doc.as_dict()
            material_master_data["children"] = [d.as_dict() for d in material_doc.get_all_children()]

        except Exception as e:
            frappe.log_error(f"Failed to get Material Master '{mm_ref}'", str(e))

    # Fetch Material Onboarding (with children)
    material_onboarding_data = {}
    mo_ref = requestor_doc.get("material_onboarding_ref_no")
    if mo_ref:
        try:
            mo_doc = frappe.get_doc("Material Onboarding", mo_ref)
            material_onboarding_data = mo_doc.as_dict()
            material_onboarding_data["children"] = [d.as_dict() for d in mo_doc.get_all_children()]
            material_onboarding_data = mo_doc.as_dict()
            if mo_doc.company:
                material_onboarding_data["company_name"] = frappe.db.get_value("Company Master", mo_doc.company, "company_name")
        except Exception as e:
            frappe.log_error(f"Failed to get Material Onboarding '{mo_ref}'", str(e))

    return {
        "requestor_master": requestor_dict,
        "material_request_item": material_request_item,
        "material_master": material_master_data,
        "material_onboarding": material_onboarding_data
    }