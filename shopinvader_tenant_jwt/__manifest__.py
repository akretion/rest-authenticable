# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Shopinvader Tenant Jwt",
    "summary": """
        Adds Tenants and JWT to Shopinvader""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "https://www.akretion.com",
    "depends": [
        "tenant_auth_jwt",
        "shopinvader",
        "tenant_password_constraint",
        "tenant_password_expiration",
        "tenant_password_rotation",
    ],
    "data": [],
    "demo": [
        "demo/backend_demo.xml",
        "demo/email_demo.xml",
        "demo/notification_demo.xml",
        "demo/shopinvader_partner_demo.xml",
    ],
    # "external_dependencies": {"python": ["pyjwt"]},
}
