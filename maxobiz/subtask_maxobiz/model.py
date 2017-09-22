# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class MB_Task_Extension(models.Model):
	_inherit = 'project.task'

	sub_task = fields.Boolean(string='Sub Tasks', default=True)
	task_name = fields.Many2one('project.task', "Task Name")
	task_val = fields.Char("Task Value")
	proj_id = fields.Char("Project Id")
	task_type = fields.Char("Task Type")
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date")
	dep = fields.Char("Department")
	mail = fields.Char("Email") 
	choose_team = fields.Many2one('proj.team', "Choose Team ")
	fnl_by = fields.Many2one('hr.employee',"Finalized By")