from setuptools import setup, find_packages

setup(
    name='picamkit',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'jinja2==3.1.3',
        'ruamel.yaml==0.18.6'
    ],
    entry_points={
        'console_scripts': [
            'ck-run=picamkit.tools.runner:run',
            'ck-caminfo=picamkit.tools.camera_info:run',
        ]
    }
)

