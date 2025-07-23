# -*- coding: utf-8 -*-

name = 'mvl_asset_manager'
version = '0.1.0'

description = 'A Command Line Interface (CLI) for an Asset Manager.'

authors = ['DEEPAK THAPLIYAL']
help = [['README', 'README.md']] # Optional: If you have a README file

requires = [
    "mvl_core_pipeline",
    '~python-3', 
]

private_build_requires = [
    "python-3",
    "mvl_rez_package_builder",
    
]

# Optional: Define tools if your package has standalone executables
tools = [
    'asset-manager', # This refers to the alias or a script in 'bin'
]

build_command = 'python {root}/build.py {install}'

def commands():
    env.PYTHONPATH.append("{root}/python")
    env.PATH.append("{root}/bin")


tests = {
    "unit":{
        "command": "python -m unittest discover -s tests",
        "requires": ["python-3"],
    }
}