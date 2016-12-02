from setuptools import setup, find_packages


setup(
    name='flask-mongo-model',
    version='0.0.3',
    description='A module provides basic ORM feature for MongoDB to Flask applications.',
    author='Ares Ou',
    author_email='aresowj@gmail.com',
    package_dir={'mongo_model': 'mongo_model'},
    packages=['mongo_model'],
    license='MIT',
    test_suite='',
    use_2to3=False,
    convert_2to3_doctests=[''],
    use_2to3_fixers=[''],
    use_2to3_exclude_fixers=[''],
)
