from setuptools import setup, find_packages

from external_dumper import DESCRIPTION, VERSION, NAME, AUTHOR_NAME, AUTHOR_EMAIL


install_requires = [
    item.strip() for item in open('requirements.txt', 'r').readlines()
    if item.strip()
]

setup(
	# info
    name='_'.join([
        item.lower()
        for item in NAME.split(' ')
    ]),
	description=DESCRIPTION,
	license='MIT',
    keywords=['Atom 3.3', 'spectroscopy'],

	# version
    version=VERSION,

	# author details
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,

	# setup directories
    packages=find_packages(),

	# setup data
    include_package_data=True,

	# requires
    install_requires=install_requires,
    python_requires='>=3.10',

)
