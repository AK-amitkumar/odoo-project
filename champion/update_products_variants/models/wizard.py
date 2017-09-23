# -*- coding: utf-8 -*-

from odoo import models, fields, api

class wizard_products_variants(models.Model):
	_name = 'wizard.products.variants'
	@api.multi
	def setAllProductVariants(self):
		Products = self.env['product.template'].search([])
		for prod in Products:
			ProductVariants = self.env['product.product'].search([('product_tmpl_id','=',prod.id)])
			template_attr_id = 0
			for variant in ProductVariants:
				if variant.attribute_value_ids:
					for line in variant.attribute_value_ids:
						if template_attr_id != line.attribute_id.id:
							previous_line_ids = prod.attribute_line_ids.search([('product_tmpl_id','=',prod.id),('attribute_id','=',line.attribute_id.id)])
							if not previous_line_ids:
								new_product = prod.attribute_line_ids.create({
									'product_tmpl_id': prod.id,
									'attribute_id':line.attribute_id.id,
								})
								template_attr_id = line.attribute_id.id
			self.update_variants_values(prod)
			print self.update_variants_values(prod)


	def update_variants_values(self, product):
		ProductVariants = self.env['product.product'].search([('product_tmpl_id','=',product.id)])
		variants_id = []
		for variants in ProductVariants:
			if variants.attribute_value_ids:
				print variants.attribute_value_ids
				variants_id.append(variants.attribute_value_ids.id)
		if variants_id:
			product.attribute_line_ids.value_ids = variants_id