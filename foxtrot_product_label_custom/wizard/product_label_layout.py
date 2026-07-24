# -*- coding: utf-8 -*-
from odoo import api, fields, models

# (columns, rows) per Foxtrot label format.
FOXTROT_LABEL_DIMENSIONS = {
    'foxtrot_4x4': (1, 2),      # 1 column × 2 rows
    'foxtrot_4x1_75': (1, 4),   # 1 column × 4 rows
}

FOXTROT_PRINT_FORMATS = {
    'foxtrot_4x4': 'foxtrot_product_label_custom.action_report_product_label_4x4',
    'foxtrot_4x1_75': 'foxtrot_product_label_custom.action_report_product_label_4x1_75',
}


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(
        selection_add=[
            ('foxtrot_4x4', '4" x 4"'),
            ('foxtrot_4x1_75', '4" x 1 3/4"'),
        ],
        ondelete={
            'foxtrot_4x4': 'set default',
            'foxtrot_4x1_75': 'set default',
        },
    )

    @api.depends('print_format')
    def _compute_dimensions(self):
        foxtrot_wizards = self.filtered(
            lambda w: w.print_format in FOXTROT_LABEL_DIMENSIONS)
        for wizard in foxtrot_wizards:
            wizard.columns, wizard.rows = FOXTROT_LABEL_DIMENSIONS[
                wizard.print_format]
        other_wizards = self - foxtrot_wizards
        if other_wizards:
            super(ProductLabelLayout, other_wizards)._compute_dimensions()

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()
        if self.print_format in FOXTROT_PRINT_FORMATS:
            xml_id = FOXTROT_PRINT_FORMATS[self.print_format]
        return xml_id, data
