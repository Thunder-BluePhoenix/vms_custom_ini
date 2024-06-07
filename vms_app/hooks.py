app_name = "vms_app"
app_title = "vms"
app_publisher = "vms"
app_description = "vms"
app_email = "vms@vms.com"
app_license = "mit"
required_apps = []
# from vms_app.api.api import cron_method
import frappe
from frappe import hooks

def after_request(response):
	response.headers["Access-Control-Allow-Origin"] = "*"
	response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
	response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
	return response

hooks.after_request = [after_request]


# def schedule_cron_method():
# 	frappe.enqueue("vms_app.vms_app.api.api.cron_method", queue='short')


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vms_app/css/vms_app.css"
#app_include_js = "/assets/vms_app/js/vms_app.js"
app_include_js = "/vms_app/public/js/custom_keyboard_shortcuts.js"

response_headers = [
    {"fieldname": "Access-Control-Allow-Origin", "value": "*"}
]

fixtures = [ 
'Export Entry',
'Export Entry Vendor',
'Import Entry',
'Request For Quotation',
'Vendor Onboarding',
'Vendor Master',
'Tax Master',
'Shipment Type Master',
'RFQ Type Master',
'Port Master',
'Package Type Master',
'Company Master',
'City Master',
'District Master',
'Certificate Master',
'Product Master',
'Vendor Type Master',
'Department Master',
'Material Master',
'Currency Master',
'Terms Of Payment Master',
'Purchase Group Master',
'Account Master',
'Company Nature Master',
'Business Nature Master',
'Pincode Master',
'State Master',
'Country Master',
'Bank Master',
'GST Registration Type Master',
'Designation Master',
'Product Category Master',
'Brand Master',
'Product Variant Master',
'UOM Master',
'Account Group Master',
'Incoterm Master',
'Quotation',
'Vendor Master',
'Vendor Onboarding',
'Request For Quotation', 
'Import Entry',
'Quotation',
'Purchase Order',
'Export Entry Vendor'

]

# include js, css files in header of web template
# web_include_css = "/assets/vms_app/css/vms_app.css"
# web_include_js = "/assets/vms_app/js/vms_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vms_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}


# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "vms_app/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "vms_app.utils.jinja_methods",
# 	"filters": "vms_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "vms_app.install.before_install"
# after_install = "vms_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "vms_app.uninstall.before_uninstall"
# after_uninstall = "vms_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "vms_app.utils.before_app_install"
# after_app_install = "vms_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "vms_app.utils.before_app_uninstall"
# after_app_uninstall = "vms_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vms_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		# "on_update": "method",
		# "on_cancel": "method",
		# "on_trash": "method"

	},
	"Vendor Master": {

		#"validate": "vms_app.masters.doctype.vendor_master.vendor_master.hit"
		#"validate": "vms_app.api.api.send_email"
		"after_insert": "vms_app.api.api.send_email",
		#"after_insert": "vms_app.api.api.sap_fetch_token"
		#"after_insert": "vms_app.api.api.generate_onboarding_link"
		#"validate": "vms_app.api.api.create_sap_so_from_po"
	},
	"Vendor Onboarding": {

	"validate": "vms_app.api.api.send_email_on_onboarding"

	},
	"Request For Quotation":{

		#isko bhi uncomment karna hai "validate": "vms_app.api.api.hitt",
		"after_insert": "vms_app.api.api.set_rfq_raisers_name"

	},
	"Import Entry":{
	#"after_insert": "vms_app.api.api.calculate",
	#"after_insert": "vms_app.api.api.extract_text_from_pdf",
	#"after_insert": "vms_app.vms.doctype.import_entry.import_entry.test_method"

	
	},
	"Quotation": {

	#iskouncommentkarnahaibadmai"validate": "vms_app.api.api.send_email_on_quotation_creation"

	},
	"Purchase Order": {

	#iskouncommentkarnahai"validate": "vms_app.api.api.send_email_on_po_creation"

	},

	"Export Entry Vendor": {

	#"after_insert": "vms_app.api.api.calculate_export_entry"

	}


}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"vms_app.tasks.all"
# 	],
# 	"daily": [
# 		"vms_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"vms_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"vms_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"vms_app.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "vms_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "vms_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vms_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vms_app.utils.before_request"]
# after_request = ["vms_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["vms_app.utils.before_job"]
# after_job = ["vms_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"vms_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }




#     data =  {
#     "Bukrs": company_code,
#     "Ekorg": data.get("purchase_organization"),
#     "Ktokk": "ZDOM",
#     "Title": data.get("ZDOM"),
#     "Name1": data.get('Name1'),
#     "Name2": "",
#     "Sort1": data.get('Sort1'),
#     "Street": data.get('Street'),
#     "StrSuppl1": data.get('StrSuppl1'),
#     "StrSuppl2": data.get('StrSuppl2'),
#     "StrSuppl3": data.get('StrSuppl3'),
#     "PostCode1": pincode,
#     "City1": city,
#     "Country": country,
#     "J1kftind": "",
#     "Region": state,
#     "TelNumber": "",
#     "MobNumber": "1256651",
#     "SmtpAddr": "hitesh.mahto@merillife.com",
#     "SmtpAddr1": "hitesh@gmail.com",
#     "Zuawa": "",
#     "Akont": "16101020",
#     "Waers": currency,
#     "Zterm": terms_of_payment,
#     "Inco1": incoterms1,
#     "Inco2": incoterms2,
#     "Kalsk": "",
#     "Ekgrp": purchasing_group,
#     "Xzemp": "X",
#     "Reprf": "X",
#     "Webre": "X",
#     "Lebre": "",
#     "Stcd3": "GST12345",
#     "J1ivtyp": vendor_type,
#     "J1ipanno": data.get('J1ipanno'),
#     "J1ipanref": "Hitesh Mahto",
#     "Namev": "Hitesh",
#     "Name11": "Mahto",
#     "Bankl": "HDFC0000170",
#     "Bankn": "ac91201001898261",
#     "Bkref": "2001",
#     "Banka": "UTIB0019191",
#     "Xezer": "",
#     "Refno": "VMS/368b008a78/0101",
#     "Vedno": "",
#     "Zmsg": ""
# }

   # company_code = frappe.db.get_value("Company Master", filters={'name': data.get('Bukrs')}, fieldname='company_code')
   #  purchase_organization = frappe.db.get_value("Company Master", filters={'name': data.get('Ekorg')}, fieldname='company_code')
   #  pincode = frappe.db.get_value("Pincode Master", filters={'name': data.get('PostCode1')}, fieldname='pincode')
   #  city = frappe.db.get_value("City Master", filters={'name': data.get('City1')}, fieldname='city_name')
   #  country = frappe.db.get_value("Country Master", filters={'name': data.get('country')}, fieldname='country_name')
   #  state = frappe.db.get_value("State Master", filters={'name': data.get('Region')}, fieldname='state_name')
   #  currency = frappe.db.get_value("Currency Master", filters={'name': data.get('Waers')}, fieldname='currency_code')
   #  terms_of_payment = frappe.db.get_value("Terms Of Payment Master", filters={'name': data.get('Zterm')}, fieldname='terms_of_payment_name')
   #  incoterms1 = frappe.db.get_value("Incoterm Master", filters={'name': data.get('Inco1')}, fieldname='incoterm_name')
   #  incoterms2 = frappe.db.get_value("Incoterm Master", filters={'name': data.get('Inco1')}, fieldname='incoterm_name')
   #  #purchase_group = frappe.db.get_value("Purchase Group Master", filters={'name': data.get('purchase_group')}, fieldname='purchase_group_name')
   #  vendor_type = frappe.db.get_value("Vendor Type Master", filters={'name': data.get('J1ivtyp')}, fieldname='vendor_type_name')
   #  purchasing_group = frappe.db.get_value("Purchase Group Master", filters={'name': data.get('Ekgrp')},fieldname='' )

