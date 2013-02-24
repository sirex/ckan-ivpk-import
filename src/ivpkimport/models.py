# -*- coding: utf-8 -*-

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



## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

DeclarativeBase = declarative_base()


class Formatas(DeclarativeBase):
    __tablename__ = 't_formatas'

    __table_args__ = {}

    #column definitions
    id = Column(u'ID', INTEGER(), primary_key=True, nullable=False)
    pavadinimas = Column(u'PAVADINIMAS', VARCHAR(length=50), nullable=False)

    #relation definitions


class Istaiga(DeclarativeBase):
    __tablename__ = 't_istaiga'

    __table_args__ = {}

    #column definitions
    adresas = Column(u'ADRESAS', VARCHAR(length=100), nullable=False)
    id = Column(u'ID', INTEGER(), primary_key=True, nullable=False)
    kodas = Column(u'KODAS', VARCHAR(length=20), nullable=False)
    pavadinimas = Column(u'PAVADINIMAS', VARCHAR(length=50), nullable=False)
    vad_id = Column(u'VAD_ID', INTEGER())

    #relation definitions


class Kategorija(DeclarativeBase):
    __tablename__ = 't_kategorija'

    __table_args__ = {}

    #column definitions
    id = Column(u'ID', INTEGER(), primary_key=True, nullable=False)
    kategorija_id = Column(u'KATEGORIJA_ID', INTEGER())
    lygis = Column(u'LYGIS', INTEGER(), nullable=False)
    pavadinimas = Column(u'PAVADINIMAS', VARCHAR(length=100), nullable=False)

    #relation definitions


class KategorijaRinkmena(DeclarativeBase):
    __tablename__ = 't_kategorija_rinkmena'

    __table_args__ = {}

    #column definitions
    id = Column(u'ID', INTEGER(), primary_key=True, nullable=False)
    kategorija_id = Column(u'KATEGORIJA_ID', INTEGER(), nullable=False)
    rinkmena_id = Column(u'RINKMENA_ID', INTEGER(), nullable=False)

    #relation definitions


class Rinkmena(DeclarativeBase):
    __tablename__ = 't_rinkmena'

    __table_args__ = {}

    #column definitions
    pavadinimas = Column(u'PAVADINIMAS', VARCHAR(length=50))
    alt_pavadinimas = Column(u'ALT_PAVADINIMAS', VARCHAR(length=200))
    atnaujinimas = Column(u'ATNAUJINIMAS', VARCHAR(length=30))
    formatas_alt = Column(u'FORMATAS_ALT', VARCHAR(length=50))
    formatas_id = Column(u'FORMATAS_ID', INTEGER())
    galioja = Column(u'GALIOJA', CHAR(length=1), nullable=False)
    g_data = Column(u'G_DATA', INTEGER())
    id = Column(u'ID', INTEGER(), primary_key=True, nullable=False)
    issamumas = Column(u'ISSAMUMAS', CHAR(length=1))
    istaiga_alt = Column(u'ISTAIGA_ALT', VARCHAR(length=50))
    kl_g_data = Column(u'KL_G_DATA', VARCHAR(length=12))
    kl_p_data = Column(u'KL_P_DATA', VARCHAR(length=12))
    kodas = Column(u'KODAS', INTEGER(), nullable=False)
    k_email = Column(u'K_EMAIL', VARCHAR(length=50))
    k_telefonas = Column(u'K_TELEFONAS', VARCHAR(length=20))
    pastabos = Column(u'PASTABOS', VARCHAR(length=250))
    patikimumas = Column(u'PATIKIMUMAS', CHAR(length=1))
    patik_priezastys = Column(u'PATIK_PRIEZASTYS', VARCHAR(length=250))
    perdavimo_data = Column(u'PERDAVIMO_DATA', DATETIME())
    pozymis = Column(u'POZYMIS', CHAR(length=1), nullable=False)
    pub_data = Column(u'PUB_DATA', DATETIME())
    p_data = Column(u'P_DATA', INTEGER())
    rusis_alt = Column(u'RUSIS_ALT', VARCHAR(length=50))
    rusis_id = Column(u'RUSIS_ID', INTEGER())
    r_zodziai = Column(u'R_ZODZIAI', VARCHAR(length=250))
    santrauka = Column(u'SANTRAUKA', VARCHAR(length=250))
    statusas = Column(u'STATUSAS', CHAR(length=1), nullable=False)
    sukaupta = Column(u'SUKAUPTA', VARCHAR(length=20))
    teikimas = Column(u'TEIKIMAS', VARCHAR(length=250))
    tinklapis = Column(u'TINKLAPIS', VARCHAR(length=100))
    tr_data = Column(u'TR_DATA', DATETIME())
    istaiga_id = Column(u'istaiga_id', INTEGER())

    #relation definitions


class Rusis(DeclarativeBase):
    __tablename__ = 't_rusis'

    __table_args__ = {}

    #column definitions
    id = Column(u'ID', INTEGER(), primary_key=True, nullable=False)
    pavadinimas = Column(u'PAVADINIMAS', VARCHAR(length=50), nullable=False)

    #relation definitions
