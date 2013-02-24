# coding: utf-8

# This file is part of ckan-ivpk-import.
#
# ckan-ivpk-import is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ckan-ivpk-import is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ckan-ivpk-import.  If not, see <http://www.gnu.org/licenses/>.

import re
import unidecode
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ckanclient

from .models import DeclarativeBase
from .models import Formatas
from .models import Istaiga
from .models import Rinkmena
from .models import Rusis


def slugify(title=None, length=60):
    if not title:
        return ''

    # Replace all non-ascii characters to ascii equivalents.
    slug = unidecode.unidecode(title)

    # Make slug.
    slug = unicode(re.sub('[^\w\s-]', '', slug).strip().lower())
    slug = re.sub('[-\s]+', '-', slug)

    # Make sure, that slug is not longer that specied in `length`.
    begining_chars = length / 5
    if len(slug) > length:
        words = slug.split('-')
        a, b = [], []
        while words and len('-'.join(a + b)) < length:
            if len('-'.join(a)) <= (len('-'.join(b)) + begining_chars):
                a.append(words.pop(0))
            else:
                b.insert(0, words.pop())
        if b:
            slug = '-'.join(a) + '---' + '-'.join(b)
        else:
            slug = '-'.join(a)

    return slug[:length + begining_chars]


def get_notes(dataset, formatas, rusis):
    notes = []

    if dataset.pastabos:
        notes.append(dataset.pastabos)

    if dataset.santrauka:
        notes.extend([
            '',
            dataset.santrauka,
        ])

    if dataset.patik_priezastys:
        notes.extend([
            '',
            dataset.patik_priezastys,
        ])

    if dataset.atnaujinimas:
        notes.extend([
            '',
            'Atnaujinimas',
            '------------',
            '',
            dataset.atnaujinimas,
        ])

    if dataset.teikimas:
        notes.extend([
            '',
            'Teikimas',
            '--------',
            '',
            dataset.teikimas,
        ])

    if formatas or dataset.formatas_alt:
        notes.extend([
            '',
            'Formatas',
            '--------',
        ])
        if formatas:
            notes.extend([
                '',
                formatas.pavadinimas,
            ])
        if dataset.formatas_alt:
            notes.extend([
                '',
                dataset.formatas_alt,
            ])


    if rusis or dataset.formatas_alt:
        notes.extend([
           u'',
           u'Rūšis',
           u'-----',
        ])
        if rusis:
            notes.extend([
                '',
                rusis.pavadinimas,
            ])
        if dataset.rusis_alt:
            notes.extend([
                '',
                dataset.rusis_alt,
            ])

    return '\n'.join(notes)


def get_tags(dataset):
    tags = []
    for tag in dataset.r_zodziai.split(','):
        tag = slugify(tag.strip())
        tags.append(tag)
    return tags


def get_extras(dataset):
    extras = dict()
    if dataset.alt_pavadinimas:
        extras['Alternatyvus pavadinimas'] = dataset.alt_pavadinimas

    if dataset.kodas:
        extras['IVPK kodas'] = dataset.kodas

    if dataset.k_telefonas:
        extras['Kontaktinis telefonas'] = dataset.k_telefonas

    return extras


def query_datasets_to_import(session):
    return (
        session.query(Rinkmena, Istaiga, Formatas, Rusis).
        outerjoin(Istaiga, Rinkmena.istaiga_id==Istaiga.id).
        outerjoin(Formatas, Rinkmena.formatas_id==Formatas.id).
        outerjoin(Rusis, Rinkmena.rusis_id==Rusis.id).
        filter(Rinkmena.statusas=='U', Rinkmena.galioja=='T',
               Rinkmena.pub_data>=datetime.datetime.fromtimestamp(0))
    )


def update_datasets(ckan, qry):
    for dataset, institution, formatas, rusis in qry:
        if institution:
            institution_title = institution.pavadinimas
        else:
            institution_title = dataset.istaiga_alt

        data = {
            'name': slugify(dataset.pavadinimas),
            'title': dataset.pavadinimas,
            'url': dataset.tinklapis,
            'author': institution_title,
            'author_email': dataset.k_email,
            'tags': get_tags(dataset),
            'extras': get_extras(dataset),
            'notes': get_notes(dataset, formatas, rusis),
        }
        print(data['title'])

        try:
            ckan.package_register_post(data)
        except ckanclient.CkanApiConflictError:
            # FIXME: pass for now, but existing datasets should be known and
            # updated.
            print('Skip.')


def main():
    dbi = 'mysql://root:@localhost/rinkmenos?charset=utf8'
    api_key = '9736a753-7d17-4bff-a62c-afca37d8fda0'
    ckan_url = 'http://localhost:5000'


    engine = create_engine(dbi)

    metadata = DeclarativeBase.metadata
    metadata.bind = engine

    Session = sessionmaker(bind=engine)
    session = Session()

    ckan = ckanclient.CkanClient(base_location='%s/api' % ckan_url, api_key=api_key)

    qry = query_datasets_to_import(session)
    update_datasets(ckan, qry)
