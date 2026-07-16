from odoo import api, exceptions, fields, models #ty: ignore
from .data.keyboard_layout import KEYBOARD_LAYOUT
from .data.movement_types import MOVEMENT_TYPES

class StaffMovement(models.Model):
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
    job_id = fields.Many2one("hr.job", readonly=True)

    gram = fields.Char()


    effective_date = fields.Date(default=fields.Date.context_today, required=True, tracking=True)
    is_done = fields.Boolean(string="Done", default=False, tracking=True)
    remark = fields.Html()

    movement_type = fields.Selection(MOVEMENT_TYPES, required=True)

    keyboard_layout = fields.Selection(KEYBOARD_LAYOUT, tracking=True)
    need_equipment = fields.Boolean(string="Equipment needed", default=False, tracking=True)
    new_position_id = fields.Many2one("hr.job", tracking=True)
    new_company_id = fields.Many2one("res.company", string="New Company", tracking=True)


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

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            employee_company_id = record.employee_id.company_id
            if employee_company_id:
                if not record.company_id:
                    record.company_id = employee_company_id             
                if record.movement_type == 'change_of_position':
                    if not record.new_company_id:
                        record.new_company_id = employee_company_id
            if not record.job_id:
                record.job_id = record.employee_id.job_id
        return records
    
    def unlink(self):
        raise exceptions.UserError(
            "For audit compliance purposes, staff movement logs cannot be deleted! Archive it instead."
        )
