# -*- coding:utf-8- -*-


from openerp import fields,models,api
from datetime import datetime
from openerp.exceptions import except_orm, Warning


class formulaire_vente(models.Model):
	_name = 'formulaire.vente'

	def _get_default_date(self):
		return datetime.now()


	def prepare_picking(self):
		picking_env = self.env['stock.picking']
		picking_type_env = self.env['stock.picking.type']
		outgoing_pick_type = picking_type_env.search([('code','=','outgoing')])
		if len(outgoing_pick_type) > 1:
			outgoing_pick_type=outgoing_pick_type[0]
		picking_id = picking_env.create({'name':'BL/'+str(self.name),'partner_id':self.partner_id.id,'picking_type_id':outgoing_pick_type.id,'is_bl':True})
		return picking_id

	def _get_default_name(self):
		sequence_obj = self.env['ir.sequence']
		return sequence_obj.next_by_code('term.sale.form.sequence')




	name = fields.Char('Numero Piece',default=_get_default_name)
	date = fields.Datetime("Date",default=_get_default_date)
	picking_id = fields.Many2one("stock.picking","Bon de livraison")
	state = fields.Selection([('open','Ouvert'),('done',u'Validé'),('payed',u'Payé')],"Etat",default="open")
	partner_id = fields.Many2one('res.partner','Client')
	partner_ref = fields.Char(string='Numero Client',store=True,related='partner_id.reference')
	birth_day = fields.Date(string='Date de naissance',store=True,related='partner_id.birth_day')
	adresse = fields.Text('Adresse')#on_change ou related
	job_id = fields.Many2one('term.job',string='Fonction',store=True,related='partner_id.job_id')
	telephone = fields.Char(string='Numero Telephone',store=True,related='partner_id.phone')
	card_id_reference = fields.Char(srting="Numero de piece d'identité",store=True,related='partner_id.card_id_reference')
	card_id_delivred_date = fields.Date(string="Delivre le",store=True,related='partner_id.card_id_delivred_date')
	card_id_delivred_town = fields.Char(string="Daira",store=True,related='partner_id.card_id_delivred_town')
	bank = fields.Char(string="Banque",store=True,related='partner_id.bank')
	account_number = fields.Char(string="Numéro de compte",store=True,related='partner_id.account_number')
	salary_average = fields.Boolean(string="Salaire > 15000 DA",store=True,related='partner_id.salary_average')
	account_raised = fields.Boolean(string="Releve de compte",store=True,related='partner_id.account_raised')
	cni_pc_available = fields.Boolean(string="validité CNI/PC",store=True,related='partner_id.cni_pc_available')
	job_company_id = fields.Many2one('term.company',string='Lieu de fonction',store=True,related='partner_id.job_company_id')


	move_ids = fields.One2many('stock.move','formulaire_id',string="Lignes de livraison")

	@api.one
	@api.depends('move_ids','avance')
	def get_total(self):
		amount = sum([line.subtotal for line in self.move_ids])
		self.total = amount
		self.reste = self.total - self.avance - self.payer #Ramzi  ==> self.reste = self.total - self.avance
		if self.methode == 'echeance':
			if self.echeance != 0:
				if self.reste % self.echeance == 0:
					self.nb_echeance = self.reste // self.echeance
				else:
					self.nb_echeance = self.reste // self.echeance + 1
		else:
			self.nb_echeance = self.nb_mois

	total = fields.Float('Total',compute='get_total')
	avance = fields.Float('Avance')
	reste = fields.Float('Reste',compute='get_total')
	nb_mois = fields.Integer('Nbre mensuelle')
	echeance = fields.Float('Echeance')
	date_reglement = fields.Date('Date reglement')

	methode = fields.Selection([('echeance','Par echéance'),('nbre_mens','Par nombre mensuelle')],'Méthode',default='nbre_mens')

	payer = fields.Float('Payer',default=0)#Ramzi
	nb_echeance = fields.Integer('Nombre d\'echeance',compute="get_total")


	# Ramzi
	@api.one
	def get_payment_count(self):
		self.env.cr.execute("SELECT COUNT(*) FROM suivi_payement WHERE formulaire_id=%s",(self.id,))
		#raise Exception(self.env.cr.dictfetchall()[0]['count'])
		self.payment_count = self.env.cr.dictfetchall()[0]['count']

	payment_count = fields.Integer('# de paiement',compute="get_payment_count")
	oeuvre_id = fields.Many2one('oeuvre.sociale','Oeuvre sociale')
	type_vente = fields.Selection([('normal','Normal'),('oeuvre','Oeuvre sociale')],string="Type de vente",required=True,default='normal')
	etat_id = fields.Many2one('oeuvre.etat')


	@api.onchange("type_vente")
	def onchange_type_vente(self):
		if self.type_vente == 'oeuvre':
			self.methode = 'nbre_mens'

	@api.model
	def create(self,data):
		if data['type_vente'] == 'oeuvre':
			data['methode'] = 'echeance'
		return super(formulaire_vente,self).create(data)

			# Fin


	@api.multi
	def action_do_validate(self):
		if not self.move_ids:
			raise Warning('Tu dois au moins selectionner un article !')
		if self.avance == 0 or self.echeance == 0:
			raise Warning('Quelque champs ne doivent pas égal a 0 !')
		self.create_picking()
		self.state="done"
		#Ramzi
		if not self.oeuvre_id and self.type_vente == 'oeuvre':
			data = {}
			tmp = str(self.job_id.name)
			data['name'] = "Oeuvre sociale " + tmp
			data['fonction'] = self.job_id.id

			id = self.env['oeuvre.sociale'].create(data)
			self.oeuvre_id = id
		return self.pool['report'].get_action(self._cr,self._uid,self.ids,'term_sale.formulaire_vente_report',context=self._context)


	@api.onchange('avance')
	def onchange_avance(self):
		if self.methode == 'echeance' and self.echeance == 0:
			self.echeance = self.avance


	@api.onchange('nb_mois')
	def onchange_nbmois(self):
		if self.nb_mois != 0:
			self.echeance = (self.total - self.avance) / self.nb_mois



	@api.multi
	def create_picking(self):
		self.picking_id = self.prepare_picking()
		self.picking_id.move_lines = self.move_ids
		self.picking_id.do_transfer()

	@api.onchange('partner_id')
	def onchange_partner(self):
		try:
			self.adresse = self.partner_id.street +"\n" +  self.partner_id.city +" " + self.partner_id.country_id.name
		except:
			self.adresse = ""

		
		

	@api.multi
	def unlink(self):
		if self.state != "open":
			raise Warning('Tu ne peux pas supprimer les données valider !')
		else:
			return super(self,formulaire_vente).unlink()

	



class stock_move(models.Model):
	_inherit = 'stock.move'

	formulaire_id = fields.Many2one('formulaire.vente')
	unit_price = fields.Float('Prix unitaire')

	@api.one
	@api.depends('unit_price','product_uom_qty')
	def get_subtotal(self):
		self.subtotal = self.unit_price * self.product_uom_qty

   

	subtotal = fields.Float('Sous total',compute='get_subtotal')
   


	@api.onchange('product_id')
	def onchange_product_id(self):
		self.unit_price = self.product_id.list_price
		self.name = self.product_id.name
		self.product_uom = self.product_id.uom_id
		picking_type_env = self.env['stock.picking.type']
		outgoing_pick_type = picking_type_env.search([('code','=','outgoing')])
		if len(outgoing_pick_type) > 1:
			outgoing_pick_type=outgoing_pick_type[0]
		self.location_id = outgoing_pick_type.default_location_src_id
		self.location_dest_id = outgoing_pick_type.default_location_dest_id



class stock_picking(models.Model):
	_inherit="stock.picking"

	is_bl = fields.Boolean("Bon de livraison",default=False)


stock_picking()



class term_tresorerie(models.Model):
	_name = 'term.tresorerie'



	@api.multi
	@api.depends('amount_purchase','amount_sale')
	def _amount_ca(self):
		self.amount_ca = self.amount_sale - self.amount_purchase


	date_start = fields.Date('Date début',required=True)
	date_end = fields.Date('Date fin',required=True)
	product_id = fields.Many2one('product.product','Produit')
	amount_purchase = fields.Float('Total achat')
	amount_sale = fields.Float('Total vente')
	amount_ca = fields.Float('Chiffre d\'affaire',compute='_amount_ca')
	
	@api.model
	def _get_currency(self):
		return self.env.user.company_id.currency_id

	currency_id = fields.Many2one('res.currency','devise',default=_get_currency)



	@api.multi
	def calculer(self):
		date_start = datetime.strptime(self.date_start,'%Y-%m-%d')
		date_end = datetime.strptime(self.date_end,'%Y-%m-%d')
		amount_purchase = 0
		amount_sale = 0
		move_ids = False
		if self.product_id:
			product = self.product_id.id
			if product:
				move_ids = self.env['stock.move'].search([('product_id','=',product)])
		else:
			move_ids = self.env['stock.move'].search([])

		for move in move_ids:
			if move.formulaire_id:
				date = datetime.strptime(move.formulaire_id.date,'%Y-%m-%d %H:%M:%S')
				if date>=date_start and date<date_end:
					if move.picking_id.picking_type_id.code == 'outgoing':
						amount_sale += move.subtotal
			date = datetime.strptime(move.date,'%Y-%m-%d %H:%M:%S')
			if date>=date_start and date<date_end:
				if move.picking_id.picking_type_id.code == 'incoming':
					amount_purchase += move.subtotal

		self.amount_purchase = amount_purchase
		self.amount_sale = amount_sale


		return {
	        'name': ('Trésorerie'),
	        'view_type': 'form',
	        'view_mode': 'form',
	        'res_model': 'term.tresorerie',
	        'view_id': False,
	        'type': 'ir.actions.act_window',
	        'target': 'new',
	        'readonly': True,
	        'res_id': self.id,
    }





























