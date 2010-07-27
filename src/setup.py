#!/usr/bin/env python

from distutils.core import setup

setup(name="Backup DAR",
      version="0.1",
      description="Wrapper para Disk Archiver (dar)",
      author="Carlos Aguilar",
      author_email="caguilar@dwdandsolutions.com",
      url="http://www.dwdandsolutions.com/html/descargas/utilidades/backup.zip",
      licence="GPL",
      scripts=["backup.py"],
      packages=["core"]
)