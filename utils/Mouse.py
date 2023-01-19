class Mouse:
    pyautogui = ''


    def __init__(self, pyautogui):
        self.pyautogui = pyautogui
        return
    
    def clickOn(self, coords):
        for(x,y,w,h) in coords:
            self.pyautogui.click(x=(x+(w/2)), y=y)