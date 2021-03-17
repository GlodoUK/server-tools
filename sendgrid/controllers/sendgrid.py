from odoo import http, api, SUPERUSER_ID, registry
from odoo.http import request
import contextlib


@contextlib.contextmanager
def _with_environment(db):
    with api.Environment.manage():
        with registry(db).cursor() as new_cr:
            env = api.Environment(new_cr, SUPERUSER_ID, {})
            yield env


class Sendgrid(http.Controller):
    @http.route('/sendgrid/inbound/<string:db>', auth='none', type='http', csrf=False)
    def sendgrid_inbound(self, db, **kwargs):

        with _with_environment(db) as env:
            mime = kwargs.get("email", "")
            if not mime:
                return 'OK'

            env['mail.thread'].message_process(False, mime)
