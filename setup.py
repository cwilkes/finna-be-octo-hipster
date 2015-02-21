from setuptools import setup

setup(
    name='file-server',
    version='0.1',
    py_modules=['server'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        file-server=server:run_server
    ''',
)
