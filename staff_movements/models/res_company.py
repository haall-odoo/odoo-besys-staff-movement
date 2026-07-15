from odoo import fields, models # ty: ignore

class ResCompany(models.Model):
    _inherit = "hr.job"

    staff_movement_ids = fields.One2many(comodel_name="staff.movement", inverse_name="new_company")