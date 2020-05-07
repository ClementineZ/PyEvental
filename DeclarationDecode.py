import timeSpecifier
def decodeEventDeclaration(s):
    if isinstance(s,str) == False or len(s)<=5:
        return None
    if s[0]!='!':
        return None
    left = s.find('(')
    if left == -1:
        return None
    name=s[1:left]
    right = s.find(')')
    paras = s[left+1:right].split(',')
    while '' in paras:
        paras.remove('')
    return (name,paras)
def decodeTriggerDeclaration(s):
    if isinstance(s,str) == False or len(s)<=3:
        return None
    if s[0] not in ['@','#','$']:
        return None
    time = None
    if s[0] == '@':
        time = timeSpecifier.after
    elif s[0] == '#':
        time = timeSpecifier.before
    elif s[0] == '$':
        time = timeSpecifier.concurrent
    else:
        return None
    ep = s.find(' ')
    if ep == -1:
        name=None
        listen = s[1:s.find(':')]
        return (name,time,listen)
    listen = s[1:ep]
    
    zep = s.find(':')
    if zep==-1:
        name = None
    else:
        name = s[ep+1:zep]
    
    return (name,time,listen)
def decodeRelation(s):
    pass
def toPlain(code):
    s=''
    for c in code:
        s += c+'\n'
    return s
def paras2dict(event,*args,**kwargs):
    d = kwargs
    i = 0
    for p in event.paras:
        d[p] = args[i]
        i += 1
    return d

    
