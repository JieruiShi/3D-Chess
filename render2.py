import pygame
import os
from components import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
CAPTURE = (176, 35, 35)
CURSOR = (28, 232, 103)


pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill(WHITE)

class ChessRender:
    """All functions to draw chessboard with pygame"""

    def __init__(self, initialLayout = 'empty', boardNo=8):
        self.surface = WIN
        self.chessBoard = ChessBoard(initialLayout, boardNo) #generate a chessBoard that holds information about the game
        self.boardNo = boardNo
        self.spriteDict = dict()
        self.cursorPos = (0,0)
        self.cursorCoordinate = None

    sizeDimensions = {
        8: (2, 25, 30, 4, 20, 20) #TODO: what each dimension does
    }

    def drawChessBoard(self):
        BOARDNO = self.boardNo
        Dimensions = self.sizeDimensions[self.boardNo]
        LINEWIDTH = Dimensions[0]
        BLOCKWIDTH = Dimensions[1]
        BOARDGAPWIDTH = Dimensions[2]
        BOARDPERROW = Dimensions[3]
        left, top = Dimensions[4], Dimensions[5]
        BOARDDISTANCE = ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH + BOARDGAPWIDTH)

        for k in range(BOARDNO):
            LEFT, TOP = left + (k % BOARDPERROW) * BOARDDISTANCE, top + (k // BOARDPERROW) * BOARDDISTANCE
            boardRECT = (LEFT, TOP, ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH),
                         ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH))
            pygame.draw.rect(self.surface, BLACK, boardRECT)
            for i in range(BOARDNO):
                for j in range(BOARDNO):
                    cellRECT = (
                        (LEFT + LINEWIDTH + i * (LINEWIDTH + BLOCKWIDTH)),
                        (TOP + LINEWIDTH + j * (LINEWIDTH + BLOCKWIDTH)),
                        BLOCKWIDTH, BLOCKWIDTH)
                    pygame.draw.rect(self.surface, WHITE, cellRECT)

    def drawMovablePositions(self, coordinatesList):
        BOARDNO = self.boardNo
        Dimensions = self.sizeDimensions[self.boardNo]
        LINEWIDTH = Dimensions[0]
        BLOCKWIDTH = Dimensions[1]
        BOARDGAPWIDTH = Dimensions[2]
        BOARDPERROW = Dimensions[3]
        left, top = Dimensions[4], Dimensions[5]
        CIRCLERADIUS = 3
        BOARDDISTANCE = ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH + BOARDGAPWIDTH)

        for coordinate in coordinatesList:
            x, y, z = coordinate
            X = (left + (z % BOARDPERROW) * BOARDDISTANCE) + (
                        LINEWIDTH + round(0.5 * BLOCKWIDTH) + x * (LINEWIDTH + BLOCKWIDTH))
            Y = (top + (z // BOARDPERROW) * BOARDDISTANCE) + (
                        LINEWIDTH + round(0.5 * BLOCKWIDTH) + y * (LINEWIDTH + BLOCKWIDTH))
            pygame.draw.circle(self.surface, GREY, (X, Y), CIRCLERADIUS)

    def loadSprite(self, chessPiece):
        """load the sprites address from ChessPiece to a dict for ChessRender,
        called whenever encountering a sprite whose address is not in the self.spriteDict yet"""
        if not isinstance(chessPiece, ChessPiece):
            raise Exception("this function cannot be called with a non chessPiece object")

        Dimensions = self.sizeDimensions[self.boardNo]
        BLOCKWIDTH = Dimensions[1]
        id = chessPiece.getID()
        addresses = [os.path.join(os.getcwd(), "sprites", address) for address in chessPiece.getAddress()]
        sprite = [pygame.transform.scale(pygame.image.load(address),(BLOCKWIDTH, BLOCKWIDTH)) for address in addresses]
        self.spriteDict[id] = sprite

    def drawChessPieces(self, chessPieceList):
        """draw chess sprites onto the screen according to input list of chesspieces"""
        BOARDNO = self.boardNo
        Dimensions = self.sizeDimensions[self.boardNo]
        LINEWIDTH = Dimensions[0]
        BLOCKWIDTH = Dimensions[1]
        BOARDGAPWIDTH = Dimensions[2]
        BOARDPERROW = Dimensions[3]
        left, top = Dimensions[4], Dimensions[5]
        CIRCLERADIUS = 3
        BOARDDISTANCE = ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH + BOARDGAPWIDTH)

        for chesspiece in chessPieceList:
            x, y, z = chesspiece.getCoordinates()
            X = (left + (z % BOARDPERROW) * BOARDDISTANCE) + (
                        LINEWIDTH + x * (LINEWIDTH + BLOCKWIDTH))
            Y = (top + (z // BOARDPERROW) * BOARDDISTANCE) + (
                        LINEWIDTH + y * (LINEWIDTH + BLOCKWIDTH))

            if not chesspiece.getID() in self.spriteDict:
                self.loadSprite(chesspiece)
            sprite = self.spriteDict[chesspiece.getID()][chesspiece.side]
            self.surface.blit(sprite,(X,Y))

    def drawCurrent(self):
        """draw shading for selected piece"""
        BOARDNO = self.boardNo
        Dimensions = self.sizeDimensions[self.boardNo]
        LINEWIDTH = Dimensions[0]
        BLOCKWIDTH = Dimensions[1]
        BOARDGAPWIDTH = Dimensions[2]
        BOARDPERROW = Dimensions[3]
        left, top = Dimensions[4], Dimensions[5]
        BOARDDISTANCE = ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH + BOARDGAPWIDTH)
        currentPiece = self.chessBoard.getCurrentPiece()

        x, y, z = currentPiece.getCoordinates()
        X = (left + (z % BOARDPERROW) * BOARDDISTANCE) + (
                LINEWIDTH + x * (LINEWIDTH + BLOCKWIDTH))
        Y = (top + (z // BOARDPERROW) * BOARDDISTANCE) + (
                LINEWIDTH + y * (LINEWIDTH + BLOCKWIDTH))

        pygame.draw.rect(self.surface, GREY, (X, Y, BLOCKWIDTH, BLOCKWIDTH))

    def drawCapture(self, coordinatesList):
        """draw shading for capturable positions"""
        #TODO: draw shades for currentpiece and the capturable pieces
        BOARDNO = self.boardNo
        Dimensions = self.sizeDimensions[self.boardNo]
        LINEWIDTH = Dimensions[0]
        BLOCKWIDTH = Dimensions[1]
        BOARDGAPWIDTH = Dimensions[2]
        BOARDPERROW = Dimensions[3]
        left, top = Dimensions[4], Dimensions[5]
        BOARDDISTANCE = ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH + BOARDGAPWIDTH)

        for coordinate in coordinatesList:
            x, y, z = coordinate
            X = (left + (z % BOARDPERROW) * BOARDDISTANCE) + (
                        LINEWIDTH + x * (LINEWIDTH + BLOCKWIDTH))
            Y = (top + (z // BOARDPERROW) * BOARDDISTANCE) + (
                        LINEWIDTH + y * (LINEWIDTH + BLOCKWIDTH))
            pygame.draw.rect(self.surface, CAPTURE, (X, Y, BLOCKWIDTH, BLOCKWIDTH))

    def drawCursor(self):
        """draw shading for selected piece"""
        if not self.cursorCoordinate:
            return
        BOARDNO = self.boardNo
        Dimensions = self.sizeDimensions[self.boardNo]
        LINEWIDTH = Dimensions[0]
        BLOCKWIDTH = Dimensions[1]
        BOARDGAPWIDTH = Dimensions[2]
        BOARDPERROW = Dimensions[3]
        left, top = Dimensions[4], Dimensions[5]
        BOARDDISTANCE = ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH + BOARDGAPWIDTH)

        x, y, z = self.cursorCoordinate
        X = (left + (z % BOARDPERROW) * BOARDDISTANCE) + (
                LINEWIDTH + x * (LINEWIDTH + BLOCKWIDTH))
        Y = (top + (z // BOARDPERROW) * BOARDDISTANCE) + (
                LINEWIDTH + y * (LINEWIDTH + BLOCKWIDTH))

        pygame.draw.rect(self.surface, CURSOR, (X, Y, BLOCKWIDTH, BLOCKWIDTH))

    def updateCursorCoordinate(self):
        """updates the cursor coordinate based on the cursorPos"""
        BOARDNO = self.boardNo
        Dimensions = self.sizeDimensions[self.boardNo]
        LINEWIDTH = Dimensions[0]
        BLOCKWIDTH = Dimensions[1]
        BOARDGAPWIDTH = Dimensions[2]
        BOARDPERROW = Dimensions[3]
        left, top = Dimensions[4], Dimensions[5]
        CIRCLERADIUS = 3
        BOARDDISTANCE = ((BOARDNO + 1) * LINEWIDTH + BOARDNO * BLOCKWIDTH + BOARDGAPWIDTH)

        X, Y = self.cursorPos
        z = (X - left) // BOARDDISTANCE + ((Y - top) // BOARDDISTANCE) * BOARDPERROW
        boardLeft, boardTop = X - left - (z % BOARDPERROW) * BOARDDISTANCE, Y - top - (z // BOARDPERROW) * BOARDDISTANCE #distance relative to the current zth board
        x = boardLeft // (LINEWIDTH + BLOCKWIDTH)
        y = boardTop // (LINEWIDTH + BLOCKWIDTH)

        if self.chessBoard.withinBoardBoundaries((x,y,z)):
            self.cursorCoordinate = (x,y,z)
        else:
            self.cursorCoordinate = None

    def processClick(self):
        """based on current state of chessBoard(_currentPiece & _currentSide), decide what the click should do
        currentPiece: None or a chessPiece
        currentSide: The side supposed to move now, 0 or 1"""

        currentPiece, currentSide = self.chessBoard.getCurrentPiece(), self.chessBoard.getCurrentSide()
        if not currentPiece:
            # no piece is currently selected
            if self.cursorCoordinate:
                #cursor in a valid coordinate
                chessPiece = self.chessBoard.getPieceByCoordinate(self.cursorCoordinate)
                if chessPiece:
                    #actually exists a chessPiece in that coordinates
                    if chessPiece.side == currentSide:
                        self.chessBoard.selectPiece(chessPiece)
                    else:
                        return #TODO: selected piece not the side to move for now, might enable check movement in the future though
                else:
                    return # returned None from chessBoard._pieceDict, doesn't exist a chessPiece in that coordinate
            else:
                return # cursor not in a valid coordinate (lying out of board)
        else:
            # there is a currentPiece
            if self.cursorCoordinate:
                #cursor in a valid coordinate
                move, capture = self.chessBoard.currentNextMoveCapture()
                movable = move + capture
                if self.cursorCoordinate in movable:
                    #cursor coordinate within a next movable/capturable position
                    self.chessBoard.moveCurrentPiece(self.cursorCoordinate)
                else:
                    chessPiece = self.chessBoard.getPieceByCoordinate(self.cursorCoordinate)
                    if chessPiece:
                        #cursor coordinates on a chessPiece that the current chessPiece couldn't capture
                        if chessPiece.side == currentSide:
                            #a piece on the same side, select this piece instead
                            self.chessBoard.unselectPiece()
                            self.chessBoard.selectPiece(chessPiece)
                        else:
                            return #TODO: selected piece not the side to move for now, might enable check movement in the future though

                    else:
                        return # returned None from chessBoard._pieceDict, doesn't exist a chessPiece in that coordinate
            else:
                self.chessBoard.unselectPiece() #unselect the piece by clicking outside the board

    def update(self):
        """function to be called every frame"""
        #get update on cursor information
        self.cursorPos = pygame.mouse.get_pos()
        self.updateCursorCoordinate()
        #draw chessBoard and chessPiece
        self.drawChessBoard()
        if self.chessBoard.getCurrentPiece():
            move, capture = self.chessBoard.currentNextMoveCapture()
            self.drawCurrent()
            self.drawMovablePositions(move)
            self.drawCapture(capture)
        self.drawCursor()
        self.drawChessPieces(self.chessBoard.getpieceList())
        pygame.display.update()

def main():
    # r1 = Rook((3,5,5),0)
    # r2 = Rook((3,5,6),1)
    # b1 = Bishop((2,4,6),0)
    # b2 = Bishop((3,1,5),1)
    # q1 = Queen((1,2,3), 0)
    # q2 = Queen((3,2,6), 1)
    # k1 = King((3,5,7), 0)
    # k2 = King((1,2,2), 1)
    # n1 = Knight((2,6,7), 0)
    # n2 = Knight((3,4,5), 1)

    #main
    testChessRender = ChessRender("testing")
    #testChessRender.chessBoard.addPieces((r1,r2,b1,b2,q1,q2,k1,k2,n1,n2))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(testChessRender.chessBoard.getCurrentPiece())
                testChessRender.processClick()

        testChessRender.update()
        clock.tick(50)
    pygame.quit()


if __name__ == "__main__":
    main()
