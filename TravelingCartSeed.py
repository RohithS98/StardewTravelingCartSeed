import TravelingCart
import heapq
import Utility

class Constraint:

    def __init__(self, itemList, dayRange):
        self.itemList = set(itemList)
        self.toFind = set(itemList)
        self.startDay = dayRange[0]
        self.endDay = dayRange[1]+1

    def reset(self):
        self.toFind = self.itemList.copy()

    def isCompleted(self):
        return len(self.toFind) == 0
    
    def updateCompleted(self, foundItems):
        fIS = set(foundItems)
        updatedItems = self.toFind & fIS
        self.toFind -= fIS
        return updatedItems

class PartConstr(Constraint):

    def __init__(self,itemList,dayRange, minReq):
        Constraint.__init__(self,itemList,dayRange)
        self.minReq = minReq

    def isCompleted(self):
        return len(self.toFind) <= (len(self.itemList) - self.minReq)

def isValidDay(day):
    if day % 7 in (0,5):
        return True
    return False

def nextValidDay(day):
    return day + (5 if day%7 < 5 else 7) - (day % 7)

def checkSeed(seed, constrList):

    HARD_CAP = 5000

    if len(constrList) == 0:
        return True, dict()
    eventQueue = []
    for ind,constr in enumerate(constrList):
        eventQueue.append((constr.startDay, 0, ind))
        eventQueue.append((constr.endDay, 1, ind))
    heapq.heapify(eventQueue)
    flag = True
    currDay = eventQueue[0][0]
    actConstrInd = set()
    shopList = {}
    while flag:
        ## Update active constraints
        while len(eventQueue) > 0 and eventQueue[0][0] <= currDay:
            newEv = heapq.heappop(eventQueue)
            if newEv[1] == 1:   #Remove constraint
                if not constrList[newEv[2]].isCompleted():
                    return False, dict()
                actConstrInd -= set([newEv[2]])
            elif newEv[1] == 0: #Add constraint
                actConstrInd.add(newEv[2])
            else:
                raise NameError     #Should not reach here
        
        ## If there are no active constraints, either we are done or skip to the next date
        if len(actConstrInd) == 0:
            if len(eventQueue) == 0:
                return True, shopList
            else:
                currDay = eventQueue[0][0]
                continue
        
        if isValidDay(currDay):
            stock = TravelingCart.getTravelingMerchantStock(seed, currDay)
            found = set()
            toDelete = set()
            for i in actConstrInd:
                found = found.union(constrList[i].updateCompleted(stock.keys()))
                if constrList[i].isCompleted():
                    toDelete.add(i)
            actConstrInd -= toDelete
            if len(found) > 0:
                shopList[currDay] = found
        
        currDay = nextValidDay(currDay)

        if currDay >= HARD_CAP:
            flag = False

    return False, dict()


def convertItemList(itemNameList):
    return set(map(lambda x : int(x) if x.isnumeric() else TravelingCart.ObjectIDFromName[x], itemNameList))

if __name__ == "__main__":
    pass
    #for i in range(12,55,7):
    #    print(i,TravelingCart.getTravelingMerchantStock(100,i).keys())
    #    print(i+2,TravelingCart.getTravelingMerchantStock(100,i+2).keys())
    #res = checkSeed(100,[Constraint([766,415], (8,19))])
    #print(res[1])