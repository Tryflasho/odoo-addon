from odoo import _, api, fields, models
from odoo.exceptions import UserError

TERMINAL = {'DELIVERED', 'CANCELLED', 'REJECTED', 'FAILED'}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    flasho_delivery_id = fields.Char(string='Flasho delivery ID', copy=False, readonly=True)
    flasho_order_number = fields.Char(string='Flasho order number', copy=False, readonly=True)
    flasho_status = fields.Char(string='Flasho status', copy=False, readonly=True)
    flasho_driver_name = fields.Char(string='Driver', copy=False, readonly=True)
    flasho_driver_phone = fields.Char(string='Driver phone', copy=False, readonly=True)
    flasho_price = fields.Char(string='Quoted price (KWD)', copy=False, readonly=True)
    flasho_collect_cash = fields.Boolean(string='Collect cash (COD)')

    def action_confirm(self):
        res = super().action_confirm()
        auto = self.env['ir.config_parameter'].sudo().get_param('flasho.auto_book') == 'True'
        if auto:
            for order in self:
                if not order.flasho_delivery_id:
                    order._flasho_create_delivery()
        return res

    def action_flasho_book(self):
        for order in self:
            order._flasho_create_delivery()

    def action_flasho_refresh(self):
        for order in self:
            order._flasho_refresh_status()

    def _flasho_create_delivery(self):
        self.ensure_one()
        if self.flasho_delivery_id:
            raise UserError(_('This order already has a Flasho delivery.'))
        partner = self.partner_shipping_id or self.partner_id
        if not partner.flasho_latitude or not partner.flasho_longitude:
            raise UserError(_('Set Flasho latitude and longitude on the delivery address.'))
        client = self.env['flasho.client']
        cfg = client._params()
        if not cfg['pickup_lat'] or not cfg['pickup_lng']:
            raise UserError(_('Set pickup coordinates in Settings → Flasho.'))
        phone = partner.mobile or partner.phone
        if not phone:
            raise UserError(_('The delivery partner needs a phone number.'))

        address = [p for p in (partner.street, partner.street2, partner.city, partner.country_id.name) if p]
        payload = {
            'customerName': partner.name,
            'customerNumber': phone,
            'pickupLatitude': float(cfg['pickup_lat']),
            'pickupLongitude': float(cfg['pickup_lng']),
            'deliveryLatitude': partner.flasho_latitude,
            'deliveryLongitude': partner.flasho_longitude,
            'deliveryAddress': address or [partner.name],
            'pickupAddress': cfg['pickup_address'] or None,
            'collectCash': bool(self.flasho_collect_cash),
            'totalAmount': f'{self.amount_total:.3f}' if self.flasho_collect_cash else '0.000',
            'specialNotes': self.note and str(self.note)[:500] or None,
            'vehicleType': cfg['vehicle'],
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        data = client.request('POST', '/api/v1/deliveries', payload)
        delivery = data.get('delivery') or {}
        self.write({
            'flasho_delivery_id': delivery.get('id'),
            'flasho_order_number': delivery.get('orderNumber'),
            'flasho_status': delivery.get('status'),
            'flasho_price': delivery.get('estimatedPrice'),
        })

    def _flasho_refresh_status(self):
        self.ensure_one()
        if not self.flasho_delivery_id:
            return
        data = self.env['flasho.client'].request('GET', f'/api/v1/deliveries/{self.flasho_delivery_id}')
        delivery = data.get('delivery') or {}
        self.write({
            'flasho_status': delivery.get('status'),
            'flasho_order_number': delivery.get('orderNumber') or self.flasho_order_number,
            'flasho_driver_name': delivery.get('driverName'),
            'flasho_driver_phone': delivery.get('driverPhone'),
            'flasho_price': delivery.get('estimatedPrice') or self.flasho_price,
        })

    @api.model
    def _cron_flasho_sync(self):
        orders = self.search([
            ('flasho_delivery_id', '!=', False),
            ('flasho_status', 'not in', list(TERMINAL)),
        ])
        for order in orders:
            try:
                order._flasho_refresh_status()
            except Exception:
                continue
