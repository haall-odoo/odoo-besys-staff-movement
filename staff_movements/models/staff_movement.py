from odoo import api, fields, models #ty: ignore
from .data.keyboard_layout import KEYBOARD_LAYOUT

class StaffMovement(models.Model):
    _name = "staff.movement"
    _description = "Staff Movement"
    _order = "effective_date desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one("hr.employee")
    
    employee_name = fields.Char(related="employee_id.name", string="Employee name")
    profile_picture = fields.Image(related="employee_id.image_1920")
    actual_company = fields.Many2one(related="employee_id.company_id")
    company_id = fields.Many2one("res.company", readonly=True)
    job_id = fields.Many2one("hr.job", readonly=True)


    effective_date = fields.Date(default=fields.Date.context_today)
    is_done = fields.Boolean(string="Done", default=False)
    remark = fields.Html()

    movement_type = fields.Selection([
        ('entry', 'Entry'),
        ('departure', 'Departure'),
        ('change_of_position', 'Change of position'),
        ('review', 'Review'),
    ])

    keyboard_layout = fields.Selection(KEYBOARD_LAYOUT, string="Keyboard Layout")
    need_backpack = fields.Boolean(string="Backpack needed", default=False)
    new_position_id = fields.Many2one("hr.job")
    new_company_id = fields.Many2one("res.company")


    @api.onchange('employee_id', 'movement_type')
    def _onchange_employee_and_type(self):
        for record in self.filtered("employee_id"):
            employee_company_id = record.employee_id.company_id
            if employee_company_id:
                if not record.company_id:
                    record.company_id = employee_company_id             
                if record.movement_type == 'change_of_position':
                    if not record.new_company_id:
                        record.new_company_id = employee_company_id
            if not record.job_id:
                record.job_id = record.employee_id.job_id