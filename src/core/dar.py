#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import smtplib
from subprocess import Popen, PIPE
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
        options.server_admin_email = Especifica la direccion de correo a la que se enviara el resultado del backup
        options.server = Especifica el servidor que se usara para enviar el correo
        options.originate_address = Especifica la direccion de correo que se usara por el script
        options.originate_password = Especifica la clave de la direccion de correo que se usara por el script
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
        
    def run(self):
        self._runDar()
    
    def _runDar(self):
        """
        La ejecución de dar se hara aqui de acuerdo a las opciones que se le pasen
        """
        if (self._options.diferencial == True and self._options.completo == True):
            logger.critical("El backup solo puede ser incremental, diferencial o completo!")
        else:
            #TODO: Se agregua la fecla al nombre del archivo
            today = date.today()
            self.filename = self._options.filename + "_" + str(today)
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
                logger.critical("El archivo " + self.filename + " ya existe")
                sys.exit(1)
                
            if self._options.recFile and self._options.completo:
                logger.error("Solo se puede definir la opcion -r si se utiliza backup diferencial o incremental")
                sys.exit(1)
                
            self.backupInstruction = self.getBackupInstruction()
            #salida = os.popen(self.backupInstruction).read()
            backup = Popen(self.backupInstruction, stdout=PIPE, shell=True)
            (salida, errores) = backup.communicate() 
            if errores is not None:
                salida += " \n\nSe produjeron los siguientes errores:\n\n %s" % errores
            self.sendMail(salida)
            
    def getBackupInstruction(self):
        '''
        Funcion que genera la instruccion para realizar el backup dependiendo de las opciones utilizadas en la linea de comandos
        '''
        cadenaBackup = "dar "
        if not self._options.extract:
            cadenaBackup += "-c " + self._destinationDirectory + self.filename + " -R " + self._originDirectory + " -s " + self._options.size + " -D -y" + str(self._options.compresion)
        
        if len(self._options.excluir_compresion) > 0:
            for exc in self._options.excluir_compresion:
                cadenaBackup += " -Z " + "\"" + exc + "\""
                
        if self._options.excluidos != None:
            if len(self._options.excluidos) > 0:
                for excluido in self._options.excluidos:
                    cadenaBackup += " -P " + excluido
                    
        if self._options.diferencial:
            if self._options.recFile != None:
                cadenaBackup += " -A " + self._options.recFile
                
        return cadenaBackup
    
    def sendMail(self, mensaje):
        serverAdmin = self._options.server_admin_email
        mailServer = self._options.server
        mailServerPort = 25
        originateAddress = self.originate_address
        originatePassword = self.originate_password
        
        email_message = MIMEText(mensaje)
        email_message["From"] = originateAddress
        email_message["To"] = serverAdmin
        email_message["Subject"] = "Resultado del Backup"
        
        s = smtplib.SMTP(mailServer, mailServerPort)
        s.ehlo()
        s.starttls()
        print s.ehlo()
        s.login(originateAddress, originatePassword)
        s.sendmail(originateAddress, serverAdmin, email_message.as_string())
        s.close()