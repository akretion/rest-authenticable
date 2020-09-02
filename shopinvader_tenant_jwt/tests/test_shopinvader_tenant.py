# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import hashlib
import datetime
from odoo.addons.base_rest.controllers.main import _PseudoCollection
from odoo.addons.component.core import WorkContext
from odoo.addons.component.tests.common import SavepointComponentCase
from mock import patch
from odoo.addons.datamodel.tests.common import SavepointDatamodelCase
from odoo.addons.tenant_auth_jwt.common import translate_claims
from .common import ShopinvaderJwtTenantCase

TIMESTAMP_CONSTANT = datetime.datetime.utcnow().timestamp()


class ShopinvaderJwtTenantTest(ShopinvaderJwtTenantCase):
    def test_sign_in(self):
        """ Test we get a token on signin """
        mock_token = self.make_mock_token(
            self.backend, self.shopinvader_partner, TIMESTAMP_CONSTANT
        ).decode("utf-8")
        with patch(
            "odoo.addons.tenant_auth_jwt.models.tenant_backend_jwt.TenantBackendJwt._jwt_get_timestamp",
            return_value=TIMESTAMP_CONSTANT,
        ):
            signin_output = self.tenant_service.sign_in(self.payload_sign_in)
        mock_token_split = mock_token.split(".")
        token_split = signin_output.token.split(".")
        self.assertEqual(token_split[0], mock_token_split[0])
        self.assertEqual(token_split[1], mock_token_split[1])

    def test_sign_up(self):
        """
        Use sign up with some demo data
         1. test a new partner is created
         2. test data is correct
        """
        shopinvader_partners_start = self.env["shopinvader.partner"].search([])
        self.tenant_service.sign_up(self.payload_sign_up)
        new_shopinvader_partner = self.env["shopinvader.partner"].search(
            [("id", "not in", shopinvader_partners_start.ids)]
        )
        self.assertTrue(new_shopinvader_partner)
        for key in self.address_vals.keys():
            # we test as str for compactness (datetime.datetime != str ... )
            self.assertEqual(
                str(getattr(new_shopinvader_partner, key)), str(self.address_vals[key])
            )
        self.assertEqual(new_shopinvader_partner.external_id, "MyExternalId")
        self.assertAlmostEqual(
            new_shopinvader_partner.sync_date.timestamp(), self.demo_time, places=0
        )
        self.assertEqual(new_shopinvader_partner.backend_id.id, self.backend.id)

    def test_sign_out(self):
        """
        Nothing to do server-side, token must be destroyed client-side
        Just test everything works
         1. get token from sign in
         2. mock same token on sign out
        """
        token = self.tenant_service.sign_in(self.payload_sign_in).token
        with patch(
            "odoo.addons.shopinvader_tenant_jwt.services.shopinvader_tenant_service.jwt_info",
            return_value=translate_claims(token, self.env),
        ):
            self.tenant_service.sign_out()

    def test_change_pwd(self):
        """
        1. Sign in
        2. Use sign in token to change password
        3. Check password is changed
        """
        token = self.tenant_service.sign_in(self.payload_sign_in).token
        new_pwd_hash = hashlib.sha256("aNewPass".encode("utf-8")).hexdigest()
        with patch(
            "odoo.addons.shopinvader_tenant_jwt.services.shopinvader_tenant_service.jwt_info",
            return_value=translate_claims(token, self.env),
        ):
            self.tenant_service.change_password(self.payload_change_pwd)
        self.assertEqual(self.shopinvader_partner.password_hash, new_pwd_hash)

    def test_reset_pwd(self):
        """
        1. Call the reset password functionality
        2. Ensure a notification was created
        3. Ensure the token works to change password
        """
        notifs_before = self.env["shopinvader.notification"].search([])
        token = self.tenant_service.sign_in(self.payload_sign_in).token
        with patch(
            "odoo.addons.shopinvader_tenant_jwt.services.shopinvader_tenant_service.jwt_info",
            return_value=translate_claims(token, self.env),
        ):
            self.tenant_service.reset_password()
        new_notif = self.env["shopinvader.notification"].search(
            [("id", "not in", notifs_before.ids)]
        )
        self.assertTrue(new_notif)
