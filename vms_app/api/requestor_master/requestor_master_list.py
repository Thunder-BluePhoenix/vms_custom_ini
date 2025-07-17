import frappe
from frappe import _

@frappe.whitelist()
def show_requestor_master_list():
    requestor_master_list = []

    requestor_names = frappe.get_all(
        "Requestor Master",
        fields=["name"],
        order_by="request_date DESC, creation DESC"
    )

    for item in requestor_names:
        doc = frappe.get_doc("Requestor Master", item.name)
        doc_dict = doc.as_dict()

        if "material_request" in doc_dict:
            del doc_dict["material_request"]

        material_request_items = []
        for child in doc.material_request:
            company_name = frappe.db.get_value("Company Master", child.company_name, "company_name") if child.company_name else ""

            material_request_items.append({
                "child_name": child.name,
                "company_code": child.company_name,
                "company_name": company_name,
                "plant_name": child.plant_name,
                "material_description": child.material_name_description,
                "material_type": child.material_type,
                "comment_by_user": child.comment_by_user,
            })

        doc_dict["material_request_items"] = material_request_items

        requestor_master_list.append(doc_dict)

    return requestor_master_list