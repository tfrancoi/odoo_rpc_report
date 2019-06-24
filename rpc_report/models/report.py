import base64
import xmltodict

from odoo import api, models
from odoo.http import request, root

class RPCReport(models.Model):
    _inherit = 'ir.actions.report'

    def _force_session_store(self):
        """
            Authenticate like a normal user to have all the needed info
            in the session and save the session on the filesystem prior to call
            wkhtmltopdf
        """
        db, password = '', ''
        if request.params: #Case of jsonrpc
            password = request.params['args'][2]
            db = request.params['args'][0]
        elif request.httprequest._cached_data: #Case of xmlrpc
            req = xmltodict.parse(request.httprequest._cached_data)
            password = req['methodCall']['params']['param'][2]['value']['string']
            db = req['methodCall']['params']['param'][0]['value']['string']
        if db and password:
            request.session.authenticate(db, self.env.user.login, password)
            root.session_store.save(request.session)


    @api.multi
    def render_rpc(self, res_ids, data):
        self._force_session_store()
        res = self.render(res_ids, data)
        if isinstance(res, tuple):
            return base64.b64encode(res[0]), res[1]
        else:
            return base64.b64encode(res)
