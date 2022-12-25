from setuptools import setup, find_packages

setup(name='message_client',
      version='1.0',
      description='client_for_messenger',
      author='Aleksandr',
      author_email='django@django.ru',
      packages=find_packages(),
      install_requires=['PyQT5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
