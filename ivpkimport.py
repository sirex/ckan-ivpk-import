import argparse
import json
import re
import textwrap
import uuid
import unidecode


def read_jsonl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            yield json.loads(line.strip())


def slugify(title=None, length=60):
    if not title:
        return ''

    # Replace all non-ascii characters to ascii equivalents.
    slug = unidecode.unidecode(title)

    # Make slug.
    slug = str(re.sub(r'[^\w\s-]', '', slug).strip().lower())
    slug = re.sub(r'[-\s]+', '-', slug)

    # Make sure, that slug is not longer that specied in `length`.
    begining_chars = length // 5
    if len(slug) > length:
        words = slug.split('-')
        a, b = [], []
        while words and len('-'.join(a + b)) < length:
            if len('-'.join(a)) <= (len('-'.join(b)) + begining_chars):
                a.append(words.pop(0))
            else:
                b.insert(0, words.pop())
        if b:
            slug = '-'.join(a) + '--' + '-'.join(b)
        else:
            slug = '-'.join(a)

    return slug[:length + begining_chars]


def split_contact_info(value):
    result = {'email': [], 'phone': [], 'name': []}

    last_type = None
    for part in value.split():
        if '@' in part:
            this_type = 'email'
        elif re.search(r'\d', part):
            this_type = 'phone'
        else:
            this_type = 'name'

        if last_type == this_type:
            result[this_type][-1] += ' ' + part
        else:
            result[this_type].append(part)

        last_type = this_type

    for k, v in result.items():
        v = [x.strip() for x in v]
        result[k] = v[0] if v else None

    return result


class IvpkToCkan:

    # "Pavadinimas": "2013 m. viršutinės kelio dangos duomenys",
    # "Apibūdinimas": "Pateikiama informacija: duomenų data, kelio numeris, ruožo pradžia, ruožo pabaiga, dangos tipas",
    # "Kontaktiniai duomenys": "(8 5) 232 9640 vytautas.timukas@lakd.lt",
    # "Internetinis adresas": "http://www.lakd.lt/files/atviri_duomenys/danga2013.csv",
    # "Rinkmenos tvarkytojas": "Lietuvos automobilių kelių direkcija",
    # "Reikšminiai žodžiai": "keliai, dangos",
    # "Kodas": "6055",
    # "key": "http://opendata.gov.lt/index.php?vars=/public/public/print/566/",

    # "Rinkmenos duomenų teikimo sąlygos": "Skelbiama internete",
    # "Duomenų patikimumas": "Įstaiga prisiima atsakomybę",
    # "Atnaujinimo dažnumas": "Kartą per metus",
    # "Rinkmenos rūšis": "Kita",
    # "Alternatyvus pavadinimas": "",
    # "Rinkmenos pabaigos data": "2013",
    # "Rinkmenos aprašymo publikavimo duomenys": "2016-12-05 17:07:50",
    # "Duomenų formatas": "CSV formatas",
    # "Duomenų išsamumas": "Visi duomenys sukaupti",
    # "Rinkmenos pradžios data": "2013",
    # "Kategorija (informacijos sritis)": "Transportas ir ryšiai"

    def get_organization(self, title):
        return None

    def get_tag(self, name):
        return None

    def get_dataset(self, code):
        return None

    def convert(self, data):
        maintainer = split_contact_info(data['Kontaktiniai duomenys'])

        organization = self.get_organization(data['Rinkmenos tvarkytojas']) or {
            'id': str(uuid.uuid4()),
            'type': 'organization',
            'name': slugify(data['Rinkmenos tvarkytojas']),
            'title': data['Rinkmenos tvarkytojas'],
            'approval_status': 'approved',
            'is_organization': True,
            'state': 'active',
        }

        tags = [
            self.get_tag(x) or {
                'id': str(uuid.uuid4()),
                'display_name': x,
                'name': x,
                'state': 'active',
                'vocabulary_id': None
            }
            for x in map(str.strip, data['Reikšminiai žodžiai'].split(';'))
        ]

        # See: https://github.com/ckan/ckan/blob/master/ckan/logic/schema.py
        return self.get_dataset(data['Kodas']) or {
            'id': str(uuid.uuid4()),
            'name': slugify(data['Pavadinimas']),
            'title': data['Pavadinimas'],
            'notes': data['Apibūdinimas'],
            'maintainer': maintainer['name'] or '',
            'maintainer_email': maintainer['email'],
            'url': data['Internetinis adresas'],
            'organization': organization,
            'owner_org': organization['id'],
            'private': False,
            'state': 'active',
            'tags': tags,
            'type': 'dataset',
            'extras': [
                {'key': 'ivpk code', 'value': data['Kodas']},
                {'key': 'ivpk url', 'value': data['key']}
            ],
        }


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Example:

            ivpkimport ckan.jsonl ivpk.jsonl ckan-ivpk.jsonl
        ''')
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('ckan', help='jsonl ckanapi dump')
    parser.add_argument('ivpk', help='raw ivpk data from atviriduomenys.lt/data/ivpk')
    parser.add_argument('output', help='output form jsonl ckanapi dump file')
    args = parser.parse_args()

    ivpk2ckan = IvpkToCkan()

    for data in read_jsonl(args.ivpk):
        ckan = ivpk2ckan.convert(data)
        print(json.dumps(ckan, indent=2))
        break
