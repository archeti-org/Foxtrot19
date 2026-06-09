# -*- coding: utf-8 -*-
{
    'name': 'Purchase Product Attachments Link',
    'summary': """
        Creates a zip file with all the attachments related to the products of
        a PO and exposes a temporary public download link.
        """,
    'author': 'ArcheTI',
    'website': 'https://archeti.com',
    'category': 'Purchases',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'data/config_parameter_data.xml',
        'data/cron.xml',
        'views/views.xml',
        'templates/invalid_product_attachments_url.xml',
    ],
    'installable': True,
}
