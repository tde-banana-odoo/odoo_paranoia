# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class Game(models.Model):
    _name = 'paranoia.game'
    _description = 'Game'
    _inherit = 'mail.thread'

    name = fields.Char('Name')
    character_ids = fields.One2many('paranoia.character', 'game_id', string='Characters')


class Player(models.Model):
    _name = 'paranoia.player'
    _description = 'Player'

    name = fields.Char('Name')


class Character(models.Model):
    _name = 'paranoia.character'
    _description = 'Character'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # description
    name = fields.Char('Name', required=True)
    accreditation = fields.Selection([
        ('IR', 'Infra Rouge'), ('R', 'Rouge'),
        ('O', 'Orange')], string='Accreditation', default='IR', required=True)
    accreditation_short = fields.Char(
        'Accreditation Short',
        compute='_compute_accreditation_short', store=True)
    color = fields.Integer(default=0)
    sector = fields.Char('Sector', required=True)
    clone_number = fields.Integer('Clone Number', default=1, required=True)
    full_name = fields.Char(
        'Full Name',
        compute='_compute_full_name', store=True)
    image = fields.Binary("Image", attachment=True)
    image_medium = fields.Binary("Medium-sized image", attachment=True)
    image_small = fields.Binary("Small-sized image", attachment=True)
    # game & player
    game_id = fields.Many2one('paranoia.game', 'Game', required=True)
    player_id = fields.Many2one('paranoia.player', 'Player', required=True)
    # status
    treason = fields.Integer('Trahison', default=0)
    life = fields.Selection([
        ('full', 'Ok'),
        ('egra', 'Egratiné')], string='Life', default='full', required=True)
    xp_total = fields.Integer('XP Total', default=0)
    xp_current = fields.Integer('XP', default=0)
    # skill and attributes
    attribute_ids = fields.One2many(
        'paranoia.attribute', 'character_id', 'Attributes')
    skill_ids = fields.One2many(
        'paranoia.skill', 'character_id', 'Skills')

    @api.depends('accreditation')
    def _compute_accreditation_short(self):
        for record in self:
            record.accreditation_short = record.accreditation

    @api.depends('name', 'accreditation_short', 'sector', 'clone_number')
    def _compute_full_name(self):
        for record in self:
            record.full_name = '%s-%s-%s-%s' % (record.name, record.accreditation_short, record.sector, record.clone_number)

    @api.model
    def create(self, values):
        tools.image_resize_images(values, sizes={'image': (1024, None)})
        character = super(Character, self).create(values)
        character._add_missing_skills()
        return character

    def _add_missing_skills(self):
        for character in self:
            cmd = []
            char_skill_tpls = character.mapped('skill_ids.skill_template_id')
            all_skill_tpls = self.env['paranoia.skill.template'].search([('default', '=', True)])
            for skill_tpl in all_skill_tpls - char_skill_tpls:
                cmd.append((0, 0, {
                    'skill_template_id': skill_tpl.id,
                }))
            character.write({'skill_ids': cmd})
        return

    @api.multi
    def write(self, values):
        if 'image' in values:
            tools.image_resize_images(values, sizes={'image': (1024, None)})
        return super(Character, self).write(values)


class AttributeTemplate(models.Model):
    _name = 'paranoia.attribute.template'
    _description = 'Attribute Template'
    _order = 'sequence, name'

    name = fields.Char('Name')
    sequence = fields.Integer('Sequence', default=10)


class Attribute(models.Model):
    _name = 'paranoia.attribute'
    _description = 'Attribute'

    name = fields.Char('Name')
    attribute_template_id = fields.Many2one('paranoia.attribute.template', 'Attribute Template', required=True)
    character_id = fields.Many2one('paranoia.character', 'Character', required=True)
    value = fields.Integer('Value', default=0)


class SkillTemplate(models.Model):
    _name = 'paranoia.skill.template'
    _order = 'sequence, name'

    name = fields.Char('Name')
    sequence = fields.Integer('Sequence', default=10)
    default = fields.Boolean('Default', default=True)


class Skill(models.Model):
    _name = 'paranoia.skill'
    _description = 'Skill'

    name = fields.Char('Name')
    skill_template_id = fields.Many2one('paranoia.skill.template', 'Skill Template', required=True)
    character_id = fields.Many2one('paranoia.character', 'Character', required=True)
    attribute_id = fields.Many2One('paranoia.attribute', 'Attribute')
    value = fields.Integer('Value', default=0)
