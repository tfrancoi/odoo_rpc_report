import base64

from odoo import api, models

class RPCReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.multi
    def render_rpc(self, res_ids, data):
        res = self.render(res_ids, data)
        if isinstance(res, tuple):
            return base64.b64encode(res[0]), res[1]
        else:
            return base64.b64encode(res)
