# Copyright (c) 2023, SMB and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OrderItems(Document):
	# def before_save(self):
	# 	if self.items:
	# 		for row in self.items:
	# 			if(row.processing_qty==0):
	# 				row.processing_qty = 1

	def on_submit(self):
		if self.items:
			mr = frappe.new_doc("Material Request")
			mr.material_request_type = "Purchase"
			mr.transaction_date = self.posting_date
			mr.schedule_date = self.posting_date
			mr.order_items = self.name
			
			for row in self.items:
				mr_item = frappe.new_doc("Material Request Item")
				mr_item.item_code = row.item_code
				mr_item.item_name = row.item_name
				mr_item.schedule_date = self.posting_date
				mr_item.qty = row.processing_qty
				mr_item.uom = row.uom
				mr.append("items", mr_item)

			mr.save()
			mr.submit()				


@frappe.whitelist()
def get_all_items(supplier,item_group):
	items = frappe.db.sql("""
        SELECT i.item_code, i.item_name, i.item_group, i.stock_uom, i.size_p
        FROM `tabItem` i
        INNER JOIN `tabItem Supplier` s ON s.parent = i.name
        WHERE s.supplier = %s and i.disabled = 0 and i.has_variants = 0 and i.item_group = %s
        """, (supplier,item_group), as_dict=True)

	for row in items:
		row['valuation_rate'] = frappe.db.get_value("Bin", {"item_code":row.item_code}, "valuation_rate")
		row['qty_onhand'] = frappe.db.get_value("Bin", {"item_code":row.item_code}, "actual_qty")

	return items






	# main_items = []
	# for so in sales_order:
	# 	so_items = frappe.db.sql('''select item_code,item_name,qty,uom,rate,amount,parent from `tabSales Order Item` 
	# 						where `tabSales Order Item`.parent = "{0}"'''.format(so),as_dict = 1)
	# 	for soi in so_items:					
	# 		main_items.append(soi)					

	# bom = {}
	# boms = []
	# recipe_item = {}
	# recipe_items = []

	# for item in main_items:
	# 	bom['bom_name'] = frappe.db.get_value("BOM", {"item": item.item_code, "is_default": 1}, "name")
	# 	bom['total_cost'] = frappe.db.get_value("BOM", {"item": item.item_code, "is_default": 1}, "total_cost")
	# 	bom['main_item'] = item.item_code
	# 	bom['sales_order'] = item.parent					

	# 	bom_copy = bom.copy()
	# 	boms.append(bom_copy)

	# 	if bom['bom_name']:
	# 		bom_doc = frappe.get_doc('BOM', bom['bom_name'])
	# 		bom_doc_items = bom_doc.items
	# 		for re_item in bom_doc_items:
	# 			recipe_item['item_code'] = re_item.item_code
	# 			recipe_item['item_name'] = re_item.item_name
	# 			recipe_item['qty'] = re_item.qty
	# 			recipe_item['uom'] = re_item.uom
	# 			recipe_item['available_qty'] = frappe.db.get_value("Bin", {"item_code":re_item.item_code, "warehouse":source_warehouse}, "actual_qty")
	# 			recipe_item['rate'] = frappe.db.get_value("Bin", {"item_code":re_item.item_code, "warehouse":source_warehouse}, "valuation_rate")
	# 			recipe_item['amount'] = recipe_item['qty'] * recipe_item['rate']
	# 			recipe_item['parent_item'] = item.item_code
	# 			recipe_item['bom'] = re_item.parent
	# 			recipe_item['sales_order'] = item.parent

	# 			recipe_item_copy = recipe_item.copy()
	# 			recipe_items.append(recipe_item_copy)

	
	# return main_items,boms,recipe_items
