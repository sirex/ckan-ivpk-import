import argparse
import json
import re
import textwrap
import uuid
import unidecode
import logging
import os.path
import subprocess
import itertools

logger = logging.getLogger(__name__)


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
    for part in value.split() if value else []:
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


def get_ckan_orgs(ckan_url, orgs_old_file):
    logger.info('export existing organizations from %s', ckan_url)
    subprocess.run([
        'ckanapi', 'dump', 'organizations', '--all',
        '-O', orgs_old_file,
        '-r', ckan_url,
    ], check=True)

    orgs = {}

    logger.info('read existing organizations from %s', orgs_old_file)
    for data in read_jsonl(orgs_old_file):
        extras = {x['key']: x['value'] for x in data.get('extras', [])}
        if 'IVPK Title' in extras:
            orgs[extras['IVPK Title']] = data
        else:
            orgs[data['title']] = data

    return orgs


def create_orgs_new_file(orgs, ivpk_export_file, orgs_new_file):
    with open(orgs_new_file, 'w', encoding='utf-8') as f:
        logger.info('read ivpk organizations from %s into %s', ivpk_export_file, orgs_new_file)
        for data in read_jsonl(ivpk_export_file):
            if not data.get('Kodas'):
                logger.warn('skip entry without Kodas: %s', data['key'])
                continue

            title = data['Rinkmenos tvarkytojas']

            write = False

            if title not in orgs:
                write = True
                org = {
                    'id': str(uuid.uuid4()),
                    'type': 'organization',
                    'name': slugify(title),
                    'title': title,
                    'approval_status': 'approved',
                    'is_organization': True,
                    'state': 'active',
                    'extras': [
                        {'key': 'IVPK Title', 'value': title},
                    ],
                }
                orgs[title] = org
            else:
                org = orgs[title]

            extras = {x['key']: x['value'] for x in org.get('extras', [])}

            if 'extras' not in org:
                org['extras'] = []

            if 'IVPK Title' not in extras:
                write = True
                org['extras'].append({'key': 'IVPK Title', 'value': title})

            if write:
                logger.debug('export organization %s', data['key'])
                f.write(json.dumps(orgs[title]) + '\n')


def get_ckan_datasets(ckan_url, datasets_old_file):
    logger.info('export existing datasets from %s', ckan_url)
    subprocess.run([
        'ckanapi', 'dump', 'datasets', '--all',
        '-O', datasets_old_file,
        '-r', ckan_url,
    ], check=True)

    tags = {}
    datasets = {}

    logger.info('read existing organizations from %s', datasets_old_file)
    for data in read_jsonl(datasets_old_file):
        extras = {x['key']: x['value'] for x in data.get('extras', [])}

        if 'IVPK Code' in extras:
            datasets[extras['IVPK Code']] = data

        for tag in data.get('tags', []):
            tags[tag['name'].lower()] = tag

    return tags, datasets


def create_datasets_new_file(orgs, tags, datasets, ivpk_export_file, datasets_new_file):
    # See: https://github.com/ckan/ckan/blob/master/ckan/logic/schema.py
    #      http://docs.ckan.org/en/latest/api/index.html#module-ckan.logic.action.create

    with open(datasets_new_file, 'w', encoding='utf-8') as f:
        logger.info('convert ivpk datasets to ckan format')
        for data in read_jsonl(ivpk_export_file):
            if not data.get('Kodas'):
                logger.warn('skip entry without Kodas: %s', data['key'])
                continue

            logger.debug('importing %s', data['key'])

            maintainer = split_contact_info(data.get('Kontaktiniai duomenys'))
            organization = orgs[data['Rinkmenos tvarkytojas']]

            write = False

            if data['Kodas'] not in datasets:
                write = True
                dataset = {
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
                    'tags': [],
                    'type': 'dataset',
                    'extras': [
                        {'key': 'IVPK Code', 'value': data['Kodas']},
                        {'key': 'IVPK URL', 'value': data['key']}
                    ],
                }
            else:
                dataset = datasets[data['Kodas']]

            dataset_tags = [x['name'].lower() for x in dataset['tags']]

            if 'tags' not in dataset:
                dataset['tags'] = []

            for tag in itertools.chain(map(str.strip, data['Reikšminiai žodžiai'].split(';')), ['IVPK import']):
                key = tag.lower()

                if key not in tags:
                    tags[key] = {
                        'id': str(uuid.uuid4()),
                        'display_name': tag,
                        'name': tag,
                        'state': 'active',
                        'vocabulary_id': None
                    }

                if key not in dataset_tags:
                    write = True
                    dataset['tags'].append(tags[key])

            extras = {x['key']: x['value'] for x in dataset.get('extras', [])}

            if 'extras' not in dataset:
                dataset['extras'] = []

            if 'IVPK Code' not in extras:
                write = True
                dataset['extras'].append({'key': 'IVPK Code', 'value': data['Kodas']})

            if 'IVPK URL' not in extras:
                write = True
                dataset['extras'].append({'key': 'IVPK URL', 'value': data['key']})

            if write:
                logger.debug('export dataset %s', data['key'])
                f.write(json.dumps(dataset) + '\n')


def main(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Example:

            ivpkimport http://opendata.lt/ path/to/data/dir

        ''')
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('ckan_url', nargs='?', default='http://opendata.lt/', help='url of existing ckan instance')
    parser.add_argument('path', nargs='?', default='data', help='path to a directory where all data files will be stored')
    parser.add_argument('-l', '--log', default='INFO', help='log level, one of: debug, info, warning, error')
    args = parser.parse_args(argv)

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=getattr(logging, args.log.upper()))

    ivpk_export_file = os.path.join(args.path, 'ivpk-export.jsonl')
    orgs_old_file = os.path.join(args.path, 'orgs-old.jsonl')
    orgs_new_file = os.path.join(args.path, 'orgs-new.jsonl')
    datasets_old_file = os.path.join(args.path, 'datasets-old.jsonl')
    datasets_new_file = os.path.join(args.path, 'datasets-new.jsonl')

    logger.info('download ivpk dump from http://atviriduomenys.lt/')
    subprocess.run(itertools.chain(
        ('curl', '-s', 'http://atviriduomenys.lt/data/ivpk/opendata-gov-lt/datasets.jsonl'),
        ('-o', ivpk_export_file),
        ('-z', ivpk_export_file) if os.path.exists(ivpk_export_file) else (),
    ), check=True)

    # Synchronize organizations
    orgs = get_ckan_orgs(args.ckan_url, orgs_old_file)
    create_orgs_new_file(orgs, ivpk_export_file, orgs_new_file)

    # Synchronize datasets
    orgs = get_ckan_orgs(args.ckan_url, orgs_old_file)
    tags, datasets = get_ckan_datasets(args.ckan_url, datasets_old_file)
    create_datasets_new_file(orgs, tags, datasets, ivpk_export_file, datasets_new_file)
