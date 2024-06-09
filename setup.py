from setuptools import setup, find_packages

setup(
    name='pickforme',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
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
