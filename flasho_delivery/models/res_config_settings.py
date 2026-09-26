from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    flasho_api_key = fields.Char(
        string='API Key',
        config_parameter='flasho.api_key',
    )
    flasho_base_url = fields.Char(
        string='API Base URL',
        config_parameter='flasho.base_url',
        default='https://vendors.tryflasho.com',
    )
    flasho_pickup_latitude = fields.Char(
        string='Pickup latitude',
        config_parameter='flasho.pickup_latitude',
    )
    flasho_pickup_longitude = fields.Char(
        string='Pickup longitude',
        config_parameter='flasho.pickup_longitude',
    )
    flasho_pickup_address = fields.Char(
        string='Pickup address',
        config_parameter='flasho.pickup_address',
    )
    flasho_vehicle_type = fields.Selection(
        [('bike', 'Bike'), ('car', 'Car'), ('van', 'Van')],
        string='Vehicle type',
        config_parameter='flasho.vehicle_type',
        default='bike',
    )
    flasho_auto_book = fields.Boolean(
        string='Book on order confirm',
        config_parameter='flasho.auto_book',
    )
