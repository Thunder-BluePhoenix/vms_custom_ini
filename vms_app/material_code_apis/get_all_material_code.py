import frappe
from frappe import _


@frappe.whitelist()
def get_all_material_descriptions_and_codes():
    results = []

    material_master_entries = frappe.get_all(
        "Material Master",
        fields=["material_name_description", "material_code_revised","name"]
    )
    for entry in material_master_entries:
        results.append({
            "source": "Material Master",
            "name": entry.name,
            "material_name_description": entry.material_name_description,
            "material_code_revised": entry.material_code_revised
        })

    requestor_names = frappe.get_all("Requestor Master", fields=["name"])
    for item in requestor_names:
        doc = frappe.get_doc("Requestor Master", item.name)
        for child in doc.material_request:
            results.append({
                "source": "Requestor Master",
                "name": doc.name,
                "material_name_description": child.material_name_description,
                "material_code_revised": child.material_code_revised
            })
    return results

@frappe.whitelist()
def get_all_material_codes():
    try:
        materials = frappe.get_all(
            "Material Code Master",
            fields=["name", "material_description", "material_type", "material_group", "plant", "company_code"]
        )
        frappe.response["type"] = "json"
        frappe.response["data"] = materials
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Material Code Fetch Error")
        frappe.response["http_status_code"] = 500
        frappe.response["data"] = {"error": str(e)}