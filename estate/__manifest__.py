{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Mark Musili",
    'category': 'Category',
    'description': """A real-estate module to help sellers sell their property.""",
    'application': True,
    'installable': True,
    'licence': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ]
}