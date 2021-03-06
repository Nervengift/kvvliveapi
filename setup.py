import setuptools

setuptools.setup(
    name='kvvliveapi',
    version='0.2.1',
    packages=setuptools.find_packages(),
    author='Nervengift',
    author_email='github@nervengiftlabs.de',
    description='KVV live API bindings',
    keywords='kvv api',
    url='https://github.com/Nervengift/kvvliveapi',
    install_requires=['docopt', 'requests']
)
