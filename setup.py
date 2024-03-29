from setuptools import setup, find_packages

setup(
    name='mithril',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests~=2.31.0',
                      'neo4j~=5.16.0',
                      'click~=8.1.7',
                      'XlsxWriter~=3.1.9',
                      'pandas~=2.0.3',
                      'thefuzz~=0.22.1',
                      'psycopg2-binary~=2.9.9',
                      'typesense~=0.19.0',
                      'sqlalchemy~=2.0.28',
                      'jsonlines~=4.0.0'
                      ],
    entry_points={
        'console_scripts': [
            'mithril = src.scripts.mithril:mithril',
        ],
    },
)
