# -*- coding: utf-8 -*-
from odoo import models

from ..utils import image_to_report_data_uri


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _foxtrot_report_image_data_uri(self):
        """Return the product image as a data URI usable in PDF reports."""
        self.ensure_one()
        return image_to_report_data_uri(self.image_128)
