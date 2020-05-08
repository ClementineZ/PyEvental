class timeSpecifier:
    before = 0
    after = 1
    concurrent = 2
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

import debug
def wrapCode(obj):
    '''
    if isinstance(obj, Event):
        event = obj
    else:
        event = obj.listenEvent
    paraList = event.getParaList()
    codeList = ['def execution({}):'.format(paraList)]
    codeList += obj.code
    codeList += ['retv = execution({})'.format(paraList)]
    '''
    codeList = obj.code
    codeString = toPlain(codeList)
    #print(codeString)
    return codeString
def wrapEventCode(event):

    paraList = event.getParaList()
    codeList = ['def execution({}):'.format(paraList)]
    codeList += event.code
    codeList += ['retv = execution({})'.format(paraList)]


    codeString = toPlain(codeList)
    #print(codeString)
    return codeString
class Event():    
    def __init__(self,name,code,paras,module):
        self.name = name        
        self.paras = paras
        self.code = code
        self.code = wrapEventCode(self)
        self.triggers = [[],[],[]]
        self.liar = self.cheatPython()
        self.module = module
        #self.cheatPython()
    def run(self,globalDict,*args,**kwargs):
        #print(*args,**kwargs)
        runtimeDict = paras2dict(self,*args,**kwargs)
        
        for trig in self.triggers[timeSpecifier.before]:
            trig.run(globalDict,runtimeDict)
        debug.log(self.code)
        #print(self.name,'runtimeDict',runtimeDict)
        runtimeDict['retv']=None
        tempDict = {**globalDict,**self.module.globalDict}
        exec(self.code,tempDict,runtimeDict)
        for key in self.module.globalDict.keys():
            self.module.globalDict[key]=tempDict[key]
        del tempDict

        for trig in self.triggers[timeSpecifier.after]:
            trig.run(globalDict,runtimeDict)
        return runtimeDict['retv']
    def addTrigger(self,time,trigger):
        self.triggers[time].append(trigger)
    def getParaList(self):
        paraList=''
        length = len(self.paras)
        for _ in range(0,length):
            paraList += self.paras[_]
            if _ != length-1:
                paraList += ','
        return paraList
    def cheatPython(self):
        liar='def {}('.format(self.name)
        paraList = self.getParaList()
        liar += paraList+'):'
        liar += '\n\treturn director.invoke(\'{}\',{})\n'.format(self.name,paraList)        
        return liar
class Trigger():
    def __init__(self,code,time,listen,module,name=None):
        self.code = code
        self.time = time
        self.listen = listen
        self.listenEvent = None
        self.module = module
        if name == None:
            self.name = 'AnonymousTrigger'
        else:
            self.name = name
        #self.priority = None
    def run(self,globalDict,runtimeDict):

        #log('Here:',globals())
        debug.log(self.code)
        #debug.alog(*args,**kwargs)
        #print(self.name,'globalDict:',globalDict)
        #print(self.name,'RuntimeDict:',runtimeDict)
        tempDict = {**globalDict,**self.module.globalDict}
        exec(self.code,tempDict,runtimeDict)
        for key in self.module.globalDict.keys():
            self.module.globalDict[key]=tempDict[key]
        del tempDict
        #debug.alog(*args,**kwargs)
    
class Module():
    def __init__(self,fp,name=None):
        self.fp = fp
        if name == None:
            self.name = fp
        else:
            self.name = name
        self.events = []
        self.triggers = []
        self.paras=[]
        self.initCode = ''
        self.globalDict = {}
        if fp!=None:
            with open(fp,'r') as f:
                self.lines = f.read().split('\n')
        self.requiredModules = []   
        self.liar = ''     
    def compile(self):
        lines = self.lines
        length = len(lines)
        i = 0
        while lines[i].startswith('relate '):
            self.requiredModules.append(lines[i][8:len(lines[i])-1])
            i += 1
        initSp = i
        while True:
            line = lines[i]
            if len(line) == 0 or line == '':
                i += 1
                continue
            firstChar = line[0]
            if firstChar not in ['#','@','!','$']:
                self.initCode += line+'\n'
                i += 1
                continue
            else:
                break
        exec(self.initCode,{},self.globalDict)
        while i<=length-1:            
            line = lines[i]
            if len(line) == 0 or line == '':
                i += 1
                continue
            firstChar = line[0]
            if firstChar not in ['#','@','!','$']:
                debug.log('Bad Declaration at line',i)
                exit()
            declaration = line  
            if firstChar == '!':
                (name,paras)=decodeEventDeclaration(declaration)
            else:
                (name,time,listen)=decodeTriggerDeclaration(declaration)          
            i += 1
            sp = i
            while i<=length-1:
                if len(lines[i])==0:
                    i += 1
                    continue
                FirstChar = lines[i][0]
                if FirstChar not in ['#','@','!','$']:
                    i += 1
                else:
                    break
            if firstChar == '!':
                code = lines[sp:i]
            else:
                codeTemp = lines[sp:i]
                code = []
                for c in codeTemp:
                    if len(c) == 0:
                        continue
                    code.append(c[1:len(c)])
            
            
            if firstChar == '!':
                self.events.append(Event(name, code, paras,self))
            else:
                self.triggers.append(Trigger(code,time,listen,self,name))
            
        for e in self.events:
            self.liar += e.liar
    def toString(self):
        s = 'module '+self.fp+'\n'
        for e in self.events:
            s += 'Event:{} paras:{} \n'.format(e.name,e.paras)
            s+='Code:\n'
            for c in e.code:
                s += c + '\n'
        for t in self.triggers:
            s += 'Trigger:{} time:{} listen:{}\n'.format(t.name,t.time,t.listen)
            s+='Code:\n'
            for c in t.code:
                s += c + '\n'
        return s
class Director():
    def __init__(self,fps):
        self.modules = []
        
        self.eventPool = []
        self.triggerPool = []
        self.requiredModules = []
        self.liar = ''
        self.globalDict = {'director':self}
        for fp in fps:
            m = Module(fp)
            m.compile()
            self.modules.append(m)
            self.requiredModules += m.requiredModules
            self.eventPool += m.events
            self.triggerPool += m.triggers
            self.liar += m.liar
        for rm in self.requiredModules:
            if rm not in fp:
                debug.error('Require module',rm)
                exit()
        listenList = [trig.listen for trig in self.triggerPool]
        eventList = [event.name for event in self.eventPool]
        for l in listenList:
            if l not in eventList:
                debug.log('Warning: Lisnening an unexist event',l)
        for trig in self.triggerPool:
            for event in self.eventPool:
                if trig.listen == event.name:
                    event.addTrigger(trig.time,trig)
                    trig.listenEvent = event
                    trig.code = wrapCode(trig)
    def toString(self):
        s = 'Director:\nModules:'
        for m in self.modules:
            s += m.name+','
        s += '\nEvents:'
        for e in self.eventPool:
            s += e.name+','
        return s
    def invoke(self,name,*args,**kwargs):
        debug.log('Director invokes',name)
        find=False
        for e in self.eventPool:
            if e.name==name:
                
                return e.run(self.globalDict,*args,**kwargs)
                find=True
        if find==False:
            debug.log('Cannot find event',name)
            exit()
    def run(self):
        self.invoke('main')
    def implementModuleFromFile(self):
        pass
    def removeModuleByName(self):
        pass

def main(fps):
    director = Director(fps)
    debug.log(director.liar)
    exec(director.liar,director.globalDict)#Add cheat functions to globalDict
    director.run()



            
        
