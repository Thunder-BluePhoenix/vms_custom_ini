import frappe
import requests # type: ignore
import json
from frappe import _
from requests.auth import HTTPBasicAuth # type: ignore
from vms_app.sap_api.send_sap_team_email import send_sap_team_email


@frappe.whitelist()
def erp_to_sap_material_code(doc_name):
    print("****Calling ERP TO SAP API******",doc_name)
    try:
        requestor = frappe.get_doc("Requestor Master", doc_name)
        material_master = frappe.get_doc("Material Master", requestor.material_master_ref_no)
        onboarding = frappe.get_doc("Material Onboarding", requestor.material_onboarding_ref_no)
        sap_settings = frappe.get_doc("SAP Settings")

        sap_client_code = ""
        material_items = []
        for item in requestor.material_request:
            material_items.append({
                "material_name_description": item.material_name_description or "",
                "material_code_revised": item.material_code_revised or "",
                "company_code": item.company_name or "",
                "plant_name": item.plant_name or "",
                "material_category": item.material_category or "",
                "material_type": item.material_type or "",
                "base_unit_of_measure": item.base_unit_of_measure or "",
                "comment_by_user": item.comment_by_user or "",
                "material_specifications": item.material_specifications or ""
            })
        if not sap_client_code and item.company_name:
            try:
                company_code = item.company_name
                company_doc = frappe.get_doc("Company Master", company_code)
                sap_client_code = company_doc.sap_client_code or ""
            except Exception as e:
                frappe.log_error(f"Company Master fetch failed for {item.company_name}", str(e))
        print("SAP CLIENT CODE--->",sap_client_code)
        company_code = ""
        if requestor.material_request:
            company_code = requestor.material_request[0].company_name

        if not company_code:
            frappe.throw("Company Code is missing from material request item.")

        last_request_id = frappe.db.sql("""
            SELECT request_id FROM `tabRequestor Master`
            WHERE request_id LIKE %s AND LENGTH(request_id) = 7
            ORDER BY request_id DESC LIMIT 1
        """, (f"{company_code}%",), as_dict=True)

        if last_request_id:
            last_number = int(last_request_id[0]['request_id'][-3:])
            new_suffix = f"{last_number + 1:03d}"
        else:
            new_suffix = "001"

        request_id = f"{company_code}{new_suffix}"
        requestor.request_id = request_id
        print("Request ID--->",request_id)
        requestor.save(ignore_permissions=True)

        bukrs = material_items[0]["company_code"] if material_items else ""
        batch_value = material_master.batch_requirements_yn
        batch_management_indicator = "X" if batch_value == "Yes" else ""
        inspection_1 = onboarding.inspection_require
        inspection_sap = "X" if inspection_1 == "Yes" else ""
        inspection_01 = "X" if onboarding.incoming_inspection_01 else ""
        inspection_09 = "X" if onboarding.incoming_inspection_09 else ""
        serial_number = "" if material_master.serial_number_profile == "No" else material_master.serial_number_profile or ""
        material_type_code = frappe.get_value("Material Type Master", {"name": material_items[0]["material_type"]}, "material_type")
        plant_code = frappe.get_value("Plant Master", {"name": material_items[0]["plant_name"]}, "plant_code")
        category_code = frappe.get_value("Material Category Master", {"name": material_items[0]["material_category"]}, "material_category_name")
        storage_code = frappe.get_value("Storage Location Master", {"name": material_master.storage_location}, "storage_location")
        purchase_group_code = frappe.get_value("Purchase Group Master", {"name": material_master.purchasing_group}, "purchase_group_code")
        division_code = frappe.get_value("Division Master", {"name": material_master.division}, "division_code")
        material_group_code = frappe.get_value("Material Group", {"name": material_master.material_group}, "material_group_name")
        mrp_code = frappe.get_value("MRP Type Master", {"name": material_master.mrp_type}, "mrp_code")
        valuation_class_code = frappe.get_value("Valuation Class Master", {"name": onboarding.valuation_class}, "valuation_class_code")
        material_code = frappe.get_value("Material Master", {"name": requestor.material_master_ref_no}, "material_code_revised")

        data_list = {
            "Reqno": "",
            "Matnr": "",
            "Maktx": "",
            "Zmsg": "",
            "Ztext": "",
            "ZMATSet": []
        }
        data = {
            "Reqno": request_id,
            "Bukrs": bukrs,
            "Matnr" :material_code or "",
            "Adrnr": "",
            "Matkey": "",
            "Mat": category_code or "",
            "Mtart": material_type_code or "",
            "Mbrsh": "P",
            "Werks": plant_code or "",
            "Lgort": storage_code or "",
            "Maktx": material_items[0]["material_name_description"] or "",
            "Meins": material_items[0]["base_unit_of_measure"] or "",
            "Matkl": material_group_code or "",
            "Spart": division_code or "",
            "Brgew": "",
            "Ntgew": "",
            "Gewei": "",
            "Bmatnr": "",
            "Xchpf": batch_management_indicator,
            "Mtvfp": material_master.availability_check or "",
            "Ekgrp": purchase_group_code or "",
            "Bstme": material_master.purchase_uom or "",
            "Umrez": material_master.numerator_purchase_uom or "",
            "Umren": material_master.denominator_purchase_uom or "",
            "Webaz": material_master.gr_processing_time or "",
            "Dismm": mrp_code or "",
            "Dispo": material_master.mrp_controller_revised or "",
            "Disls": material_master.lot_size_key or "",
            "Bstma": "",
            "Mabst": "",
            "Beskz": material_master.procurement_type or "",
            "Lgortep": "",
            "Plifz": material_master.lead_time or "",
            "Fhori": material_master.scheduling_margin_key or "",
            "Eisbe": "",
            "Mhdrz": onboarding.minimum_remaining_shell_life or "",
            "Mhdhb": onboarding.total_shell_life or "",
            "Iprkz": onboarding.expiration_date or "",
            "Prctr": onboarding.profit_center or "",
            "Ausme": material_master.issue_unit or "",
            "Umren1": material_master.numerator_issue_uom or "",
            "Umrez1": material_master.denominator_issue_uom or "",
            "Qmatv": inspection_sap,
            "Qminst": inspection_01,
            "Qminst1": inspection_09,
            "Prfrq": onboarding.inspection_interval or "",
            "Bklas": valuation_class_code or "",
            "Vprsv": onboarding.price_control or "",
            "Ncost": onboarding.do_not_cost or "",
            "Ekalr": "X",
            "Hkmat": "X",
            "Oldmat": material_master.old_material_code or "",
            "Sernp": serial_number,
            "Taxim": "1",
            "Steuc": "",
            "Aedat": "",
            "Aezet": "",
            "Aenam": "",
            "Emailid": "",
            "Storecom": onboarding.comment_by_store or "",
            "Purcom": material_master.purchase_order_text or "",
            "Taxcom": "",
            "Div": "",
            "Ygroup": "",
            "Sgroup": "",
            "Tcode": "", 
            "Ekwsl": material_master.purchasing_value_key or "",
            "Mstcom": "",
            "Qacom": "",
            "Class": material_master.class_type or "",
            "Klart": material_master.class_number or "",
            "Disgr": material_master.mrp_group or "",
            "Lgpro": "",
            "Serlv": ""
        }

        data_list["ZMATSet"].append(data)
        # if debug:
        #     return {
        #         "status": "debug",
        #         "data": data,
        #         "data_list": data_list
        #     }

        # Send to SAP
        url = f"{sap_settings.url}{sap_client_code}"
        headers = {
            'x-csrf-token': 'fetch',
            'Authorization': f"{sap_settings.authorization_type} {sap_settings.authorization_key}",
            'Content-Type': 'application/json'
        }
        auth = HTTPBasicAuth(sap_settings.auth_user_name, sap_settings.auth_user_pass)
        response = requests.get(url, headers=headers, auth=auth)

        if response.status_code == 200:
            csrf_token = response.headers.get('x-csrf-token')
            key1 = response.cookies.get(f'SAP_SESSIONID_BHD_{sap_client_code}')
            key2 = response.cookies.get('sap-usercontext')

            # Send data
            send_material_detail(csrf_token, data_list, key1, key2, sap_client_code, doc_name)
            return {"status": "success", "data_sent": data_list}
        else:
            frappe.log_error(f"Failed to fetch CSRF token: {response.status_code}", "ERP to SAP Material Code")
            return {"status": "fail", "error": "Could not fetch CSRF token"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "ERP to SAP Material Code Error")
        return {"status": "error", "message": str(e)}

def safe_get(obj, list_name, index, attr, default=""):
    try:
        return getattr(getattr(obj, list_name)[index], attr) or default
    except (AttributeError, IndexError, TypeError):
        return default

@frappe.whitelist(allow_guest=True)
def send_material_detail(csrf_token, data_list, key1, key2, sap_client_code, doc_name):
    print("************* Entered send_material_detail *************")
    try:
        sap_settings = frappe.get_doc("SAP Settings")
        erp_to_sap_pr_url = sap_settings.url
        url = f"{erp_to_sap_pr_url}{sap_client_code}"
        header_auth_type = sap_settings.authorization_type
        header_auth_key = sap_settings.authorization_key
        user = sap_settings.auth_user_name
        password = sap_settings.auth_user_pass

        headers = {
            'X-CSRF-TOKEN': csrf_token,
            'Authorization': f"{header_auth_type} {header_auth_key}",
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json',
            'Cookie': f"SAP_SESSIONID_BHD_{sap_client_code}={key1}; sap-usercontext={key2}"
        }

        auth = HTTPBasicAuth(user, password)
        print("Sending payload to SAP...")
        print("Headers:", headers)
        print("Payload:", json.dumps(data_list, indent=2))
        print("*************")
        
        response = requests.post(url, headers=headers, auth=auth, json=data_list)
        print("Response received from SAP")

        try:
            mo_sap_code = response.json()
        except Exception as parse_error:
            print("Failed to parse SAP response as JSON:", parse_error)
            mo_sap_code = response.text

        print("SAP Response Content:", mo_sap_code)

        sap_log = frappe.new_doc("Material SAP Logs")
        sap_log.requestor_ref_no = doc_name
        sap_log.erp_to_sap_data = json.dumps(data_list, indent=2)
        sap_log.sap_response = response.text
        sap_log.save(ignore_permissions=True)
        frappe.db.commit()

        if response.status_code == 201:
            if isinstance(mo_sap_code, dict):
                ztext = mo_sap_code.get("d", {}).get("Ztext", "").strip().lower()
            if ztext == "record insreated.":
                frappe.msgprint("✅ Material record successfully sent to SAP.", alert=True)
                print("Material Onboarding posted successfully.")
                frappe.db.set_value("Requestor Master", doc_name, "approval_status", "Sent to SAP")
                frappe.db.commit()
                send_sap_team_email(doc_name)
        else:
            print(f"SAP POST returned status: {response.status_code}")

        return mo_sap_code

    except Exception as e:
        traceback_str = frappe.get_traceback()
        print("Exception in send_material_detail:")
        print(traceback_str)
        frappe.log_error(traceback_str, "SAP Sync Error")

        return {"status": "error", "message": str(e)}