import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_all_material_type_master_details():
    try:
        material_type_masters = frappe.get_all(
            "Material Type Master",
            fields=["*"],
        )

        result = []

        for mt in material_type_masters:
            doc = frappe.get_doc("Material Type Master", mt.name)

            valuation_rows = []
            for row in doc.valuation_and_profit:
                valuation_class_description = ""
                if row.valuation_class:
                    vc = frappe.get_value("Valuation Class Master",row.valuation_class,"valuation_class_name")
                    valuation_class_description = vc or ""
                
                profit_center_description = ""
                if row.profit_center:
                    pc = frappe.get_value("Profit Center Master",row.profit_center,"description")
                    profit_center_description = pc or ""

                division_description = ""
                division_code = ""
                if row.division:
                    division_code = frappe.get_value( "Division Master", row.division, "division_code") or ""
                    dd = frappe.get_value( "Division Master", row.division, "description")
                    division_description = dd or ""

                valuation_rows.append({
                    "valuation_class": row.valuation_class,
                    "valuation_class_description": valuation_class_description,
                    "profit_center": row.profit_center,
                    "profit_center_description": profit_center_description,
                    "division": row.division,
                    # "division_name": f"{division_code} - {division_description}".strip(" -"),
                    "division_name": " - ".join(filter(None, [division_code, division_description])),
                    "company": row.company,
                })

            company_rows = []
            for row in doc.multiple_company:
                company_name = ""
                if row.code_of_company:
                    company_name = frappe.get_value("Company Master", row.code_of_company, "company_name") or ""
                company_rows.append({
                    "company": row.code_of_company,
                    "company_name": company_name,
                })

            storage_rows = []
            for row in doc.storage_table:
                storage_desc = ""
                if row.storage_location:
                    storage_desc = frappe.get_value("Storage Location Master",row.storage_location,"storage_location_name") or ""
                storage_rows.append({
                    "storage_location": row.storage_location,
                    "storage_name": storage_desc,
                })

            result.append({
                "name": doc.name,
                "material_type_name": doc.material_type_name,
                "description": doc.description,
                "company": doc.company,
                "material_category_type": doc.material_category_type,
                "valuation_and_profit": valuation_rows,
                "multiple_company": company_rows,
                "storage_table": storage_rows,
            })

        return result

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_all_material_type_master_details_error")
        return frappe.throw(_("Failed to fetch Material Type Master details: {0}").format(str(e)))