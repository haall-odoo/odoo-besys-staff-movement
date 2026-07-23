from ..models.data.keyboard_layout import KEYBOARD_LAYOUT
from odoo import api, fields, models # ty: ignore


class StaffMovementDeparturWizard(models.TransientModel):
    _name = "staff.movement.default.wizard"
    _description = f"{_name}.description"

    employee_id = fields.Many2one("hr.employee")
    former_employee_id = fields.Many2one("hr.employee")

    movement_type_id = fields.Many2one("staff.movement.type")
    effective_date = fields.Date()

    actual_company_id = fields.Many2one(related="employee_id.company_id", string="Actual Company", readonly=True)
    actual_department_id = fields.Many2one(related="employee_id.department_id", string="Actual Department", readonly=True)
    actual_position_id = fields.Many2one(related="employee_id.job_id", string="Actual Position", readonly=True)

    keyboard_layout = fields.Selection(KEYBOARD_LAYOUT)
    is_equipment_needed = fields.Boolean(string="Equipment needed", default=False)

    new_position_id = fields.Many2one("hr.job", string="New Position")
    new_department_id = fields.Many2one("hr.department", string="New Department")
    new_company_id = fields.Many2one("res.company", string="New Company")


    is_changing_company = fields.Boolean(related="movement_type_id.is_changing_company")
    is_changing_department = fields.Boolean(related="movement_type_id.is_changing_department")
    is_changing_position = fields.Boolean(related="movement_type_id.is_changing_position")
    is_needing_equipment = fields.Boolean(related="movement_type_id.is_needing_equipment")
    is_former_employee_link_needed = fields.Boolean(related="movement_type_id.is_former_employee_link_needed")

    def action_wizard(self):
        self.env['staff.movement'].create([
            {
                'employee_id': self.employee_id.id,
                'movement_type_id': self.movement_type_id,
                'effective_date': self.effective_date,

                'new_company_id': self.new_company_id.id,
                'new_department_id': self.new_department_id.id,
                'new_position_id': self.new_position_id.id,

                'former_employee_id': self.former_employee_id.id,

                'is_equipment_needed': self.is_equipment_needed,
                'keyboard_layout': self.keyboard_layout,
            }
        ])
        return {'type': 'ir.actions.act_window_close'}
    
    @api.onchange('employee_id')
    def _onchange_employee_and_type(self):
        for record in self.filtered("employee_id"):
            employee_id = record.employee_id
            if employee_id:
                if not record.actual_company_id:
                    record.actual_company_id = employee_id.company_id
                if not record.actual_department_id:
                    record.actual_department_id = employee_id.department_id
                if not record.actual_position_id:
                    record.actual_position_id = employee_id.job_id
                if not record.actual_position_id:
                    record.actual_position_id = employee_id.job_id
                if not self.new_company_id and self.actual_company_id:
                    self.new_company_id = self.actual_company_id
