states =[i for i in range(16)]
values=[0 for _ in range(16)]
actions=["n","e","s","w"]
ds_actions={"n":-4,"e":1,"s":4,"w":-1}
gamma=1.00

# s为当前的state,a为要采取的action
def nextState(s,a):
    next_state=s
    #边界判断
    if(s%4==0 and a=="w") or (s<4 and a=="n") or \
      ((s+1)%4==0 and a=="e") or (s>11 and a=="s"):
        pass
    else:
        ds=ds_actions[a]
        next_state=s+ds
    return next_state

#计算某一状态的即时奖励
def rewardOf(s):
    return 0 if s in [0,15] else -1

def isEnd(s):
    return s in [0,15]

#获取当前状态的下一步的状态
def getSuccessors(s):
    successors=[]
    if(isEnd(s)):
        return successors
    for a in actions:
        next_state=nextState(s,a)
        successors.append(next_state)
    return successors

def updateValue(s):
    successors=getSuccessors(s)
    newValue=0
    num=4
    reward= rewardOf(s)
    for next_state in successors:
        newValue+= 1.00/num*(reward + gamma *values[next_state])
    return newValue

def performOneIteration():
    newValues=[0 for _ in range(16) ]
    for s in states:
        newValues[s]=updateValue(s)
