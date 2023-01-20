from resources.paths import *
from utils.Constants import *
class Screen:

    mss = ""
    cv2 = ""
    numpy = ""
    click1 = False
    point = (0,0)
    image = ""
    monitorNumber = 1
    gameDimensions = { }
    gameXDimensions = { }

    def __init__(self, mss, cv2, numpy, mouse, sleep):
        self.mss = mss
        self.cv2 = cv2
        self.numpy = numpy
        self.mouse = mouse
        self.sleep = sleep

    def getFullScreenOnMonitor(self):
        with self.mss.mss() as sct:
            mon = sct.monitors[self.monitorNumber]
            monitor = self.getDimensions(mon[TOP],mon[LEFT],
                mon[WIDTH],mon[HEIGHT],self.monitorNumber)
            self.gameDimensions[LEFT] = mon[LEFT]
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
                cv2.imshow(TITLE, img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
                # on mouseUp, create subimage
                self.click1 = False
                self.gameAreaCoordinates = (self.point1[0],self.point1[1],x,y)
                self.gameDimensions = self.getDimensions(self.point1[0],self.getLeft(self.point1[1]),x,y,self.monitorNumber)
                self.gameXDimensions = self.getXDimensions(self.point1[0],self.getLeft(self.point1[1]),x,y,self.monitorNumber)
                cv2.destroyAllWindows()

    def showDependantImage(self, image):
        cv2 = self.cv2
        self.image = image
        cv2.namedWindow(TITLE)
        cv2.setMouseCallback(TITLE, self.screen_select)

        cv2.imshow(TITLE, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def selectGameArea(self):
        full_screen = self.getFullScreenOnMonitor()
        self.showDependantImage(full_screen)

    def takeGameScreenshot(self):
        with self.mss.mss() as sct:
            return self.numpy.array(sct.grab(self.gameDimensions))
    
    def takeXScreenshot(self):
        with self.mss.mss() as sct:
            return self.numpy.array(sct.grab(self.gameXDimensions))


    def showImage(self,image):
        cv2 = self.cv2
        cv2.imshow(TITLE, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def setMonitorNumber(self, number):
        self.monitorNumber = number
    
    def getDimensions(self, x,y,width,height, monitor):
        return {
                TOP: x,
                LEFT: y,
                WIDTH: width,
                HEIGHT: height,
                MONITOR: monitor
            }
    
    def getXDimensions(self, x,y,width,height, monitor):
        return {
                TOP: height - 20,
                LEFT: y + (width - 100),
                WIDTH: 100,
                HEIGHT: 20,
                MONITOR: monitor
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
        return int(self.gameDimensions[LEFT]) + int(left)

    def goToTraining(self):
        trainButtonImg = self.cv2.imread(TRAIN_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        matchingCoords = self.getImageCoordinates(trainButtonImg, self.takeGameScreenshot(), .9)
        self.mouse.clickOn(matchingCoords,0.5)
        
    def goToFight(self):
        fightButtonImg = self.cv2.imread(FIGHT_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        matchingCoords1 = self.getImageCoordinates(fightButtonImg, self.takeGameScreenshot(), .8)
        self.mouse.clickOn(matchingCoords1,0.5)

    def trainCurrentWindow(self, numberOfUpgrades):
        currentScreen = self.takeGameScreenshot()
        valueButtonImg = self.cv2.imread(VALUE_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        valueCoords = self.getImageCoordinates(valueButtonImg,currentScreen,.9)
        speedButtonImg = self.cv2.imread(SPEED_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        speedCoords = self.getImageCoordinates(speedButtonImg,currentScreen,.9)
        upgradeButtonImg = self.cv2.imread(UPGRADE_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        upgradeCoords = ''
        for (x,y,w,h) in valueCoords:
            self.mouse.clickOnSingle(x,y,w,h,0.4)
            if upgradeCoords == '':
                upgradeCoords = self.getImageCoordinates(upgradeButtonImg,self.takeGameScreenshot(),.8)
            for x in range(numberOfUpgrades):
                self.mouse.clickOn(upgradeCoords,0.1)
        for (x,y,w,h) in speedCoords:
            self.mouse.clickOnSingle(x,y,w,h,0.6)
            if upgradeCoords == '':
                upgradeCoords = self.getImageCoordinates(upgradeButtonImg,self.takeGameScreenshot(),.8)
            for x in range(numberOfUpgrades):
                self.mouse.clickOn(upgradeCoords,0.1)

    def set5X(self):
        xTimeImg = self.cv2.imread(TIMES_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        while True:
            xTimesLookup = self.takeXScreenshot()
            speedCoords = self.getImageCoordinates(xTimesLookup,xTimeImg,.9)
            if len(speedCoords) > 0:
                break
            self.mouse.clickOnSingleCoords(self.gameDimensions[LEFT]+self.gameDimensions[WIDTH]-20,
                                        self.gameDimensions[TOP]+self.gameDimensions[HEIGHT]-20
                                        ,0.1)
    def singleClickOnImagePath(self, path, threshold, sleepTime):
        gymButtonImg = self.cv2.imread(path, self.cv2.IMREAD_UNCHANGED)
        matchingCoords1 = self.getImageCoordinates(gymButtonImg, self.takeGameScreenshot(), threshold)
        self.mouse.clickOn(matchingCoords1,sleepTime)

    def buySkillersIfNeeded(self):
        currentScreen = self.takeGameScreenshot()
        valueButtonImg = self.cv2.imread(VALUE_BUTTON_PATH, self.cv2.IMREAD_UNCHANGED)
        valueCoords = self.getImageCoordinates(valueButtonImg,currentScreen,.9)
        if len(valueCoords) == 5:
            return
        self.singleClickOnImagePath(SKILLER_BUTTON_PATH,0.9,0.2)

    def usePowers(self):
        self.goToFight()
        self.singleClickOnImagePath(CHANGE_REVERSED_BUTTON_IMG,0.8,0.2)
        self.singleClickOnImagePath(CLAW_BUTTON_IMG,0.8,0.2)
        # self.singleClickOnImagePath(POISON_BUTTON_IMG,0.8,0.1)
        self.singleClickOnImagePath(METEOR_BUTTON_IMG,0.8,0.2)
        self.singleClickOnImagePath(FLURRY_BUTTON_IMG,0.8,0.2)
        self.singleClickOnImagePath(SMITE_BUTTON_IMG,0.8,0.2)
        self.singleClickOnImagePath(CHANGE_BUTTON_IMG,0.8,0.2)
        self.singleClickOnImagePath(HEAL_BUTTON_IMG,0.8,0.2)
        self.singleClickOnImagePath(VISION_BUTTON_IMG,0.8,0.2)
        # self.singleClickOnImagePath(MIDAS_BUTTON_IMG,0.8,0.1)
        # self.singleClickOnImagePath(SEAL_BUTTON_IMG,0.8,0.1)
        self.singleClickOnImagePath(VALOR_BUTTON_IMG,0.8,0.2)
        self.singleClickOnImagePath(CHANGE_REVERSED_BUTTON_IMG,0.8,0.2)

    def trainAll(self):
        self.goToTraining()
        self.set5X()
        self.singleClickOnImagePath(GYM_BUTTON_PATH,0.8,0.5)
        self.buySkillersIfNeeded()
        self.trainCurrentWindow(1)
        self.singleClickOnImagePath(DOJO_BUTTON_PATH,0.8,0.5)
        self.buySkillersIfNeeded()
        self.trainCurrentWindow(1)
        self.singleClickOnImagePath(DESERT_BUTTON_PATH,0.8,0.5)
        self.buySkillersIfNeeded()
        self.trainCurrentWindow(1)
        self.singleClickOnImagePath(POND_BUTTON_PATH,0.8,0.5)
        self.buySkillersIfNeeded()
        self.trainCurrentWindow(1)
        self.goToFight()