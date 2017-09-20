# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class MB_Task_Extension(models.Model):
	_inherit = 'project.task'
	sub_task = fields.Boolean(string='Sub Task', default=True)

	
	task_name = fields.Many2one('project.task', "Task Name")
	task_val = fields.Char("Task Value")
