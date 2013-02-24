from setuptools import find_packages
from setuptools import setup


setup(name='ckan-ivpk-import',
      version='0.1',
      license='GPL',
      zip_safe=False,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      entry_points={
          'console_scripts': ['ivpkimport=ivpkimport.main:main',]
      },
      install_requires=[
        'ckanclient',
        'SQLAlchemy',
        'Unidecode',
      ])
