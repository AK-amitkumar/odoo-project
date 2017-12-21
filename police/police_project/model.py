# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
from openerp import models, fields, api


class PoliceDetail(models.Model):
	_name = 'police.detail'
	_rec_name = 'number'

	number = fields.Char(string="Report Number")
	case_id = fields.Char(string="Case ID")
	date = fields.Date(default = datetime.date.today())
	day = fields.Char()
	time = fields.Char()
	road_name = fields.Many2one('road.name', string="Road Name")
	center_name = fields.Many2one('center.name', string="Center Name")
	location_name = fields.Many2one('location.name', string="Location Name")
	digital_tag = fields.Many2one('digital.tag', string="Digital Tag")
	direction_name = fields.Many2one('direction.name', string="Direction Name")
	violation = fields.Char(string='Time of Violation')
	code = fields.Char(string='Code of Police CAR')
	police_officer = fields.Char(string='Name of Police Officer 1')
	rank_officer = fields.Char(string='Rank Of Police Officer 1')
	sex_of1 = fields.Selection(string="Sex of Officer 1", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
	sex_of2 = fields.Selection(string="Sex of Officer 2", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
	name_officer_2 = fields.Char(string='Name of Police officer 2')
	rank_officer_2 = fields.Char(string='Rank of police officer 2')
	tosc = fields.Char(string="Case submitting Time", required=False, )
	receiving_party = fields.Many2one('receiving.party', string="Receiving Party")
	receiving_party_rank = fields.Many2one('receiving.party.rank', string="Receiving Party Rank")
	receiving_name = fields.Char(string="Receiving Party Name", required=False, )
	case_detail = fields.Text(string='Case details ')
	party_link = fields.One2many('party.detail', "main_class", string="Party Detail")
	case_type = fields.One2many('case.type', "main_class", string="Case Type")


	def confirm(self):
		pass

	@api.model
	def create(self, vals):
		vals['number'] = self.env['ir.sequence'].next_by_code('rec.number')
		new_record = super(PoliceDetail, self).create(vals)
		return new_record

	@api.onchange('date')
	def _change_daytime(self):
		if self.date:
			self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')
			self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")

class CaseType(models.Model):
	_name = 'case.type'
	_rec_name = 'case_type'
	case_type = fields.Many2one(comodel_name="type.case", string="Case Type", required=False, )
	cate_case = fields.Many2one(comodel_name="cate.case", string="Case Category", required=False, )
	qty = fields.Float(string="Qty",  required=False, )

	main_class = fields.Many2one(comodel_name="police.detail", string="Case Type", required=False, )


class HajjUmrah(models.Model):
	_name = 'hajj.umrah'
	_rec_name = 'number'

	number = fields.Char(string="Report Number")
	case_id = fields.Char(string="Case ID")
	date = fields.Date(default=datetime.date.today())
	day = fields.Char()
	time = fields.Char()
	road_name = fields.Many2one('road.name', string="Road Name")
	center_name = fields.Many2one('center.name', string="Center Name")

	violation_type = fields.One2many(comodel_name="hajjumrah.violation", inverse_name="main_class", string="Hajj and Umrah", required=False, )

	@api.model
	def create(self, vals):
		vals['number'] = self.env['ir.sequence'].next_by_code('rec.umrah')
		new_record = super(HajjUmrah, self).create(vals)
		return new_record


	@api.onchange('date')
	def _change_daytime(self):
		if self.date:
			self.day = datetime.datetime.strptime(self.date, '%Y-%m-%d').strftime('%A')
			self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")


class HajjUmrahViolation(models.Model):
	_name = 'hajjumrah.violation'
	_rec_name = 'violation'

	violation = fields.Char(string="Violation name", required=False, )
	violation_type = fields.Char(string="Violation type", required=False, )
	nop = fields.Integer(string="Number of people", required=False, )
	receiving_party = fields.Char(string="Receiving Party", required=False, )


	main_class  = new_field_id = fields.Many2one(comodel_name="hajj.umrah", string="Hajj and Umrah", required=False, )



class PartyDetail(models.Model):
	_name = 'party.detail'

	name = fields.Char("Driver Name")
	car_name = fields.Char("Name of Car")
	car_color = fields.Char("Color of Car")
	car_model = fields.Char("Model of Car")
	car_plate = fields.Char("Plate Number")
	driver_country = fields.Many2one('res.country', "Nationality")
	id_num = fields.Char("ID number")
	sex = fields.Selection(string="Sex", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
	id_type = fields.Many2one('id.type', "ID Type")
	what_found = fields.Many2one('what.found', "What we found")
	qty = fields.Float(string="Qty",  required=False, )
	accident_reason = fields.Char("Reason of accident ")
	result = fields.Char("Results")
	mean_trans = fields.Many2one('mean.trans', "Means of Transportation")
	hospital_name = fields.Many2one('hospital.name', "Name of Hospital")
	main_class = fields.Many2one('police.detail', "Party Detail")
	remark = fields.Text("Remarks")
	additional = fields.Text("Additional Details")
	previous_record = fields.Boolean("Previous records")
	companion_detail = fields.Boolean("Companion Details")

	previous_record_link = fields.One2many('previous.record', "main_class", string="Rrevious Record")
	companion_detail_link = fields.One2many('companion.detail', "main_class", string="Companion Detail")


class CompanionDetail(models.Model):
	_name = 'companion.detail'

	name = fields.Char("Name")
	country = fields.Many2one('res.country', "Nationality")
	id_num = fields.Char("ID number")
	id_type = fields.Many2one('id.type', "ID Type")
	relation = fields.Char("Relation")
	sex = fields.Selection(string="Sex", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
	what_found = fields.Char("What we found")
	qty = fields.Float(string="Qty",  required=False, )
	accident_reason = fields.Char("Reason of accident ")
	result = fields.Char("Results")
	mean_trans = fields.Many2one('mean.trans', "Means of Transportation")
	hospital_name = fields.Many2one('hospital.name', "Name of Hospital")

	main_class = fields.Many2one('party.detail')


class PreviousRecord(models.Model):
	_name = 'previous.record'

	ministry_name = fields.Many2one('ministry.name', "Name of Ministry")
	no_complaint = fields.Char("Number Of Complaint")
	date = fields.Date()
	day = fields.Char()

	main_class = fields.Many2one('party.detail')

	@api.onchange('date')
	def _change_daytime(self):
		if self.date:
			self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')


class ViolationDetail(models.Model):
	_name = 'violation.detail'
	_rec_name = 'number'

	number = fields.Char(string="Report Number")
	case_id = fields.Char(string="Case ID")
	date = fields.Date(default=datetime.date.today())
	day = fields.Char()
	time = fields.Char()
	road_name = fields.Many2one('road.name', string="Road Name")
	center_name = fields.Many2one('center.name', string="Center Name")
	location_name = fields.Many2one('location.name', string="Location Name")
	digital_tag = fields.Many2one('digital.tag', string="Digital Tag")
	direction_name = fields.Many2one('direction.name', string="Direction Name")
	violation = fields.Char(string='Time of Violation')
	code = fields.Char(string='Code of Police CAR')
	police_officer = fields.Char(string='Name of Police Officer 1')
	rank_officer = fields.Char(string='Rank Of Police Officer 1')
	sex_of1 = fields.Selection(string="Sex of Officer 1", selection=[('m', 'Male'), ('f', 'Female'), ],
							   required=False, )
	sex_of2 = fields.Selection(string="Sex of Officer 2", selection=[('m', 'Male'), ('f', 'Female'), ],
							   required=False, )
	name_officer_2 = fields.Char(string='Name of Police officer 2')
	rank_officer_2 = fields.Char(string='Rank of police officer 2')
	tosc = fields.Char(string="Case submitting Time", required=False, )
	receiving_party = fields.Many2one('receiving.party', string="Receiving Party")
	receiving_party_rank = fields.Many2one('receiving.party.rank', string="Receiving Party Rank")
	receiving_name = fields.Char(string="Receiving Party Name", required=False, )
	case_detail = fields.Text(string='Case details ')
	case_type = fields.One2many('case.type', "main_class", string="Case Type")
	party_link = fields.One2many('traffic.party.detail', "main_class", string="Party Detail")

	def confirm(self):
		pass

	@api.model
	def create(self, vals):
		vals['number'] = self.env['ir.sequence'].next_by_code('recrod.number')
		new_record = super(ViolationDetail, self).create(vals)
		return new_record

	@api.onchange('date')
	def _change_daytime(self):
		if self.date:
			self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')
			self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")


class trafficPartyDetail(models.Model):
	_name = 'traffic.party.detail'

	# party = fields.Text("Party")
	car_name = fields.Char("Name of Car")
	car_plate = fields.Char("Plate Number")
	name = fields.Char("Driver Name")
	driver_country = fields.Many2one('res.country', "Nationality")
	id_num = fields.Char("ID number")
	id_type = fields.Many2one('id.type', "ID Type")
	dln = fields.Char("Driving License Number")
	oftc = fields.Char("Owner of the car")
	remark = fields.Text("Remarks")
	other_onwer = fields.Boolean("Owner Is Someone Else ?")

	main_class = fields.Many2one('violation.detail')
	owner_detail = fields.One2many('owner.detail', 'main_class', string="Owner Detail")


class OwnerDetail(models.Model):
	_name = 'owner.detail'

	name = fields.Char("Name of Owner")
	country = fields.Many2one('res.country', "Nationality of Owner")
	id_num = fields.Char("ID number of Owner")
	id_type = fields.Many2one('id.type', "ID Type of Owner")
	mobile = fields.Char("Mobile Number of Owner")
	remark = fields.Text("Remarks")

	main_class = fields.Many2one('traffic.party.detail')


class MinistryName(models.Model):
	_name = 'ministry.name'

	name = fields.Char(string="Name of Ministry")


class HospitalName(models.Model):
	_name = 'hospital.name'

	name = fields.Char(string="Name of Hospital")


class MaenTrans(models.Model):
	_name = 'mean.trans'

	name = fields.Char(string="Means of Transportation")


class WhatFound(models.Model):
	_name = 'what.found'

	name = fields.Char(string="What we found")


class IDType(models.Model):
	_name = 'id.type'

	name = fields.Char(string="ID Type")


class RoadName(models.Model):
	_name = 'road.name'

	name = fields.Char(string="Road Name")


class CenterName(models.Model):
	_name = 'center.name'

	name = fields.Char(string="Center Name")


class Location(models.Model):
	_name = 'location.name'

	name = fields.Char(string="Location Name")


class DigitalTag(models.Model):
	_name = 'digital.tag'

	name = fields.Char(string="Name")


class Direction(models.Model):
	_name = 'direction.name'

	name = fields.Char(string="Direction")


class ReceivingParty(models.Model):
	_name = 'receiving.party'

	name = fields.Char(string="Receiving Party")


class ReceivingPartyRank(models.Model):
	_name = 'receiving.party.rank'

	name = fields.Char(string="Receiving Party Rank")


class TypeOfCase(models.Model):
	_name = 'type.case'

	name = fields.Char(string="Type of Case")


class TypeOfViolation(models.Model):
	_name = 'type.violation'

	name = fields.Char(string="Type of Case")

class CategoryCase(models.Model):
	_name = 'cate.case'

	name = fields.Char(string="Category of Case")