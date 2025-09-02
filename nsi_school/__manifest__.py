{
    'name': 'School Management System',
    'author': 'Nutshell Infosoft Pvt Ltd.',
    'website': 'www.nutshell.com',
    'summary': 'This is a School Management System',
    'category': 'Eduction',
    # 'icon': 'nsi_school/static/description/icon.png',
    'description': """
    School Management System
    ========================
    This module helps manage school operations, including departments, classes, students, teachers, attendance, and admissions.
""",

    # imported xml file and anothers file in manifest file
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/menu.xml',
        'views/teacher.xml',
        'views/student.xml',
        'views/admission.xml',
        'views/attendance.xml',
        'views/classes.xml',
        'views/department.xml',
        'views/division.xml',
        'views/fees.xml',
        'views/subject.xml',
        # 'views/nutshell/nutshell_letters.xml',
        # 'views/nutshell/nutshell_employee.xml',
        'views/auto_ids_generator.xml',
        # 'views/student_qualification.xml',

        # Report Files
        'report/school_report.xml',
        'report/student_fees_report.xml',
        'report/student_admission_report.xml',
        'report/student_ID_reporting.xml',
        'report/teacher_id_reporting.xml',
        'report/student_label.xml',
        'report/nutshell_report/nutshell_report.xml',
        'report/nutshell_report/nutshell_joining_letter_report.xml',
        'report/nutshell_report/nutshell_offer_letter_report.xml',
        'report/nutshell_report/nutshell_internship_certification_report.xml',
        'report/nutshell_report/nutshell_paper_format_report.xml',
        'report/nutshell_report/nutshell_other_report.xml',

    ],
'depends': ['base', 'hr'],

    'application': True,
    'sequence': "1",
    # 'assets': {
    #     'web.assets_backend': [
    #         '/nsi_school/static/src/css/student.css',
    #         '/nsi_school/static/src/css/styles.css',
    #         '/nsi_school/static/src/css/report.css'
    #     ],
    # },
}