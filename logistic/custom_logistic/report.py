import os
import xlsxwriter
from datetime import datetime,date,timedelta
from odoo import models, fields, api
from odoo.exceptions import Warning,ValidationError


class XlsxReport(models.Model):
	_name = 'xl.report'
	_rec_name = 'customer'

	customer = fields.Many2one('res.partner',string="Customer",required=True)
	s_date = fields.Date("Start Date")
	e_date = fields.Date("End Date")
	ttype =  fields.Selection([
					 ('export', 'Export'),
					 ('import', 'Import'),
					 ],default='export',string="Report Type",required=True) 
	total = fields.Boolean("Total Report" ,default=False)

	@api.onchange('total')
	def onchange_total(self):
		if self.total == True:
			self.s_date = ''
			self.e_date = ''

	@api.multi
	def print_report(self):
		if self.total == True:
			if self.ttype == 'export':
				data=self.env['export.logic'].search([('customer','=',self.customer.id)])
				if data:
						return self.xlsx_report(data,ttype='export')
				else:
					raise  ValidationError('Report Does Not Exist According To Given Data')
			elif self.ttype == 'import':
				data=self.env['import.logic'].search([('customer','=',self.customer.id)])
				if data:
						return self.xlsx_report(data,ttype='import')
				else:
					raise  ValidationError('Report Does Not Exist According To Given Data')
			else:
				raise  ValidationError('Report Does Not Exist According To Given Data')
		else:
			if self.ttype == 'export' and self.e_date and self.s_date :
				data=self.env['export.logic'].search([('customer','=',self.customer.id),('date','>=',self.s_date),('date','<=',self.e_date)])
				if data:
					return self.xlsx_report(data,ttype='export')
				else:
					raise  ValidationError('Report Does Not Exist According To Given Data')

			elif self.ttype == 'import' and self.e_date and self.s_date :
				data=self.env['import.logic'].search([('customer','=',self.customer.id),('date','>=',self.s_date),('date','<=',self.e_date)])
				if data:
					return self.xlsx_report(data,ttype='import')
				else:
					raise  ValidationError('Report Does Not Exist According To Given Data')
			else:
				raise  ValidationError('Report Does Not Exist According To Given Data')
	
	@api.multi
	def xlsx_report(self,input_records,ttype):
		with xlsxwriter.Workbook("/home/odoo/odoo-dev/Projects/logistic/custom_logistic/static/src/lib/DAILY_SHIPMENT_STATUS_REPORT.xlsx") as workbook:
			main_heading = workbook.add_format({
				"bold": 1, 
				"align": 'center',
				"valign": 'vcenter',
				"font_color":'white',
				"bg_color": '548235'
				})
			# Create a format to use in the merged range.
			merge_format = workbook.add_format({
				'bold': 1,
				'border': 1,
				'align': 'left',
				'valign': 'vcenter',
				'font_size': '20',
				"font_color":'white',
				'fg_color': '7030a0'})


			
			main_data = workbook.add_format({
				"align": 'center',
				"valign": 'vcenter'

				})

			worksheet = workbook.add_worksheet(self.customer.name)

			# Merge 3 cells.
			worksheet.merge_range('A1:AF3', 'DAILY SHIPMENT STATUS REPORT  '+str(date.today())+' - '+str(self.customer.name), merge_format)

			worksheet.set_column('A4:AF4', 20)

			worksheet.write('A4', 'SR. no.',main_heading)
			worksheet.write('B4', 'Our Job No',main_heading)
			worksheet.write('C4', 'Customer Name',main_heading)
			worksheet.write('D4', 'Order No.',main_heading) 
			worksheet.write('E4', 'Shipment Recived Date',main_heading)
			worksheet.write('F4', 'B/L Number',main_heading)
			worksheet.write('G4', 'Number Of Containers',main_heading)
			worksheet.write('H4', 'Terminal',main_heading)
			worksheet.write('I4', 'Shipping Line',main_heading)
			worksheet.write('J4', 'Vessel Name',main_heading)
			worksheet.write('K4', 'ETA',main_heading)
			worksheet.write('L4', 'ETD',main_heading)
			worksheet.write('M4', 'CC Days',main_heading)
			worksheet.write('N4', 'Manifest documents Recived Date',main_heading)
			worksheet.write('O4', 'Bayan NO.',main_heading)
			worksheet.write('P4', 'Rotation NO.',main_heading)
			worksheet.write('Q4', 'Initial Bayan Date',main_heading)
			worksheet.write('R4', 'Pre-Bayan',main_heading)
			worksheet.write('S4', 'Manifest to Initial Bayan Printed',main_heading)
			worksheet.write('T4', 'Initial Bayan to Pre Bayan Printed',main_heading)
			worksheet.write('U4', 'Shuttling Start',main_heading)
			worksheet.write('V4', 'Shuttling End',main_heading)
			worksheet.write('W4', 'Final Bayan Date',main_heading)
			worksheet.write('X4', 'Shuttle to final bayan',main_heading)
			worksheet.write('Y4', 'Random Inspection',main_heading)
			worksheet.write('Z4', 'Custom Exam Of Containers no.',main_heading)
			worksheet.write('AA4', 'New Seal no.',main_heading)
			worksheet.write('AB4', 'Load Permit Printed On',main_heading)
			worksheet.write('AC4', 'Total Expenses',main_heading)
			worksheet.write('AD4', 'Status',main_heading)
			worksheet.write('AE4', 'Remarks',main_heading)
			worksheet.write('AF4', 'Reason for the delay (Shutout) (If any)',main_heading)

			row = 4
			col = 0	
			records = input_records
			def check_false(data):
				if data:
					return data
				else:
					return ' '

			if ttype == 'export':
				for x in records:
					worksheet.write_string (row, col,str(check_false(x.sr_no)),main_data)
					worksheet.write_string (row, col+1,str(check_false(x.our_job_no)),main_data)
					worksheet.write_string (row, col+2,str(check_false(x.customer.name)),main_data)
					worksheet.write_string (row, col+3,str(check_false(x.cust_ref_inv)),main_data)
					worksheet.write_string (row, col+4,str(check_false(x.shipper_date)),main_data)
					worksheet.write_string (row, col+5,str(check_false(x.bill_no)),main_data)
					worksheet.write_string (row, col+6,str(len(x.export_link)),main_data)
					worksheet.write_string (row, col+7,' ',main_data)
					worksheet.write_string (row, col+8,str(check_false(x.s_supplier.name)),main_data)
					worksheet.write_string (row, col+9,str(check_false(x.vessel_name)),main_data)
					worksheet.write_string (row, col+10,str(check_false(x.eta)),main_data)
					worksheet.write_string (row, col+11,str(check_false(x.etd)),main_data)
					if x.eta and x.shipper_date:
						k_e = (datetime.date(datetime.strptime(x.eta,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.shipper_date,'%Y-%m-%d'))).days
					else:
						k_e = ''
					worksheet.write_string (row, col+12,str(k_e),main_data)
					worksheet.write_string (row, col+13,str(check_false(x.mani_date)),main_data)
					worksheet.write_string (row, col+14,str(check_false(x.bayan_no)),main_data)
					worksheet.write_string (row, col+15,str(check_false(x.rot_no)),main_data)
					worksheet.write_string (row, col+16,str(check_false(x.bayan_date)),main_data)
					worksheet.write_string (row, col+17,str(check_false(x.pre_bayan)),main_data)
					if x.pre_bayan and x.mani_date:
						r_o = (datetime.date(datetime.strptime(x.pre_bayan,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.mani_date,'%Y-%m-%d'))).days
					else:
						r_o = ''
					worksheet.write_string (row, col+18,str(r_o),main_data)
					if x.pre_bayan and x.shipper_date:
						s_r = (datetime.date(datetime.strptime(x.pre_bayan,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.bayan_date,'%Y-%m-%d'))).days
					else:
						s_r = ''
					worksheet.write_string (row, col+19,str(s_r),main_data)
					worksheet.write_string (row, col+20,str(check_false(x.shutl_start_date)),main_data)
					worksheet.write_string (row, col+21,str(check_false(x.shutl_end_date)),main_data)
					worksheet.write_string (row, col+22,str(check_false(x.fin_bayan_date)),main_data)
					if x.fin_bayan_date and x.shutl_start_date:
						x_v = (datetime.date(datetime.strptime(x.fin_bayan_date,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.shutl_start_date,'%Y-%m-%d'))).days
					else:
						x_v = ''
					worksheet.write_string (row, col+23,str(x_v),main_data)
					worksheet.write_string (row, col+24,' ',main_data)
					worksheet.write_string (row, col+25,'N/A',main_data)
					worksheet.write_string (row, col+26,' - ',main_data)
					worksheet.write_string (row, col+27,' ',main_data)
					worksheet.write_string (row, col+28,' ',main_data)
					worksheet.write_string (row, col+29,str(check_false(x.status.comment)),main_data)
					worksheet.write_string (row, col+30,str(check_false(x.remarks)),main_data)
					worksheet.write_string (row, col+31,' ',main_data)

					row += 1
			
			elif ttype == 'import':
				for x in records:
					worksheet.write_string (row, col,str(check_false(x.s_no)),main_data)
					worksheet.write_string (row, col+1,str(check_false(x.job_no)),main_data)
					worksheet.write_string (row, col+2,str(check_false(x.customer.name)),main_data)
					worksheet.write_string (row, col+3,str(check_false(x.cust_ref_inv)),main_data)
					worksheet.write_string (row, col+4,str(check_false(x.shipper_date)),main_data)
					worksheet.write_string (row, col+5,str(check_false(x.bill_no)),main_data)
					worksheet.write_string (row, col+6,str(len(x.import_id)),main_data)
					worksheet.write_string (row, col+7,' ',main_data)
					worksheet.write_string (row, col+8,str(check_false(x.s_supplier.name)),main_data)
					worksheet.write_string (row, col+9,str(check_false(x.vessel_name)),main_data)
					worksheet.write_string (row, col+10,str(check_false(x.eta)),main_data)
					worksheet.write_string (row, col+11,str(check_false(x.etd)),main_data)
					if x.eta and x.shipper_date:
						k_e = (datetime.date(datetime.strptime(x.eta,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.shipper_date,'%Y-%m-%d'))).days
					else:
						k_e = ''
					worksheet.write_string (row, col+12,str(k_e),main_data)
					worksheet.write_string (row, col+13,' ',main_data)
					worksheet.write_string (row, col+14,str(check_false(x.bayan_no)),main_data)
					worksheet.write_string (row, col+15,str(check_false(x.rot_no)),main_data)
					worksheet.write_string (row, col+16,str(check_false(x.bayan_date)),main_data)
					worksheet.write_string (row, col+17,' ',main_data)
					worksheet.write_string (row, col+18,' ',main_data)
					worksheet.write_string (row, col+19,' ',main_data)
					worksheet.write_string (row, col+20,' ',main_data)
					worksheet.write_string (row, col+21,' ',main_data)
					worksheet.write_string (row, col+22,str(check_false(x.fin_bayan_date)),main_data)
					worksheet.write_string (row, col+23,' ',main_data)
					worksheet.write_string (row, col+24,' ',main_data)
					worksheet.write_string (row, col+25,'N/A',main_data)
					worksheet.write_string (row, col+26,' - ',main_data)
					worksheet.write_string (row, col+27,' ',main_data)
					worksheet.write_string (row, col+28,' ',main_data)
					worksheet.write_string (row, col+29,str(check_false(x.status.comment)),main_data)
					worksheet.write_string (row, col+30,str(check_false(x.remarks)),main_data)
					worksheet.write_string (row, col+31,' ',main_data)

					row += 1

		return {
			'type': 'ir.actions.act_url',
			'url': 'custom_logistic/static/src/lib/DAILY_SHIPMENT_STATUS_REPORT.xlsx',
			'target': 'blank',}
