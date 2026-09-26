import json
import logging
import urllib.error
import urllib.request

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

DEFAULT_BASE = 'https://vendors.tryflasho.com'


class FlashoClient(models.AbstractModel):
    _name = 'flasho.client'
    _description = 'Flasho API client'

    def _params(self):
        icp = self.env['ir.config_parameter'].sudo()
        key = (icp.get_param('flasho.api_key') or '').strip()
        if not key:
            raise UserError(_('Set the Flasho API key in Settings → Flasho.'))
        return {
            'base': (icp.get_param('flasho.base_url') or DEFAULT_BASE).rstrip('/'),
            'key': key,
            'pickup_lat': icp.get_param('flasho.pickup_latitude'),
            'pickup_lng': icp.get_param('flasho.pickup_longitude'),
            'pickup_address': icp.get_param('flasho.pickup_address') or '',
            'vehicle': icp.get_param('flasho.vehicle_type') or 'bike',
            'auto_book': icp.get_param('flasho.auto_book') == 'True',
        }

    def request(self, method, path, payload=None):
        cfg = self._params()
        url = f"{cfg['base']}{path}"
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                'Authorization': f"Bearer {cfg['key']}",
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as err:
            body = err.read().decode(errors='ignore')
            _logger.warning('Flasho %s %s failed: %s %s', method, path, err.code, body)
            try:
                msg = json.loads(body).get('message') or body
            except Exception:
                msg = body or str(err)
            raise UserError(_('Flasho API error: %s') % msg) from err
        except urllib.error.URLError as err:
            raise UserError(_('Could not reach Flasho: %s') % err.reason) from err
