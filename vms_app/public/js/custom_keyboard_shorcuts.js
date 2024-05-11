frappe.ui.keys.add_shortcut({

	"description": "Show error Logs",
	"shortcut": "shift+ctrl+s",
	action: () => {

		frappe.set_route("List", "Error Log")


	}




})