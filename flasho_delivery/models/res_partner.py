from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    flasho_latitude = fields.Float(string='Flasho latitude', digits=(10, 6))
    flasho_longitude = fields.Float(string='Flasho longitude', digits=(10, 6))
