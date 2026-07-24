from odoo import fields, models # ty: ignore

class StaffMovementType(models.Model):
    _name = "staff.movement.type"
    _description = f"{_name}.description"

    name = fields.Char("Display Name", required=True)
    technical_name = fields.Char("Technical Name", required=True)

    _technical_name_uniq_constraints = models.Constraint(
            'UNIQUE(technical_name)',
            'The technical name must be unique!'
        )
    
    _name_uniq_constraint = models.Constraint(
            'UNIQUE(name)',
            'The display name must be unique!'
        )
    
    related_movement_task_ids = fields.Many2many("staff.movement.task.template")


    is_changing_company = fields.Boolean(required=True, default=False)
    is_changing_department = fields.Boolean(required=True, default=False)
    is_changing_position = fields.Boolean(required=True, default=False)

    is_needing_equipment = fields.Boolean(required=True, default=False)
    is_former_employee_link_needed = fields.Boolean(required=True, default=False)

    is_link_to_user_needed = fields.Boolean(required=True, default=False)
    
