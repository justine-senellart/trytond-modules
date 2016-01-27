# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pool import Pool

__all__ = ['Configuration']


class Configuration(ModelSingleton, ModelSQL, ModelView):
    'Party Configuration'
    __name__ = 'party.configuration'

    party_sequence = fields.Property(fields.Many2One('ir.sequence',
            'Party Sequence', domain=[
                ('code', '=', 'party.party'),
                ]))
    # change tryton behavior in order to automatically initialize party lang
    party_lang = fields.Function(fields.Many2One('ir.lang', 'Party Language',
        help=('The value set on this field will preset the language on new '
            'parties')),
        'get_party_lang', setter='set_party_lang')

    @classmethod
    def _get_lang_field(cls, name):
        pool = Pool()
        ModelField = pool.get('ir.model.field')
        field, = ModelField.search([
            ('model.model', '=', 'party.party'),
            ('name', '=', 'lang'),
            ], limit=1)
        return field

    def get_party_lang(self, name):
        pool = Pool()
        Property = pool.get('ir.property')
        lang_field = self._get_lang_field(name)
        properties = Property.search([
                ('field', '=', lang_field.id),
                ('res', '=', None),
                ], limit=1)
        if properties:
            prop, = properties
            return prop.value.id

    @classmethod
    def set_party_lang(cls, configurations, name, value):
        pool = Pool()
        Property = pool.get('ir.property')
        lang_field = cls._get_lang_field(name)
        properties = Property.search([
                ('field', '=', lang_field.id),
                ('res', '=', None),
                ])
        Property.delete(properties)
        if value:
            Property.create([{
                        'field': lang_field.id,
                        'value': 'ir.lang,%s' % value,
                        }])
