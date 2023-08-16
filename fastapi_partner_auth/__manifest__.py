# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Auth",
    "summary": """
        Implements the base features for a authenticable partner""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/akretion/rest-authenticable",
    "depends": [
        "extendable_fastapi",
        "mail",
        "base_future_response",
        "queue_job",
    ],
    "data": [
        "security/res_group.xml",
        "security/ir.model.access.csv",
        "data/email_data.xml",
        "views/fastapi_endpoint_view.xml",
    ],
    "demo": [
        "demo/fastapi_auth_directory_demo.xml",
        "demo/res_partner_demo.xml",
        "demo/fastapi_auth_partner_demo.xml",
        "demo/fastapi_endpoint_demo.xml",
    ],
    "external_dependencies": {
        "python": ["itsdangerous"],
    },
}