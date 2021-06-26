# -*- coding: utf-8 -*-
# from odoo import http


# class RateCurrencyBi(http.Controller):
#     @http.route('/rate_currency_bi/rate_currency_bi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rate_currency_bi/rate_currency_bi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rate_currency_bi.listing', {
#             'root': '/rate_currency_bi/rate_currency_bi',
#             'objects': http.request.env['rate_currency_bi.rate_currency_bi'].search([]),
#         })

#     @http.route('/rate_currency_bi/rate_currency_bi/objects/<model("rate_currency_bi.rate_currency_bi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rate_currency_bi.object', {
#             'object': obj
#         })
