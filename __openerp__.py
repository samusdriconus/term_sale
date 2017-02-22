# -*- coding: utf-8 -*-

##############################################################################

{
    'name': 'Sale Term payment ',
    'version': '1.0',
    'author': 'Saidi Oussama',
    'summary': 'Inventory, Logistic, Storage,Sale',
    'description': """


    """,
    'website': 'https://www.dualpos.com',
    'depends': ['sale', 'purchase'],
    'category': 'Term payment Management',
    'sequence': 1,
   
    'data': [
       'security/groups.xml',
        'security/ir.model.access.csv',
      'menu_root.xml',
      'res_company_view.xml',
       'wizard/payement_wizard_view.xml',
       'suivi_payement_view.xml',
       'term_sale_view.xml',
       'wizard/oeuvre_wizard_view.xml',
       'data/term_sequence.xml',
       'term_report.xml',
       'product_view.xml',
       'report/report_term_form.rml',
       'oeuvre_sociale_view.xml',
       'views/oeuvre_sociale_report.xml',
       'views/oeuvre_sociale_report2.xml',
       'views/formulaire_vente_report.xml',
    ],
    'test': [
        
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
