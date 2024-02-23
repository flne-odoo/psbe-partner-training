{
    "name": "Real Estate",
    "summary": """
        Training module designed for partner training - Simulating Real Estate Custom Flow
        """,
    "category": "",
    "version": "17.0.0.0.0",
    "author": "Odoo PS",
    "website": "https://www.odoo.com",
    "license": "OEEL-1",
    "depends": [
        "base",
    ],
    "data": [
        # SECURITY
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        # VIEWS
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        # MENUS
        "views/estate_menu.xml",
    ],
    "demo": [
        "demo/demo.xml"
    ]
}
