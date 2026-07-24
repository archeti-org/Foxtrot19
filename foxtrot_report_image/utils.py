# -*- coding: utf-8 -*-
import base64
import io
import logging

from PIL import Image
from PIL import WebPImagePlugin  # noqa: F401  # register WebP decoder

from odoo.tools.image import image_data_uri
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

# Formats wkhtmltopdf can render natively.
WKHTMLTOPDF_SAFE_MIMETYPES = ('image/png', 'image/jpeg', 'image/gif')


def image_to_report_data_uri(image_b64):
    """Return an image data URI usable in PDF reports.

    Odoo 19 may store images as WebP, which wkhtmltopdf cannot decode.
    Convert unsupported formats to PNG when needed.
    """
    if not image_b64:
        return False
    image_bin = base64.b64decode(image_b64)
    if guess_mimetype(image_bin) in WKHTMLTOPDF_SAFE_MIMETYPES:
        return image_data_uri(image_b64)
    try:
        image = Image.open(io.BytesIO(image_bin))
        # WebP variants are often stored full-size (image_process skips
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
            "Could not convert image to PNG for PDF report",
            exc_info=True)
        return image_data_uri(image_b64)
