debug=False
problems = []
class Error():
    def __init__(self,msg):
        self.msg = msg
class Warning():
    def __init__(self,msg):
        self.msg = msg        
def log(*args,**kwargs):
    if debug==True:
        print('Debug:')
        print(*args,**kwargs)
def alog(*args,**kwargs):
    if debug==False:
        print('Debug:',end=' ')
        print(*args,**kwargs)
def warning(s):
    problems.append(Warning(s))
def error(s):
    problems.append(Error(s))
def show():
    warningNum = 0
    errorNum = 0
    for p in problems:
        if isinstance(p,Warning):
            print('Warning: ',p.msg)
            warningNum += 1
        else:
            print('Error: ',p.msg)
            errorNum += 1
    print('PyEvental:',errorNum,'error(s),',warningNum,'warning(s).')