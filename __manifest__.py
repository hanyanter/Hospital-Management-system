{
    'name': "Hospital Management sys.",
    'author': "Hany Antar Hassan",
    'category': "Medical",
    'version': "17.0.0.1.0",
    'description': """This module made to save the main
    information about doctors and patients""",
    'depends': ['base', 'mail',
                ],
    'data': [
        'security/res_group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/doctor_view.xml',
        'views/patient_view.xml',
        'views/department_view.xml',
        'views/patient_history_view.xml',
        'wizard/change_state_view.xml',
        'reports/patient_report.xml',
    ],
    'assets': {'web.assets_backend': ['/hospital_ms/static/src/css/patient.css'],
        'web.report_assets_common': ['/hospital_ms/static/src/fonts/EduNSWACTFoundation-VariableFont_wght.ttf']
    },
    'application': True
}
