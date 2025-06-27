import json
import frappe
from frappe import _
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def custom_employee_login():
    try:
        data = json.loads(frappe.request.data)
    except Exception as e:
        return {"status": "fail", "message": "Invalid request data."}

    usr = data.get("usr")
    pwd = data.get("pwd")
    if not usr.endswith("@merillife.com"):
        return {"status": "fail", "message": "Only @merillife.com emails are allowed."}

    employee = frappe.db.get("Employee Master", {"email": usr})
    if not employee:
        return {"status": "fail", "message": "User not found in Employee Master."}

    if not frappe.db.exists("User", usr):
        new_user = frappe.get_doc({
            "doctype": "User",
            "email": usr,
            "first_name": employee.full_name,
            "enabled": 1,
            "new_password": pwd,
            "send_welcome_email": 0,
            "roles": [{"role": "System Manager"}]
        })
        new_user.flags.ignore_permissions = True
        new_user.insert(ignore_permissions=True)

    # Login using Frappe LoginManager
    try:
        frappe.local.login_manager = LoginManager()
        frappe.local.login_manager.authenticate(usr, pwd)
        frappe.local.login_manager.post_login()
    except frappe.AuthenticationError:
        return {"status": "fail", "message": "Invalid username or password."}

    company_code = employee.company
    company_name = frappe.db.get_value("Company Master", {'name': company_code}, 'company_name')
    company_short = frappe.db.get_value("Company Master", {'name': company_code}, 'short_form')

    return {
        "status": "success",
        "message": "Logged in",
        "sid": frappe.session.sid,
        "email": usr,
        "full_name": employee.full_name,
        "role": employee.role,
        "company_code": company_code,
        "user_company": company_name,
        "company_short_form": company_short
    }
