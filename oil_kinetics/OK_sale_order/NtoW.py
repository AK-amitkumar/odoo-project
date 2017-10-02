from openerp import models, fields, api
from datetime import date
from num2words import num2words

class Num2Words(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def convert_amount(self):
        word = num2words(self.amount_total)
        word = word.title() + " " + "Only"
        return word