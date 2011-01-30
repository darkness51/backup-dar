#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from core.dar import backupDar
from optparse import OptionParser

def main():
    usage = "Usage: %prog [options] origin_directory dest_directory"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename", help="Nombre del archivo de backup", metavar="BKFILE")
    parser.add_option("-c", "--compresion", dest="compresion", help="Fija el nivel de compresion, default 1, max 9", default=9, metavar="NIVEL")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)
    parser.add_option("-Z", "--exclude-compression", dest="excluir_compresion", action='append', type='string',  help="Excluye el archivo o directorio dado", metavar="FILE")
    parser.add_option("-d", "--diferencial", action="store_true", dest="diferencial", help="Especifica si el tipo de backup es diferencial", default=False)
    parser.add_option("-C", "--complete", action="store_true", dest="completo", help="Especifica si el tipo de backup sera completo", default=False)
    parser.add_option("-r", "--resource", dest="recFile", help="Especifica el archivo de backup completo", metavar="FILE")
    parser.add_option("-s", "--size", dest="size", help="Especifica el tamano en MB en el que se dividiran los archivos", metavar="TAMANO")
    parser.add_option("-x",  "--extract",  action="store_true",  dest="extract",  help="Especifica  si se extraera el backup")
    parser.add_option("-P", "--prune", action="append", dest="excluidos", default=None, help="Especifica los archivos o carpetas que no se incluiran en el backup")
    parser.add_option("-se", "--server-admin", dest="server_admin_email", help="Nombre del administrador del sistema o sea, la persona que recibira el correo", metavar="SYSADMIN")
    parser.add_option("-s", "--server", dest="server", help="Servidor de correos a usar", metavar="SERVER")
    parser.add_option("-oa", "--originate-address", dest="originate_address", help="Correo que usara el script para enviar el resultado", metavar="EMAIL")
    parser.add_option("-op", "--originate-password", dest="originate_password", help="Password del correo que usara el script", metavar="PASSWORD")

    (options, args) = parser.parse_args()
    if  not os.path.isfile("/usr/bin/dar"):
        print "La utilidad dar no esta instalada. Intente instalarla mediante apt-get"
        sys.exit(1)
        
    if len(args) <= 1:
        parser.error("Numero de argumentos incorrectos")
        
    dar = backupDar(options, args)
    dar.run()
        
if __name__ == "__main__":
    main()
