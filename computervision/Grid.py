import computervision.EwanCV.newEllipse as getSides
import computervision.EwanCV.checkMove as checkMove
import computervision.getMallet as getMallet
import computervision.CenterPoint as CP
list = []
#list of key centers

gui = None
boundarycenterleft = None
boundarycenterright = None
prec = (None, None)

def Swapped():
    isSwapped = getSides.Swapped()
    print("Swapped: ", isSwapped)
    return isSwapped

def generateList(GUI):
    global isSwapped, gui
    gui = GUI
    print(" Generating LIst")
    getSides.run(gui)
    # gui.updateCenterpointsImage()
    list = getSides.getList()
    return list

def getOffset(key, previous_coordinates = (None, None)):
    global gui, boundarycenterleft, boundarycenterright, prec
    if previous_coordinates == (None, None):
        previous_coordinates = prec
    boundarycenterleft, boundarycenterright = getSides.getBoundaryMidpoints()
    mallet, prevc = getMallet.run(gui, previous_coordinates, boundarycenterleft, boundarycenterright)
    prec = prevc
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

def monitorSides(gui):
    global boundarycenterleft, boundarycenterright
    bcl, bcr = checkMove.run(gui)
    if bcl is not None:
        if (abs(int(boundarycenterleft[0]) - int(bcl[0])) > 50) or (abs(int(boundarycenterleft[1]) - int(bcl[1])) > 50):
            gui.update_log("Xylophone appears to have moved. Please recalibrate")
    if bcr is not None:
        if (abs(int(boundarycenterright[0]) - int(bcr[0])) > 50) or (abs(int(boundarycenterright[1]) - int(bcr[1])) > 50):
            gui.update_log("Xylophone appears to have moved. Please recalibrate")
    return bcl, bcr



