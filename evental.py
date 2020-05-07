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
def badHint():
    print('Command listed below is required: newProject, run or newModule.')
    print('Examples:')
    print('evental newProject HelloWorld')
    print('evental run')
    print('evental newModule AModule')
    os._exit(0)
argv = sys.argv
argc = len(sys.argv)
if argc == 1 or (argc == 2 and (argv[1]=='-h' or argv[1]=='--help')):
    badHint()
if argc == 2:
    command = argv[1]
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
            badHint()
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
        badHint()
        os._exit(0)