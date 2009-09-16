#!/usr/bin/env python

import os, sys
from optparse import OptionParser

def main():
    usage = "Usage: %prog [options] origin_directory dest_directory"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename", help="Nombre del archivo de backup", metavar="BKFILE")
    parser.add_option("-c", "--compresion", dest="compresion", help="Fija el nivel de compresion, default 6, max 9", default=6, metavar="NIVEL")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)

    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("Numero de argumentos incorrectos")
        
    if options.verbose:
        print "Verbose seleccionado" 
        
if __name__ == "__main__":
    main()