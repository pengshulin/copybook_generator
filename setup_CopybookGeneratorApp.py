#coding:utf-8
from distutils.core import setup
import py2exe

setup(
    name=u'Copybook Generator',
    version='1.0',
    description='automatically generate copybooks',
    author='Peng Shulin',
    windows = [
        {
            "script": "CopybookGeneratorApp.py",
        }
    ],
    options = {
        "py2exe": {
            "compressed": 1,
            "optimize": 2,
            "dist_dir": "dist",
        }
    },
)
