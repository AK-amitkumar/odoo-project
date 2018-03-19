# -*- encoding: utf-8 -*-
import xlwt
from odoo.report import report_sxw
from odoo.addons.report_xls.report_xls import report_xls
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class BomStructure(report_xls):
	pass
#     def get_children(self, object, level=0):
#         result = []

#         def _get_rec(object, level):
#             for l in object:
#                 res = {}
#                 res['pname'] = l.product_id.name
#                 res['pcode'] = l.product_id.default_code
#                 res['pqty'] = l.product_qty
#                 res['uname'] = l.product_uom.name
#                 res['level'] = level
#                 res['code'] = l.bom_id.code
#                 res['cost'] = l.product_standard_price
#                 res['total'] = l.total_cost
#                 result.append(res)
#                 if l.child_line_ids:
#                     res['cost'] = False
#                     res['total'] = False
#                     if level < 6:
#                         level += 1
#                     _get_rec(l.child_line_ids, level)
#                     if level > 0 and level < 6:
#                         level -= 1
#             return result

#         children = _get_rec(object, level)

#         return children

#     def generate_xls_report(self, _p, _xs, data, objects, wb):
#         report_name = _('Bom Structure')
#         ws = wb.add_sheet(report_name[:31])
#         ws.panes_frozen = True
#         ws.remove_splits = True
#         ws.portrait = 0
#         ws.fit_width_to_pages = 1
#         row_pos = 0
#         ws.header_str = self.xls_headers['standard']
#         ws.footer_str = self.xls_footers['standard']
#         cell_style = xlwt.easyxf(_xs['xls_title'])
#         c_specs = [
#             ('report_name', 1, 2, 'text', report_name),
#         ]
#         row_data = self.xls_row_template(c_specs, ['report_name'])
#         row_pos = self.xls_write_row(
#             ws, row_pos, row_data, row_style=cell_style)
#         row_pos += 1
#         rh_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
#         rh_cell_style_right = xlwt.easyxf(rh_cell_format + _xs['left'])
#         c_specs = [
#             ('name', 1, 45, 'text', _('BOM Name')),
#             ('ref', 1, 25, 'text', _('BOM Ref')),
#             ('qty', 1, 18, 'text', _('Quantity')),
#             ('unit_price', 1, 18, 'text', _('Unit Price')),
#             ('total', 1, 18, 'text', _('Total')),
#         ]
#         row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
#         row_pos = self.xls_write_row(
#             ws, row_pos, row_data, row_style=rh_cell_style_right,
#             set_column_size=True)
#         ws.set_horz_split_pos(row_pos)
#         absl_cell_format = _xs['borders_all']
#         absl_cell_style_decimal1 = xlwt.easyxf(
#             absl_cell_format + _xs['left'] + _xs['bold'] + _xs['fill'] + _xs['borders_all'],
#             num_format_str=report_xls.decimal_format)
#         absl_cell_style_decimal = xlwt.easyxf(
#             absl_cell_format + _xs['left'],
#             num_format_str=report_xls.decimal_format)
#         ctotal = 0
#         for record in objects:
#             c_specs = [
#                 ('name', 1, 0, 'text', record.product_tmpl_id.name),
#                 ('ref', 1, 0, 'text', record.code),
#                 ('qty', 1, 0, 'number', record.product_qty),
#             ]
#             row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
#             row_pos = self.xls_write_row(
#                 ws, row_pos, row_data, row_style=absl_cell_style_decimal)
#             for line in self.get_children(record.bom_line_ids):
#                 spaces = "   " * (line['level'] + 3)
#                 c_specs = [
#                     ('name', 1, 1, 'text', spaces + line['pname']),
#                     ('ref', 1, 1, 'text', record.code),
#                     ('qty', 1, 1, 'number', line['pqty']),
#                     ('unit_price', 1, 1, 'number', line['cost']),
#                     ('total', 1, 1, 'number', line['total'])
#                 ]
#                 ctotal += line['total']
#                 row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
#                 row_pos = self.xls_write_row(
#                     ws, row_pos, row_data, row_style=absl_cell_style_decimal)
#         c_specs = [
#             ('total1', 1, 1, 'text', "Total"),
#             ('total2', 1, 1, 'text', " "),
#             ('total3', 1, 1, 'text', " "),
#             ('total3', 1, 1, 'text', " "),
#             ('total4', 1, 1, 'number', ctotal),
#         ]
#         row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
#         self.xls_write_row(
#             ws, row_pos, row_data, row_style=absl_cell_style_decimal1)


BomStructure(
    'report.mrp.bom.list.xls',
    'mrp.bom',
    parser=report_sxw.rml_parse)
