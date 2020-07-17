{
    'name': 'mail_force_sender',
    'summary': """Force the outgoing email address, overriding Odoo's default
    behaviour of using the initiating user's email.""",
    'version': '12.0.1.0.0',
    'category': 'Discuss',
    'author': 'Karl Southern',
    'website': 'https://www.glo.systems/',
    'depends': ['mail'],
    'data': ['data/ir_config_parameter.xml']
}
