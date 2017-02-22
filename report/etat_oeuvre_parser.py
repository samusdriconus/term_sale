# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

from openerp.osv import osv
from openerp.report import report_sxw


class etat_oeuvre_parser(report_sxw.rml_parse):
    _name = 'etat.oeuvre.parser'

    def __init__(self, cr, uid, name, context=None):
        super(etat_oeuvre_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_oeuvre' : self.get_oeuvre,
        })



    def get_oeuvre(self,oeuvre_ids):
        tmp = self.pool.get('oeuvre.etat').browse(self.cr,self.uid,oeuvre_ids)
        return tmp



class oeuvre_etat2(osv.AbstractModel):
    _name = 'report.term_sale.oeuvre_etat2'
    _inherit = 'report.abstract_report'
    _template = 'term_sale.oeuvre_etat2'
    _wrapped_report_class = etat_oeuvre_parser

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
