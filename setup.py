from setuptools import setup, find_packages

setup(
    name='picamkit',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ck-run=picamkit.tools.ck_run:run',
            'ck-caminfo=picamkit.tools.ck_caminfo:run',
        ]
    }
)

