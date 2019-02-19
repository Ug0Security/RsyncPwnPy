#!/usr/bin/env python3

import sys, os, argparse
from multiprocessing import Pool
import socket


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE =range(8)

def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)


def printout(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)

def findvnc(domain):
    
    
    try:
        host = domain.rstrip() + "::"
        
        retvalue = os.popen("torify rsync --list-only " + host + " 2> /dev/null").readlines()
        list=[]
        for x in retvalue: 
            list.append(x.split(" ",1)[0])
        
        for i in list: 
            retvalue2 = os.popen("torify sshpass rsync --list-only  " + host + i + " 2> /dev/null").readlines()
            print (host + i + "\n" + "".join([str(x) for x in retvalue2]), file=open(OUTPUTFILE, "a"))
       


    except Exception as e: 
        print(e)
        
           
        
   
   

if __name__ == '__main__':
    

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='results_rsync.txt', help='input file')
    parser.add_argument('-o', '--outputfile', default='Rsync_list.txt', help='output file')
    parser.add_argument('-t', '--threads', default=5, help='threads')
    args = parser.parse_args()

    DOMAINFILE=args.inputfile
    OUTPUTFILE=args.outputfile
    MAXPROCESSES=int(args.threads)
    print(" ##                                      .__                                    ##")
    print(" ##	  ____  _____    ___  _______    |  |   ____  __ _________              ##")
    print(" ##	_/ ___\ \__  \   \  \/ /\__  \   |  | _/ __ \|  |  \_  __ \             ##")
    print(" ##	\  \___  / __ \_  \   /  / __ \_ |  |_\  ___/|  |  /|  | \/             ##")
    print(" ##	 \___  > ____  /   \_/  (____  / |____/\___  >____/ |__|                ##")	
    print(" ##	     \/      \/              \/            \/                           ##")
    print(" ##	  _____       .__                 .__           ___.   .__  __          ##")
    print(" ##	_/ ____\____  |__|______   ____   |  | _____    \_ |__ |__|/  |_  ____  ##")
    print(" ##	\   __\ \__  \|  \_  __ \_/ __ \  |  | \__  \    | __ \|  \   __\/ __ \ ##")
    print(" ##	 |  |   / __ \|  ||  | \/\  ___/  |  |__/ __ \_  | \_\ \  ||  | \  ___/ ##")
    print(" ##	 |__|  (____  /__||__|    \___  > |____(____  /  |___  /__||__|  \___  >##")
    print(" ##	            \/                \/            \/       \/              \/ ##")

    print("Scanning...")
    pool = Pool(processes=MAXPROCESSES)
    domains = open(DOMAINFILE, "r").readlines()
    pool.map(findvnc, domains)
    print("Finished")
