from odoo import api, exceptions, fields, models #ty: ignore
from odoo import Command #ty : ignore
from .data.keyboard_layout import KEYBOARD_LAYOUT

class StaffMovement(models.Model):
    _name = "staff.movement"
    _description = "Staff Movement"
    _order = "effective_date desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, tracking=True)
    is_done = fields.Boolean(default=False, tracking=True)

    employee_id = fields.Many2one("hr.employee", required=True)

    former_employee_id = fields.Many2one("hr.employee")    
    profile_picture = fields.Image(related="employee_id.image_1920")
    
    actual_company_id = fields.Many2one("res.company", readonly=True)
    actual_department_id = fields.Many2one("hr.department", readonly=True)
    actual_position_id = fields.Many2one("hr.job", readonly=True)

    effective_date = fields.Date(default=fields.Date.context_today, required=True, tracking=True)
    remark = fields.Html()

    movement_type_id = fields.Many2one("staff.movement.type", required=True)

    keyboard_layout = fields.Selection(KEYBOARD_LAYOUT, tracking=True)
    is_equipment_needed = fields.Boolean(string="Equipment needed", default=False, tracking=True)
    
    new_position_id = fields.Many2one("hr.job", tracking=True)
    new_department_id = fields.Many2one("hr.department", tracking=True)
    new_company_id = fields.Many2one("res.company", string="New Company", tracking=True)

    related_user_id = fields.Many2one("res.users", tracking=True)


    is_changing_company = fields.Boolean(related="movement_type_id.is_changing_company")
    is_changing_department = fields.Boolean(related="movement_type_id.is_changing_department")
    is_changing_position = fields.Boolean(related="movement_type_id.is_changing_position")
    is_needing_equipment = fields.Boolean(related="movement_type_id.is_needing_equipment")
    is_former_employee_link_needed = fields.Boolean(related="movement_type_id.is_former_employee_link_needed")
    is_link_to_user_needed = fields.Boolean(related="movement_type_id.is_link_to_user_needed")

    task_ids = fields.One2many("staff.movement.task", "movement_id", string="Tasks")

    @api.onchange("movement_type_id")
    def _onchange_movement_type_id(self):
        """ Instantiates fresh copies of tasks based on the selected type """
        if not self.movement_type_id:
            self.task_ids = [Command.clear()]
            return

        task_commands = [Command.clear()]
        for task_template in self.movement_type_id.related_movement_task_ids:
            task_commands.append(Command.create({
                'name': task_template.name,
                'description': task_template.description,
                'template_id': task_template.id,
                'active': True,
            }))
        self.task_ids = task_commands

    @api.onchange('employee_id')
    def _onchange_employee(self):
        for record in self.filtered("employee_id"):
            employee_id = record.employee_id
            if employee_id:
                if not record.actual_company_id:
                    record.actual_company_id = employee_id.company_id
                if not record.actual_department_id:
                    record.actual_department_id = employee_id.department_id
                if not record.actual_position_id:
                    record.actual_position_id = employee_id.job_id
                if not record.actual_position_id:
                    record.actual_position_id = employee_id.job_id
                if not record.new_company_id and record.actual_company_id:
                    record.new_company_id = record.actual_company_id

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            employee_id = record.employee_id
            if employee_id:
                if not record.actual_company_id:
                    record.actual_company_id = employee_id.company_id
                if not record.actual_department_id:
                    record.actual_department_id = employee_id.department_id
                if not record.actual_position_id:
                    record.actual_position_id = employee_id.job_id
                if not record.actual_position_id:
                    record.actual_position_id = employee_id.job_id
                if not self.new_company_id and self.actual_company_id:
                    self.new_company_id = self.actual_company_id
        return records
    
    def unlink(self):
        raise exceptions.UserError(
            "For audit compliance purposes, staff movement logs cannot be deleted! Archive it instead."
        )
    
    def mark_as_done(self):
        self.is_done = True
        if self.is_changing_company:
            self.employee_id.company_id = self.new_company_id.id
        if self.is_changing_department:
            self.employee_id.department_id = self.new_department_id.id
        if self.is_changing_position:
            self.employee_id.job_id = self.new_position_id.id

    def mark_as_cancelled(self):
        if self.is_done:
            raise exceptions.UserError(
                "For audit compliance purposes, staff movement validated cannot be archived or cancelled!"
            )
        self.active = False

    def open_archive_reason_wizard(self):
        wizard = self.env["staff.movement.archive.reason.wizard"].create({
            'staff_movement_id': self.id,
        })
        
        return {
            'name': 'Archive this movement record',
            'type': 'ir.actions.act_window',
            'res_model': 'staff.movement.archive.reason.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
            'context': self.env.context,
        }
