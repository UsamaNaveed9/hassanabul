// Copyright (c) 2023, SMB and contributors
// For license information, please see license.txt

frappe.ui.form.on('Order Items', {
	get_items: function(frm) {
		frm.clear_table("items");
		frappe.call({
			method: "hassanabul.hassan_abul.doctype.order_items.order_items.get_all_items",
			freeze: true,
			freeze_message: "Processing",
			callback: function(r) {
					if(r.message) {
						//console.log(r.message);
						let items_details = r.message;
						for (let i = 0; i < items_details.length; i++){
							let row_item = cur_frm.add_child("items");
							row_item.item_code = items_details[i].item_code;
							row_item.item_name = items_details[i].item_name;
							row_item.item_group = items_details[i].item_group;
							row_item.qty_onhand = items_details[i].qty_onhand;
							row_item.uom = items_details[i].stock_uom;
							row_item.unit_cost = items_details[i].valuation_rate;
							cur_frm.refresh_field("items");
						}
					}
			}
		});
	}
});
