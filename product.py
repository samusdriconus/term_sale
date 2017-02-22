#--*- coding:utf-8 -*-




from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import datetime
import time

import openerp.addons.decimal_precision as dp


#####################################
#product
#####################################



class product_template(osv.osv):
	"""product.product class inheritance for adding the functional
	field stock value"""

	def _get_stock_value(self,cr,uid,ids,field_name,arg,context=None):
		res = {}
		for prod in self.browse(cr,uid,ids,context):
			value = prod.qty_available * prod.standard_price
			res[prod.id] = value
		return res
	_inherit = 'product.template'
	_columns = {'value':fields.function(_get_stock_value,type='float',string='Stock en valeur'),
}



	_defaults = {
		'type' : 'product'
	}


product_template()

class product_product(osv.osv):
	"""product.product class inheritance for adding the functional
	field stock value"""

	def _get_stock_value(self,cr,uid,ids,field_name,arg,context=None):
		res = {}
		for prod in self.browse(cr,uid,ids,context):
			value = prod.qty_available * prod.standard_price
			res[prod.id] = value
		return res
	_inherit = 'product.product'
	_columns = {'value':fields.function(_get_stock_value,type='float',string='Stock en valeur'),
}


product_product()


class purchase_order(osv.osv):
	_inherit = 'purchase.order'


	def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, group_id, context=None):
		res = super(purchase_order,self)._prepare_order_line_move(cr,uid,order,order_line,picking_id,group_id,context)
		res[0]['unit_price'] = order_line.price_unit
		return res
		raise Exception(res)




