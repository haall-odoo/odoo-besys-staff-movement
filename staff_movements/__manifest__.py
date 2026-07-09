{
    'name': "Staff Movements",
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_maintenance'],
    'author': "Odoo S.A. <besysadmin@odoo.com>",
    'category': 'Administration/Staff Movements',
    'description': """
    This app allows HR to create entries, changes of position and departures record.
    It also should keep traces of what has been done, when and who and why (reason log).
    It is intended to replace the Google sheet 'next arrivals' used until today.
    """,
    'installable': True,
    'auto_install': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'data/ir.model.access.csv',
        'views/staff_movements_views.xml',
        'views/staff_movements_menus.xml',
    ]
}