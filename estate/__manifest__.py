{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Mark Musili",
    'description': """A real-estate module to help sellers sell their property.""",
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ]
}