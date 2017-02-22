# -*- coding:utf-8 -*-

from openerp import models, fields, api,exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta


class res_partner(models.Model):
    _inherit="res.partner"


    @api.model
    def create(self,data):
        if data['customer']:
            obj_sequence = self.env['ir.sequence']
            data['reference'] = obj_sequence.next_by_code('term.partner.sequence')
        return super(res_partner,self).create(data)




    reference = fields.Char("Numéro",readonly=True)
    card_id_reference = fields.Char("Numéro de piece d'identité")
    card_id_delivred_date = fields.Date("Délivré le")
    use_bio_id = fields.Boolean("Utiliser Biométrique ID",default=False)
    bio_id = fields.Char("ID biométrique")
    card_id_delivred_town = fields.Char("Daira")
    job_id = fields.Many2one("term.job","Fonction")
    job_company_id = fields.Many2one("term.company","Lieu de fonction")
    bank = fields.Char("Banque")
    account_number = fields.Char("Numéro de compte")
    salary_average = fields.Boolean("Salaire > 15000 DA",default=False)
    account_raised = fields.Boolean("Relevé de compte",default=False)
    cni_pc_available = fields.Boolean("validité CNI/PC",defualt=False)
    birth_day = fields.Date("Date de naissance")


    _sql_constraints = [
    ('code_uniq', 'unique(bio_id)', ("ID biométrique doit etre unique !!"))
]


res_partner()

class term_job(models.Model):
    _name="term.job"

    name=fields.Char("Nom",required=True)
    description=fields.Char("Description")


term_job()



class term_company(models.Model):
    _name="term.company"

    name=fields.Char("Nom",required=True)
    address = fields.Char("Address")
    phone_number = fields.Char("Téléphone")

term_company()


class res_company(models.Model):
    _inherit = 'res.company'


    entete = fields.Html('Entéte')
