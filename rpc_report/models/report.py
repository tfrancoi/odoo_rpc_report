import base64

from odoo import api, models

class RPCReport(models.Model):
    _inherit = 'ir.actions.report.xml'

    @api.model
    def render_rpc(self, res_ids, name, data):
        res = self.render_report(res_ids, name, data)
        if isinstance(res, tuple):
            return base64.b64encode(res[0]), res[1]
        else:
            return base64.b64encode(res)
