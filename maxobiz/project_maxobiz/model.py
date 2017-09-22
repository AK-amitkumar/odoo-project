# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class MB_Project_Extension(models.Model):
	_inherit = 'project.project'

	proj_id = fields.Char("Project Id")
	# task_type = fields.Char("Task Type")
	# task_val = fields.Char("Task Value")
	start_date = fields.Date("Start Date")
	end_date = fields.Date("End Date")
	dep = fields.Char("Department")
	mail = fields.Char("Email") 
	choose_team = fields.Many2one('proj.team', "Choose Team ")
	fnl_by = fields.Many2one('hr.employee',"Finalized By")


	srce = fields.Char("Source")
	cli_name = fields.Char("Client Name")
	url = fields.Char("URL")
	ext_status = fields.Char("External Status")
	t_amount = fields.Float("Total Amount")
	proj_aletr = fields.Char("Project Alert")
	fsl_fdb = fields.Char("Final Feedback")


class MB_Team(models.Model):
	_name = 'proj.team'
	_rec_name = 'team_name'

	team_name = fields.Char('Team Name')	
	team_lead = fields.Many2one('hr.employee',"Team Lead")
	team_mem_link = fields.One2many('ext.employee','team_mem')



class MB_Employee_Ext(models.Model):
	_name = 'ext.employee'

	team_mem = fields.Many2one('proj.team')
	name = fields.Many2one('hr.employee')
	dep = fields.Many2one('hr.department')
	job = fields.Many2one('hr.job')







