#!/usr/bin/env python3
from odoolib import get_connection
import base64

connection = get_connection(hostname="localhost", database='report', port=8069, login='admin', password='admin', protocol='jsonrpc')

model_data = connection.get_model('ir.model.data')

#get a demo data
_, sale_order_id = model_data.get_object_reference('sale', 'sale_order_7')


report = connection.get_model('ir.actions.report.xml')
res = report.render_rpc([sale_order_id], 'sale.report_saleorder', False)




outfile = open('sale.pdf', 'wb')
outfile.write(base64.b64decode(res[0]))
outfile.close()
