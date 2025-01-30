import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-akretion-rest-authenticable",
    description="Meta package for akretion-rest-authenticable Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-partner_auth',
        'odoo14-addon-partner_auth_jwt',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
