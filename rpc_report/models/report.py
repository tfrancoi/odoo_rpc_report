import base64

from odoo import api, models
from odoo.http import request, root

class RPCReport(models.Model):
    _inherit = 'ir.actions.report.xml'

    def _force_session_store(self):
        """
            Authenticate like a normal user to have all the needed info
            in the session and save the session on the filesystem prior to call
            wkhtmltopdf
        """
        password = request.params['args'][2]
        db = request.params['args'][0]
        request.session.authenticate(db, self.env.user.login, password)
        root.session_store.save(request.session)

    @api.model
    def render_rpc(self, res_ids, name, data):
        self._force_session_store()
        res = self.render_report(res_ids, name, data)
        if isinstance(res, tuple):
            return base64.b64encode(res[0]), res[1]
        else:
            return base64.b64encode(res)
