from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

packages = [
    'dlr_light_api',
    'dlr_light_api.datatypes'
]

setup(
    name='discord-linked-roles-light-api',
    version='v0.1.dev1',

    url='https://github.com/imPDA/discord-linked-roles-light-api',
    author='imPDA',
    author_email='impda@mail.ru',
    package_dir={'': 'src'},
    packages=packages,
    install_requires=requirements,
)
