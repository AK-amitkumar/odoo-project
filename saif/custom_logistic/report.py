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
	b_name = fields.Many2one('by.customer',"By Customer")
	site = fields.Many2one(comodel_name="import.site", string="Site", required=True, )

	@api.onchange('total')
	def onchange_total(self):
		if self.total:
			self.s_date = self.e_date = ''

	@api.onchange('customer')
	def onchange_customer(self):
		if not self.customer.by_customer:
			self.b_name = ''

	@api.multi
	def print_report(self):
		if self.total:
			if self.ttype == 'export':
				data=self.env['export.logic'].search([('customer','=',self.customer.id),('by_customer','=',self.b_name.id),('site','=',self.site.id)])
				if data:
					return self.xlsx_report(data,ttype='export')
				else:
					raise  ValidationError('Report Does Not Exist According To Given Data')
			elif self.ttype == 'import':
				data=self.env['import.logic'].search([('customer','=',self.customer.id),('by_customer','=',self.b_name.id),('site','=',self.site.id)])
				if data:
					return self.xlsx_report(data,ttype='import')
				else:
					raise  ValidationError('Report Does Not Exist According To Given Data')
			else:
				raise  ValidationError('Report Does Not Exist According To Given Data')
		else:
			if self.ttype == 'export' and self.e_date and self.s_date:
				data=self.env['export.logic'].search([('customer','=',self.customer.id),('by_customer','=',self.b_name.id),('date','>=',self.s_date),('date','<=',self.e_date),('site','=',self.site.id)])
				if data:
					return self.xlsx_report(data,ttype='export')
				else:
					raise  ValidationError('Report Does Not Exist According To Given Data')

			elif self.ttype == 'import' and self.e_date and self.s_date:
				data=self.env['import.logic'].search([('customer','=',self.customer.id),('by_customer','=',self.b_name.id),('date','>=',self.s_date),('date','<=',self.e_date),('site','=',self.site.id)])
				if data:
					return self.xlsx_report(data,ttype='import')
				else:
					raise  ValidationError('Report Does Not Exist According To Given Data')
			else:
				raise  ValidationError('Report Does Not Exist According To Given Data')
	
	@api.multi
	def xlsx_report(self,input_records,ttype):
		with xlsxwriter.Workbook("/home/odoo/odoo-dev/odoo/custom-addons/custom_logistic/static/src/lib/SHIPMENT_STATUS_REPORT.xlsx") as workbook:
			main_heading = workbook.add_format({
				"bold": 1, 
				"border": 1,
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
				'font_size': '16',
				"font_color":'white',
				'fg_color': '7030a0'})
			
			main_data = workbook.add_format({
				"align": 'center',
				"valign": 'vcenter'

				})

			worksheet = workbook.add_worksheet(self.customer.name)

			for row in range(1, 2):
				worksheet.set_row(row, 30)
			worksheet.merge_range('A1:AJ2', 'SHIPMENT STATUS REPORT  {0} - {1}  {2}'.format(str(date.today())
																								  ,str(self.customer.name),
																								  str(self.b_name.name)),merge_format)

			worksheet.set_column('A3:AJ3', 20)

			worksheet.write('A3', 'SR. no.',main_heading)
			worksheet.write('B3', 'Our Job No',main_heading)
			worksheet.write('C3', 'Customer Name',main_heading)
			worksheet.write('D3', 'Order No.',main_heading) 
			worksheet.write('E3', 'Shipment Received Date',main_heading)
			worksheet.write('F3', 'B/L Number',main_heading)
			worksheet.merge_range('G3:H3', 'Number Of Containers',main_heading)
			worksheet.write('I3', 'Terminal',main_heading)
			worksheet.write('J3', 'Shipping Line',main_heading)
			worksheet.write('K3', 'Vessel Name',main_heading)
			worksheet.merge_range('L3:M3', 'ETA',main_heading)
			worksheet.write('N3', 'CC Days',main_heading)
			worksheet.write('O3', 'Manifest documents Received Date',main_heading)
			worksheet.write('P3', 'Bayan NO.',main_heading)
			worksheet.write('Q3', 'Rotation NO.',main_heading)
			worksheet.write('R3', 'Initial Bayan Date',main_heading)
			worksheet.write('S3', 'Pre-Bayan',main_heading)
			worksheet.write('T3', 'Manifest to Initial Bayan Printed',main_heading)
			worksheet.write('U3', 'Initial Bayan to Pre Bayan Printed',main_heading)
			worksheet.merge_range('V3:W3', 'Shuttling',main_heading)
			worksheet.write('X3', 'Final Bayan Date',main_heading)
			worksheet.write('Y3', 'Shuttle to final bayan',main_heading)
			worksheet.write('Z3', 'Random Inspection',main_heading)
			worksheet.write('AA3', 'Custom Exam Of Containers no.',main_heading)
			worksheet.write('AB3', 'New Seal no.',main_heading)
			worksheet.write('AC3', 'Load Permit Printed On',main_heading)
			worksheet.merge_range('AD3:AG3', 'Total Expenses',main_heading)
			worksheet.write('AH3', 'Status',main_heading)
			worksheet.write('AI3', 'Remarks',main_heading)
			worksheet.write('AJ3', 'Reason for the delay (Shutout) (If any)',main_heading)
			worksheet.write('A4', ' ',main_heading)
			worksheet.write('B4', ' ',main_heading)
			worksheet.write('C4', ' ',main_heading)
			worksheet.write('D4', ' ',main_heading)
			worksheet.write('E4', ' ',main_heading)
			worksheet.write('F4', ' ',main_heading)
			worksheet.write('G4', '20ft',main_heading)
			worksheet.write('H4', ' 40ft',main_heading)
			worksheet.write('I4', ' ',main_heading)
			worksheet.write('J4', ' ',main_heading)
			worksheet.write('K4', ' ',main_heading)
			worksheet.write('L4', 'On or About',main_heading)
			worksheet.write('M4', 'Revised ETA Date',main_heading)
			worksheet.write('N4', ' ',main_heading)
			worksheet.write('O4', ' ',main_heading)
			worksheet.write('P4', ' ',main_heading)
			worksheet.write('Q4', ' ',main_heading)
			worksheet.write('R4', ' ',main_heading)
			worksheet.write('S4', ' ',main_heading)
			worksheet.write('T4', ' ',main_heading)
			worksheet.write('U4', ' ',main_heading)
			worksheet.write('V4', 'Start Date',main_heading)
			worksheet.write('W4', 'End Date',main_heading)
			worksheet.write('X4', ' ',main_heading)
			worksheet.write('Y4', ' ',main_heading)
			worksheet.write('Z4', ' ',main_heading)
			worksheet.write('AA4', ' ',main_heading)
			worksheet.write('AB4', ' ',main_heading)
			worksheet.write('AC4', ' ',main_heading)
			worksheet.write('AD4', 'Custom Duty',main_heading)
			worksheet.write('AE4', 'Inspection',main_heading)
			worksheet.write('AF4', 'Container Seal',main_heading)
			worksheet.write('AG4', 'Total ',main_heading)
			worksheet.write('AH4', ' ',main_heading)
			worksheet.write('AI4', ' ',main_heading)
			worksheet.write('AJ4', ' ',main_heading)

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
					if x.export_id:
						worksheet.write_string (row, col,str(check_false(x.sr_no)),main_data)
						worksheet.write_string (row, col+1,str(check_false(x.our_job_no)),main_data)
						worksheet.write_string (row, col+2,str(check_false(x.customer.name)),main_data)
						worksheet.write_string (row, col+3,str(check_false(x.customer_ref)),main_data)
						worksheet.write_string (row, col+4,str(check_false(x.shipper_date)),main_data)
						worksheet.write_string (row, col+5,str(check_false(x.bill_no)),main_data)
						def ft20 (line):
							count = 0
							for x in line:
								if x.types == '20 ft':
									count = count + 1
							return count
						def ft40 (line):
							count = 0
							for x in line:
								if x.types == '40 ft':
									count = count + 1
							return count

						worksheet.write_string (row, col+6,str(check_false(ft20(x.export_id))),main_data)
						worksheet.write_string (row, col+7,str(check_false(ft40(x.export_id))),main_data)

						worksheet.write_string (row, col+8,' - ',main_data)
						worksheet.write_string (row, col+9,str(check_false(x.s_supplier.name)),main_data)
						worksheet.write_string (row, col+10,str(check_false(x.vessel_name)),main_data)
						worksheet.write_string (row, col+11,str(check_false(x.vessel_date)),main_data)
						worksheet.write_string (row, col+12,str(check_false(x.eta)),main_data)
						if x.vessel_date and x.shipper_date:
							k_e = (datetime.date(datetime.strptime(x.vessel_date,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.shipper_date,'%Y-%m-%d'))).days
						else:
							k_e = ''
						worksheet.write_string (row, col+13,str(k_e),main_data)
						worksheet.write_string (row, col+14,str(check_false(x.mani_date)),main_data)
						worksheet.write_string (row, col+15,str(check_false(x.bayan_no)),main_data)
						worksheet.write_string (row, col+16,str(check_false(x.rot_no)),main_data)
						worksheet.write_string (row, col+17,str(check_false(x.bayan_date)),main_data)
						worksheet.write_string (row, col+18,str(check_false(x.pre_bayan)),main_data)
						if x.pre_bayan and x.mani_date:
							r_o = (datetime.date(datetime.strptime(x.pre_bayan,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.mani_date,'%Y-%m-%d'))).days
						else:
							r_o = ''
						worksheet.write_string (row, col+19,str(r_o),main_data)
						if x.pre_bayan and x.shipper_date:
							s_r = (datetime.date(datetime.strptime(x.pre_bayan,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.bayan_date,'%Y-%m-%d'))).days
						else:
							s_r = ''
						worksheet.write_string (row, col+20,str(s_r),main_data)
						worksheet.write_string (row, col+21,str(check_false(x.shutl_start_date)),main_data)
						worksheet.write_string (row, col+22,str(check_false(x.shutl_end_date)),main_data)
						worksheet.write_string (row, col+23,str(check_false(x.fin_bayan_date)),main_data)
						if x.fin_bayan_date and x.shutl_start_date:
							x_v = (datetime.date(datetime.strptime(x.fin_bayan_date,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.shutl_start_date,'%Y-%m-%d'))).days
						else:
							x_v = ''
						worksheet.write_string (row, col+24,str(x_v),main_data)
						worksheet.write_string (row, col+25,' ',main_data)
						worksheet.write_string (row, col+26,'N/A',main_data)
						worksheet.write_string (row, col+27,' - ',main_data)
						worksheet.write_string (row, col+28,' ',main_data)
						for y in x.export_id:
							if x.custom_exam == True and  x.export_link:
								for z in x.export_link:
									if y.crt_no == z.container_no:
										worksheet.write_string (row, col+29,' N/A',main_data)
										worksheet.write_string (row, col+30,' N/A',main_data)
										worksheet.write_string (row, col+31,str(check_false(z.new_seal)),main_data)
										worksheet.write_string (row, col+32,str(check_false(z.amt_paid)),main_data)
						else:
							worksheet.write_string (row, col+29,' / ',main_data)
							worksheet.write_string (row, col+30,' / ',main_data)
							worksheet.write_string (row, col+31,' / ',main_data)
							worksheet.write_string (row, col+32,' / ',main_data)

						worksheet.write_string (row, col+33,str(check_false(x.status.comment)),main_data)
						worksheet.write_string (row, col+34,str(check_false(x.remarks)),main_data)
						worksheet.write_string (row, col+35,' ',main_data)

						row += 1
			
			elif ttype == 'import':
				for x in records:
					if x.import_id:
						worksheet.write_string (row, col,str(check_false(x.s_no)),main_data)
						worksheet.write_string (row, col+1,str(check_false(x.job_no)),main_data)
						worksheet.write_string (row, col+2,str(check_false(x.customer.name)),main_data)
						worksheet.write_string (row, col+3,str(check_false(x.cust_ref_inv)),main_data)
						worksheet.write_string (row, col+4,str(check_false(x.shipper_date)),main_data)
						worksheet.write_string (row, col+5,str(check_false(x.bill_no)),main_data)

						def ft20(line):
							count = 0
							for x in line:
								if x.types == '20 ft':
									count = count + 1
							return count

						def ft40(line):
							count = 0
							for x in line:
								if x.types == '40 ft':
									count = count + 1
							return count

						worksheet.write_string(row, col + 6, str(check_false(ft20(x.import_id))), main_data)
						worksheet.write_string(row, col + 7, str(check_false(ft40(x.import_id))), main_data)
						worksheet.write_string (row, col+8,' - ',main_data)
						worksheet.write_string (row, col+9,str(check_false(x.s_supplier.name)),main_data)
						worksheet.write_string (row, col+10,str(check_false(x.vessel_name)),main_data)
						worksheet.write_string (row, col+11,str(check_false(x.vessel_date)),main_data)
						worksheet.write_string (row, col+12,str(check_false(datetime.strptime(x.eta,'%d-%m-%Y'))),main_data)
						if x.vessel_date and x.shipper_date:
							k_e = (datetime.date(datetime.strptime(x.vessel_date,'%Y-%m-%d')) - datetime.date(datetime.strptime(x.shipper_date,'%Y-%m-%d'))).days
						else:
							k_e = ''
						worksheet.write_string (row, col+13,str(k_e),main_data)
						worksheet.write_string (row, col+14,' N/A',main_data)
						worksheet.write_string (row, col+15,str(check_false(x.bayan_no)),main_data)
						worksheet.write_string (row, col+16,str(check_false(x.rot_no)),main_data)
						worksheet.write_string (row, col+17,str(check_false(x.bayan_date)),main_data)
						worksheet.write_string (row, col+18,'N/A',main_data)
						worksheet.write_string (row, col+19,'N/A',main_data)
						worksheet.write_string (row, col+20,'N/A',main_data)
						worksheet.write_string (row, col+21,'N/A',main_data)
						worksheet.write_string (row, col+22,'N/A',main_data)
						worksheet.write_string (row, col+24,'N/A',main_data)
						worksheet.write_string (row, col+25,' ',main_data)
						worksheet.write_string (row, col+26,'N/A',main_data)
						worksheet.write_string (row, col+27,' - ',main_data)
						worksheet.write_string (row, col+28,' ',main_data)
						worksheet.write_string (row, col+29,'  ',main_data)
						worksheet.write_string (row, col+30,'  ',main_data)
						worksheet.write_string (row, col+31,'  ',main_data)
						worksheet.write_string (row, col+32,'  ',main_data)
						worksheet.write_string (row, col+33,str(check_false(x.status.comment)),main_data)
						worksheet.write_string (row, col+34,str(check_false(x.remarks)),main_data)
						worksheet.write_string (row, col+35,' ',main_data)

						row += 1

		return {
			'type': 'ir.actions.act_url',
			'url': 'custom_logistic/static/src/lib/SHIPMENT_STATUS_REPORT.xlsx',
			'target': 'blank',}
