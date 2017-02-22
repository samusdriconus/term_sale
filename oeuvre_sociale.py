# -*-coding:utf-8 -*-

from openerp import models,api,fields
import time



class oeuvre_sociale(models.Model):
	_name = 'oeuvre.sociale'

	@api.one
	def get_nb_client(self):
		self.nb_client = len(self.client_ids)

	client_ids = fields.One2many('formulaire.vente','oeuvre_id','Clients')
	name = fields.Char('Nom')
	fonction = fields.Many2one('term.job',string="Fontion")
	nb_client = fields.Integer('# client',compute="get_nb_client")
	date = fields.Date('Date',default=time.strftime("%Y-%m-%d"))

	@api.one
	def get_nb_etat(self):
		etat_obj = self.env['oeuvre.etat'].search([('oeuvre_id','=',self.id)])
		self.nb_etat = str(len(etat_obj)) + " Etat(s)"


	nb_etat = fields.Char('# etat',compute='get_nb_etat')
	mois = fields.Selection([('1','Janvier'),('2','Février'),('3','Mars'),('4','Avril'),('5','Mai'),('6','Juin'),('7','Juillet'),('8','Aout'),('9','Septembre'),('10','Octobre'),('11','Novembre'),('12','Decembre')],string='Mois'),
	annee = fields.Integer('Année')



"""	@api.multi
	def get_action(self):
		id = self.env.ref("term_sale.act_oeuvre")
		return id
		if not self.mois:
			id = self.env.ref("term_sale.act_oeuvre")
			raise Exception(id)
			return {
				'type': 'ir.actions.act_window',
            	'name': "Générer etat",
	            'res_model': 'oeuvre.wizard',
	            'view_type': 'form',
	            'view_mode': 'form',
	            'view_id':"term_sale_oeuvre_wizard",
	            'target': 'new',
            }
"""



class oeuvre_sociale_etat(models.Model):
	_name = 'oeuvre.etat'



	name = fields.Char('Designation')
	date_impression = fields.Date('Date d\'impression',default=time.strftime('%Y-%m-%d'))
	#client_ids = fields.Many2many('formulaire.vente')
	client_ids = fields.One2many('oeuvre.etat.line','etat_id')
	oeuvre_id = fields.Many2one('oeuvre.sociale')

	@api.one
	@api.depends('name','oeuvre_id')
	def get_complete_name(self):
		self.complete_name = self.name + str(self.oeuvre_id)

	complete_name = fields.Char('Name',compute=get_complete_name,store=True)


	@api.one
	@api.depends('client_ids')
	def get_total(self):
		self.total_avance = sum([line.avance for line in self.client_ids])
		self.total_echeance = sum([line.echeance for line in self.client_ids])

	total_avance = fields.Float(compute="get_total",store=True)
	total_echeance = fields.Float(compute="get_total",store=True)






	_sql_constraints = [
    ('code_uniq', 'unique(complete_name)', ("Etat déja imprimer !!"))
]

class oeuvre_etat_line(models.Model):
	_name = 'oeuvre.etat.line'

		

	name = fields.Char('Numero Piece')
	partner_id = fields.Many2one('res.partner','Client')
	partner_ref = fields.Char(string='Numero Client')



	total = fields.Float('Total')
	avance = fields.Float('Avance')
	echeance = fields.Float('Echeance')
	nb_echeance = fields.Integer('Nombre d\'echeance')
	etat_id = fields.Many2one('oeuvre.etat')


	# Ramzi


