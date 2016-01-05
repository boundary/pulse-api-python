from distutils.core import setup

setup(
    name='tspapi',
    version='0.1.0',
    url="http://boundary.github.io/pulse-api-python/",
    author='David Gwartney',
    author_email='david_gwartney@bmc.com',
    packages=['tspapi', ],
#    entry_points={
#        'console_scripts': [
#            'actionhandler = boundary.webhook_handler:main',
#        ],
#    },
#    scripts=[
#        'tsp-cli-env.sh',
#   ],
#    package_data={'boundary': ['templates/*']},
    license='Apache 2',
    description='Python Bindings for the TrueSight Pulse REST APIs',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests >= 2.3.0",
    ],
)
