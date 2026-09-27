# Flasho Delivery for Odoo

Odoo 17 addon that books and tracks [Flasho](https://vendors.tryflasho.com) deliveries from sales orders.

## Features

- Store your Flasho API key and pickup coordinates in **Settings → Flasho**
- Book an on-demand delivery from a confirmed sales order
- Optional auto-book when a quotation is confirmed
- Refresh driver and status from Flasho
- Scheduled cron sync for open deliveries
- Cash-on-delivery when the order still has a residual amount

## Install

1. Clone this repo into your Odoo addons path:

   ```bash
   git clone git@github.com:Tryflasho/odoo-addon.git
   ```

2. Add the folder to `addons_path` and update the apps list.
3. Install **Flasho Delivery**.
4. Open **Settings → Flasho** and set:

   - API key (`flsh_...` from [Website API](https://vendors.tryflasho.com/))
   - Pickup latitude / longitude
   - Vehicle type

5. On each delivery customer, set **Flasho latitude / longitude**.

## Usage

1. Confirm a sales order (or click **Book Flasho Delivery**).
2. Flasho returns an order number (`FLH…`) stored on the order.
3. Use **Refresh Flasho Status** or wait for the 15-minute cron.

## API

Base URL: `https://vendors.tryflasho.com`

See the [Flasho Merchant API docs](https://github.com/Tryflasho).
