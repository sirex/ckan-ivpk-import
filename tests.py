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
