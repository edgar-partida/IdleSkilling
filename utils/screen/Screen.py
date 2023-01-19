from resources.paths import *
class Screen:

    TOP = 'top'
    LEFT = 'left'
    WIDTH = 'width'
    HEIGHT = 'height'
    MONITOR = 'mon'
    TITLE = 'Idle Skilling game hack 1.0'

    mss = ""
    cv2 = ""
    numpy = ""
    click1 = False
    point = (0,0)
    image = ""
    monitorNumber = 1
    gameDimensions = { }

    def __init__(self, mss, cv2, numpy, mouse):
        self.mss = mss
        self.cv2 = cv2
        self.numpy = numpy
        self.mouse = mouse

    def getFullScreenOnMonitor(self):
        with self.mss.mss() as sct:
            mon = sct.monitors[self.monitorNumber]
            monitor = self.getDimensions(mon[self.TOP],mon[self.LEFT],
                mon[self.WIDTH],mon[self.HEIGHT],self.monitorNumber)
            self.gameDimensions[self.LEFT] = mon[self.LEFT]
            print(monitor)
            img = self.numpy.array(sct.grab(monitor))
            return img

    def screen_select(self, event,x,y,flags, params):
        cv2 = self.cv2
        if event == cv2.EVENT_LBUTTONDOWN:
                # if mousedown, store the x,y position of the mous
                self.click1 = True
                self.point1 = (x,y)
        elif event == cv2.EVENT_MOUSEMOVE and self.click1:
                # when dragging pressed, draw rectangle in image
                img_copy = self.image.copy()
                cv2.rectangle(img_copy, self.point1, (x,y), (0,0,255),2)
                cv2.imshow(self.TITLE, img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
                # on mouseUp, create subimage
                self.click1 = False
                self.gameAreaCoordinates = (self.point1[0],self.point1[1],x,y)
                self.gameDimensions = self.getDimensions(self.point1[0],self.getLeft(self.point1[1]),x,y,self.monitorNumber)
                cv2.destroyAllWindows()

    def showDependantImage(self, image):
        cv2 = self.cv2
        self.image = image
        cv2.namedWindow(self.TITLE)
        cv2.setMouseCallback(self.TITLE, self.screen_select)

        cv2.imshow(self.TITLE, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def selectGameArea(self):
        full_screen = self.getFullScreenOnMonitor()
        self.showDependantImage(full_screen)

    def takeGameScreenshot(self):
        with self.mss.mss() as sct:
            return self.numpy.array(sct.grab(self.gameDimensions))

    def showImage(self,image):
        cv2 = self.cv2
        cv2.imshow(self.TITLE, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def setMonitorNumber(self, number):
        self.monitorNumber = number
    
    def getDimensions(self, x,y,width,height, monitor):
        return {
                self.TOP: x,
                self.LEFT: y,
                self.WIDTH: width,
                self.HEIGHT: height,
                self.MONITOR: monitor
            }
    
    def getImageCoordinates(self, lookupImage, captureImage, threshold):
        matchingSpots = []
        imageWidth = lookupImage.shape[1]
        imageHeight = lookupImage.shape[0]
        result = self.cv2.matchTemplate(lookupImage, captureImage, self.cv2.TM_CCOEFF_NORMED)
        yloc, xloc = self.numpy.where(result >= threshold)
        for(x,y) in zip(xloc, yloc):
            matchingSpots.append([self.getLeft(x), int(y), int(imageWidth), int(imageHeight)])
        for(x,y,w,h) in matchingSpots:
            self.cv2.rectangle(captureImage,(x,y),(x+w,y+h),(0,255,255),2)
        return matchingSpots
    
    def getLeft(self, left):
        return int(self.gameDimensions[self.LEFT]) + int(left)

    def goToTraining(self):
        trainButtonImg = self.cv2.imread(TRAIN_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        matchingCoords = self.getImageCoordinates(trainButtonImg, self.takeGameScreenshot(), .9)
        self.mouse.clickOn(matchingCoords)
        
    def goToFight(self):
        fightButtonImg = self.cv2.imread(FIGHT_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        matchingCoords1 = self.getImageCoordinates(fightButtonImg, self.takeGameScreenshot(), .8)
        self.mouse.clickOn(matchingCoords1)


