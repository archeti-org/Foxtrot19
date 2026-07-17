import base64
import logging

from odoo import models
from odoo.tools.image import image_data_uri, image_process

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _foxtrot_report_image_data_uri(self):
        """Return the product image as a PNG data URI for PDF reports.

        wkhtmltopdf cannot decode some image formats (e.g. WebP), so the
        stored image is converted to PNG before being embedded.
        """
        self.ensure_one()
        if not self.image_128:
            return False
        try:
            image_png = image_process(
                base64.b64decode(self.image_128), output_format='PNG')
            return 'data:image/png;base64,%s' % base64.b64encode(image_png).decode()
        except Exception:
            _logger.warning(
                "Could not convert image of product %s to PNG for report",
                self.display_name, exc_info=True)
            return image_data_uri(self.image_128)
