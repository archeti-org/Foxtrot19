# -*- coding: utf-8 -*-

import json

from odoo import api, http, SUPERUSER_ID
from odoo.http import content_disposition, Controller, request
from odoo.modules.registry import Registry
from odoo.tools import html_escape


class PurchaseController(Controller):

    @http.route('/web/binary/saveas/att_url', type='http', auth='public')
    def saveas_attachment_url(self, db, hash=None):
        """Download attachment.

        :param str db: name of the db
        :param str hash: hash to fetch the binary from
        :returns: :class:`werkzeug.wrappers.Response`
        """
        registry = Registry(db)
        with registry.cursor() as cr:
            invalid_flag = False
            attachment = None

            if hash:
                env = api.Environment(cr, SUPERUSER_ID, {})
                attachment = env['ir.attachment'].search(
                    [('hash_code', '=', hash)], limit=1)
                if attachment:
                    order = env[attachment.res_model].browse(attachment.res_id)
                    if not order.attachments_url_validity:
                        if order.attachment_url:
                            order.clear_url_zip_file(attachment.id)
                        invalid_flag = True
                else:
                    invalid_flag = True
            else:
                invalid_flag = True

            if invalid_flag:
                return request.render(
                    'purchase_product_attachments_link.invalid_attachments_url'
                )

            filecontent = attachment.raw
            if not filecontent:
                return request.not_found()

            filename = attachment.name or 'ir_attachment_%s' % attachment.id
            try:
                return request.make_response(
                    filecontent,
                    [
                        ('Content-Type', 'application/zip'),
                        ('Content-Disposition', content_disposition(filename)),
                    ],
                )
            except Exception as e:
                error = {
                    'code': 200,
                    'message': 'Odoo Server Error',
                    'data': http.serialize_exception(e),
                }
                return request.make_response(html_escape(json.dumps(error)))
