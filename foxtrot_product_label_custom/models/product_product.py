# -*- coding: utf-8 -*-
from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _foxtrot_label_supplier_name(self):
        """Return the first vendor name for the product label."""
        self.ensure_one()
        seller = self.seller_ids[:1]
        return seller.partner_id.display_name if seller else ''
