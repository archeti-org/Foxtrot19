# -*- coding: utf-8 -*-
from odoo import api, fields, models


FOXTROT_PRINT_FORMATS = {
    'foxtrot_4x4': 'foxtrot_product_label_custom.action_report_product_label_4x4',
    'foxtrot_4x1_75': 'foxtrot_product_label_custom.action_report_product_label_4x1_75',
}


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(
        selection_add=[
            ('foxtrot_4x4', '4 x 4'),
            ('foxtrot_4x1_75', '4 x 1 3/4'),
        ],
        ondelete={
            'foxtrot_4x4': 'set default',
            'foxtrot_4x1_75': 'set default',
        },
    )

    @api.depends('print_format')
    def _compute_dimensions(self):
        super()._compute_dimensions()
        for wizard in self:
            if wizard.print_format == 'foxtrot_4x4':
                wizard.columns = 1
                wizard.rows = 4
            if wizard.print_format == 'foxtrot_4x1_75':
                wizard.columns = 1
                wizard.rows = 2

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()
        if self.print_format in FOXTROT_PRINT_FORMATS:
            xml_id = FOXTROT_PRINT_FORMATS[self.print_format]
        return xml_id, data
