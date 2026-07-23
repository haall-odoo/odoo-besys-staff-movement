# Staff Movements
This model is intended to extend the *hr.employee* model providing a comprehensive logs view of change of position/office.

## Run
A Makefile is provided, make sure to update the path to run it without errors.
You can customize these environement variable:
- ODOO_PATH → should contains the path to the odoo community repository
- ENTERPRISE_PATH → should contains the path to the odoo enterprise repository
- MODULE_PATH → should contains the path to this repository
- DB_NAME (default = TestModule) → should contains the name of the DB you want to use in this project

Several commands are available to help you run this project:
- make setup_venv: Will install a virtual environement with all depandencies needed by odoo community, enterprise and this module
- make reset_db: alias for `dropdb ${DB_NAME}`
- make clean: remove all `__pycache__` directories in the project tree
- make run: start odoo with enterprise and module loaded in dev mode with auto reload for python and xml and demo data loaded
- make: alias for `make reset_db && make run`

## staff.movement structure
```py
{
  _name = "staff.movement"
    _description = "Staff Movement"
    _order = "effective_date desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    active = fields.Boolean(default=True, tracking=True)
    employee_id = fields.Many2one("hr.employee", required=True)
    employee_name = fields.Char(related="employee_id.name", string="Employee name")
    profile_picture = fields.Image(related="employee_id.image_1920")
    actual_company = fields.Many2one(related="employee_id.company_id", string="Actual Company")
    company_id = fields.Many2one("res.company", readonly=True, string="Company")
    actual_position_id = fields.Many2one("hr.job", readonly=True)
    gram = fields.Char()
    effective_date = fields.Date(default=fields.Date.context_today, required=True, tracking=True)
    is_done = fields.Boolean(string="Done", default=False, tracking=True)
    remark = fields.Html()
    movement_type = fields.Selection(MOVEMENT_TYPES, required=True)
    keyboard_layout = fields.Selection(KEYBOARD_LAYOUT, tracking=True)
    need_equipment = fields.Boolean(string="Equipment needed", default=False, tracking=True)
    new_position_id = fields.Many2one("hr.job", tracking=True)
    new_company_id = fields.Many2one("res.company", string="New Company", tracking=True)
}
```

## Models
This model is splitted in several logic files:
- models/hr_employee.py → extend *hr.employee* model
- models/staff_movement.py → main model of records 
- wizard/staff_movement_departure_wizard.py → Transient model for batch departure
- wizard/staff_movement_default_wizard.py → Transient model to create one movement from an employee record 