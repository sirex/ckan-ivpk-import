import re
import unidecode
import argparse
import textwrap

import ckanclient


def slugify(title=None, length=60):
    if not title:
        return ''

    # Replace all non-ascii characters to ascii equivalents.
    slug = unidecode.unidecode(title)

    # Make slug.
    slug = str(re.sub('[^\w\s-]', '', slug).strip().lower())
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
            '',
            'Rūšis',
            '-----',
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
        if tag:
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


def query_ivpk_codes(ckan):
    codes = {}
    for name in ckan.package_register_get():
        dataset = ckan.package_entity_get(name)
        try:
            code = dataset['extras']['IVPK kodas']
        except KeyError:
            pass
        else:
            if code:
                codes[code] = dataset['name']
    return codes


def update_datasets(ckan, qry, codes):
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

        code = data['extras']['IVPK kodas']
        if code in codes:
            name = codes[code]
            print('UPDATE: [%d] %s' % (code, name))
            try:
                ckan.package_entity_put(data, name)
            except ckanclient.CkanApiConflictError:
                data['name'] += '-%d' % code
                ckan.package_entity_put(data, name)
        else:
            print('INSERT: [%d] %s' % (code, data['name']))
            try:
                ckan.package_register_post(data)
            except ckanclient.CkanApiConflictError:
                data['name'] += '-%d' % code
                ckan.package_register_post(data)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Example:

            ivpkimport 1d836686-1f13-42f6-ae7e-9172fe972294 data/ivpk/opendata-gov-lt/datasets.jsonl http://opendata.lt
        ''')
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('api-key')
    parser.add_argument('data-file')
    parser.add_argument('ckan-url')
    args = parser.parse_args()

    ckan = ckanclient.CkanClient(base_location='%s/api' % args.ckan_url, api_key=args.api_key)

    print('Query existing IVPK datasets from CKAN...')
    codes = query_ivpk_codes(ckan)
    update_datasets(ckan, codes)
