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
    
    def action_fire_employees(self, date):
        created = self.env['staff.movement'].create([
            {
                'employee_id': employee.id,
                'effective_date': date,
                'movement_type': 'departure',
            }
            for employee in self])
        return created
    
    def action_movement(self, movement_type):
        created = self.env['staff.movement'].create([
            {
                'employee_id': self.id,
                'movement_type': movement_type,
            }
        ])
        return created
    
    def open_movement_default_wizard(self):
        wizard = self.env["staff.movement.default.wizard"].create({
            'employee_id': self.id,
        })
        
        # 2. Return standard window dictionary context to display the popup
        return {
            'name': 'Create Staff Movement',
            'type': 'ir.actions.act_window',
            'res_model': 'staff.movement.default.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
            'context': self.env.context,
        }
        
    def open_wizard_staff_departure(self):
        wizard = self.env["staff.movement.departure.wizard"].create(
            {
                'employee_ids': self.ids,
            }
        )
        return wizard._get_records_action(target='new')