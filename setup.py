from setuptools import setup

setup(
    name='dbcl',
    long_description='',
    packages=['dbcl'],
    entry_points={
        'console_scripts': ['dbcl=dbcl.command_line:command_loop'],
    },
    include_package_data=True,
    install_requires=[
        'sqlalchemy',
        'prompt_toolkit',
        'pygments',
        'terminaltables',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
        'coverage',
    ],
)
