# -*- coding: utf-8 -*-
# from odoo import http


# class BaramegBirthdayReminder(http.Controller):
#     @http.route('/barameg_birthday_reminder/barameg_birthday_reminder/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/barameg_birthday_reminder/barameg_birthday_reminder/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('barameg_birthday_reminder.listing', {
#             'root': '/barameg_birthday_reminder/barameg_birthday_reminder',
#             'objects': http.request.env['barameg_birthday_reminder.barameg_birthday_reminder'].search([]),
#         })

#     @http.route('/barameg_birthday_reminder/barameg_birthday_reminder/objects/<model("barameg_birthday_reminder.barameg_birthday_reminder"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('barameg_birthday_reminder.object', {
#             'object': obj
#         })
