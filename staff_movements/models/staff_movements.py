from odoo import fields, models


class StaffMovements(models.Model):
    _name = "staff.movements"
    _description =  """
                    This module is intended to replace the shitty google sheets in next arrivals
                    """

    user = fields.Char()