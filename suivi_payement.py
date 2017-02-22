# -*- coding:utf-8 -*-


from openerp import models, api, fields




class suivi_payement(models.Model):
	_name = 'suivi.payement'


	date = fields.Date('Date de paiement')
	echeance = fields.Float('échéance')
	methode = fields.Selection([('espece','Espèce'),('cheque','Chéque')],string='Méthode de paiement')
	formulaire_id = fields.Many2one('formulaire.vente',string='Formulaire de vente')
	date_virement = fields.Date('Date de virement')