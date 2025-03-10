import frappe
import secrets

@frappe.whitelist(allow_guest=True)
def create_rfq(select_service, consignee_name, division):
    token = secrets.token_hex(16)
    print("********************************************************")
    print(csrf_token)
    if frappe.request.method == 'POST' and frappe.form_dict.get('csrf_token') == token:
        frappe.logger().debug('Received POST request with data: Service: {}, Consignee: {}, Division: {}'.format(select_service, consignee_name, division))
        doc = frappe.get_doc({
            'doctype': 'Request For Quotation',
            'select_service': select_service,
            'consignee_name': consignee_name,
            'division': division
        })
        doc.insert(ignore_permissions=True)
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/test"

create_rfq.csrf_exempt = True


# token 061940ef4019166:362286f9d121a49