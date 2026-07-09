from odoo import fields, models


class StaffMovements(models.Model):
    _name = "staff.movements"
    _description =  """
                    This module is intended to replace the shitty google sheets in next arrivals
                    """

    legal_name = fields.Char()
    mode = fields.Selection(
        selection=[
            ("entry", "Entry"),
            ("departures", "Departures"),
            ("change_of_position", "Change of position")
        ]
    )
    effective_date = fields.Date()