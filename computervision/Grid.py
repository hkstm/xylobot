import computervision.EwanCV.getSides as getSides
import computervision.getMallet as getMallet
import computervision.CenterPoint as CP
list = []
#list of key centers



def generateList():
    print(" Generating LIst")
    getSides.run()
    list = getSides.getList()
    return list

def getOffset(key):
    mallet = getMallet.run()
    try:
        xoffset = mallet[0][0]-key.px
        yoffset = mallet[0][1]-key.py
    except:
        print("Mallet not found")
        return None
    return(xoffset, yoffset)
