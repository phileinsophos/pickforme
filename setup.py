from setuptools import setup, find_packages

setup(
    name='pickforme',
    version='0.1.1',
    author='phileinsophos',
    author_email='oapatil24@gmail.com',
    description='A tool to manage and pick activities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/phileinsophos/pickforme',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'pickforme=pickforme.main:main',
        ],
    },
)
