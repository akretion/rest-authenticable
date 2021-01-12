# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api
from odoo.tests.common import SavepointCase
from odoo.exceptions import AccessDenied
from odoo.addons.partner_auth_login_policy.models.partner_auth import (
    TooManyLoginsExc,
    AccountBlockedExc,
)
from mock import Mock


class TestPartnerAuthLoginPolicy(SavepointCase):
    def setUp(self):
        super().setUp()
        self.registry.enter_test_mode(self.env.cr)
        self.env = api.Environment(
            self.registry.test_cr, self.env.uid, self.env.context
        )
        self.directory = self.env.ref("partner_auth.demo_directory")
        self.partner = self.env.ref("partner_auth.demo_readymat_auth")
        self.partner.password = "covfefe"
        self.directory.policy_login_attempts = 7
        self.env.cr.commit = Mock()

    def tearDown(self):
        self.registry.leave_test_mode()
        super().tearDown()

    def test_too_many_logins(self):
        for x in range(9):
            with api.Environment.manage():
                env = api.Environment(
                    self.registry.test_cr, self.env.uid, self.env.context
                )
                with self.assertRaises(AccessDenied):
                    env["partner.auth"].sign_in(
                        self.directory, "ready.mat28@example.com", "wrong_pwd"
                    )
        with self.assertRaises(TooManyLoginsExc):
            self.env["partner.auth"].sign_in(
                self.directory, "ready.mat28@example.com", "wrong_pwd"
            )
        with self.assertRaises(AccountBlockedExc):
            self.env["partner.auth"].sign_in(
                self.directory, "ready.mat28@example.com", "wrong_pwd"
            )
