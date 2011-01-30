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
        Crea una nueva clase que se encarga de todas las tareas que realiza dar
        desde crear backups hasta restaurarlos.
        Las opciones son facilmente capturadas por optparse.
        Las opciones que soporta son las siguientes:
        options.filename = la ruta del archivo a generar
        options.compresion = el nivel de compresion a utilizar
        options.verbose = indica el nivel de logeo de ejecucion
        options.excluir_compresion = directorios o archivos a excluir de la compresion
        options.incremental = Especifica si se hara un backup incremental
        options.diferencial = Especifica si se hara un backup diferencial
        options.completo = Especifica si se hara un backup completo
        options.recDir = Especifica el directorio al que se le hara backup
        options.size = Especifica el tamaño de los archivos en los que se dividira el backup
        options.extract = Especifica si lo que se desea hacer es extraer los archivos del backup
        '''
        
        # Opciones básicas sobre el backup
        self._options = options
        # Directorio de Origen
        self._originDirectory = args[0]
        # Directorio de Destino
        self._destinationDirectory = args[1]
        #TODO: Creo que aqui va la configuracion pero averiguar con certeza
                
        if self._options.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # creamos un formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        # Agregamos al Console Handler al logger
        logger.addHandler(ch)