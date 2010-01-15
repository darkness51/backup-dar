# -*- coding: utf-8 -*-
#
# backup - un front end en linea de comandos para dar
#
# Copyright (c) 2009 Carlos Aguilar <caguilar@dwdandsolutions.com>

import logging
import subprocess
import os
import sys

# Loggers de alto nivel
logger = logging.getLogger("BackupDar")

class backupDar (object):
    def __init__(self, options, args):
        """
        Crea una nueva clase que se encarga de todas las tareas que realiza dar
        desde crear backups hasta restaurarlos.
        Las opciones son facilmente capturadas por optparse.
        Las opciones que soporta son las siguientes:
            options.filename = la ruta del archivo a generar
            options.compresion = el nivel de compresion a utilizar
            options.verbose = indica el nivel de logeo de ejecucion
            options.excluir = directorios o archivos a excluir
            options.incremental = Especifica si se hara un backup incremental
            options.diferencial = Especifica si se hara un backup diferencial
            options.completo = Especifica si se hara un backup completo
            options.recDir = Especifica el directorio al que se le hara backup
            options.size = Especifica el tamaño de los archivos en los que se dividira el backup
        """
        
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
        
    def run(self):
        self._runDar()
        
    def _runDar(self):
        """
        La ejecución de dar se hara aqui de acuerdo a las opciones que se le pasen"
        """
        if (self._options.incremental == True and self._options.diferencial == True and self._options.completo == True):
            logger.critical("El backup solo puede ser incremental, diferencial o completo!")
        else:
            #TODO: Aqui va toda la rutina para generar el backup
            self.filename = self._options.filename
            file = self.filename.split(".")

            if len(file) > 1:
                logger.error('Debe eliminar la extension: %s del nombre del archivo', file[1])
                sys.exit(1)
                
            if not os.path.isdir(self._originDirectory) and not os.path.exists(self._originDirectory):
                logger.error("La ruta de origen debe de ser un directorio")
                sys.exit(1)
            
            if not os.path.isdir(self._destinationDirectory) and not os.path.exists(self._destinationDirectory):
                logger.error("La ruta de destino debe de ser un directorio, compruebe que el directorio exista")
                sys.exit(1)
                
            if os.path.exists(self._options.filename):
                logger.critical("El archivo "+self._options.filename+" ya existe")
                sys.exit(1)
                
            if self._options.recFile and self._options.completo:
                logger.error("Solo se puede definir la opcion -r si se utiliza backup diferencial o incremental")
                sys.exit(1)
            
            if self._options.diferencial:
                self.backupInstruction = self.getDiferencialBackupInstruction()
                
            if self._options.incremental:
                self.backupInstruction =  self.getIncrementalBackupInstruction()
                
            if self._options.completo:
                self.backupInstruction = self.getCompleteBackupInstruction()
            
            subprocess.call(self.backupInstruction, shell=True)
    
    def getDiferencialBackupInstruction (self):
        return "dar -c "+self._destinationDirectory + self._options.filename +" -R "+ self._originDirectory +" -s "+self._options.size+" -D -y"+self._options.compresion+" -Z \"*.gz\" -Z \"*.zip\" -A "+self._options.recFile
    
    def getCompleteBackupInstruction (self):
        return "dar -c "+self._destinationDirectory + self._options.filename +" -R "+ self._originDirectory +" -s "+self._options.size+" -D -y"+self._options.compresion+" -Z \"*.gz\" -Z \"*.zip\""
    
    def getIncrementalBackupInstruction (self):
        return "dar -c "+self._destinationDirectory + self._options.filename +" -R "+ self._originDirectory +" -s "+self._options.size+" -D -y"+self._options.compresion+" -Z \"*.gz\" -Z \"*.zip\" -A "+self._options.recFile
         
