from odoo import api, fields, models # ty: ignore


class StaffMovementArchiveReason(models.TransientModel):
    _name = "staff.movement.archive.reason"
    _description = f"{__name__}.description"

    