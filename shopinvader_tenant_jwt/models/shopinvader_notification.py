# Copyright 2020 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools.translate import _


class ShopinvaderNotification(models.Model):
    _inherit = "shopinvader.notification"
    _description = "Shopinvader Notification"

    def _get_all_notification(self):
        result = super()._get_all_notification()
        result.update(
            {
                "customer_password_reset": {
                    "name": _("Customer password Reset"),
                    "model": "shopinvader.partner",
                },
                "customer_password_change": {
                    "name": _("Customer password Change"),
                    "model": "shopinvader.partner",
                },
            }
        )
        return result
