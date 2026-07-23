from odoo import fields, models # ty: ignore

class StaffMovementTaskTemplate(models.Model):
    _name = "staff.movement.task.template"
    _description = f"{_name}.description"

    name = fields.Char(required=True)
    description = fields.Html()
    active = fields.Boolean(default=True, required=True)
