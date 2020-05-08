#!/usr/bin/python3
import sys
import os
import base
curdirs = os.listdir(os.curdir)
def fileExist(filename,path=os.curdir):
    if path == os.curdir:
        dirs = curdirs
    else:
        dirs = os.listdir(path)
    if filename in dirs:
        return True
    else:
        return False
def helpHint():
    print('Usage: evental COMMAND')
    print()
    print('List of Commands:')
    print('    version                    to show the version of PyEvental version.')
    print('    run [directory]            to run an PyEvental project.')
    print('    newProject [project name]  to create a new project in the current working directory.')
    print('    newModule [module name]    to create a new module in the current working directory.')
    print('    rmMoudle [module name]     to remove a existing module in the current working directory.')
    os._exit(0)
argv = sys.argv
argc = len(sys.argv)
if argc == 1 or (argc == 2 and (argv[1]=='-h' or argv[1]=='--help')):
    helpHint()
if argc == 2:
    command = argv[1]
    if command == 'version':
        print('PyEvental Version 0.1, developed by ClementineZ.')
        os._exit(0)
    if command == 'run':
        if not fileExist('.evental'):
            print('Evental Error: This is not a evental project diretory. File \'.evental\' is required.')
            os._exit(0)
        else:
            if os.path.isdir('.evental'):
                print('Evental Error: .evental must be a file instead of a directory.')
                os._exit()
            with open('.evental','r') as f:
                fileString = f.read()
                fps = fileString.strip().split(' ')
                for fp in fps:
                    fp = fp.strip()
                    executable = True
                    if not fileExist(fp) or os.path.isdir(fp):
                        print('Evental Error: File {} does not exist.'+fp)
                        executable = False
                if executable:
                    base.main(fps)                
    else:
        if command == 'newProject' or command == 'newModule':
            print('Evental Error: Command '+command+' need a name')
            os._exit(0)
        else:
            helpHint()
if argc == 3:
    command = argv[1]
    name = argv[2]
    if command == 'newProject':
        if fileExist(name):
            print('File/Directory already exists. Find another name for you project.')
            os._exit(0)
        os.mkdir('./'+name)
        fs=open('./'+name+'/.evental','w')
        fs.close()
    elif command == 'newModule':
        if not fileExist('.evental'):
            print('This is not a evental project diretory. File \'.evental\' is required.')
            os._exit(0)
        if os.path.isdir('.evental'):
            print('Evental Error: .evental must be a file instead of a directory.')
            os._exit(0)
        else:
            with open('.evental','a') as f:
                f.write(name+' ')
                if not fileExist(name):
                    fs = open(name,'w')
                    fs.close()
    else:
        helpHint()
        os._exit(0)