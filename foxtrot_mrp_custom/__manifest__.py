{
    'name': 'Foxtrot MRP Custom',
    'version': '19.0.1.0.1',
    'category': 'Manufacturing',
    'summary': 'Show product images on the Production Order report',
    'author': 'ArcheTI',
    'website': 'https://archeti.com',
    'license': 'LGPL-3',
    'depends': ['mrp', 'foxtrot_report_image'],
    'data': [
        'report/mrp_production_templates.xml',
    ],
    'installable': True,
    'application': False,
}
