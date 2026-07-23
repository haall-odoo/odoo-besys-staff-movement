from odoo import fields, models # ty: ignore

class StaffMovementTask(models.Model):
    _name = "staff.movement.task"
    _description = f"{_name}.description"

    name = fields.Char(required=True)
    description = fields.Char(required=True)
    # related_movement_type_ids = fields.Many2many("")
