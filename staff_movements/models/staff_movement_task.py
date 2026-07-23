from odoo import fields, models # ty: ignore

class StaffMovementTask(models.Model):
    _name = "staff.movement.task"
    _description = f"{_name}.description"

    name = fields.Char(required=True)
    state = fields.Boolean(default=False)
    description = fields.Html()
    active = fields.Boolean(default=True, required=True)

    template_id = fields.Many2one("staff.movement.task.template")
    movement_id = fields.Many2one("staff.movement", string="Movement")

    def mark_as_done(self):
        self.state = True

    def mark_as_cancelled(self):
        self.active = False