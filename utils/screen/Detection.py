class Detection:

    def __init__(self,cv2):
        self.cv2 = cv2
        return
    
    def getImageCoordinates(self, lookupImage, captureImage, threshold):
        matchingSpots = []
        imageWidth = lookupImage.shape[1]
        imageHeight = lookupImage.shape[0]
        captureImageWithNoAlpha = captureImage[:,:,:3]
        result = self.cv2.matchTemplate(lookupImage, captureImageWithNoAlpha, self.cv2.TM_CCOEFF_NORMED)
        yloc, xloc = numpy.where(result >= threshold)
        for(x,y) in zip(xloc, yloc):
            matchingSpots.append([int(x), int(y), int(imageWidth), int(imageHeight)])
            matchingSpots.append([int(x), int(y), int(imageWidth), int(imageHeight)])
            self.cv2.rectangle(captureImage, (x,y), (x+imageWidth,y+imageHeight),
            (0,255,255),2)
        print(matchingSpots)
        return matchingSpots