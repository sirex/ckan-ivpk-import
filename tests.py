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


def test_convert(mocker):
    from uuid import UUID
    from ivpkimport import IvpkToCkan

    mocker.patch('uuid.uuid4', side_effect=[
        UUID('{2fc0b9da-6269-4972-ad93-ecfd2465a3c0}'),
        UUID('{1dd47e3a-f373-4ee1-931a-9d401bd16b65}'),
        UUID('{e6d487f6-41ca-4d1a-9420-e831ca3bc7c1}'),
        UUID('{3cfa6253-050e-447b-820c-2a8d19a9d3d6}'),
        UUID('{08e014cb-27b3-45b5-ad83-42be48abe8b7}'),
        UUID('{e48d28b0-2b72-4d9b-902f-1fdd70ba9c00}'),
        UUID('{276c6c37-79d9-4d54-8834-a239e18f8c14}'),
        UUID('{2bad1853-1ff6-434f-b97c-a5e9b25e9cda}'),
    ])

    ivpk_data = {
        'key': 'http://opendata.gov.lt/index.php?vars=/public/public/print/14/',
        'Kodas': '5503',
        'Pavadinimas': 'Registrų ir valstybės informacinių sistemų registras',
        'Alternatyvus pavadinimas': '',
        'Apibūdinimas': 'Pateikiama aktuali informacija apie įstatymais nustatytų valstybės ir žinybinių registrų steigimą, kūrimo eigą bei funkcionavimą, registruose kaupiamus duomenis, registrus tvarkančias įstaigas.',
        'Kategorija (informacijos sritis)': 'Valstybės valdymas, viešasis administravimas',
        'Reikšminiai žodžiai': 'Valstybinis registras; žinybinis registras; registrų steigimas; registrų funkcionavimas; nekilnojamieji, kilnojamieji daiktai; juridiniai faktai',
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
    }

    assert IvpkToCkan().convert(ivpk_data) == {
        'id': '2bad1853-1ff6-434f-b97c-a5e9b25e9cda',
        'type': 'dataset',
        'name': 'registru-ir-valstybes-informaciniu-sistemu-registras',
        'title': 'Registrų ir valstybės informacinių sistemų registras',
        'notes': 'Pateikiama aktuali informacija apie įstatymais nustatytų valstybės ir žinybinių registrų steigimą, kūrimo eigą bei funkcionavimą, registruose kaupiamus duomenis, registrus tvarkančias įstaigas.',
        'url': 'http://www.registrai.lt/',
        'state': 'active',
        'private': False,
        'maintainer': '',
        'maintainer_email': 'i.zdanaviciene@ivpk.lt',
        'extras': [
            {'key': 'ivpk code', 'value': '5503'},
            {'key': 'ivpk url', 'value': 'http://opendata.gov.lt/index.php?vars=/public/public/print/14/'},
        ],
        'owner_org': '2fc0b9da-6269-4972-ad93-ecfd2465a3c0',
        'organization': {
            'id': '2fc0b9da-6269-4972-ad93-ecfd2465a3c0',
            'type': 'organization',
            'name': 'informacines-visuomenes-pletros-komitetas--susisiekimo-ministerijos',
            'title': 'Informacinės visuomenės plėtros komitetas prie Susisiekimo ministerijos',
            'is_organization': True,
            'approval_status': 'approved',
            'state': 'active',
        },
        'tags': [
            {
                'id': '1dd47e3a-f373-4ee1-931a-9d401bd16b65',
                'display_name': 'Valstybinis registras',
                'name': 'Valstybinis registras',
                'state': 'active',
                'vocabulary_id': None,
            },
            {
                'id': 'e6d487f6-41ca-4d1a-9420-e831ca3bc7c1',
                'display_name': 'žinybinis registras',
                'name': 'žinybinis registras',
                'state': 'active',
                'vocabulary_id': None,
            },
            {
                'id': '3cfa6253-050e-447b-820c-2a8d19a9d3d6',
                'display_name': 'registrų steigimas',
                'name': 'registrų steigimas',
                'state': 'active',
                'vocabulary_id': None,
            },
            {
                'id': '08e014cb-27b3-45b5-ad83-42be48abe8b7',
                'display_name': 'registrų funkcionavimas',
                'name': 'registrų funkcionavimas',
                'state': 'active',
                'vocabulary_id': None,
            },
            {
                'id': 'e48d28b0-2b72-4d9b-902f-1fdd70ba9c00',
                'display_name': 'nekilnojamieji, kilnojamieji daiktai',
                'name': 'nekilnojamieji, kilnojamieji daiktai',
                'state': 'active',
                'vocabulary_id': None,
            },
            {
                'id': '276c6c37-79d9-4d54-8834-a239e18f8c14',
                'display_name': 'juridiniai faktai',
                'name': 'juridiniai faktai',
                'state': 'active',
                'vocabulary_id': None,
            },
        ],
    }
