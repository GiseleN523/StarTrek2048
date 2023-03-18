import random
import math
from graphics import *

class Game:
    def __init__(self):
        self.win=GraphWin("2048", 690, 620)
        self.win.setBackground("white")
        self.grid=[[], [], [], []]
        for y in range(0, 4):
            for x in range(0, 4):
                newCell=Cell(10+(x*150), 10+(y*150))
                self.grid[y].append(newCell)
                newCell.getBackgroundImage().draw(self.win)
        self.lifeRemaining=True
        self.highestValue=2
        self.addKeyImage(2)
        self.addRandomCellVal()
        self.addRandomCellVal()
        self.win.master.bind("<Key>",self.handleKeyPress)
        
    def addRandomCellVal(self):
        unoccupiedRs=[]
        unoccupiedCs=[]
        for r in range(0, len(self.grid)):
            for c in range(0, len(self.grid[r])):
                if self.grid[r][c].isEmpty():
                    unoccupiedRs.append(r)
                    unoccupiedCs.append(c)
        ind=random.choice(range(0, len(unoccupiedRs)))
        rInd=unoccupiedRs[ind]
        cInd=unoccupiedCs[ind]
        self.grid[rInd][cInd].addValue(random.choice([2, 4]))
        if self.grid[rInd][cInd].getValue()>self.highestValue:
            self.highestValue=self.grid[rInd][cInd].getValue()
            self.addKeyImage(self.highestValue)
        self.grid[rInd][cInd].getImage().draw(self.win)
        
    def shiftCellContent(self, xDirection, yDirection):
        shifted=False
        if xDirection==-1:
            xRange=range(0, len(self.grid))
        else:
            xRange=range(len(self.grid)-1, -1, -1)
        if yDirection==-1:
            yRange=range(0, len(self.grid))
        else:
            yRange=range(len(self.grid)-1, -1, -1)
        promotions=[]
        for x in range(0, 4):
            promotions.append([False, False, False, False])
        finished=False
        while finished==False:
            finished=True
            toShift=[]
            toPromote=[]
            toUndraw=[]
            toDraw=[]
            for r in yRange:
                for c in xRange:
                    newR=r+yDirection
                    newC=c+xDirection
                    if not self.grid[r][c].isEmpty():
                        if newR>=0 and newC>=0 and newR<len(self.grid) and newC<len(self.grid[newR]):
                            if self.grid[newR][newC].isEmpty():
                                self.grid[newR][newC].addValue(self.grid[r][c].getValue(), self.grid[r][c].getImage())
                                self.grid[r][c].resetContent()
                                toShift.append(self.grid[newR][newC].getImage())
                                shifted=True
                                finished=False
                            elif self.grid[newR][newC].getValue()==self.grid[r][c].getValue() and promotions[newR][newC]==False and promotions[r][c]==False:
                                toUndraw.append(self.grid[newR][newC].getImage())
                                toShift.append(self.grid[r][c].getImage())
                                self.grid[newR][newC].addValue(self.grid[r][c].getValue(), self.grid[r][c].getImage())
                                self.grid[r][c].resetContent()
                                toPromote.append(self.grid[newR][newC])
                                promotions[newR][newC]=True
                                shifted=True
                                finished=False
            for x in range(0, 10):
                for item in toShift:
                    item.move(xDirection*15, yDirection*15)
                time.sleep(.013)
            for item in toPromote:
                item.promote()
                item.getImage().draw(self.win)
                if item.getValue()>self.highestValue:
                    self.highestValue=item.getValue()
                    self.addKeyImage(self.highestValue)
                if self.highestValue>=2048:
                    self.drawPopup("You Win!")
                    self.drawPlayAgainButton()
            for item in toUndraw:
                item.undraw()
        return shifted

    def drawPopup(self, wrds, wrds2=None):
        content=[]
        popup=Rectangle(Point(100, 200), Point(520, 420))
        popup.setFill("white")
        popup.draw(self.win)
        content.append(popup)
        txt=Text(Point(310, 280), wrds)
        txt.setFace("arial")
        txt.setSize(24)
        txt.setStyle("bold")
        txt.draw(self.win)
        content.append(txt)
        if not wrds2 is None:
            txt2=Text(Point(310, 340), wrds2)
            txt2.setFace("arial")
            txt2.setSize(16)
            txt2.setStyle("bold")
            txt2.draw(self.win)
            content.append(txt2)
        return content

    def drawPlayAgainButton(self):
        rect=Rectangle(Point(200, 330), Point(420, 380))
        rect.setFill("#a2ddff")
        txt=Text(Point(310, 355), "Play Again")
        txt.setFace("arial")
        txt.setSize(14)
        txt.setStyle("bold")
        rect.draw(self.win)
        txt.draw(self.win)
        self.win.setMouseHandler(self.handleButtonClick)

    def addKeyImage(self, val):
        newImg=Image(Point(650, (int(math.log(val, 2)-1)*54)+22.5+15), "images/image"+str(int(math.log(val, 2)+1))+"small.png")
        newImg.draw(self.win)

    def performStateCheck(self):
        emptyCell=False
        canCombine=False
        for r in range(0, len(self.grid)):
            for c in range(0, len(self.grid[r])):
                if self.grid[r][c].isEmpty():
                    emptyCell=True
                    break
                val=self.grid[r][c].getValue()
                if r+1<len(self.grid) and c+1<len(self.grid[r]) and (val==self.grid[r+1][c].getValue() or val==self.grid[r][c+1].getValue()):
                    canCombine=True
                    break
        if not emptyCell and not canCombine:
            if self.lifeRemaining>0:
                self.lifeRemaining=False
                popupContent=self.drawPopup("Looks like you're stuck!", "One more chance...")
                time.sleep(3)
                for item in popupContent:
                    item.undraw()
                for row in self.grid:
                    for cell in row:
                        if cell.getValue()==2 or cell.getValue()==4 or cell.getValue()==8:
                            time.sleep(.5)
                            cell.getImage().undraw()
                            cell.resetContent()
            else:
                self.drawPopup("You lose :(")
                self.drawPlayAgainButton()
                    
    def handleKeyPress(self, key):
        if key.keysym=="Up":
            self.win.master.unbind("<Key>")
            shift=self.shiftCellContent(0, -1)
            if shift:
                time.sleep(.25)
                self.addRandomCellVal()
                self.performStateCheck()
            self.win.master.bind("<Key>",self.handleKeyPress)
        elif key.keysym=="Down":
            self.win.master.unbind("<Key>")
            shift=self.shiftCellContent(0, 1)
            if shift:
                time.sleep(.25)
                self.addRandomCellVal()
                self.performStateCheck()
            self.win.master.bind("<Key>",self.handleKeyPress)
        elif key.keysym=="Left":
            self.win.master.unbind("<Key>")
            shift=self.shiftCellContent(-1, 0)
            if shift:
                time.sleep(.25)
                self.addRandomCellVal()
                self.performStateCheck()
            self.win.master.bind("<Key>",self.handleKeyPress)
        elif key.keysym=="Right":
            self.win.master.unbind("<Key>")
            shift=self.shiftCellContent(1, 0)
            if shift:
                time.sleep(.25)
                self.addRandomCellVal()
                self.performStateCheck()
            self.win.master.bind("<Key>",self.handleKeyPress)

    def handleButtonClick(self, point):
        if point.getX()>=200 and point.getX()<=420 and point.getY()>=330 and point.getY()<=380:
            self.win.setMouseHandler(None)
            self.win.close()
            self=Game()
            
class Cell:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.backgroundImage=Image(Point(self.x+75, self.y+75), "images/blank.png")
        self.resetContent()
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getValue(self):
        return self.value
    def getImage(self):
        return self.image
    def getBackgroundImage(self):
        return self.backgroundImage
    def getContentX(self):
        return self.image.getAnchor().getX()-75
    def getContentY(self):
        return self.image.getAnchor().getY()-75
    def isEmpty(self):
        return self.value==0
    def resetContent(self):
        self.value=0
        self.image=None
    def addValue(self, value, image=None):
        self.value=value
        if image is None:
            if not self.image is None:
                self.image.undraw()
            self.image=Image(Point(self.x+75, self.y+75), "images/image"+str(int(math.log(self.value, 2)+1))+".png")
        else:
            self.image=image
    def promote(self):
        self.addValue(self.value*2)

def main():
    game=Game()
    input("Press ENTER to close from command prompt: ")
    
main()
