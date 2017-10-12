# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class accessories(models.Model):
    _name = 'purchase.accessories'
    _rec_name = 'sr_no'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    sr_no = fields.Char(string="Sr no")
    wonumber = fields.Char(string="WO No",)
    style = fields.Char(string="Style No")
    date = fields.Date(string="Date")
    merchant = fields.Char(string="Merchant Name")

    vendor = fields.Many2one('res.partner',string="Vendor Name", required= True)
    warehouse = fields.Many2one('stock.picking.type',string="Warehouse")
    destination_location = fields.Many2one('stock.location',string="Destination Location Zone")
    source_location = fields.Many2one('stock.location',string="Source Location Zone")
    delivery = fields.Many2one('stock.picking',string="Delivery")
    
    accessories_stages = fields.Selection([
        ('draft', 'Draft'),
        ('recieved', 'Received'),
        ('customer_approval', 'Customer Approval'),
        ('approved', 'Approved'),
        ('validate', 'Validate'),
        ('cancel', 'Cancel'),
        ],default='draft')

    tree_link = fields.One2many('purchase.accessories.tree','tree')

    @api.model
    def create(self, vals):
        vals['sr_no'] = self.env['ir.sequence'].next_by_code('purchase.accessories')
        new_record = super(accessories, self).create(vals)

        return new_record
                        
    @api.multi
    def in_draft(self):
        self.accessories_stages = "draft"
                        
    @api.multi
    def in_recieved(self):
        self.accessories_stages = "recieved"

    @api.multi
    def in_customer_approval(self):
        self.accessories_stages = "customer_approval"

    @api.multi
    def in_approved(self):
        self.accessories_stages = "approved"

    @api.multi
    def in_validate(self):
        self.accessories_stages = "validate"

        create_reorder = self.env['stock.picking'].create({
            'partner_id': self.vendor.id,
            'min_date': self.date,
            'origin': self.sr_no,
            'picking_type_id': self.warehouse.id,
            'location_id': self.source_location.id,
            'location_dest_id': self.destination_location.id,

        })

        for x in self.tree_link:
            create_variants = self.env['stock.move'].create({
                'product_id': x.product.id,
                # 'product_tmpl_id': x.product_tmpl_id.id ,
                'product_uom_qty': x.recieved,
                'product_uom': x.unit_measurement.id,
                'picking_id': create_reorder.id,
                'location_id': create_reorder.location_id.id,
                'name': x.product.name,
                'location_dest_id': create_reorder.location_dest_id.id,
            })

        self.delivery = create_reorder.id

    @api.multi
    def in_cancel(self):
        self.accessories_stages = "cancel"

class yarn(models.Model):
    _name = 'purchase.yarn'
    _rec_name = 'sr_no'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    sr_no = fields.Char(string="Sr no")
    wonumber = fields.Char(string="WO No",)
    style = fields.Char(string="Style No")
    date = fields.Date(string="Date")
    merchant = fields.Char(string="Merchant Name")

    vendor = fields.Many2one('res.partner',string="Vendor Name", required= True)
    broker = fields.Many2one('res.partner',string="Broker")
    warehouse = fields.Many2one('stock.picking.type',string="Warehouse")
    destination_location = fields.Many2one('stock.location',string="Destination Location Zone")
    source_location = fields.Many2one('stock.location',string="Source Location Zone")
    delivery = fields.Many2one('stock.picking',string="Delivery")

    tree_link = fields.One2many('purchase.accessories.tree','yarn_tree')

    @api.model
    def create(self, vals):
        vals['sr_no'] = self.env['ir.sequence'].next_by_code('purchase.yarn')
        new_record = super(yarn, self).create(vals)

        return new_record

class accessories_tree(models.Model):
    _name = "purchase.accessories.tree"

    product = fields.Many2one('product.product',string="Product")
    unit_measurement = fields.Many2one('product.uom', string="Unit of Measurement")

    to_recieve = fields.Float(string="To Recieve")
    recieved = fields.Float(string="Recieved")
    rejected = fields.Float(string="Rejected")
    price = fields.Float(string="price")

    tree = fields.Many2one('purchase.accessories')
    yarn_tree = fields.Many2one('purchase.yarn')

    remarks = fields.Char(string="Remarks")

class YarnRequirement(models.Model):
    _name = "yarn.requirement"
    _rec_name = 'date'

    date = fields.Date("Date" ,required = True)
    won = fields.Many2many('mrp.production',string="Work Order No",required = True)
    stage = fields.Selection([('draft', 'Draft'),('val', 'Validate')],default = 'draft') 

    tree_link = fields.One2many('yarn.requirement.tree','yarn_tree')

    @api.multi
    def in_draft(self):
        self.stage = "draft"


    @api.multi
    def val(self):
        self.stage = "val"

class YarnRequirementTree(models.Model):
    _name = "yarn.requirement.tree"

    product = fields.Many2one('product.product',string="Product")
    won = fields.Many2many('mrp.production',string="W/O")
    brand = fields.Char("Brand")
    ttype = fields.Char("Type")
    delv_date = fields.Date("Delivery Date")
    prod_type = fields.Char("Product Type")
    qty = fields.Integer("Quantity")
    nob = fields.Integer("No of Bags")
    rate = fields.Many2many('yarn.rates',string="Rate")
    appr_rate = fields.Many2many('yarn.rates',string="Approved Rate")
    unit_price = fields.Float("Unit Price")
    broker = fields.Many2one('res.partner',"Broker")
    contract = fields.Binary("Contract")

    yarn_tree = fields.Many2one('yarn.requirement')

    @api.onchange('rate')
    def rate_change(self):
        self.appr_rate = self.rate

class YarnRate(models.Model):
    _name = "yarn.rates"

    name = fields.Char("Name")
    partner = fields.Many2one('res.partner',"Partner")
    rate = fields.Float("Rate")

class PurchaseOrderExt(models.Model):
    _inherit = 'purchase.order'

    style = fields.Char("Style No")
    merchant = fields.Many2one('hr.employee',string="Merchant Name")
    won = fields.Many2many('mrp.production',string="Work Order No",required = True)

class YarnDyeing(models.Model):
    _name = "yarn.dyeing"

    name = fields.Many2one('res.partner',string="To")
    date = fields.Date("Date")
    subject = fields.Char("Subject")
    buyer = fields.Char("Buyer")
    style = fields.Char("Style No")
    won = fields.Many2many('mrp.production',string="Work Order No",required = True)
    delv_date = fields.Date("Delivery Date")
    primary = fields.Char("Primary")
    secondary = fields.Char("Secondary")
    des = fields.Text("Note")
    mf = fields.Char("MF No")
    tree_link = fields.One2many('yarn.dyeing.tree','yarn_tree')

    stage = fields.Selection([('draft', 'Draft'),
        ('sent', 'Sent'),
        ('in_house', 'In House')
        ],default = 'draft') 

    @api.multi
    def in_draft(self):
        self.stage = "draft"


    @api.multi
    def in_sent(self):
        self.stage = "sent"

    @api.multi
    def in_house(self):
        self.stage = "in_house"

class YarnDyeingTree(models.Model):
    _name = "yarn.dyeing.tree"

    won = fields.Many2many('mrp.production',string="W/O",required = True)
    color = fields.Char("Colors")
    yarn = fields.Char("Yarn")

    lot = fields.Char("Lot")
    fabric = fields.Many2one('product.product',"Fabric")
    dia = fields.Many2one('purchase.dia' , string="Dia")
    gauge = fields.Many2one('purchase.gauge' , string="Gauge")
    cutting = fields.Many2one('purchase.cutting' , string="Cutting")
    width = fields.Many2one('purchase.width' , string="Width")
    gsm = fields.Many2one('purchase.gsm' , string="GSM")
    process = fields.Many2one('purchase.process' , string="Process")

    rate = fields.Float("Rate")
    issue_qty = fields.Float("Issue Quantity")
    receive_qty = fields.Float("Received Qty")
    blc = fields.Float("Balance" ,compute='_blc')
    wastage = fields.Float("Wastage" ,compute='_wastage')
    std = fields.Char("STD")
    yarn_tree = fields.Many2one('yarn.dyeing')



    
    @api.one
    @api.depends('issue_qty','receive_qty')
    def _blc(self):
        self.blc = self.issue_qty - self.receive_qty

    @api.one
    @api.depends('issue_qty','receive_qty')
    def _wastage(self):
        if self.issue_qty > 0.0 and self.receive_qty > 0.0:
            self.wastage = (self.receive_qty / self.issue_qty)* 100

class ResPartnerExt(models.Model):
    _inherit = "res.partner"

    knitting = fields.Boolean("Knitting")

class YarnKnitting(models.Model):
    _name = "yarn.knitting"

    name = fields.Many2one('res.partner',string="To")
    date = fields.Date("Date")
    customer = fields.Char("Customer")
    won = fields.Many2many('mrp.production',string="W/O")
    delv_date = fields.Date("Delivery Date")
    tree_link = fields.One2many('yarn.knitting.tree','yarn_tree')

    stage = fields.Selection([('draft', 'Draft'),
        ('sent', 'Sent'),
        ('complete', 'Complete'),
        ('cancel', 'Cancel')
        ],default = 'draft') 

    @api.multi
    def in_draft(self):
        self.stage = "draft"

    @api.multi
    def in_sent(self):
        self.stage = "sent"

    @api.multi
    def in_complete(self):
        self.stage = "complete"

    @api.multi
    def in_cancel(self):
        self.stage = "cancel"

class YarnKnittingTree(models.Model):
    _name = "yarn.knitting.tree"

    won = fields.Many2many('mrp.production',string="W/O")
    fabric = fields.Many2one('product.product',string="Fabric")
    yarn = fields.Many2many('product.product',string="Yarn")
    uom = fields.Many2one('product.uom',string="UOM")
    sl = fields.Many2one('purchase.sl' , string="S.L")
    otm = fields.Many2one('purchase.otm' , string="OTM")
    dia = fields.Many2one('purchase.dia' , string="Dia")
    gauge = fields.Many2one('purchase.gauge' , string="Gauge")
    cutting = fields.Many2one('purchase.cutting' , string="Cutting")
    requested = fields.Float("Requested")
    received = fields.Float("Received")
    balance = fields.Float("Balance" ,compute='_balance')
    wastage = fields.Char("Wastage Percentage" ,compute='_wastage')   
    rate  = fields.Char("Rates") 
    yarn_tree = fields.Many2one('yarn.knitting')

    @api.one
    @api.depends('requested','received')
    def _balance(self):
        if self.received and self.requested:
            self.balance = self.received - self.requested

    @api.one
    @api.depends('requested','received','balance')
    def _wastage(self):
        if self.balance < 0:
            if self.received > 0.0 and self.requested > 0.0:
                self.wastage = str((-1*((self.balance) / self.requested)* 100 )) + "%"

class ProductExt(models.Model):
    _inherit = 'product.product'

    ttype = fields.Selection([
        ('yarn', 'Yarn'),
        ('fabric', 'Fabric'),
        ('accessories', 'Accessories'),
        ('general', 'General Products'),
        ('thread', 'Thread')
        ], required=True, string="Type") 

    net_weight = fields.Float("Net Weight")
    # yarn = fields.Many2many('product.product',string="Yarn")

class PurchaseDia(models.Model):
    _name = 'purchase.dia'

    name = fields.Char("Dia")

class PurchaseSL(models.Model):
    _name = 'purchase.sl'

    name = fields.Char("SL")

class PurchaseGauge(models.Model):
    _name = 'purchase.gauge'

    name = fields.Char("Gauge")

class PurchaseCutting(models.Model):
    _name = 'purchase.cutting'

    name = fields.Char("Cutting Line")

class PurchaseWidth(models.Model):
    _name = 'purchase.width'

    name = fields.Char("Width")

class PurchaseGSM(models.Model):
    _name = 'purchase.gsm'

    name = fields.Char("GSM")

class PurchaseProcess(models.Model):
    _name = 'purchase.process'

    name = fields.Char("Process")

class PurchaseOTM(models.Model):
    _name = 'purchase.otm'

    name = fields.Char("OTM")


