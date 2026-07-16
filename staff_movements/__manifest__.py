{
    'name': "Staff Movements",
    'version': '0.1',
    'depends': ['hr_maintenance', 'hr_recruitment'],
    'author': "Odoo S.A. <besysadmin@odoo.com>",
    'category': 'Administration/Staff Movements',
    'description': """
    This app allows HR to create entries, changes of position and departures record.
    It also should keep traces of what has been done, when and who and why (reason log).
    It is intended to replace the Google sheet 'next arrivals' used until today.
    """,
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
    'data': [
        'views/staff_movements_views.xml',
        'wizard/staff_movement_departure_wizard.xml',
        'views/menus.xml',
        'security/ir.model.access.csv',
    ]
}