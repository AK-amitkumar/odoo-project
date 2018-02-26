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
    case1 = fields.Many2one(comodel_name="case.level", string="Case", required=False, )
    case2 = fields.Many2one(comodel_name="case.level", string="Case", required=False, )
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
                'font_size': '15',
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
                "/home/muhammad/odoo-dev/Projects/police/police_project/static/src/lib/Case Report.xlsx") as workbook:
            main_heading = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                "font_size": '15',
                'fg_color': 'dbeef4'
            })

            main_heading1 = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                "font_size": '15',
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
                'font_size': '12',
                'fg_color': 'd0e5fc',
                'bold': 1,
            })
            worksheet = workbook.add_worksheet('تقرير الحالة الجنائية'.decode('utf-8'))
            worksheet.set_column('A3:A3', 12, )
            worksheet.set_column('B3:B3', 12, )
            worksheet.right_to_left()
            main_heading.set_border()
            main_heading1.set_border()
            add_data.set_border()
            worksheet.set_row(0, 30, merge_format1)

            def check_false(input_data):
                if input_data:
                    return input_data
                else:
                    return ' '

            row = 4
            col = 2
            last = 2

            worksheet.merge_range('A3:A5', 'قيادات الطرق'.decode('utf-8'), merge_format1)
            worksheet.merge_range('B3:B5', 'المراكز'.decode('utf-8'), merge_format1)
            for x in rec.tree_link:
                for y in x.case_level_cate:
                    worksheet.write_string(row, col, check_false(y.case_cate.name), main_heading)
                    col += 1
                    rRange = string.ascii_uppercase[row] + '4:' + string.ascii_uppercase[col - 1] + '5'
                    worksheet.set_column(rRange, 15)

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
                rRange = string.ascii_uppercase[last]+'3:' + string.ascii_uppercase[col] + '5'
                worksheet.set_column(rRange, 25)
                worksheet.merge_range(rRange, rec.case.name+' إجمالي '.decode('utf-8'),add_data)

            rRow = 5
            rCol = 1
            rLast = 6
            row = 5
            col = 2
            sum_count = 0
            for x in road:
                for r in x.road_tree:
                    worksheet.write_string(rRow, rCol, check_false(r.center.name), main_heading)
                    rRow += 1
                    case_data = self.env['police.detail'].search([('center_name', '=', r.center.id)])
                    for case_id in self.case.tree_link:
                        for sub_id in case_id.case_level_cate:
                            count = 0
                            for line in case_data:
                                for case_cate in line.case_type:
                                    if sub_id.case_cate.id == case_cate.cate_case.id:
                                        count += 1

                                for line1 in line:
                                    for sub_line in line1.party_link:
                                        if sub_line.companion_detail and sub_line.companion_detail_link:
                                            for sub_party in sub_line.companion_detail_link:
                                                if sub_party.case_detail and sub_party.case_type_link:
                                                    for case_count in sub_party.case_type_link:
                                                        if sub_id.case_cate.id == case_count.cate_case.id:
                                                            count += 1

                            sum_count +=count
                            if count == 0:
                                worksheet.write_string(row, col, check_false(str(" ")), main_heading1)
                            else:
                                worksheet.write_string(row, col, check_false(str(count)), main_heading1)

                            col +=1
                            if sum_count == 0:
                                worksheet.write_string(row, col, check_false(str(" ")), main_heading)
                            else:
                                worksheet.write_string(row, col, check_false(str(sum_count)), main_heading)
                    row +=1
                    col = 2
                    sum_count = 0

                rRange = 'A' + str(rLast) + ':' + 'A' + str(rRow)
                worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(x.name),
                                      merge_format)
                rLast = rRow + 1
        return {
            'type': 'ir.actions.act_url',
            'url': 'police_project/static/src/lib/Case Report.xlsx',
            'target': 'blank', }

    def Test1_Report(self):
        rec = self.env['case.level'].search([('id', '=', self.case1.id)])
        road = self.env['road.name'].search([])

        with xlsxwriter.Workbook(
                "/home/muhammad/odoo-dev/Projects/police/police_project/static/src/lib/Case1 Report.xlsx") as workbook:
            main_heading = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                "font_size": '15',
                'fg_color': 'dbeef4'
            })

            main_heading1 = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                "font_size": '15',
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
                'font_size': '12',
                'fg_color': 'd0e5fc',
                'bold': 1,
            })
            worksheet = workbook.add_worksheet('تقرير عن مخالفات نظام الإقامة والعمل / وغيرها من المخالفات'.decode('utf-8'))
            worksheet.set_column('A3:A3', 12, )
            worksheet.set_column('B3:B3', 12, )
            worksheet.right_to_left()
            main_heading.set_border()
            main_heading1.set_border()
            add_data.set_border()
            worksheet.set_row(0, 30, merge_format1)

            def check_false(input_data):
                if input_data:
                    return input_data
                else:
                    return ' '

            row = 5
            col = 2
            last = 2
            l_last = 2

            worksheet.merge_range('A3:A6', 'قيادات الطرق'.decode('utf-8'), merge_format1)
            worksheet.merge_range('B3:B6', 'المراكز'.decode('utf-8'), merge_format1)
            for x in rec.tree_link:
                for y in x.case_level_cate:
                    for z in range(2):
                        if z == 0:
                            worksheet.write_string(row, col, 'حالات'.decode('utf-8'), add_data)
                        else:
                            worksheet.write_string(row, col, 'اشخاص'.decode('utf-8'), add_data)
                        col += 1
                    for abc in range(1, 2):
                        worksheet.set_row(abc, 20)
                        if col > 25 and last > 25:
                            rRange = "A"+string.ascii_uppercase[last-26] + '5:' + "A"+string.ascii_uppercase[((col-1)-26)]+ '5'
                            worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(y.case_cate.name),
                                                  merge_format)
                            last = col
                        elif col > 25 > last:
                            rRange = string.ascii_uppercase[last] + '5:' + string.ascii_uppercase[
                                (col -1)] + '5'
                            worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(y.case_cate.name),
                                                  merge_format)
                            last = col

                        elif col < 25 < last:
                            rRange = "A"+string.ascii_uppercase[last-25] + '5:' + string.ascii_uppercase[
                                (col -1)] + '5'
                            worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(y.case_cate.name),
                                                  merge_format)
                            last = col
                        else:
                            rRange = string.ascii_uppercase[last] + '5:' + string.ascii_uppercase[col - 1] + '5'
                            worksheet.merge_range(rRange,'{0}'.decode('utf-8').format(y.case_cate.name),
                                                  merge_format)
                            last = col


                for abc in range(1, 2):
                    worksheet.set_row(abc, 20)
                    if col >25:
                        rRange = string.ascii_uppercase[l_last] + '3:' + "A"+string.ascii_uppercase[(col -2) -25] + '4'
                        worksheet.merge_range(rRange,'{0}'.decode('utf-8').format(x.case_type.name),
                                              merge_format)
                        l_last = col
                    else:
                        rRange = string.ascii_uppercase[l_last] + '3:' + string.ascii_uppercase[col - 1] + '4'
                        worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(x.case_type.name),
                                              merge_format)
                        l_last = col

            for abc in range(0, 1):
                worksheet.set_row(abc, 20)
                if col > 25:
                    rRange = 'A1:' + "A"+string.ascii_uppercase[col-25] + '2'
                    worksheet.merge_range(rRange, '{0}__________'.decode('utf-8').format(rec.case.name),main_data)
                else:
                    rRange = 'A1:' + string.ascii_uppercase[col] + '2'
                    worksheet.merge_range(rRange, '{0}__________'.decode('utf-8').format(rec.case.name), main_data)

                if col > 25:
                    rRange = "A"+string.ascii_uppercase[last-25]+'3:' + "A"+string.ascii_uppercase[col-26] + '5'
                    worksheet.set_column(rRange, 15)
                    worksheet.merge_range(rRange, rec.case.name+' إجمالي '.decode('utf-8'),add_data)
                    for z in range(2):
                        if z == 0:
                            worksheet.write_string(row, col, 'حالات'.decode('utf-8'), add_data)
                        else:
                            worksheet.write_string(row, col, 'اشخاص'.decode('utf-8'), add_data)
                        col += 1
                else:
                    rRange = string.ascii_uppercase[last] + '3:' + string.ascii_uppercase[col] + '5'
                    worksheet.set_column(rRange, 15)
                    worksheet.merge_range(rRange, rec.case.name + ' إجمالي '.decode('utf-8'), add_data)
                    for z in range(2):
                        if z == 0:
                            worksheet.write_string(row, col, 'حالات'.decode('utf-8'), add_data)
                        else:
                            worksheet.write_string(row, col, 'اشخاص'.decode('utf-8'), add_data)
                        col += 1

            rRow = 6
            rCol = 1
            rLast = 7
            row = 6
            col = 2
            sum_count = 0
            a_sum_count = 0
            for x in road:
                for r in x.road_tree:
                    worksheet.write_string(rRow, rCol, check_false(r.center.name), main_heading)
                    rRow += 1

                    case_data = self.env['police.detail'].search([('center_name', '=', r.center.id)])
                    for case_id in self.case1.tree_link:
                        for sub_id in case_id.case_level_cate:
                            count = 0
                            a_count = 0
                            for line in case_data:
                                for case_cate in line.case_type:
                                    if sub_id.case_cate.id == case_cate.cate_case.id:
                                        count += 1

                                for line1 in line:
                                    for sub_line in line1.party_link:
                                        if sub_line.companion_detail and sub_line.companion_detail_link:
                                            for sub_party in sub_line.companion_detail_link:
                                                if sub_party.case_detail and sub_party.case_type_link:
                                                    for case_count in sub_party.case_type_link:
                                                        if sub_id.case_cate.id == case_count.cate_case.id:
                                                            a_count += 1
                            
                            if count == 0:
                                worksheet.write_string(row, col, check_false(str(" ")), main_heading1)
                            else:
                                worksheet.write_string(row, col, check_false(str(count)), main_heading1)
                            col += 1

                            if a_count == 0:
                                worksheet.write_string(row, col, check_false(str(" ")), main_heading1)
                            else:
                                worksheet.write_string(row, col, check_false(str(a_count)), main_heading1)
                            col +=1
                            sum_count +=count
                            a_sum_count +=a_count
                    if sum_count == 0:
                        worksheet.write_string(row, col, check_false(str(" ")), main_heading)
                    else:
                        worksheet.write_string(row, col, check_false(str(sum_count)), main_heading)
                    col +=1

                    if a_sum_count == 0:
                        worksheet.write_string(row, col, check_false(str(" ")), main_heading)
                    else:
                        worksheet.write_string(row, col, check_false(str(a_sum_count)), main_heading)

                    row +=1
                    col = 2
                    sum_count = 0
                    a_sum_count = 0

                rRange = 'A' + str(rLast) + ':' + 'A' + str(rRow)
                worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(x.name),
                                      merge_format)
                rLast = rRow + 1
        return {
            'type': 'ir.actions.act_url',
            'url': 'police_project/static/src/lib/Case1 Report.xlsx',
            'target': 'blank', }

    def Test2_Report(self):
        rec = self.env['case.level'].search([('id', '=', 3)])
        road = self.env['road.name'].search([])

        with xlsxwriter.Workbook(
                "/home/muhammad/odoo-dev/Projects/police/police_project/static/src/lib/Case3 Report.xlsx") as workbook:
            main_heading = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                "font_size": '15',
                'fg_color': 'dbeef4'
            })

            main_heading1 = workbook.add_format({
                "align": 'center',
                "valign": 'vcenter',
                "font_size": '15',
            })
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '13',
                "font_color": 'black',
                'fg_color': 'dcdcf8'})
            merge_format1 = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '13',
                "font_color": 'black',
                'fg_color': 'dcdcf8'})

            main_data = workbook.add_format({
                "align": 'right',
                'font_size': '16',
                'bold': 1,
            })

            add_data = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'fg_color': 'd0e5fc',
                'bold': 1,
            })
            worksheet = workbook.add_worksheet('بيان يمثل حالات المخدرات المضبوطة وكمياتها'.decode('utf-8'))
            worksheet.set_column('A3:A3', 12, )
            worksheet.set_column('B3:B3', 12, )
            worksheet.right_to_left()
            main_heading.set_border()
            main_heading1.set_border()
            add_data.set_border()
            worksheet.set_row(0, 30, merge_format1)

            def check_false(input_data):
                if input_data:
                    return input_data
                else:
                    return ' '

            row = 5
            col = 3
            last =3

            worksheet.merge_range('A3:A6', 'قيادات الطرق'.decode('utf-8'), merge_format1)
            worksheet.merge_range('B3:B6', 'المراكز'.decode('utf-8'), merge_format1)
            worksheet.merge_range('C3:C6', 'عدد حالات المخدرات'.decode('utf-8'), merge_format1)
            for x in rec.tree_link:
                if 'حبوب'.decode('utf-8') not in x.case_type.name and 'اخرى'.decode('utf-8') not in x.case_type.name:
                    for z in range(2):
                        if z == 0:
                            worksheet.write_string(row, col, 'جرام'.decode('utf-8'), add_data)
                        else:
                            worksheet.write_string(row, col, 'كيلو'.decode('utf-8'), add_data)
                        col += 1
                elif 'حبوب'.decode('utf-8') in x.case_type.name:
                    for abc in range(0, 1):
                        worksheet.write_string(row, col, 'بالعدد'.decode('utf-8'), add_data)
                        col += 1
                elif 'اخرى'.decode('utf-8') in x.case_type.name:
                    for z in range(2):
                        if z == 0:
                            worksheet.write_string(row, col, 'بالجرام'.decode('utf-8'), add_data)
                        else:
                            worksheet.write_string(row, col, 'بالعدد'.decode('utf-8'), add_data)
                        col += 1

                for abc in range(1, 2):
                    worksheet.set_row(abc, 20)
                    rRange = string.ascii_uppercase[last] + '4:' + string.ascii_uppercase[col - 1] + '5'
                    worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(x.case_type.name),
                                          merge_format)
                    last = col

            for abc in range(0, 1):
                worksheet.set_row(abc, 20)
                rRange = 'D3:' + string.ascii_uppercase[col - 1] + '3'
                worksheet.merge_range(rRange, 'أنواع وكميات المخدرات المضبوطة'.decode('utf-8'),merge_format)

            for abc in range(0, 1):
                worksheet.set_row(abc, 20)
                rRange = 'A1:' + string.ascii_uppercase[col -1] + '1'
                worksheet.merge_range(rRange, '{0}__________'.decode('utf-8').format(rec.case.name), main_data)

            for abc in range(0, 1):
                worksheet.set_row(abc, 20)
                rRange = 'A2:' + string.ascii_uppercase[col -1] + '2'
                worksheet.merge_range(rRange, 'بيان يمثل حالات المخدرات المضبوطة وكمياتها'.decode('utf-8'), main_data)

            rRow = 6
            rCol = 1
            rLast = 7
            sum_count = 0

            for x in road:
                for r in x.road_tree:
                    count = 0
                    worksheet.write_string(rRow, rCol, check_false(r.center.name), main_heading)
                    rRow += 1
                    case_data = self.env['police.detail'].search([('center_name', '=', r.center.id)])
                    for case_id in self.case2.tree_link:
                        for line in case_data:
                            for case_cate in line.case_type:
                                if case_id.case_type.id == case_cate.main_case.id:
                                    count += 1
                            for line1 in line:
                                for sub_line in line1.party_link:
                                    if sub_line.companion_detail and sub_line.companion_detail_link:
                                        for sub_party in sub_line.companion_detail_link:
                                            if sub_party.case_detail and sub_party.case_type_link:
                                                for case_count in sub_party.case_type_link:
                                                    if case_id.case_type.id == case_count.main_case.id:
                                                        count += 1

                    if count == 0:
                        worksheet.write_string(rRow-1, rCol+1, check_false(str(" ")), main_heading1)
                    else:
                        worksheet.write_string(rRow-1, rCol+1, check_false(str(count)), main_heading1)
                        sum_count += count

                if sum_count == 0:
                    worksheet.write_string(rRow, rCol+1, check_false(str(" ")), main_heading)
                else:
                    worksheet.write_string(rRow, rCol+1, check_false(str(sum_count)), main_heading)

                rRange = 'A' + str(rLast) + ':' + 'A' + str(rRow)
                worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(x.name),
                                      merge_format)
                rLast = rRow + 1

                for abc in range(0, 1):
                    worksheet.set_row(abc, 20)
                    rRange = 'A' + str(rLast) + ':' + 'B' + str(rLast)
                    worksheet.merge_range(rRange, 'المجموع'.decode('utf-8'), merge_format)

            row = 6
            col = 3
            for xx in road:
                for yy in xx.road_tree:
                    case_data = self.env['police.detail'].search([('center_name', '=', yy.center.id)])
                    for zz in rec.tree_link:
                        g_count = 0
                        k_count = 0
                        p_count = 0
                        for xxx in case_data:
                            if xxx.case_type:
                                for xxxx in xxx.case_type:
                                    for sub_line in xxx.party_link:
                                        if sub_line.what_found.id == xxxx.case_type.id and sub_line.what_found.id == zz.case_type.id:
                                            if sub_line.qty_uom == 'g':
                                                g_count += sub_line.qty
                                            elif sub_line.qty_uom == 'k':
                                                k_count += sub_line.qty
                                            else:
                                                p_count += sub_line.qty
                            if xxx.party_link:
                                for sub_line in xxx.party_link:
                                    if sub_line.companion_detail == True and sub_line.companion_detail_link:
                                        for sub_party in sub_line.companion_detail_link:
                                            if sub_party.what_found.id == zz.case_type.id:
                                                if sub_party.qty_uom == 'g':
                                                    g_count += sub_party.qty
                                                if sub_party.qty_uom == 'k':
                                                    k_count += sub_party.qty
                                                if sub_party.qty_uom == 'p':
                                                    p_count += sub_party.qty
                        if g_count == 0:
                            worksheet.write_string(row, col, check_false(str(" ")), main_heading)
                        else:
                            worksheet.write_string(row, col, check_false(str(g_count)), main_heading)
                        col += 1

                        if k_count == 0:
                            worksheet.write_string(row, col, check_false(str(" ")), main_heading)
                        else:
                            worksheet.write_string(row, col, check_false(str(k_count)), main_heading)
                        col += 1

                        if g_count > 0:
                            print "GGGGGGGGGGGGGGGGGGGGGGG" + str(g_count)
                        if k_count > 0:
                            print "KKKKKKKKKKKKKKKKKKKKKKK" + str(k_count)
                        if p_count > 0:
                            print "PPPPPPPPPPPPPPPPPPPPPPP" + str(p_count)
                    row += 1
                    break


                # for case_id2 in self.case2.tree_link:
                #     for line2 in case_data:
                #         gram_count = 0
                #         kg_count = 0
                #         for rec in line2.police_rec:
                #             for line1 in line2:
                #                 for sub_line in line1.party_link:
                #                     if sub_line.qty_uom == 'g':
                #                         gram_count += gram_count
                #                     if sub_line.qty_uom == 'k':
                #                         kg_count += kg_count
                #         print "GGGGGGGGGGGRRRRRRRRRRRMMMMMMMMMM" + str(gram_count)
                #         print "KKKKKKKKKKKKKKKKKGGGGGGGGGGGGGGG" + str(gram_count)


                                # if sub_line.companion_detail and sub_line.companion_detail_link:
                                #     for sub_party in sub_line.companion_detail_link:
                                #         if sub_party.case_detail and sub_party.case_type_link:
                                #             for case_count in sub_party.case_type_link:
                                #                 if case_id.case_type.id == case_count.main_case.id:
                                #                     count += 1

                # gram_count = 0
                # for xx in rec_list:
                #     for yy in  xx.party_link:
                #         if yy.qty_uom == 'g':
                #             gram_count += yy.qty
                # print "GGGGGGGGGGGRRRRRRRRRRRMMMMMMMMMM" + str(gram_count)

                # rRange = 'A' + str(rLast) + ':' + 'A' + str(rRow)
                # worksheet.merge_range(rRange, '{0}'.decode('utf-8').format(x.name),
                #                       merge_format)
                # rLast = rRow + 1
            # for abc in range(0, 1):
            #     worksheet.set_row(abc, 20)
            #     rRange = 'A'+ str(rLast) +':'  + 'B' + str(rLast)
            #     worksheet.merge_range(rRange, 'الدوريات السرية'.decode('utf-8'),merge_format)

            # for abc in range(0, 1):
            #     worksheet.set_row(abc, 20)
            #     rRange = 'A' + str(rLast) + ':' + 'B' + str(rLast)
            #     worksheet.merge_range(rRange, 'المجموع'.decode('utf-8'),merge_format)
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': 'police_project/static/src/lib/Case Report.xlsx',
        #     'target': 'blank', }
