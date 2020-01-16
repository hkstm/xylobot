import computervision.EwanCV.newEllipse as getSides
import computervision.getMallet as getMallet
import computervision.CenterPoint as CP
list = []
#list of key centers

def Swapped():
    isSwapped = getSides.Swapped()
    print("Swapped: ", isSwapped)
    return isSwapped

def generateList():
    global isSwapped
    print(" Generating LIst")
    getSides.run()
    #gui.updateCenterpointsImage()
    list = getSides.getList()
    return list

def getOffset(key, previous_coordinates = (None, None)):
    boundarycenterleft, boundarycenterright = getSides.getBoundaryMidpoints()
    mallet = getMallet.run(previous_coordinates, boundarycenterleft, boundarycenterright)
    try:
        xoffset = mallet[0][0]-key.px
        yoffset = mallet[0][1]-key.py
    except:
        print("Mallet not found")
        return (None, None)
    print("xoffset: ", xoffset)
    print("yoffset: ", yoffset)
    return(xoffset, yoffset)

def destroyWindows():
    getSides.destroyWindows()
    getMallet.destroyWindows()
    print("Windows destroyed")