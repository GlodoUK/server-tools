from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    twilio_enabled = fields.Boolean(
        config_parameter="twilio_sms.enabled",
    )
    twilio_sid = fields.Char(
        config_parameter="twilio_sms.sid",
    )
    twilio_token = fields.Char(
        config_parameter="twilio_sms.token",
    )
    twilio_from = fields.Char(
        config_parameter="twilio_sms.from",
    )
