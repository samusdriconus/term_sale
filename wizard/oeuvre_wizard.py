# -*-coding:utf-8 -*-


#from openerp import fields,models,api
from openerp.osv import osv,fields
import time
from openerp.exceptions import except_orm, Warning



class oeuvre_wizard(osv.osv_memory):
	_name = 'oeuvre.wizard'


	def get_default_month(self,cr,uid,ids,context=None):
		now = time.strftime('%B')
		return now

	def get_default_year(self,cr,uid,ids,context=None):
		now = time.strftime('%Y')
		return now

	_columns = {
		'mois' : fields.selection([('janvier','Janvier'),('fevrier','Février'),('mars','Mars'),('avril','Avril'),('mai','Mai'),('juin','Juin'),('juillet','Juillet'),('aout','Aout'),('septembre','Septembre'),('octobre','Octobre'),('novembre','Novembre'),('decembre','Decembre')],string='Mois'),
		'annee' : fields.integer('Année')
	}
	_defaults = {
		'mois' : get_default_month,
		'annee' : get_default_year,
	}


	def generer(self,cr,uid,ids,context=None):
		etat_ids = []
		self_brow = self.browse(cr,uid,ids[0],context)
		fields_get = dict(self.fields_get(cr, uid, allfields=['mois'], context=context)['mois']['selection'])
		for oeuvre in self.pool['oeuvre.sociale'].browse(cr,uid,context['active_ids'],context):
			data = {}
			form_ids = []
			id_etat = self.pool['oeuvre.etat'].create(cr,uid,{'name' : (fields_get[self_brow.mois]).encode('utf-8').strip() + " " + str(self_brow.annee),'oeuvre_id' : oeuvre.id},context)
			for formulaire in oeuvre.client_ids:
				tmp = formulaire.reste
				if formulaire.state != 'payed':
					if tmp - formulaire.echeance < 0:
						formulaire.echeance = tmp
						formulaire.payer += formulaire.echeance
						formulaire.state = 'payed'
						self.pool.get('oeuvre.etat.line').create(cr,uid,{'name':formulaire.name,'partner_id':formulaire.partner_id.id,'partner_ref':formulaire.partner_ref,
							'total':formulaire.total,'avance':formulaire.avance,'echeance':formulaire.echeance,'nb_echeance':formulaire.nb_echeance - 1,'etat_id':id_etat})
						
					elif tmp - formulaire.echeance > 0:
						formulaire.payer += formulaire.echeance
						form_ids.append(formulaire.id)
						self.pool.get('oeuvre.etat.line').create(cr,uid,{'name':formulaire.name,'partner_id':formulaire.partner_id.id,'partner_ref':formulaire.partner_ref,
							'total':formulaire.total,'avance':formulaire.avance,'echeance':formulaire.echeance,'nb_echeance':formulaire.nb_echeance - 1,'etat_id':id_etat})
					else:
						formulaire.payer += formulaire.echeance
						formulaire.state = 'payed'
						form_ids.append(formulaire.id)
						self.pool.get('oeuvre.etat.line').create(cr,uid,{'name':formulaire.name,'partner_id':formulaire.partner_id.id,'partner_ref':formulaire.partner_ref,
							'total':formulaire.total,'avance':formulaire.avance,'echeance':formulaire.echeance,'nb_echeance':formulaire.nb_echeance - 1,'etat_id':id_etat})
			#raise Exception(form_ids)
			if not self.pool['oeuvre.etat'].browse(cr,uid,id_etat,context).client_ids:
				self.pool['oeuvre.etat'].unlink(cr,uid,id_etat,context)
				raise Warning('Etat vide pour cet oeuvre sociale !!')
			else:
				etat_ids.append(id_etat)
		data['form'] = self.read(cr,uid,ids,['mois','annee'],context)[0]
		data['form']['ids'] = etat_ids
		return self.pool['report'].get_action(cr,uid,[],'term_sale.oeuvre_etat2',data=data,context=context)