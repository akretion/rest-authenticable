# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestPasswordPolicies(SavepointCase):
    def setUp(self):
        super().setUp()
        self.directory = self.env.ref("partner_auth.demo_directory")
        self.partner = self.env.ref("partner_auth.demo_readymat_auth")
        self.partner.password = "covfefe"

    def test_password_expiry_no_check(self):
        self.env["partner.auth"].sign_in(
            self.directory, "ready.mat28@example.com", "covfefe"
        )

    def test_password_expiry_pass(self):
        self.env["partner.auth"].sign_in(
            self.directory, "ready.mat28@example.com", "covfefe"
        )
        self.directory.policy_password_expiration = 3
        valid_date = fields.Datetime.today() - relativedelta(days=2)
        self.partner.date_password_updated = valid_date
        self.env["partner.auth"].sign_in(
            self.directory, "ready.mat28@example.com", "covfefe"
        )

    def test_password_expiry_fail(self):
        self.directory.policy_password_expiration = 3
        expired_date = fields.Datetime.today() - relativedelta(days=4)
        self.partner.date_password_updated = expired_date
        with self.assertRaises(ValidationError):
            self.env["partner.auth"].sign_in(
                self.directory, "ready.mat28@example.com", "covfefe"
            )

    def test_password_rotation_no_check(self):
        self.partner.password = "bigly"

    def test_password_rotation_pass(self):
        self.directory.policy_password_rotation = 3
        self.partner.password = "bigly"

    def test_password_rotation_fail(self):
        self.directory.policy_password_rotation = 3
        self.partner.password = "one"
        self.partner.password = "two"
        with self.assertRaises(ValidationError):
            self.partner.password = "one"

    def test_password_rotation_pass_history(self):
        """ Overflow history to check we kept only n last hashes """
        self.directory.policy_password_rotation = 3
        self.partner.password = "one"
        self.partner.password = "two"
        self.partner.password = "three"
        self.partner.password = "four"
        self.partner.password = "five"
        self.partner.password = "one"

    def test_password_complexity_no_check(self):
        self.partner.password = "bigly"

    def test_password_complexity_fail_lower(self):
        self.directory.policy_password_complexity_lower = 1
        with self.assertRaises(ValidationError):
            self.partner.password = "NOLOWER"

    def test_password_complexity_fail_upper(self):
        self.directory.policy_password_complexity_upper = 1
        with self.assertRaises(ValidationError):
            self.partner.password = "noupper"

    def test_password_complexity_fail_numeric(self):
        self.directory.policy_password_complexity_numeric = 1
        with self.assertRaises(ValidationError):
            self.partner.password = "lettersonly"

    def test_password_complexity_fail_special(self):
        self.directory.policy_password_complexity_special = 1
        with self.assertRaises(ValidationError):
            self.partner.password = "NoSpecialChars1"

    def test_password_complexity_fail_length(self):
        self.directory.policy_password_complexity_length = 10
        with self.assertRaises(ValidationError):
            self.partner.password = "tooshort"

    def test_password_complexity_fail_estimate(self):
        self.directory.policy_password_complexity_estimate = 1
        with self.assertRaises(ValidationError):
            self.partner.password = "simple"
