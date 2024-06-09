from setuptools import setup, find_packages

setup(
    name='pickforme',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'prettytable',
        'sqlalchemy',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'pickforme = pickforme.main:main',
        ],
    },
)
