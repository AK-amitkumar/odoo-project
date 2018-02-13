# -*- coding: utf-8 -*-
import xlsxwriter
import string
from datetime import date
from openerp import models, fields, api, http
from odoo.exceptions import Warning,ValidationError

class Police_Report(models.TransientModel):
    _name = 'police.report'
    _rec_name = 'today'

    today  = fields.Boolean(string="Today Date", required=False, default=True)
    from_date  = fields.Date(string="From Date", required=False, )
    to_date  = fields.Date(string="To Date", required=False, )
    today_date  = fields.Date(string="To Date", required=False,)
    case = fields.Many2one(comodel_name="case.level", string="Case", required=False, )
    @api.onchange('today')
    def onchange_method(self):
        if self.today:
            self.today_date = date.today()
            self.from_date = self.to_date = False

    def print_daily_report(self):
        if self.today:
            data = self.env['police.detail'].search(
                [('date', '=', self.today_date)])
            if data:
                return self.xlsx_report(data, self.today, self.from_date, self.to_date, self.today_date)
            else:
                raise ValidationError('Report Does Not Exist According To Given Dates')

        if not self.today:
            data = self.env['police.detail'].search([('date','>=',self.from_date),('date','<=',self.to_date)])
            if data:
                return self.xlsx_report(data,self.today,self.from_date,self.to_date,self.today_date)
            else:
                raise ValidationError('Report Does Not Exist According To Given Dates')

    def xlsx_report(self ,data,today,from_date,to_date,today_date):
        with xlsxwriter.Workbook(
                "/home/muhammad/odoo-dev/Projects/police/police_project/static/src/lib/Daily Report.xlsx") as workbook:
            main_heading = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                "font_size": '15',
                # 'border':   6,

            })
            main_data = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                'font_size': '11',
            })
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '13',
                "font_color": 'black',
                'fg_color': 'd0e5fc'})
            worksheet = workbook.add_worksheet('Testing')
            worksheet.set_column('A3:A3', 3,)
            worksheet.set_column('B3:E3', 12,)
            worksheet.set_column('H3:H3', 12,)
            worksheet.set_column('F3:G3', 16,)
            worksheet.set_column('I3:I3', 22,)
            worksheet.set_row(2, 40, main_heading)
            worksheet.right_to_left()
            merge_format.set_shrink()
            main_heading.set_text_justlast(1)
            main_data.set_border()
            if not today:
                for row in range(1, 2):
                    worksheet.set_row(row, 20)
                worksheet.merge_range('A1:I2', 'Daily Report  From {0}  - To {1}'.format(str(from_date)
                                                                                         ,str(to_date)), merge_format)
            if today:
                for row in range(1, 2):
                    worksheet.set_row(row, 20)
                worksheet.merge_range('A1:I2', 'Daily Report  For {0}'.format(str(today_date)),
                                      merge_format)
            worksheet.write('A3', '#'.decode('utf-8'), main_heading)
            worksheet.write('B3', 'المركز'.decode('utf-8'), main_heading)
            worksheet.write('C3', 'الحالة'.decode('utf-8'), main_heading)
            worksheet.write('D3', 'نوع الحالة'.decode('utf-8'), main_heading)
            worksheet.write('E3', 'تفاصيل'.decode('utf-8'), main_heading)
            worksheet.write('F3', 'تفاصيل اكثر'.decode('utf-8'), main_heading)
            worksheet.write('G3', 'الوقت'.decode('utf-8'), main_heading)
            worksheet.write('H3', 'الموقع'.decode('utf-8'), main_heading)
            worksheet.write('I3', 'ملخص الحالة'.decode('utf-8'), main_heading)
            row = 4
            col = 0

            def check_false(input_data):
                if input_data:
                    return input_data
                else:
                    return ' '
            i = 1
            for x in data:
                for y in x.case_type:
                    worksheet.write_string(row, col, str(i), main_data)
                    worksheet.write_string(row, col + 1, check_false(x.center_name.name), main_data)
                    worksheet.write_string(row, col + 2, check_false(y.main_case.name), main_data)
                    worksheet.write_string(row, col + 3, check_false(y.case_type.name), main_data)
                    worksheet.write_string(row, col + 4, check_false(y.cate_case.name), main_data)
                    worksheet.write_string(row, col + 5, check_false(y.sub_cate_case.name), main_data)
                    worksheet.write_string(row, col + 6, check_false(x.time), main_data)
                    worksheet.write_string(row, col + 7, check_false(x.location_name.name), main_data)
                    worksheet.write_string(row, col + 8, 'N/A', main_data)
                    row += 1
                    i += 1

        return {
            'type': 'ir.actions.act_url',
            'url': 'police_project/static/src/lib/Daily Report.xlsx',
            'target': 'blank', }

    def Test_Report(self):
        rec = self.env['case.level'].search([('id', '=', self.case.id)])
        road = self.env['road.name'].search([])
        case_data = self.env['case.type'].search([('main_case','=', self.case.id)])

        with xlsxwriter.Workbook(
                "/home/muhammad/odoo-dev/Projects/police/police_project/static/src/lib/Test Report.xlsx") as workbook:
            main_heading = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                "font_size": '15',
                'fg_color': 'dbeef4'
            })
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '13',
                "font_color": 'black',
                'fg_color': 'dbeef4'})
            merge_format1 = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '13',
                "font_color": 'black',
                'fg_color': 'd0e5fc'})

            main_data = workbook.add_format({
                "align": 'right',
                'font_size': '16',
                'bold': 1,
            })

            add_data = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '9',
                'fg_color': 'd0e5fc',
                'bold': 1,
            })
            worksheet = workbook.add_worksheet('Testing')
            worksheet.set_column('A3:A3', 12, )
            worksheet.set_column('B3:B3', 12, )
            worksheet.right_to_left()
            main_heading.set_border()
            add_data.set_border()
            def check_false(input_data):
                if input_data:
                    return input_data
                else:
                    return ' '

            rRow = 5
            rCol = 1
            rLast = 6
            row = 5
            col = 2
            center_list = []
            for x in road:
                for r in x.road_tree:
                    worksheet.write_string(rRow, rCol, check_false(r.center.name), main_heading)
                    rRow += 1
                    case_data = self.env['police.detail'].search([('center_name', '=', r.center.id),])
                    center_list.append(case_data)
            # case_count = 0
            # for xx in case_data:
            #        for z in xx.case_type:
            #             for y in rec.tree_link:
            #                 if z.case_type == y.case_type:
            #                     case_count += 1
            # worksheet.write_string(row, col, check_false(str(case_count)), main_heading)
            # col +=1
            # print "11111111111111111111111111111111111111"
            # print case_count
                rRange = 'A' + str(rLast) + ':' + 'A' + str(rRow)
                worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(x.name),
                                      merge_format)
                rLast = rRow + 1
            print "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
            print center_list

            row = 4
            col = 2
            last = 2

            worksheet.merge_range('A3:A5', 'قيادات الطرق'.decode('utf-8'), merge_format1)
            worksheet.merge_range('B3:B5', 'المراكز'.decode('utf-8'), merge_format1)
            for x in rec.tree_link:
                for y in x.case_level_cate:
                    worksheet.write_string(row, col, check_false(y.case_cate.name), main_heading)
                    # worksheet.write_string(row, col +1, check_false(y.case_cate.name), main_heading)
                    col += 1

                    # for c_name in center_list[0]:
                    #     count = 0
                    #     for case_tree in c_name.case_type:
                    #         if y.case_cate == case_tree.case_cate:
                    #             count += 1


                for abc in range(1, 2):
                    worksheet.set_row(abc, 20)
                    rRange = string.ascii_uppercase[last] + '3:' + string.ascii_uppercase[col - 1] + '4'
                    worksheet.merge_range(rRange,'{0}'.decode('utf-8').format(x.case_type.name),
                                          merge_format)
                    last = col
            for abc in range(0, 1):
                worksheet.set_row(abc, 20)
                rRange = 'A1:' + string.ascii_uppercase[col] + '2'
                worksheet.merge_range(rRange, '{0}__________'.decode('utf-8').format(rec.case.name),main_data)
                rRange = string.ascii_uppercase[last]+'3:' + string.ascii_uppercase[col] + '4'
                worksheet.merge_range(rRange, rec.case.name+'إجمالي'.decode('utf-8'),add_data)
                worksheet.write_string(4, col,'دوريات'.decode('utf-8'), add_data)


