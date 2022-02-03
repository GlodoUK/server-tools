import phonenumbers
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from odoo import _, api, models

from ..tools import twilio_error_codes_dict


class SmsApi(models.AbstractModel):
    _inherit = "sms.api"

    @api.model
    def _contact_twilio_api(self, numbers, message):
        icp = self.env["ir.config_parameter"].sudo()

        account_sid = icp.get_param("twilio_sms.sid", default="")
        auth_token = icp.get_param("twilio_sms.token", default="")
        country_code = icp.get_param("twilio_sms.default_country_code", default="GB")
        send_as = icp.get_param("twilio_sms.from", default="")

        client = Client(account_sid, auth_token)
        res = []

        for number in numbers:
            try:
                parsed_number = phonenumbers.parse(number, country_code)

                if phonenumbers.number_type(parsed_number) not in (
                    phonenumbers.PhoneNumberType.MOBILE,
                    phonenumbers.PhoneNumberType.UNKNOWN,
                ):
                    res.append(
                        {
                            "error_code": "Invalid Number",
                            "error_message": _("Does not appear to be a mobile number"),
                        }
                    )
                    continue

                e164_formatted_number = phonenumbers.format_number(
                    parsed_number, phonenumbers.PhoneNumberFormat.E164
                )

                req = client.messages.create(
                    body=message, from_=send_as, to=e164_formatted_number
                )

                res.append(
                    {
                        "res": req,
                    }
                )
            except phonenumbers.NumberParseException as e:
                res.append(
                    {
                        "error_code": e.error_type,
                        "error_message": e._msg,
                    }
                )
            except TwilioRestException as e:
                res.append(
                    {
                        "error_code": e.code,
                        "error_message": e.msg,
                    }
                )

        return res

    @api.model
    def _send_sms(self, numbers, message):
        twilio_enabled = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("twilio_sms.enabled", default=False)
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
            .get_param("twilio_sms.enabled", default=False)
        )

        if not twilio_enabled:
            return super()._send_sms_batch(messages)

        res = []

        for message in messages:
            message_res = next(
                iter(
                    self._contact_twilio_api(
                        [message.get("number")], message.get("content")
                    )
                ),
                {},
            )

            # maintain an upstream compatible _send_sms_batch response
            res.append(
                {
                    "res_id": message.get("res_id"),
                    "state": (
                        f"twilio:{message_res.get('error_code')}"
                        if message_res.get("error_code")
                        else "success"
                    ),
                    "twilio_err": message_res.get("error_message"),
                    "credit": 0,  # we used 0 odoo partner credits
                }
            )

        return res

    @api.model
    def _get_sms_api_error_messages(self):
        res = super()._get_sms_api_error_messages()

        twilio_enabled = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("twilio_sms.enabled", default=False)
        )
        if twilio_enabled:
            res.update(twilio_error_codes_dict)

        return res
