
{
    'version': "12.0.1.00",
    'name': "cron_running",
    'summary': "Shows if a scheduled action is running",
    'category': "Uncategorized",
    'images': [],
    'application': False,

    'author': "Glo",
    'website': "https://glo.systems",
    'license': "Other proprietary",

    'depends': [
        'base',
    ],

    'external_dependencies': {"python": [], "bin": []},

    'data': [
        'views/views.xml',
    ],
    'qweb': [],
    'demo': [],

    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'auto_install': False,
    'installable': True,

    'description': """
Shows if a scheduled action is running
"""
}
