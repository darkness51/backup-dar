#!/usr/bin/env python

import os, sys
from core.backup import backupDar
from optparse import OptionParser

def main():
    usage = "Usage: %prog [options] origin_directory dest_directory"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename", help="Ruta completa del archivo de backup", metavar="BKFILE")
    parser.add_option("-c", "--compresion", dest="compresion", help="Fija el nivel de compresion, default 1, max 9", default=9, metavar="NIVEL")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)
    parser.add_option("-e", "--exclude", dest="excluir", help="Excluye el archivo o directorio dado", metavar="FILE")
    parser.add_option("-i", "--incremental", action="store_true", dest="incremental", help="Especifica si el tipo de backup es incremental", default=False)
    parser.add_option("-d", "--diferencial", action="store_true", dest="diferencial", help="Especifica si el tipo de backup es diferencial", default=False)
    parser.add_option("-C", "--complete", action="store_true", dest="completo", help="Especifica si el tipo de backup sera completo", default=False)
    parser.add_option("-r", "--resource", dest="recFile", help="Especifica el archivo de backup completo", metavar="FILE")
    parser.add_option("-s", "--size", dest="size", help="Especifica el tamano en MB en el que se dividiran los archivos", metavar="TAMANO")

    (options, args) = parser.parse_args()
    
    if len(args) <= 1:
        parser.error("Numero de argumentos incorrectos")
        
    dar = backupDar(options, args)
    dar.run()
        
if __name__ == "__main__":
    main()
