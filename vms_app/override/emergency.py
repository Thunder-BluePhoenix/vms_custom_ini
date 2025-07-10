import frappe
from frappe import _

@frappe.whitelist()
def delete_material_master_workflow():
    """
    Complete workflow to delete Material Code Master and Material Type Master documents
    
    Steps:
    1. Cancel all Material Code Master documents
    2. Delete all Material Code Master documents
    3. Cancel all Material Type Master documents
    4. Delete all Material Type Master documents
    
    Returns:
        dict: Complete summary of the deletion workflow
    """
    try:
        workflow_summary = {
            "success": False,
            "steps_completed": [],
            "material_code_master": {
                "cancelled": 0,
                "deleted": 0,
                "failed": 0,
                "errors": []
            },
            "material_type_master": {
                "cancelled": 0,
                "deleted": 0,
                "failed": 0,
                "errors": []
            },
            "total_time": None
        }
        
        import time
        start_time = time.time()
        
        # Step 1: Cancel all Material Code Master documents
        frappe.publish_progress(10, title="Processing Material Code Master", description="Cancelling submitted documents...")
        
        mcm_cancel_result = cancel_all_submitted_docs("Material Code Master")
        workflow_summary["material_code_master"]["cancelled"] = mcm_cancel_result.get("cancelled_count", 0)
        workflow_summary["material_code_master"]["errors"].extend(mcm_cancel_result.get("errors", []))
        workflow_summary["steps_completed"].append("Material Code Master - Cancellation")
        
        # Step 2: Delete all Material Code Master documents
        frappe.publish_progress(30, title="Processing Material Code Master", description="Deleting all documents...")
        
        mcm_delete_result = delete_all_submittable_docs("Material Code Master", force_delete=False)
        workflow_summary["material_code_master"]["deleted"] = mcm_delete_result["summary"]["deleted"]
        workflow_summary["material_code_master"]["failed"] = mcm_delete_result["summary"]["failed"]
        workflow_summary["material_code_master"]["errors"].extend(mcm_delete_result["summary"]["errors"])
        workflow_summary["steps_completed"].append("Material Code Master - Deletion")
        
        # Step 3: Cancel all Material Type Master documents
        frappe.publish_progress(60, title="Processing Material Type Master", description="Cancelling submitted documents...")
        
        mtm_cancel_result = cancel_all_submitted_docs("Material Type Master")
        workflow_summary["material_type_master"]["cancelled"] = mtm_cancel_result.get("cancelled_count", 0)
        workflow_summary["material_type_master"]["errors"].extend(mtm_cancel_result.get("errors", []))
        workflow_summary["steps_completed"].append("Material Type Master - Cancellation")
        
        # Step 4: Delete all Material Type Master documents
        frappe.publish_progress(90, title="Processing Material Type Master", description="Deleting all documents...")
        
        mtm_delete_result = delete_all_submittable_docs("Material Type Master", force_delete=False)
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


def cancel_all_submitted_docs(doctype):
    """
    Cancel all submitted documents in a doctype
    """
    try:
        submitted_docs = frappe.get_all(doctype, filters={"docstatus": 1}, fields=["name"])
        
        if not submitted_docs:
            return {
                "success": True,
                "message": f"No submitted documents found in {doctype}",
                "cancelled_count": 0,
                "errors": []
            }
        
        cancelled_count = 0
        failed_count = 0
        errors = []
        
        for i, doc_info in enumerate(submitted_docs):
            try:
                # Progress update for large datasets
                if len(submitted_docs) > 10 and i % 10 == 0:
                    progress = int((i / len(submitted_docs)) * 100)
                    frappe.publish_progress(progress, title=f"Cancelling {doctype}", 
                                          description=f"Processing {i+1} of {len(submitted_docs)}")
                
                doc = frappe.get_doc(doctype, doc_info.name)
                doc.cancel()
                cancelled_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append(f"Failed to cancel {doc_info.name}: {str(e)}")
                frappe.log_error(f"Error cancelling {doctype} {doc_info.name}: {str(e)}")
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": f"Cancellation process completed for {doctype}",
            "cancelled_count": cancelled_count,
            "failed_count": failed_count,
            "errors": errors
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in cancel_all_submitted_docs for {doctype}: {str(e)}")
        raise


def delete_all_submittable_docs(doctype, force_delete=False):
    """
    Delete all documents from a submittable doctype
    """
    try:
        all_docs = frappe.get_all(doctype, fields=["name", "docstatus"])
        
        if not all_docs:
            return {
                "success": True,
                "message": f"No documents found in {doctype}",
                "summary": {
                    "total": 0,
                    "cancelled": 0,
                    "deleted": 0,
                    "failed": 0,
                    "errors": []
                }
            }
        
        summary = {
            "total": len(all_docs),
            "cancelled": 0,
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
                docstatus = doc_info.docstatus
                
                if docstatus == 1:  # Submitted
                    if force_delete:
                        frappe.db.delete(doctype, {"name": doc_name})
                        summary["deleted"] += 1
                    else:
                        # Should already be cancelled, but double-check
                        doc = frappe.get_doc(doctype, doc_name)
                        if doc.docstatus == 1:
                            doc.cancel()
                            summary["cancelled"] += 1
                        
                        frappe.delete_doc(doctype, doc_name, force=True)
                        summary["deleted"] += 1
                        
                elif docstatus == 2:  # Cancelled
                    frappe.delete_doc(doctype, doc_name, force=True)
                    summary["deleted"] += 1
                    
                else:  # Draft
                    frappe.delete_doc(doctype, doc_name)
                    summary["deleted"] += 1
                    
            except Exception as e:
                summary["failed"] += 1
                summary["errors"].append(f"Failed to process {doc_name}: {str(e)}")
                frappe.log_error(f"Error deleting {doctype} {doc_name}: {str(e)}")
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": f"Deletion process completed for {doctype}",
            "summary": summary
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in delete_all_submittable_docs for {doctype}: {str(e)}")
        raise


@frappe.whitelist()
def get_material_master_summary():
    """
    Get summary of Material Code Master and Material Type Master documents
    """
    try:
        # Material Code Master summary
        mcm_summary = frappe.db.sql("""
            SELECT 
                docstatus,
                COUNT(*) as count,
                CASE 
                    WHEN docstatus = 0 THEN 'Draft'
                    WHEN docstatus = 1 THEN 'Submitted'
                    WHEN docstatus = 2 THEN 'Cancelled'
                    ELSE 'Unknown'
                END as status_name
            FROM `tabMaterial Code Master`
            GROUP BY docstatus
        """, as_dict=True)
        
        # Material Type Master summary
        mtm_summary = frappe.db.sql("""
            SELECT 
                docstatus,
                COUNT(*) as count,
                CASE 
                    WHEN docstatus = 0 THEN 'Draft'
                    WHEN docstatus = 1 THEN 'Submitted'
                    WHEN docstatus = 2 THEN 'Cancelled'
                    ELSE 'Unknown'
                END as status_name
            FROM `tabMaterial Type Master`
            GROUP BY docstatus
        """, as_dict=True)
        
        mcm_total = sum(item.count for item in mcm_summary)
        mtm_total = sum(item.count for item in mtm_summary)
        
        return {
            "success": True,
            "material_code_master": {
                "total_documents": mcm_total,
                "status_breakdown": mcm_summary
            },
            "material_type_master": {
                "total_documents": mtm_total,
                "status_breakdown": mtm_summary
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_material_master_summary: {str(e)}")
        frappe.throw(_("An error occurred while getting summary: {0}").format(str(e)))


# Emergency force delete function
@frappe.whitelist()
def force_delete_material_master_workflow():
    """
    Emergency function to force delete all Material Code Master and Material Type Master documents
    WARNING: This bypasses all validations
    """
    try:
        results = {}
        
        # Force delete Material Code Master
        mcm_count = frappe.db.count("Material Code Master")
        if mcm_count > 0:
            frappe.db.sql("DELETE FROM `tabMaterial Code Master`")
            results["material_code_master_deleted"] = mcm_count
        
        # Force delete Material Type Master
        mtm_count = frappe.db.count("Material Type Master")
        if mtm_count > 0:
            frappe.db.sql("DELETE FROM `tabMaterial Type Master`")
            results["material_type_master_deleted"] = mtm_count
        
        # Clear related child tables if they exist
        child_tables = ["Material Code Master Item", "Material Type Master Item", 
                       "Material Code Master Details", "Material Type Master Details"]  # Add more if needed
        
        for table in child_tables:
            try:
                frappe.db.sql(f"DELETE FROM `tab{table}`")
                results[f"{table}_cleared"] = True
            except:
                pass
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": "Force deletion completed",
            "results": results
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error in force_delete_material_master_workflow: {str(e)}")
        frappe.throw(_("An error occurred during force deletion: {0}").format(str(e)))