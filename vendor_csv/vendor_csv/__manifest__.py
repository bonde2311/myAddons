{
    "name": "Vendor Bill CSV",
    "author":"Nutshell Infosoft",
    "summary": "Export Vendor Bills as CSV",
    "category": "Accounting",
    "depends": ["account"],
    "data": [
        "views/export_csv.xml",
        'security/ir.model.access.csv',
    ],
    "installable": True,
    "application": False,
    "auto_install": False
}
