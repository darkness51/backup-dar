#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os, sys, smtplib
from datetime import date
from email.MIMEText import MIMEText

# Loggers de alto nivel
logger = logging.getLogger("BackupDar")

class backupDar(object):
    def __init__(self, options, args):
        '''
        Clase que abstrae completamente la utilidad dar.
        Las opciones que soporta son las siguientes:
        options.filename = Nombre del archivo a generar
        '''