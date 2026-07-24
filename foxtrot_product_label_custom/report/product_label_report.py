# -*- coding: utf-8 -*-
from odoo import models
from odoo.addons.product.report.product_label_report import _prepare_data


class ReportProductLabel4x4(models.AbstractModel):
    _name = 'report.foxtrot_product_label_custom.report_product_label_4x4'
    _description = 'Product Label Report 4" x 4"'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)


class ReportProductLabel4x175(models.AbstractModel):
    _name = 'report.foxtrot_product_label_custom.report_product_label_4x1_75'
    _description = 'Product Label Report 4" x 1 3/4"'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)
