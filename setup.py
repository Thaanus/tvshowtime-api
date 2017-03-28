from setuptools import setup

def read(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='tvst',
    version='0.1',
    description='Thin Wrapper around the TvShowTime Rest API',
    long_description=read('README.md'),
    url='',
    author='onanypoint',
    author_email='onanypoint@gmail.com',
    license='MIT',
    packages=['tvst'],
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    zip_safe=False
)