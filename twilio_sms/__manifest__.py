{
    "version": "15.0.1.1.0",
    "name": "twilio_sms",
    "summary": "Twilio SMS Gateway",
    "author": "Glo Networks",
    "website": "https://github.com/GlodoUK/server-tools",
    "license": "Other proprietary",
    "depends": ["sms"],
    "external_dependencies": {"python": ["twilio", "phonenumbers"]},
    "data": [
        "views/res_config_settings.xml",
        "views/sms_log.xml",
    ],
}
