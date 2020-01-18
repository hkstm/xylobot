import computervision.EwanCV.newEllipse as getSides
import computervision.getMallet as getMallet
import computervision.CenterPoint as CP
list = []
#list of key centers

gui = None

def Swapped():
    isSwapped = getSides.Swapped()
    print("Swapped: ", isSwapped)
    return isSwapped

def generateList(GUI):
    global isSwapped, gui
    gui = GUI
    print(" Generating LIst")
    getSides.run(gui)
    gui.updateCenterpointsImage()
    list = getSides.getList()
    return list

def getOffset(key, previous_coordinates = (None, None)):
    global gui
    boundarycenterleft, boundarycenterright = getSides.getBoundaryMidpoints()
    mallet = getMallet.run(gui, previous_coordinates, boundarycenterleft, boundarycenterright)
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