# -*- coding: utf-8 -*-
from odoo import models

from .label_image import foxtrot_label_image_data_uri


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _foxtrot_label_image_data_uri(self):
        """Return product image as a PDF-safe data URI for label reports."""
        self.ensure_one()
        return foxtrot_label_image_data_uri(self.image_128)

    def _foxtrot_label_supplier_name(self):
        """Return the first vendor name for the product label."""
        self.ensure_one()
        seller = self.seller_ids[:1]
        return seller.partner_id.display_name if seller else ''
