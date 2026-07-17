import base64
import io
import logging

from PIL import Image
from PIL import WebPImagePlugin

from odoo import models
from odoo.tools.image import image_data_uri
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

# Formats wkhtmltopdf can render natively, no conversion needed.
WKHTMLTOPDF_SAFE_MIMETYPES = ('image/png', 'image/jpeg', 'image/gif')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _foxtrot_report_image_data_uri(self):
        """Return the product image as a data URI usable in PDF reports.

        Odoo 19's web client stores product images as WebP, which
        wkhtmltopdf cannot decode. This method converts WebP (or any other unsupported
        format) to PNG with Pillow, since odoo.tools.image_process
        refuses to process WebP.
        """
        self.ensure_one()
        if not self.image_128:
            return False
        image_bin = base64.b64decode(self.image_128)
        if guess_mimetype(image_bin) in WKHTMLTOPDF_SAFE_MIMETYPES:
            return image_data_uri(self.image_128)
        try:
            image = Image.open(io.BytesIO(image_bin))
            # WebP variants are stored full-size (image_process skips
            # WebP), so resize to keep the PDF small.
            image.thumbnail((256, 256))
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGBA')
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            return 'data:image/png;base64,%s' % base64.b64encode(
                buffer.getvalue()).decode()
        except Exception:
            _logger.warning(
                "Could not convert image of product %s to PNG for report",
                self.display_name, exc_info=True)
            return image_data_uri(self.image_128)
