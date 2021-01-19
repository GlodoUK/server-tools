{
    'name': 'mail_force_sender',
    'summary': """Force the outgoing email address, overriding Odoo's default
    behaviour of using the initiating user's email.""",
    'version': '12.0.1.1.0',
    'category': 'Discuss',
    'author': 'Glodo',
    'website': 'https://www.glodo.uk/',
    'depends': ['mail'],
    'data': ['data/ir_config_parameter.xml', 'views/res_config_settings.xml']
}
