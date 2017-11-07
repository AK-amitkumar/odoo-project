{
    "name": "Islamic Datepicker",
    'version': '1.0',
    'author': 'Techorg',
    'summary': 'Web tool',
    'website': 'www.techorg.com',
    "depends": ['web'],
    'category': 'web',
    'sequence': 17,
    'data': [
         "res_users_view.xml",
         "views/web_linkedin.xml"    
    ],
   
    'qweb' : [
        "static/src/xml/*.xml",
    ],
        'images': ['images/1.jpg','images/2.jpg'],
    'installable': True,    
    'auto_install': False,
}
