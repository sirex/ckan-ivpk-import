import json

from uuid import UUID


def test_split_contact_info():
    from ivpkimport import split_contact_info

    assert split_contact_info('252 6999, 1841 info@nma.lt') == {
        'email': 'info@nma.lt',
        'name': None,
        'phone': '252 6999, 1841',
    }

    assert split_contact_info('8 706 85 178 Eugenija Šleiterytė-Vilūnienė Eugenija.viluniene@nzt.lt') == {
        'email': 'Eugenija.viluniene@nzt.lt',
        'name': 'Eugenija Šleiterytė-Vilūnienė',
        'phone': '8 706 85 178',
    }


def test_slugify():
    from ivpkimport import slugify

    assert slugify('Statistiniai duomenys apie 15 metų amžiaus ir vyresnių '
                   'gyventojų sveikatos būklę, gyvenseną, naudojimąsi '
                   'sveikatos priežiūros paslaugomis ir jų prieinamumą.') == (
        'statistiniai-duomenys-apie-15-metu--paslaugomis-ir-ju-prieinamuma'
    )


def test_tagify():
    from ivpkimport import tagify

    assert tagify('finansai, rinkinys') == 'finansai rinkinys'


def test_fixcase():
    from ivpkimport import fixcase

    assert fixcase('test') == 'test'
    assert fixcase('Test') == 'test'
    assert fixcase('T est') == 'T est'
    assert fixcase('TEst') == 'TEst'


def test_get_ckan_orgs(tmpdir, mocker):
    mocker.patch('subprocess.run')

    from ivpkimport import get_ckan_orgs, read_ckan_orgs

    orgs_old_file = tmpdir.join('orgs-old.jsonl')
    orgs_old_file.write('\n'.join(map(json.dumps, [
        {'title': 'Org 1'},
        {'title': 'Org 2', 'extras': [{'key': 'IVPK Title', 'value': 'ORG2'}]},
    ])))

    get_ckan_orgs(None, str(orgs_old_file))

    assert read_ckan_orgs(str(orgs_old_file)) == {
        'Org 1': {'title': 'Org 1'},
        'ORG2': {'title': 'Org 2', 'extras': [{'key': 'IVPK Title', 'value': 'ORG2'}]},
    }


def test_create_orgs_new_file(tmpdir, mocker):
    mocker.patch('uuid.uuid4', side_effect=[
        UUID('{05700888-2ede-4cc2-beda-9480203a8244}'),
    ])

    from ivpkimport import create_orgs_new_file, read_ckan_orgs

    orgs = {'Org 1': {'title': 'Org 1'}}

    ivpk_export_file = tmpdir.join('ivpk-export.jsonl')
    ivpk_export_file.write(json.dumps({
        'key': 'http://opendata.gov.lt/index.php?vars=/public/public/print/14/',
        'Kodas': '5503',
        'Rinkmenos tvarkytojas': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
    }))

    orgs_new_file = tmpdir.join('orgs-new.jsonl')

    create_orgs_new_file(orgs, str(ivpk_export_file), str(orgs_new_file))

    assert read_ckan_orgs(str(orgs_new_file)) == {
        'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos': {
            'id': '05700888-2ede-4cc2-beda-9480203a8244',
            'name': 'informacines-visuomenes-pletros-komitetas--susisiekimo-ministerijos',
            'title': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
            'type': 'organization',
            'state': 'active',
            'is_organization': True,
            'approval_status': 'approved',
            'extras': [
                {
                    'key': 'IVPK Title',
                    'value': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
                },
            ],
        }
    }


def test_get_ckan_datasets(tmpdir, mocker):
    mocker.patch('subprocess.run')

    from ivpkimport import get_ckan_datasets

    datasets_old_file = tmpdir.join('datasets-old.jsonl')
    datasets_old_file.write(json.dumps({
        'extras': [{'key': 'IVPK Code', 'value': '5503'}],
        'tags': [{'name': 'Valstybinis registras'}],
    }))

    tags, datasets = get_ckan_datasets(None, str(datasets_old_file))

    assert tags == {
        'valstybinis registras': {'name': 'Valstybinis registras'},
    }

    assert datasets == {
        '5503': {
            'extras': [{'key': 'IVPK Code', 'value': '5503'}],
            'tags': [{'name': 'Valstybinis registras'}],
        },
    }


def test_create_datasets_new_file(tmpdir, mocker):
    mocker.patch('uuid.uuid4', side_effect=[
        UUID('{05700888-2ede-4cc2-beda-9480203a8244}'),
        UUID('{e6d487f6-41ca-4d1a-9420-e831ca3bc7c1}'),
        UUID('{3cfa6253-050e-447b-820c-2a8d19a9d3d6}'),
        UUID('{08e014cb-27b3-45b5-ad83-42be48abe8b7}'),
        UUID('{e48d28b0-2b72-4d9b-902f-1fdd70ba9c00}'),
        UUID('{276c6c37-79d9-4d54-8834-a239e18f8c14}'),
        UUID('{8e18339a-9307-4237-b698-0f94213cb492}'),
    ])

    from ivpkimport import create_datasets_new_file

    orgs = {
        'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos': {
            'id': '2bad1853-1ff6-434f-b97c-a5e9b25e9cda',
            'title': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
        },
    }
    tags = {'valstybinis registras': {'name': 'Valstybinis registras'}}
    datasets = {}

    ivpk_export_file = tmpdir.join('ivpk-export.jsonl')
    ivpk_export_file.write(json.dumps({
        'key': 'http://opendata.gov.lt/index.php?vars=/public/public/print/14/',
        'Kodas': '5503',
        'Pavadinimas': 'Registrų ir valstybės informacinių sistemų registras',
        'Alternatyvus pavadinimas': '',
        'Apibūdinimas': 'Pateikiama aktuali informacija apie įstatymais nustatytų valstybės ir žinybinių registrų steigimą, kūrimo eigą bei funkcionavimą, registruose kaupiamus duomenis, registrus tvarkančias įstaigas.',
        'Kategorija (informacijos sritis)': 'Valstybės valdymas, viešasis administravimas',
        'Reikšminiai žodžiai': 'Valstybinis registras; žinybinis registras; registrų steigimas; registrų funkcionavimas; kilnojamieji daiktai; juridiniai faktai',
        'Rinkmenos tvarkytojas': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
        'Kontaktiniai duomenys': '861293797 i.zdanaviciene@ivpk.lt',
        'Rinkmenos rūšis': 'Valstybės registras',
        'Duomenų formatas': 'HTML formatas',
        'Rinkmenos pradžios data': '2003',
        'Rinkmenos pabaigos data': '',
        'Atnaujinimo dažnumas': 'nuolat',
        'Internetinis adresas': 'http://www.registrai.lt/',
        'Rinkmenos duomenų teikimo sąlygos': 'Be apribojimų',
        'Duomenų patikimumas': 'Įstaiga prisiima atsakomybę',
        'Duomenų išsamumas': 'Duomenys dar kaupiami. 100%',
        'Rinkmenos aprašymo publikavimo duomenys': '2013-12-20 06:36:31',
    }))

    datasets_new_file = tmpdir.join('datasets-new.jsonl')

    create_datasets_new_file(orgs, tags, datasets, str(ivpk_export_file), str(datasets_new_file))

    assert json.loads(datasets_new_file.read()) == {
        'id': '05700888-2ede-4cc2-beda-9480203a8244',
        'type': 'dataset',
        'name': '5503-registru-ir-valstybes-informaciniu-sistemu-registras',
        'title': 'Registrų ir valstybės informacinių sistemų registras',
        'notes': 'Pateikiama aktuali informacija apie įstatymais nustatytų valstybės ir žinybinių registrų steigimą, kūrimo eigą bei funkcionavimą, registruose kaupiamus duomenis, registrus tvarkančias įstaigas.',
        'url': 'http://www.registrai.lt/',
        'state': 'active',
        'private': False,
        'maintainer': '',
        'maintainer_email': 'i.zdanaviciene@ivpk.lt',
        'extras': [
            {'key': 'IVPK Code', 'value': '5503'},
            {'key': 'IVPK URL', 'value': 'http://opendata.gov.lt/index.php?vars=/public/public/print/14/'},
        ],
        'owner_org': '2bad1853-1ff6-434f-b97c-a5e9b25e9cda',
        'organization': {
            'id': '2bad1853-1ff6-434f-b97c-a5e9b25e9cda',
            'title': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
        },
        'tags': [
            {
                'name': 'Valstybinis registras',
            },
            {
                'id': 'e6d487f6-41ca-4d1a-9420-e831ca3bc7c1',
                'display_name': 'žinybinis registras',
                'name': 'žinybinis registras',
                'state': 'active',
            },
            {
                'id': '3cfa6253-050e-447b-820c-2a8d19a9d3d6',
                'display_name': 'registrų steigimas',
                'name': 'registrų steigimas',
                'state': 'active',
            },
            {
                'id': '08e014cb-27b3-45b5-ad83-42be48abe8b7',
                'display_name': 'registrų funkcionavimas',
                'name': 'registrų funkcionavimas',
                'state': 'active',
            },
            {
                'id': 'e48d28b0-2b72-4d9b-902f-1fdd70ba9c00',
                'display_name': 'kilnojamieji daiktai',
                'name': 'kilnojamieji daiktai',
                'state': 'active',
            },
            {
                'id': '276c6c37-79d9-4d54-8834-a239e18f8c14',
                'display_name': 'juridiniai faktai',
                'name': 'juridiniai faktai',
                'state': 'active',
            },
            {
                'id': '8e18339a-9307-4237-b698-0f94213cb492',
                'display_name': 'IVPK import',
                'name': 'IVPK import',
                'state': 'active',
            },
        ],
    }


def test_main(tmpdir, mocker):
    mocker.patch('subprocess.run')
    mocker.patch('uuid.uuid4', side_effect=[
        UUID('{e6d487f6-41ca-4d1a-9420-e831ca3bc7c1}'),
        UUID('{8e18339a-9307-4237-b698-0f94213cb492}'),
    ])

    from ivpkimport import main

    ivpk_export_file = tmpdir.join('ivpk-export.jsonl')
    ivpk_export_file.write(json.dumps({
        'key': 'http://opendata.gov.lt/index.php?vars=/public/public/print/14/',
        'Kodas': '5503',
        'Pavadinimas': 'Registrų ir valstybės informacinių sistemų registras',
        'Alternatyvus pavadinimas': '',
        'Apibūdinimas': 'Pateikiama aktuali informacija apie įstatymais nustatytų valstybės ir žinybinių registrų steigimą, kūrimo eigą bei funkcionavimą, registruose kaupiamus duomenis, registrus tvarkančias įstaigas.',
        'Kategorija (informacijos sritis)': 'Valstybės valdymas, viešasis administravimas',
        'Reikšminiai žodžiai': 'Valstybinis registras; žinybinis registras',
        'Rinkmenos tvarkytojas': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
        'Kontaktiniai duomenys': '861293797 i.zdanaviciene@ivpk.lt',
        'Rinkmenos rūšis': 'Valstybės registras',
        'Duomenų formatas': 'HTML formatas',
        'Rinkmenos pradžios data': '2003',
        'Rinkmenos pabaigos data': '',
        'Atnaujinimo dažnumas': 'nuolat',
        'Internetinis adresas': 'http://www.registrai.lt/',
        'Rinkmenos duomenų teikimo sąlygos': 'Be apribojimų',
        'Duomenų patikimumas': 'Įstaiga prisiima atsakomybę',
        'Duomenų išsamumas': 'Duomenys dar kaupiami. 100%',
        'Rinkmenos aprašymo publikavimo duomenys': '2013-12-20 06:36:31',
    }))

    orgs_old_file = tmpdir.join('orgs-old.jsonl')
    orgs_old_file.write('\n'.join(map(json.dumps, [
        {'title': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos'},
    ])))

    datasets_old_file = tmpdir.join('datasets-old.jsonl')
    datasets_old_file.write(json.dumps({
        'id': '05700888-2ede-4cc2-beda-9480203a8244',
        'type': 'dataset',
        'name': 'registru-ir-valstybes-informaciniu-sistemu-registras',
        'title': 'Registrų ir valstybės informacinių sistemų registras',
        'extras': [{'key': 'IVPK Code', 'value': '5503'}],
        'tags': [{'name': 'Valstybinis registras'}],
    }))

    main(['http://127.0.0.1:5000/', str(tmpdir)])

    assert json.loads(tmpdir.join('datasets-new.jsonl').read()) == {
        'id': '05700888-2ede-4cc2-beda-9480203a8244',
        'type': 'dataset',
        'name': 'registru-ir-valstybes-informaciniu-sistemu-registras',
        'title': 'Registrų ir valstybės informacinių sistemų registras',
        'extras': [
            {'key': 'IVPK Code', 'value': '5503'},
            {'key': 'IVPK URL', 'value': 'http://opendata.gov.lt/index.php?vars=/public/public/print/14/'},
        ],
        'tags': [
            {
                'name': 'Valstybinis registras',
            },
            {
                'id': 'e6d487f6-41ca-4d1a-9420-e831ca3bc7c1',
                'display_name': 'žinybinis registras',
                'name': 'žinybinis registras',
                'state': 'active',
            },
            {
                'id': '8e18339a-9307-4237-b698-0f94213cb492',
                'display_name': 'IVPK import',
                'name': 'IVPK import',
                'state': 'active',
            },
        ],
    }
