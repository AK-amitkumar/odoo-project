# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
from openerp import models, fields, api, http
from openerp.addons.website.controllers.main import Website

class PoliceDetail(models.Model):
    _name = 'police.detail'
    _rec_name = 'number'
    number = fields.Char(string="Report Number")
    case_id = fields.Char(string="Case ID",required=False,)
    date = fields.Date(default = datetime.date.today())
    day = fields.Char()
    time = fields.Char(required=True)
    road_name = fields.Many2one('road.name', string="Road Name",required=True,)
    center_name = fields.Many2one('center.name', string="Center Name",required=True,)
    location_name = fields.Many2one('location.name', string="Location Name",required=True,)
    digital_tag = fields.Many2one('digital.tag', string="Digital Tag",required=True,)
    direction_name = fields.Many2one('direction.name', string="Direction Name",required=True,)
    violation = fields.Float(string='Time of Case' ,required=True,)
    code = fields.Many2one(comodel_name="car.code",string='Code of Police CAR',required=True,)
    police_officer = fields.Char(string='Police Officer 1',required=True,)
    rank_officer = fields.Char(string='Rank of officer 1',required=True,)
    PID1 = fields.Char(string="Officer 1 ID",required=True, )
    PID2 = fields.Char(string="Officer 2 ID", required=False, )
    sex_of1 = fields.Selection(string="Gender", selection=[('m', 'M'), ('f', 'F'), ], required=False, )
    sex_of2 = fields.Selection(string="Gender", selection=[('m', 'M'), ('f', 'F'), ], required=False, )
    name_officer_2 = fields.Char(string='Police officer 2')
    rank_officer_2 = fields.Char(string='Rank of officer 2')
    tosc = fields.Float(string="Case submitting Time", required=True )
    receiving_party = fields.Many2one('receiving.party', string="Receiving Party",required=True,)
    receiving_party_rank = fields.Many2one('receiving.party.rank', string="Receiving Party Rank",required=True,)
    receiving_name = fields.Char(string="Receiving Party Name",required=True, )
    case_detail = fields.Text(string='Case details ')
    party_link = fields.One2many('party.detail', "main_class", string="Party Detail")
    case_type = fields.One2many('case.type', "main_class", string="Case Type")

    preview = fields.Html('Report Preview',compute="generate_preview")

    @api.one
    def generate_preview(self):
        self.preview = self.env['report'].get_html(self, 'police_case_summary.module_report')

    @api.multi
    def open_menu(self):
        return {'name': 'Police Record', 'domain': [], 'res_model': 'police.detail',
                'type': 'ir.actions.act_window', 'view_mode': 'form', 'view_type': 'form',
                'context': {}, 'target': 'self', }

    @api.model
    def create(self, val):
        val['number'] = self.env['ir.sequence'].next_by_code('rec.number')
        val['case_id'] = self.env['ir.sequence'].next_by_code('rec.case')
        new_record = super(PoliceDetail, self).create(val)
        return new_record

    @api.onchange('date')
    def _change_daytime(self):
        if self.date:
            self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')
            self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")

class CaseType1(models.Model):
    _name = 'case.type1'
    _rec_name = 'case_type'
    case_type = fields.Many2one(comodel_name="type.case", string="Violation Type",required=True,)
    cate_case = fields.Many2one(comodel_name="cate.case", string="Violation Category", required=False, )
    qty = fields.Char(string="Quantity",  required=False, )
    vio_code = fields.Char(string="Violation Code ",  required=False, )
    vio_number = fields.Char(string="Violation Number",  required=False, )

    main_class = fields.Many2one(comodel_name="violation.detail", string="Violation Type", required=False, )


class CaseType(models.Model):
    _name = 'case.type'
    _rec_name = 'case_type'
    main_case = fields.Many2one(comodel_name="main.case", string="Case",required=True,)
    case_type = fields.Many2one(comodel_name="type.case", string="Case Type",required=True, )
    cate_case = fields.Many2one(comodel_name="cate.case", string="Detail",required=True, )
    sub_cate_case = fields.Many2one(comodel_name="case.sub.cate", string="More Detail", required=True, )
    # qty = fields.Char(string="Quantity",  required=False, )
    vio_code = fields.Char(string="Case Code ",  required=False, )
    vio_number = fields.Char(string="Case Number",  required=False, )

    main_class = fields.Many2one(comodel_name="police.detail", string="Case Type", required=False, )


class HajjUmrah(models.Model):
    _name = 'hajj.umrah'
    _rec_name = 'case_id'

    # number = fields.Char(string="Report Number")
    case_id = fields.Char(string="Case ID",required=True,)
    date = fields.Date(default=datetime.date.today())
    day = fields.Char()
    time = fields.Char(required=True)
    road_name = fields.Many2one('road.name', string="Road Name",required=True,)
    center_name = fields.Many2one('center.name', string="Center Name",required=True,)

    violation_type = fields.One2many(comodel_name="hajjumrah.violation", inverse_name="main_class", string="Violation Information", required=False, )

    @api.model
    def create(self, vals):
        vals['case_id'] = self.env['ir.sequence'].next_by_code('rec.umrah')
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
    remarks = fields.Text(string="Remarks", required=False, )

    main_class  = new_field_id = fields.Many2one(comodel_name="hajj.umrah", string="Hajj and Umrah", required=False, )


class PartyDetail(models.Model):
    _name = 'party.detail'

    name = fields.Char("Driver Name",required=True,)
    car_name = fields.Many2one(comodel_name="car.name",   string="Name of Car",required=False,)
    car_color = fields.Many2one(comodel_name="car.color", string="Color of Car",required=False,)
    car_model = fields.Many2one(comodel_name="car.model", string="Model of Car",required=False,)
    car_maker = fields.Many2one(comodel_name="car.maker", string="Maker of Car",required=False,)
    car_plate = fields.Char("Plate Number",required=False,)
    driver_country = fields.Many2one('res.country', "Nationality",required=True,)
    id_num = fields.Char("ID number",required=True,)
    sex = fields.Selection(string="Gender", selection=[('m', 'M'), ('f', 'F'), ],required=False,)
    id_type = fields.Many2one('id.type', "ID Type",required=True,)
    what_found = fields.Many2one('what.found', "What we found",required=False,)
    qty = fields.Float(string="Quantity",required=False,)
    accident_reason = fields.Char("Reason of accident ",required=False,)
    result = fields.Char("Results",required=False,)
    mean_trans = fields.Many2one('mean.trans', "Means of Transportation",required=False,)
    hospital_name = fields.Many2one('hospital.name', "Name of Hospital",required=False,)
    main_class = fields.Many2one('police.detail', "Party Detail",required=False,)
    remark = fields.Text("Remarks",required=False,)
    additional = fields.Text("Additional Details",required=False,)
    previous_record = fields.Boolean("Previous Records")
    companion_detail = fields.Boolean("Companion Details")

    previous_record_link = fields.One2many('previous.record', "main_class", string="Previous Record")
    companion_detail_link = fields.One2many('companion.detail', "main_class", string="Companion Detail")


class CompanionDetail(models.Model):
    _name = 'companion.detail'

    name = fields.Char("Name",required=True,)
    country = fields.Many2one('res.country', "Nationality",required=True,)
    id_num = fields.Char("ID number",required=True,)
    id_type = fields.Many2one('id.type', "ID Type",required=True,)
    relation = fields.Char("Relation",required=False,)
    sex = fields.Selection(string="Gender", selection=[('m', 'M'), ('f', 'F'), ],required=False,)
    what_found = fields.Char("What we found",required=False,)
    qty = fields.Float(string="Qty",required=False, )
    accident_reason = fields.Char("Reason of accident ",required=False,)
    result = fields.Char("Results",required=False,)
    mean_trans = fields.Many2one('mean.trans', "Means of Transportation",required=False,)
    hospital_name = fields.Many2one('hospital.name', "Name of Hospital",required=False,)

    main_class = fields.Many2one('party.detail')


class PreviousRecord(models.Model):
    _name = 'previous.record'

    ministry_name = fields.Many2one('ministry.name', "Name of Ministry",required=True,)
    no_complaint = fields.Char("Number Of Complaint",required=True,)
    date = fields.Date(required=True,)
    day = fields.Char(required=True,)

    main_class = fields.Many2one('party.detail')

    @api.onchange('date')
    def _change_daytime(self):
        if self.date:
            self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')
            self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")


class ViolationDetail(models.Model):
    _name = 'violation.detail'
    _rec_name = 'number'

    number = fields.Char(string="Report Number")
    case_id = fields.Char(string="Case ID",required=False,)
    date = fields.Date(default=datetime.date.today())
    day = fields.Char()
    time = fields.Char(required=True)
    road_name = fields.Many2one('road.name', string="Road Name",required=False,)
    center_name = fields.Many2one('center.name', string="Center Name",required=False,)
    location_name = fields.Many2one('location.name', string="Location Name",required=False,)
    digital_tag = fields.Many2one('digital.tag', string="Digital Tag",required=False,)
    direction_name = fields.Many2one('direction.name', string="Direction Name",required=False,)
    violation = fields.Float(string='Time of Violation',required=True)
    code = fields.Many2one(comodel_name="car.code",string='Code of Police CAR',required=True,)
    police_officer = fields.Char(string='Police Officer 1',required=False,)
    rank_officer = fields.Char(string='Rank of officer 1',required=False,)
    PID1 = fields.Char(string="Officer 1 ID",required=False,)
    sex_of1 = fields.Selection(string="Gender", selection=[('m', 'M'), ('f', 'F'), ],
                               required=False, )
    sex_of2 = fields.Selection(string="Gender", selection=[('m', 'M'), ('f', 'F'), ],
                               required=False, )
    name_officer_2 = fields.Char(string='Police officer 2')
    rank_officer_2 = fields.Char(string='Rank of officer 2')
    PID2 = fields.Char(string="Officer 2 ID", required=False, )
    tosc = fields.Float(string="Violation submitting Time",required=True)

    case_detail = fields.Text(string='Violation details ')
    case_type = fields.One2many('case.type1', "main_class", string="Violation Type")
    party_link = fields.One2many('traffic.party.detail', "main_class", string="Party Detail")
    receive_link = fields.One2many('traffic.receive', "main_class", string="Receiving Party")

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('record.number')
        vals['case_id'] = self.env['ir.sequence'].next_by_code('record.case')
        new_record = super(ViolationDetail, self).create(vals)
        return new_record

    @api.onchange('date')
    def _change_daytime(self):
        if self.date:
            self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')
            self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")



class TrafficReceive(models.Model):
    _name = 'traffic.receive'
    _rec_name = 'receiving_party'

    receiving_party = fields.Many2one('receiving.party', string="Receiving Party",required=False,)
    receiving_party_rank = fields.Many2one('receiving.party.rank', string="Receiving Party Rank",required=False,)
    receiving_name = fields.Char(string="Receiving Party Name",required=False,)

    main_class = fields.Many2one(comodel_name="violation.detail", string="Receiving Party", required=False, )


class trafficPartyDetail(models.Model):
    _name = 'traffic.party.detail'

    # party = fields.Text("Party")
    car_name = fields.Char("Name of Car",required=False,)
    car_plate = fields.Char("Plate Number",required=False,)
    name = fields.Char("Driver Name",required=False,)
    driver_country = fields.Many2one('res.country', "Nationality",required=False,)
    id_num = fields.Char("ID number",required=True,)
    id_type = fields.Many2one('id.type', "ID Type",required=False,)
    sex = fields.Selection(string="Gender", selection=[('m', 'M'), ('f', 'F'), ], required=False, )
    dln = fields.Char("Driving License Number",required=False,)
    oftc = fields.Char("Owner of the car",required=False,)
    car_maker = fields.Many2one(comodel_name="car.maker", string="Maker of Car", required=False, )
    remark = fields.Text("Remarks",required=False,)
    other_onwer = fields.Boolean("Owner Is Someone Else ?")
    # vio_id = fields.Char("Violation Id")

    main_class = fields.Many2one('violation.detail')
    owner_detail = fields.One2many('owner.detail', 'main_class', string="Owner Detail")


class OwnerDetail(models.Model):
    _name = 'owner.detail'

    name = fields.Char("Name of Owner",required=False,)
    country = fields.Many2one('res.country', "Nationality of Owner",required=False,)
    id_num = fields.Char("ID number of Owner",required=False,)
    id_type = fields.Many2one('id.type', "ID Type of Owner",required=False,)
    mobile = fields.Char("Mobile Number of Owner",required=False,)
    remark = fields.Text("Remarks",required=False,)

    main_class = fields.Many2one('traffic.party.detail')


class MinistryName(models.Model):
    _name = 'ministry.name'

    name = fields.Char(string="Name of Ministry",required=True,)


class HospitalName(models.Model):
    _name = 'hospital.name'

    name = fields.Char(string="Name of Hospital",required=True,)


class MeanTrans(models.Model):
    _name = 'mean.trans'

    name = fields.Char(string="Means of Transportation",required=True,)


class WhatFound(models.Model):
    _name = 'what.found'

    name = fields.Char(string="What we found",required=True,)


class IDType(models.Model):
    _name = 'id.type'

    name = fields.Char(string="ID Type",required=True,)


class RoadName(models.Model):
    _name = 'road.name'

    name = fields.Char(string="Road Name",required=True,)
    road_tree = fields.One2many(comodel_name="road.tree", inverse_name="road", string="Road Link", required=False, )
    receiving_tree = fields.One2many(comodel_name="receiving.party", inverse_name="road_link", string="Road Link", required=False, )
    direction_tree = fields.One2many(comodel_name="road.tag", inverse_name="direction_link", string="Direction Link", required=False, )

    @api.model
    def create(self, val):
        record = super(RoadName, self).create(val)
        for x in record.road_tree:
            x.center.road_name = record.id
            for y in x.car_center_link:
                y.car_center = x.center
        for z in record.receiving_tree:
            z.road_name = record.id

        for x in record.direction_tree:
            x.direction.road_link = record.id
            for y in x.direction_tag_link:
                y.direction_name = x.direction

        return record

    @api.multi
    def write(self, val):
        super(RoadName, self).write(val)
        for x in self.road_tree:
            x.center.road_name = self.id
            for y in x.car_center_link:
                y.car_center = x.center
        for z in self.receiving_tree:
            z.road_name = self.id

        for x in self.direction_tree:
            x.direction.road_link = self.id
            for y in x.direction_tag_link:
                y.direction_name = x.direction

        return True


class RoadTree(models.Model):
    _name = 'road.tree'
    _rec_name = 'road'

    center = fields.Many2one(comodel_name="center.name", string="Center Name",required=True,)
    road = fields.Many2one(comodel_name="road.name", string="Road Tree",required=True,)
    car_center_link = fields.One2many(comodel_name="car.code", inverse_name="road_link", string="Car Center", required=False, )

class RoadTag(models.Model):
    _name = 'road.tag'
    _rec_name = 'direction_link'

    direction = fields.Many2one(comodel_name="direction.name", string="Direction Name",required=True,)
    direction_link = fields.Many2one(comodel_name="road.name", string="Road Tree",required=True,)
    direction_tag_link = fields.One2many(comodel_name="digital.tag", inverse_name="road_link", string="Direction Tag", required=False, )

class CenterName(models.Model):
    _name = 'center.name'

    name = fields.Char(string="Center Name",required=True,)
    road_name  = fields.Many2one(comodel_name="road.name", string="Road Name", required=False, )


class Location(models.Model):
    _name = 'location.name'

    name = fields.Char(string="Location Name",required=True,)


class DigitalTag(models.Model):
    _name = 'digital.tag'

    name = fields.Char(string="Digital Tag",required=True,)
    direction_name = fields.Many2one(comodel_name="direction.name", string="Direction Name", required=False, )
    road_link = fields.Many2one(comodel_name="road.tag", string="Road Tree Link", required=False, )


class Direction(models.Model):
    _name = 'direction.name'

    name = fields.Char(string="Direction",required=True,)
    road_link = fields.Many2one(comodel_name="road.name", string="Road Name", required=False, )


class ReceivingParty(models.Model):
    _name = 'receiving.party'

    name = fields.Char(string="Receiving Party",required=True,)
    road_name  = fields.Many2one(comodel_name="road.name", string="Road Name", required=False, )
    road_link = fields.Many2one(comodel_name="road.name", string="Road Link", required=False, )

class ReceivingPartyRank(models.Model):
    _name = 'receiving.party.rank'

    name = fields.Char(string="Receiving Party Rank",required=True,)


class TypeOfCase(models.Model):
    _name = 'type.case'

    name = fields.Char(string="Type of Case",required=True,)
    case = fields.Many2one(comodel_name="main.case", string="Case", required=False, )


class TypeOfViolation(models.Model):
    _name = 'type.violation'

    name = fields.Char(string="Type of Violation",required=True,)


class CategoryCase(models.Model):
    _name = 'cate.case'

    name = fields.Char(string="Detail",required=True,)
    case_type = fields.Many2one(comodel_name="type.case", string="Case Type", required=False, )


class CarMaker(models.Model):
    _name = 'car.maker'

    name = fields.Char(string="Maker of Car",required=True,)


class CarName(models.Model):
    _name = 'car.name'

    name = fields.Char(string="Name of Car",required=True,)
    maker = fields.Many2one(comodel_name="car.maker", string="Car Maker", required=False, )

class CarColor(models.Model):
    _name = 'car.color'

    name = fields.Char(string="Color of Car",required=True,)
    car_name = fields.Many2one(comodel_name="car.name", string="Car Name", required=False, )


class CarModel(models.Model):
    _name = 'car.model'

    name = fields.Char(string="Model of Car",required=True,)
    maker = fields.Many2one(comodel_name="car.maker", string="Car Maker", required=False, )


class CaseLevel(models.Model):
    _name = 'case.level'
    _rec_name = 'case'
    _description = "Create Case Level"

    case = fields.Many2one(comodel_name="main.case", string="Case",required=True,)
    tree_link = fields.One2many(comodel_name="case.level.tree", inverse_name="level_link", string="Case Type", required=False, )

    @api.model
    def create(self, val):
        record = super(CaseLevel, self).create(val)
        for x in record.tree_link:
            x.case_type.case = record.case
            for y in x.case_level_cate:
                y.case_cate.case_type = x.case_type
                for z  in y.case_level_sub_cate_link:
                    z.case_sub_cate.case_cate = y.case_cate

        return record

    @api.multi
    def write(self, val):
        super(CaseLevel, self).write(val)
        for x in self.tree_link:
            x.case_type.case = self.case
            for y in x.case_level_cate:
                y.case_cate.case_type = x.case_type
                for z  in y.case_level_sub_cate_link:
                    z.case_sub_cate.case_cate = y.case_cate
        return True


class CaseLevelTree(models.Model):
    _name = 'case.level.tree'
    _rec_name = 'case_type'

    level_link = fields.Many2one(comodel_name="case.level", string="Case Type",required=True,)
    case_type = fields.Many2one(comodel_name="type.case", string="Case Type",required=True, )
    case_level_cate = fields.One2many(comodel_name="case.level.cate", inverse_name="case_level_link", string="Case Level Detail", required=False, )


class CaseSubCate(models.Model):
    _name = 'case.sub.cate'
    _rec_name = 'name'
    _description = 'More Detail'

    name = fields.Char(string="More Detail",required=True,)
    case_cate = fields.Many2one(comodel_name="cate.case", string="Detail", required=False, )


class CaseLevelCate(models.Model):
    _name = 'case.level.cate'
    _rec_name = 'case_cate'

    case_cate = fields.Many2one(comodel_name="cate.case", string="Detail",required=True,)
    case_type = fields.Many2one(comodel_name="type.case", string="Case Type",required=True,)
    case_level_link = fields.Many2one(comodel_name="case.level.tree", string="Case Level Detail", required=False, )
    case_level_sub_cate_link = fields.One2many(comodel_name="case.level.cate.sub", inverse_name="case_cate_level_link", string="Case Level More Detail", required=False, )


class CaseLevelCateSub(models.Model):
    _name = 'case.level.cate.sub'
    _rec_name = 'case_sub_cate'

    case_cate = fields.Many2one(comodel_name="cate.case", string="Detail",required=True,)
    case_sub_cate = fields.Many2one(comodel_name="case.sub.cate", string="More Detail",required=True,)
    case_cate_level_link = fields.Many2one(comodel_name="case.level.cate", string="Case Level More Detail", required=False, )


class MainCase(models.Model):
    _name = 'main.case'
    _rec_name = 'name'

    name = fields.Char(string="Case",required=True,)



class CarCode(models.Model):
    _name = 'car.code'
    _rec_name = 'name'

    name = fields.Char(string="Code of Police CAR",required=True,)
    car_center = fields.Many2one(comodel_name="center.name", string="Center Name", required=False, )
    road_link = fields.Many2one(comodel_name="road.tree", string="Road Tree Link", required=False, )


class CarConfig(models.Model):
    _name = 'car.config'
    _rec_name = 'car_maker'

    car_maker = fields.Many2one(comodel_name="car.maker", string="Car Maker", required=True, )
    car_name_config = fields.One2many(comodel_name="car.name.config", inverse_name="car_config_link", string="Car Name Config", required=False, )

    @api.model
    def create(self, val):
        record = super(CarConfig, self).create(val)
        for x in record.car_name_config:
            x.name.maker = record.id
            x.car_model.maker = record.id
            for y in x.car_color_config:
                y.name.car_name = x.name
        return record

    @api.multi
    def write(self, val):
        super(CarConfig, self).write(val)
        for x in self.car_name_config:
            x.name.maker = self.id
            x.car_model.maker = self.id
            for y in x.car_color_config:
                y.name.car_name = x.name
        return True

class CarNameConfig(models.Model):
    _name = 'car.name.config'
    _rec_name = 'name'

    name = fields.Many2one(comodel_name="car.name", string="Car Name", required=True, )
    car_model = fields.Many2one(comodel_name="car.model", string="Car Model", required=True, )
    car_config_link = fields.Many2one(comodel_name="car.config", string="Car Name Config", required=False, )
    car_color_config = fields.One2many(comodel_name="car.color.config", inverse_name="car_color_link", string="Car Color", required=False, )


class CarColorConfig(models.Model):
    _name = 'car.color.config'
    _rec_name = 'name'

    name = fields.Many2one(comodel_name="car.color", string="Car Color", required=True, )
    car_color_link = fields.Many2one(comodel_name="car.name.config", string="Car Color Config", required=False, )

#
# class NewPage(http.Controller):
#     @http.route('/police/',auth='public', website=True)
#     def index(self):
#         return http.request.render('police_project.index')
#
#
# class Websiste(Website):
#     @http.route(auth='public')
#     def index(self, data={},**kw):
#         super(Website, self).index(**kw)
#         return http.request.render('police_project.index', data)



