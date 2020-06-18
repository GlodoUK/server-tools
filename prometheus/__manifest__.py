# -*- coding: utf-8 -*-
{
    "version": "0.1",
    "name": "prometheus",
    "summary": """Monkey patches Odoo to install prometheus timings for http
    requests and sql queries.""",
    "category": "Hidden",
    # 'live_test_url': "",
    "images": [],
    "application": False,
    "author": "Karl Southern",
    "website": "https://www.glo.systems/",
    "license": "Other proprietary",
    "depends": ["base"],
    "external_dependencies": {"python": ["prometheus_client"], "bin": []},
    "data": [],
    "qweb": [],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
    "description": """
Monkey patches Odoo to install some prometheus metrics, and exposes them on
either /metrics or it's own dedicated port.
""",
}
