# -*- coding: utf-8 -*-

import base64
import hashlib
import os
import shutil
import tempfile
import zipfile
from datetime import timedelta
from random import choice

from werkzeug import urls

from odoo import models, fields, api


def random_token():
    # the token has an entropy of about 30 bits (6 bits/char * 5 chars)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(choice(chars) for _i in range(5))


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    attachment_url = fields.Char()
    url_expiration_date = fields.Datetime(copy=False)

    attachments_url_validity = fields.Boolean(
        compute='_compute_attachments_url_validity', string='Url is Valid?')

    def _compute_attachments_url_validity(self):
        now = fields.Datetime.now()
        for order in self:
            order.attachments_url_validity = bool(
                order.attachment_url
                and len(order.attachment_url) > 1
                and order.url_expiration_date
                and now <= order.url_expiration_date
            )

    def generate_att_zip_files(self, file_entries):
        """Create a zip attachment from temporary files.

        :param list file_entries: list of (file_path, archive_name) tuples
        """
        zip_subdir = 'product_attachments_%s' % random_token()
        zip_filename = '%s.zip' % zip_subdir

        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip:
            zip_path = tmp_zip.name

        try:
            with zipfile.ZipFile(
                zip_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True
            ) as zip_file:
                for file_path, file_name in file_entries:
                    zip_file.write(
                        file_path, os.path.join(zip_subdir, file_name))

            with open(zip_path, 'rb') as fp:
                data = base64.b64encode(fp.read())

            return self.env['ir.attachment'].create({
                'datas': data,
                'name': zip_filename,
                'type': 'binary',
                'res_model': self._name,
                'res_id': self.id,
            })
        finally:
            if os.path.exists(zip_path):
                os.unlink(zip_path)

    def action_generate_attachments_url(self):
        """Build a zip of product attachments and store a temporary public URL."""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        validity_days = self.env['ir.config_parameter'].sudo().get_param(
            'purchase_product_attachments_link.url_days') or 1
        expiration_date = fields.Datetime.now() + timedelta(days=int(validity_days))

        for rec in self:
            if rec.attachment_url:
                rec.clear_url_zip_file()

            documents = rec._get_product_documents()
            attachments = documents.mapped("ir_attachment_id")
            # attachments = rec.mapped(
            #     'order_line.product_id.product_tmpl_id').get_attachments()

            tmpdir = tempfile.mkdtemp()
            try:
                file_entries = []
                for attachment in attachments:
                    content = attachment.raw
                    if not content:
                        continue
                    file_name = attachment.name or 'attachment'
                    file_path = os.path.join(
                        tmpdir, '%s_%s' % (attachment.id, file_name))
                    with open(file_path, 'wb') as attachment_file:
                        attachment_file.write(content)
                    file_entries.append((file_path, file_name))

                if not file_entries:
                    continue

                att_id = rec.generate_att_zip_files(file_entries)

                hash_att = hashlib.md5(
                    (att_id.name + str(att_id)).encode('utf-8')).hexdigest()
                url = 'web/binary/saveas/att_url?db=%s&hash=%s' % (
                    self.env.cr.dbname, hash_att)
                att_url = urls.url_join(base_url, url)
                att_id.write({'hash_code': hash_att})

                rec.write({
                    'attachment_url': att_url,
                    'url_expiration_date': expiration_date,
                })
            finally:
                shutil.rmtree(tmpdir, ignore_errors=True)

    def clear_url_zip_file(self, att_id=False):
        self.ensure_one()
        if not att_id:
            if not self.attachment_url:
                return
            hash_name = self.attachment_url.split('&')[-1]
            hash_name = hash_name.split('=')[-1]
            att_id = self.env['ir.attachment'].search(
                [('hash_code', '=', hash_name)], limit=1).id

        self.sudo().write({'attachment_url': False})

        attachment = self.env['ir.attachment'].sudo().browse(att_id)
        if attachment.exists():
            attachment.unlink()

    def _check_attachments_url_expiration(self):
        if not self:
            self = self.search([('attachment_url', '!=', False)])
        for rec in self:
            if not rec.attachments_url_validity and rec.attachment_url:
                rec.clear_url_zip_file()

    def _get_product_documents(self):
        self.ensure_one()

        documents = (
            self.order_line.product_id.product_document_ids
            | self.order_line.product_id.product_tmpl_id.product_document_ids
        )
        return documents.sorted()

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    hash_code = fields.Char(string='Hash code')
