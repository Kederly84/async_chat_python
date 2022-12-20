from setuptools import setup, find_packages

setup(name='mess_server_aleks',
      version='1.0',
      description='server_for_my_messenger',
      author='Aleksandr',
      author_email='django@django.ru',
      packages=find_packages(),
      install_requires=['PyQT5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
