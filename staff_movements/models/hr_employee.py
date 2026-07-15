from odoo import api, fields, models # ty: ignore

class HREmployee(models.Model):
    _inherit = "hr.employee"

    staff_movement_ids = fields.One2many(comodel_name="staff.movement", inverse_name="employee_id")

    versions_count = fields.Integer(
        string="Movements Count", 
        compute="_compute_versions_count",
    )

    # @api.model_create_multi
    # def create(self, vals_list):
    #     employees = super(HREmployee, self).create(vals_list)
    #     for employee in employees:
    #         self.env['staff.movement'].create({
    #             'employee_id': employee.id,
    #             'effective_date': employee.create_date or fields.Date.today(),
    #             'mode': 'entry',
    #         })
    #     return employees

    @api.depends('staff_movement_ids')
    def _compute_versions_count(self):
        for record in self:
            record.versions_count = len(record.staff_movement_ids)

    def action_open_logs(self):
        # FIX: Ensure it returns a cleanly localized domain filter 
        action = self.env.ref("staff_movements.staff_movements_log_action").read()[0]
        action['domain'] = [('employee_id', '=', self.id)]
        action['context'] = {'default_employee_id': self.id}
        return action