# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    @route(['/my/paranoia/<model("paranoia.game"):game>'], type='http', auth="user", website=True)
    def portal_game_characters(self, game, **kw):
        values = {
            'game': game,
        }
        return request.render("paranoia.portal_game_page", values)
