from twilio.rest import Client

from odoo import api, models


class SmsApi(models.AbstractModel):
    _inherit = "sms.api"

    @api.model
    def _contact_twilio_api(self, numbers, message):
        icp = self.env['ir.config_parameter'].sudo()
        
        account_sid = (
            icp
            .get_param("twilio.twilio_sid", default="")
        )
        auth_token = (
            icp
            .get_param("twilio.twilio_token", default="")
        )
        
        send_as = icp.get_param('twilio_sms.from', default='')

        client = Client(account_sid, auth_token)

        res = []

        for number in numbers:
            res.append(client.messages.create(
                body=message,
                from_=send_as,
                to=number
            ))

        return res

    @api.model
    def _send_sms(self, numbers, message):
        twilio_enabled = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("twilio.twilio_enabled", default=False)
        )

        if not twilio_enabled:
            return super()._send_sms(numbers, message)

        self._contact_twilio_api(numbers, message)
        return True

    @api.model
    def _send_sms_batch(self, messages):
        twilio_enabled = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("twilio.twilio_enabled", default=False)
        )

        if not twilio_enabled:
            return super()._send_sms_batch(messages)

        res = []

        for message in messages:
            tw_res = next(
                iter(
                    self._contact_twilio_api(
                        message.get('number'), message.get('content')
                    )
                ),
                {}
            )

            # maintain an upstream compatible _send_sms_batch response
            res.append({
                'res_id': message.get("res_id"),
                # TODO add some better mappings!
                # These need to be translated to IAP states https://www.twilio.com/docs/api/errors
                # which can be found at https://github.com/odoo/odoo/blob/cd9c071c9357cef14635ef094a9f14fc5431956c/addons/sms/models/sms_sms.py#L18
                'state': "error" if tw_res.get("error_code") else "success",
                "twilio_err": tw_res.get("error_message"),
                'credit': 0, # we used 0 odoo partner credits
            })

        return res
