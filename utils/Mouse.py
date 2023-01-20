class Mouse:
    pyautogui = ''


    def __init__(self, pyautogui, sleep):
        self.pyautogui = pyautogui
        self.sleep = sleep
        return
    
    def clickOn(self, coords, sleep):
        for(x,y,w,h) in coords:
            self.pyautogui.click(x=(x+(w/2)), y=y+(h/2))
            if sleep:
                self.sleep(sleep)
            
    
    def clickOnSingle(self, x, y, w, h, sleep):
        self.pyautogui.click(x=(x+(w/2)), y=y+(h/2))
        if sleep:
            self.sleep(sleep)
    
    def clickOnSingleCoords(self, x, y, sleep):
        self.pyautogui.click(x=x, y=y)
        if sleep:
            self.sleep(sleep)