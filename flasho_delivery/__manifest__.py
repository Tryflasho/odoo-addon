{
    'name': 'Flasho Delivery',
    'summary': 'Book and track Flasho deliveries from sales orders',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Delivery',
    'author': 'Flasho',
    'website': 'https://vendors.tryflasho.com',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'data/ir_cron.xml',
    ],
    'application': False,
    'installable': True,
}
