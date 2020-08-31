# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime
from mock import patch
from odoo.addons.base_rest.controllers.main import _PseudoCollection
from odoo.addons.component.core import WorkContext
from odoo.addons.component.tests.common import SavepointComponentCase
from odoo.addons.datamodel.tests.common import SavepointDatamodelCase

TIMESTAMP_CONSTANT = datetime.datetime.utcnow().timestamp()


class ShopinvaderJwtTenantCase(SavepointComponentCase, SavepointDatamodelCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.demo_time = datetime.datetime.utcnow().timestamp()
        cls.backend = cls.env.ref("shopinvader.backend_1")
        cls.shopinvader_partner = cls.env.ref("shopinvader.shopinvader_partner_2")
        collection = _PseudoCollection("shopinvader.backend", cls.env)
        tenant_service_workcontext = WorkContext(
            model_name="shopinvader.partner", collection=collection
        )
        cls.tenant_service = tenant_service_workcontext.component(usage="auth")
        cls.setUpPayloads()

    @classmethod
    def setUpPayloads(cls):
        cls.payload_sign_in = cls.env.datamodels[
            "shopinvader.tenant.signin.input"
        ].load(
            {
                "login": "anubis@shopinvader.com",
                "password": "PwdPartner2",
                "backend": {
                    "backend_name": "shopinvader.backend",
                    "backend_id": cls.backend.id,
                },
            }
        )
        cls.address_vals = {
            "name": "NewShopinvaderTenant",
            "date": "1900-12-30",
            "street": "1, Testing Street",
            "street2": "1st floor",
            "zip": "69100",
            "city": "Villeurbanne",
            "email": "new.shopinvader.tenant@example.com",
        }
        cls.payload_sign_up = cls.env.datamodels[
            "shopinvader.tenant.signup.input"
        ].load(
            {
                "login": "new.shopinvader.tenant@example.com",
                "password": "PwdNewPartner",
                "backend": {
                    "backend_name": "shopinvader.backend",
                    "backend_id": cls.backend.id,
                },
                "address": cls.address_vals,
                "external_id": "MyExternalId",
                "sync_date": "1900-12-30",
            }
        )
        cls.payload_sign_out = cls.env.datamodels[
            "shopinvader.tenant.signout.input"
        ].load({"tenant_identifier": "anubis@shopinvader.com"})
        cls.payload_change_pwd = cls.env.datamodels[
            "shopinvader.tenant.change.pwd.input"
        ].load({"tenant_identifier": "anubis@shopinvader.com", "password": "aNewPass"})

    @classmethod
    def make_mock_token(cls, backend, tenant, timestamp):
        with patch(
            "odoo.addons.tenant_auth_jwt.models.tenant_backend_jwt.TenantBackendJwt._jwt_get_timestamp",
            return_value=timestamp,
        ):
            token = backend.jwt_generate(tenant)
        return token
