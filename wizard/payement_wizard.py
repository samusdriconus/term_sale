# -*- coding:utf-8 -*-


from openerp import models,api,fields
from openerp.osv import osv
from openerp.tools.translate import _

import time



class payement_wizard(models.TransientModel):
	_name = 'payement.wizard'



	@api.multi
	def get_echeance(self):
		res = self.env['formulaire.vente'].browse(self.env.context['active_id'])
		return res.echeance


	date = fields.Date('Date de paiement',default=time.strftime('%Y-%m-%d'))
	echeance = fields.Float('échéance',default=get_echeance)
	methode = fields.Selection([('espece','Espèce'),('cheque','Chéque')],string='Méthode de paiement',default='espece')
	formulaire_id = fields.Many2one('formulaire.vente',string='Formulaire de vente',default=lambda self:self.env.context['active_id'])
	date_virement = fields.Date('Date de virement')




	@api.multi
	def payer(self):
		res = dict()
		res['date'] = self.date
		res['echeance'] = self.echeance
		res['methode'] = self.methode
		if self.methode == 'cheque':
			res['date_virement'] = self.date_virement

		res['formulaire_id'] = self.formulaire_id.id


		self.env['suivi.payement'].create(res)
		#self.payer += self.echeance

		tmp = self.formulaire_id.reste
		
		if tmp - self.echeance < 0:
			raise osv.except_osv(_('Erreur'),_('Veuillez vérifier l\'écheance '))
		elif tmp - self.echeance > 0:
			self.formulaire_id.payer += self.echeance
		else:
			self.formulaire_id.payer += self.echeance
			self.formulaire_id.state = 'payed'

		return True

