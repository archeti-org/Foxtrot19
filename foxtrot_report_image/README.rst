====================
Foxtrot Report Image
====================

Generic module to convert product images into data URIs that wkhtmltopdf can
render in PDF reports.

Odoo 19 may store product images as WebP. wkhtmltopdf cannot decode WebP, so
this module converts unsupported formats to PNG when needed.

Usage
=====

Depend on ``foxtrot_report_image`` and call on ``product.product`` or
``product.template``::

    product._foxtrot_report_image_data_uri()

Or convert any base64 image field::

    from odoo.addons.foxtrot_report_image.utils import image_to_report_data_uri

    image_to_report_data_uri(record.image_128)


Bug Tracker
===========

Problems with the module?
Write to: <support@archeti.com>

Contributors
------------

* Martha Rondon <mrondon@archeti.com>

.. image:: https://www.archeti.com/logo.png
   :alt: ArcheTI
   :target: https://archeti.com
