import frappe
from frappe import _

@frappe.whitelist()
def delete_material_master_workflow():
    """
    Complete workflow to delete Material Code Master and Material Type Master documents
    (Non-submittable doctypes - direct deletion)
    
    Steps:
    1. Clear material_type field in all Material Code Master documents
    2. Delete all Material Code Master documents
    3. Delete all Material Type Master documents
    
    Returns:
        dict: Complete summary of the deletion workflow
    """
    try:
        workflow_summary = {
            "success": False,
            "steps_completed": [],
            "material_code_master": {
                "fields_cleared": 0,
                "deleted": 0,
                "failed": 0,
                "errors": []
            },
            "material_type_master": {
                "deleted": 0,
                "failed": 0,
                "errors": []
            },
            "total_time": None
        }
        
        import time
        start_time = time.time()
        
        # Step 1: Clear material_type field in all Material Code Master documents
        frappe.publish_progress(15, title="Processing Material Code Master", description="Clearing material_type field...")
        
        clear_result = clear_material_type_field()
        workflow_summary["material_code_master"]["fields_cleared"] = clear_result["cleared_count"]
        workflow_summary["material_code_master"]["errors"].extend(clear_result.get("errors", []))
        workflow_summary["steps_completed"].append("Material Code Master - Field Clearing")
        
        # Step 2: Delete all Material Code Master documents
        frappe.publish_progress(40, title="Processing Material Code Master", description="Deleting all documents...")
        
        mcm_delete_result = delete_all_docs("Material Code Master")
        workflow_summary["material_code_master"]["deleted"] = mcm_delete_result["summary"]["deleted"]
        workflow_summary["material_code_master"]["failed"] = mcm_delete_result["summary"]["failed"]
        workflow_summary["material_code_master"]["errors"].extend(mcm_delete_result["summary"]["errors"])
        workflow_summary["steps_completed"].append("Material Code Master - Deletion")
        
        # Step 3: Delete all Material Type Master documents
        frappe.publish_progress(80, title="Processing Material Type Master", description="Deleting all documents...")
        
        mtm_delete_result = delete_all_docs("Material Type Master")
        workflow_summary["material_type_master"]["deleted"] = mtm_delete_result["summary"]["deleted"]
        workflow_summary["material_type_master"]["failed"] = mtm_delete_result["summary"]["failed"]
        workflow_summary["material_type_master"]["errors"].extend(mtm_delete_result["summary"]["errors"])
        workflow_summary["steps_completed"].append("Material Type Master - Deletion")
        
        # Calculate total time
        end_time = time.time()
        workflow_summary["total_time"] = f"{end_time - start_time:.2f} seconds"
        
        workflow_summary["success"] = True
        
        frappe.publish_progress(100, title="Completed", description="All documents processed successfully!")
        
        return workflow_summary
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in delete_material_master_workflow: {str(e)}")
        frappe.throw(_("An error occurred during the deletion workflow: {0}").format(str(e)))


def delete_all_docs(doctype):
    """
    Delete all documents from a non-submittable doctype
    """
    try:
        all_docs = frappe.get_all(doctype, fields=["name"])
        
        if not all_docs:
            return {
                "success": True,
                "message": f"No documents found in {doctype}",
                "summary": {
                    "total": 0,
                    "deleted": 0,
                    "failed": 0,
                    "errors": []
                }
            }
        
        summary = {
            "total": len(all_docs),
            "deleted": 0,
            "failed": 0,
            "errors": []
        }
        
        for i, doc_info in enumerate(all_docs):
            try:
                # Progress update for large datasets
                if len(all_docs) > 10 and i % 10 == 0:
                    progress = int((i / len(all_docs)) * 100)
                    frappe.publish_progress(progress, title=f"Deleting {doctype}", 
                                          description=f"Processing {i+1} of {len(all_docs)}")
                
                doc_name = doc_info.name
                
                # Direct deletion for non-submittable doctypes
                frappe.delete_doc(doctype, doc_name, force=True)
                summary["deleted"] += 1
                    
            except Exception as e:
                summary["failed"] += 1
                summary["errors"].append(f"Failed to delete {doc_name}: {str(e)}")
                frappe.log_error(f"Error deleting {doctype} {doc_name}: {str(e)}")
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": f"Deletion process completed for {doctype}",
            "summary": summary
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in delete_all_docs for {doctype}: {str(e)}")
        raise


@frappe.whitelist()
def get_material_master_summary():
    """
    Get summary of Material Code Master and Material Type Master documents
    (For non-submittable doctypes - just count total documents)
    """
    try:
        # Material Code Master count
        mcm_count = frappe.db.count("Material Code Master")
        
        # Material Type Master count  
        mtm_count = frappe.db.count("Material Type Master")
        
        return {
            "success": True,
            "material_code_master": {
                "total_documents": mcm_count
            },
            "material_type_master": {
                "total_documents": mtm_count
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_material_master_summary: {str(e)}")
        frappe.throw(_("An error occurred while getting summary: {0}").format(str(e)))


@frappe.whitelist()
def force_delete_material_master_workflow():
    """
    Emergency function to force delete all Material Code Master and Material Type Master documents
    WARNING: This bypasses all validations
    """
    try:
        results = {}
        
        # Get exact table names first to avoid SQL errors
        try:
            # Check if tables exist
            mcm_exists = frappe.db.sql("SHOW TABLES LIKE 'tabMaterial Code Master'")
            mtm_exists = frappe.db.sql("SHOW TABLES LIKE 'tabMaterial Type Master'")
            
            # First clear material_type field in Material Code Master
            if mcm_exists:
                try:
                    cleared_count = frappe.db.sql("""
                        UPDATE `tabMaterial Code Master` 
                        SET material_type = '' 
                        WHERE material_type IS NOT NULL AND material_type != ''
                    """)
                    results["material_type_field_cleared"] = True
                except Exception as e:
                    results["material_type_clear_error"] = str(e)
            
            # Force delete Material Code Master
            if mcm_exists:
                mcm_count = frappe.db.count("Material Code Master")
                if mcm_count > 0:
                    frappe.db.sql("DELETE FROM `tabMaterial Code Master`")
                    results["material_code_master_deleted"] = mcm_count
                else:
                    results["material_code_master_deleted"] = 0
            else:
                results["material_code_master_table_not_found"] = True
            
            # Force delete Material Type Master
            if mtm_exists:
                mtm_count = frappe.db.count("Material Type Master")
                if mtm_count > 0:
                    frappe.db.sql("DELETE FROM `tabMaterial Type Master`")
                    results["material_type_master_deleted"] = mtm_count
                else:
                    results["material_type_master_deleted"] = 0
            else:
                results["material_type_master_table_not_found"] = True
            
        except Exception as e:
            frappe.log_error(f"Error in SQL operations: {str(e)}")
            results["sql_error"] = str(e)
        
        # Try to clear potential child tables
        potential_child_tables = [
            "Material Code Master Item", 
            "Material Type Master Item",
            "Material Code Master Details", 
            "Material Type Master Details",
            "Material Code Master Child",
            "Material Type Master Child"
        ]
        
        for table in potential_child_tables:
            try:
                table_exists = frappe.db.sql(f"SHOW TABLES LIKE 'tab{table}'")
                if table_exists:
                    count = frappe.db.count(table)
                    if count > 0:
                        frappe.db.sql(f"DELETE FROM `tab{table}`")
                        results[f"{table}_cleared"] = count
            except Exception as e:
                # Silent fail for child tables that may not exist
                results[f"{table}_error"] = str(e)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": "Force deletion completed",
            "results": results
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in force_delete_material_master_workflow: {str(e)}")
        return {
            "success": False,
            "message": f"Force deletion failed: {str(e)}",
            "error": str(e)
        }


@frappe.whitelist()
def check_table_structure():
    """
    Helper function to check the actual table structure and names
    Useful for debugging
    """
    try:
        results = {}
        
        # Check if tables exist
        tables_to_check = [
            "Material Code Master",
            "Material Type Master"
        ]
        
        for table in tables_to_check:
            try:
                # Check table existence
                table_exists = frappe.db.sql(f"SHOW TABLES LIKE 'tab{table}'")
                results[f"{table}_exists"] = len(table_exists) > 0
                
                if len(table_exists) > 0:
                    # Get table structure
                    structure = frappe.db.sql(f"DESCRIBE `tab{table}`", as_dict=True)
                    results[f"{table}_structure"] = [col.Field for col in structure]
                    
                    # Get count
                    count = frappe.db.count(table)
                    results[f"{table}_count"] = count
                    
            except Exception as e:
                results[f"{table}_error"] = str(e)
        
        return {
            "success": True,
            "results": results
        }
        
    except Exception as e:
        frappe.log_error(f"Error in check_table_structure: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }