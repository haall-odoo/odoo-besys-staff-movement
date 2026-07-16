from odoo import exceptions, fields, models # ty: ignore


class StaffMovementDeparturWizard(models.TransientModel):
    _name = "staff.movement.departure.wizard"
    _description = f"{_name}.description"

    date = fields.Date()
    employee_ids = fields.Many2many("hr.employee")

    def action_wizard(self):
        if not self.date:
            raise exceptions.ValidationError("Date field is required!")
        storage = self.employee_ids.action_fire_employees(self.date)
        return storage._get_records_action(target='current')

