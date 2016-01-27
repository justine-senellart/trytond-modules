# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pyson import Eval
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction

__all__ = ['PartyConfiguration']
__metaclass__ = PoolMeta


class PartyConfiguration:
    __name__ = 'party.configuration'

    @classmethod
    def __setup__(cls):
        super(PartyConfiguration, cls).__setup__()

        cls.party_sequence.domain = [
            cls.party_sequence.domain,
            ('company', 'in', [Eval('context', {}).get('company'), None]),
            ]

    def get_party_lang(self, name):
        pool = Pool()
        Property = pool.get('ir.property')
        company_id = Transaction().context.get('company')
        lang_field = self._get_lang_field(name)
        properties = Property.search([
                ('field', '=', lang_field.id),
                ('res', '=', None),
                ('company', '=', company_id),
                ], limit=1)
        if properties:
            prop, = properties
            return prop.value.id

    @classmethod
    def set_party_lang(cls, configurations, name, value):
        pool = Pool()
        Property = pool.get('ir.property')
        company_id = Transaction().context.get('company')
        lang_field = cls._get_lang_field(name)
        properties = Property.search([
                ('field', '=', lang_field.id),
                ('res', '=', None),
                ('company', '=', company_id),
                ])
        Property.delete(properties)
        if value:
            Property.create([{
                        'field': lang_field.id,
                        'value': 'ir.lang,%s' % value,
                        'company': company_id,
                        }])
