from odoo import models, fields, api

class CustomExportDashboard(models.Model):
    _name = "custom.export.dashboard"

    @api.one
    def _get_count(self):
        draft_count = self.env['export.logic'].search(
            [('state', '=', 'draft')])
        pre_count = self.env['export.logic'].search(
            [('state', '=', 'sales_order')])
        initial_count = self.env['export.logic'].search(
            [('state', '=', 'done')])

        final_count = self.env['export.logic'].search(
            [('state', '=', 'done')])

        custom_exam_count = self.env['export.logic'].search(
            [('state', '=', 'done')])

        done_count = self.env['export.logic'].search(
            [('state', '=', 'done')])

        self.draft_count = len(draft_count)
        self.pre_count = len(pre_count)
        self.initial_count = len(initial_count)
        self.final_count = len(final_count)
        self.custom_exam_count = len(custom_exam_count)
        self.done_count = len(done_count)

    color = fields.Integer(string='Color Index',default=1 )
    name = fields.Char(string="Name", default="Awais")
    draft_count = fields.Integer(compute='_get_count')
    pre_count = fields.Integer(compute='_get_count')
    initial_count = fields.Integer(compute='_get_count')
    final_count = fields.Integer(compute='_get_count')
    custom_exam_count = fields.Integer(compute='_get_count')
    done_count = fields.Integer(compute='_get_count')
