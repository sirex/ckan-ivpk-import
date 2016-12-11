from setuptools import find_packages
from setuptools import setup


setup(
    name='ckan-ivpk-import',
    version='0.2',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ivpkimport=ivpkimport:main',
        ]
    },
    install_requires=[
        'ckanapi',
        'Unidecode',
    ]
)
