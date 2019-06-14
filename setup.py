"""Setup module for zigpy_deconz_parser. """

from setuptools import find_packages, setup

setup(
    name="zigpy-deconz-parser",
    version="0.0.2",
    description="Homeassistant log file parser for zigpy-deconz radio",
    url="http://github.com/zha-ng/zigpy-deconz-parser",
    author="Alexei Chetroi",
    author_email="alexei.chetroi@outlook.com",
    license="GPL-3.0",
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'console_scripts': [
            'zigpy-deconz-parser=zigpy_deconz_parser.main:main'
        ],
    },
    install_requires=[
        'pyserial-asyncio',
        'zigpy-homeassistant',
    ],
    tests_require=[
        'pytest',
    ],
)
