from ..models.data.movement_types import MOVEMENT_TYPES
from odoo import fields, models # ty: ignore


class StaffMovementDeparturWizard(models.TransientModel):
    _name = "staff.movement.default.wizard"
    _description = f"{_name}.description"

    employee_id = fields.Many2one("hr.employee")
    movement_type = fields.Selection(MOVEMENT_TYPES)

    

    def action_wizard(self):
        storage = self.employee_id.open_staff_movement()
        return storage._get_records_action(target='current')