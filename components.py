import numpy as np

class ChessBoard:
    "Chess board containing information of all the chess pieces"

    def __init__(self, initialLayout='empty', boardNo=8, dimensions=3):
        self.boardNo = boardNo  # Length of each dimension
        self.dimensions = dimensions  # TODO: no intent of extending to higher dimensions at the moment! 3 for 3D
        self._pieceDict = dict()
        self.setInitialLayout(initialLayout)
        self._currentPiece = None  # currentPieces that is selected, required to show moveable positions
        self._currentSide = 0

    # functions used for collecting ChessPiece objects
    def validCoordinates(self, coordinates):
        """check if Coordinates is valid for current ChessBoard"""
        return isinstance(coordinates, (list, tuple)) and len(coordinates) == self.dimensions and all(
            isinstance(n, int) for n in coordinates)

    def withinBoardBoundaries(self, coordinates):
        """determines if coordinates passed is within boundaries of the board"""
        for n in coordinates:
            if n < 0 or n > self.boardNo - 1:
                return False
        else:
            return True

    def positionOccupied(self, coordinates):
        """determines if coordinates passed is occupied, and returns side(colour) of it, default 0 if position is empty"""
        coordinates = tuple(coordinates)  # convert input to tuple if it is numpy array
        if coordinates in self._pieceDict:
            return True, self._pieceDict[coordinates].side
        else:
            return False, 0

    def addPiece(self, piece):
        if not isinstance(piece, ChessPiece):
            raise Exception("must add a ChessPiece type object")
        if not self.validCoordinates(piece._coordinates):
            raise Exception("coordinate not valid for current chessBoard")
        if not self.withinBoardBoundaries(piece._coordinates) or self.positionOccupied(piece._coordinates)[0]:
            raise Exception("must add ChessPiece within the chessboard on an unoccupied tile")
        self._pieceDict[piece._coordinates] = piece
        piece.attachChessBoard(self)

    def addPieces(self, pieces):
        """adds multiple chessPieces to the board"""
        for piece in pieces:
            self.addPiece(piece)

    def removePiece(self, piece):
        #TODO: considering implementing such a function to clear the pieces and free memory

        pass

    def transformPiece(self, originalPiece, targetPiece):
        """transform the original chessPiece object into a new ChessPiece object, input original piece and targetPiece class
        by transform, a new piece of targetPiece class is created, coordinates is copied from the original piece
        """
        coordinates = originalPiece.getCoordinates()
        side = originalPiece.side
        boardNo = originalPiece.boardNo
        transformed = targetPiece(coordinates, side, boardNo)
        targetPiece.chessBoard = self #TODO: not elegant, consider implementing removePiece and use addPiece
        self._pieceDict[coordinates] = transformed
        return transformed

    def selectPiece(self, piece):
        if not isinstance(piece, ChessPiece):
            raise Exception("must add a ChessPiece type object")
        self._currentPiece = piece

    def unselectPiece(self):
        self._currentPiece = None

    def getCurrentPiece(self):
        return self._currentPiece

    def moveCurrentPiece(self, targetCoordinates):
        if not self.validCoordinates(targetCoordinates):
            raise Exception("this function must be called with valid targetCoordinates")
        captured = self._pieceDict.pop(targetCoordinates, None)
        self._pieceDict.pop(self._currentPiece.getCoordinates())
        self._pieceDict[targetCoordinates] = self._currentPiece  # update for _pieceDict
        self._currentPiece.changeCoordinates(
            targetCoordinates)  # update for chessPiece TODO: (consider the redundancy of information and if there is a better solution)
        self._currentPiece = None  # Action done, remove the moved chessPiece from self._currentPiece
        self._currentSide = not self._currentSide  # after a move is made, side changes
        return captured

    def getCurrentSide(self):
        return self._currentSide

    def setInitialLayout(self, initialLayout):
        """add ChessPieces to ChessBoard according to the initial settings"""
        initialLayoutDict = {
            'empty': (None, []),
            'testing': ('point symmetry',
                        [King((0, 0, 0)), Queen((1, 1, 1)), Rook((1, 0, 0)), Rook((0, 1, 0)), Rook((0, 0, 1)),
                         Bishop((2, 0, 0)), Bishop((0, 2, 0)), Bishop((0, 0, 2)), Knight((2, 2, 2)), Knight((3, 0, 0)),
                         Knight((0, 3, 0)), Knight((0, 0, 3)), Knight((1, 1, 0)), Knight((1, 0, 1)),
                         Knight((0, 1, 1))]),
            'vortex': []  # TODO: vortex standard: 20 pieces each on the edge
        }

        setup = initialLayoutDict[initialLayout]
        if setup[0] == "point symmetry":
            for piece in setup[1]:
                self.addPiece(piece)
                oppositePiece = piece.createOpposite()
                self.addPiece(oppositePiece)
        else:
            return

    def getpieceList(self):
        """returns a list containing all the ChessPiece objects, from the pieceDict"""
        return list(self._pieceDict.values())

    def getPieceByCoordinate(self, coordinates):
        """attempt to return a chessPiece from the coordinates input, return None if nothing is found"""
        if not self.validCoordinates(coordinates):
            raise Exception("must be a valid coordinate to use this function")
        try:
            return self._pieceDict[coordinates]
        except:
            return None

    def currentNextMoveCapture(self):
        """returns move and capture for the current piece"""
        if not self._currentPiece:
            raise Exception("there must be an active currentPiece to call this function")
        """returns a list containing the positions the current selected piece can move to next, and a list that the piece could capture"""
        return self._currentPiece.validNextPositions()

class ChessPiece:
    "superclass for all the chess pieces"

    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name='nameless'):      #TODO: name is redundant, consider removing it
        if not isinstance(coordinates, (list, tuple)) or not len(coordinates) == 3:
            raise Exception("coordinates argument must be passed as list or tuple with length of 3")
        self._coordinates = coordinates
        self.name = name
        self._id = None
        self._spriteAddress = None
        self.boardNo = boardNo  # correspond to boardSize TODO: need to check if boardNo matches before inserting it into ChessBoard
        self.side = side  # 0 for white, 1 for black

    def createOpposite(self, symmetryType="pointSymmetry"):
        PieceType = self.__class__
        side = not self.side
        x, y, z = self._coordinates
        coordinates = (self.boardNo - 1 - x, self.boardNo - 1 - y, self.boardNo - 1 - z)
        oppositePiece = PieceType(coordinates, side)
        return oppositePiece

    def attachChessBoard(self, ChessBoardObj):
        if not isinstance(ChessBoardObj, ChessBoard):
            raise Exception("a ChessBoard object must be passed to this method")
        self.chessBoard = ChessBoardObj

    def getCoordinates(self):
        return self._coordinates

    def changeCoordinates(self, coordinates):
        """should only be called from ChessBoardMethods"""
        if self.chessBoard.validCoordinates(coordinates):
            self._coordinates = coordinates
        else:
            raise Exception("a validCoordinate must be passed to the changeCoordinates")

    def getID(self):
        return self._id

    def getAddress(self):
        return self._spriteAddress

    def validNextPositions(self):
        # returns all valid coordinates this piece can move to or capture
        raise Exception("validMovePosition method not defined in current chess piece")

    def showNextPositions(self):
        # print all valid coordinates this piece can move to or capture
        move, capture = self.validNextPositions()
        print('Move: ')
        for coordinate in move:
            print(tuple(coordinate))
        print('Capture: ')
        for coordinate in capture:
            print(tuple(coordinate))

class LinePiece(ChessPiece):
    # superclass for pieces like Rook, Queen and Bishop
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="LinePiece"):
        super().__init__(coordinates, side, boardNo, name)
        self.moveVectors = []  # Needs to inplement the moveVectors in subclasses

    def validNextPositions(self):
        if not self.chessBoard:
            raise Exception("attach piece to ChessBoard Object before calling validMovePosition")
        """return valid coordinates to move to based on the current state of the board"""
        move = []
        capture = []
        for vector in self.moveVectors:
            validPosition = np.array(self._coordinates) + vector  # using numpy just for the vector addition
            while self.chessBoard.withinBoardBoundaries(validPosition):
                checkOccupy = self.chessBoard.positionOccupied(validPosition)
                if not checkOccupy[0]:
                    move.append(tuple(validPosition))
                    validPosition += vector
                else:
                    if self.side != checkOccupy[1]:
                        capture.append(tuple(validPosition))
                    break

        return move, capture


class Rook(LinePiece):
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="Rook"):
        super().__init__(coordinates, side, boardNo, name)
        self._id = 'Rook'
        self._spriteAddress = ('white-rook.png', 'black-rook.png')
        self.moveVectors = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


class Bishop(LinePiece):
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="Bishop"):
        super().__init__(coordinates, side, boardNo, name)
        self._id = 'Bishop'
        self._spriteAddress = ('white-bishop.png', 'black-bishop.png')
        self.moveVectors = [(1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0), (1, 0, 1), (1, 0, -1), (-1, 0, 1),
                            (-1, 0, -1), (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)]


class Queen(LinePiece):
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="Queen"):
        super().__init__(coordinates, side, boardNo, name)
        self._id = 'Queen'
        self._spriteAddress = ('white-queen.png', 'black-queen.png')
        self.moveVectors = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1), (1, 1, 0), (1, -1, 0),
                            (-1, 1, 0), (-1, -1, 0), (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1), (0, 1, 1),
                            (0, 1, -1), (0, -1, 1), (0, -1, -1)]


class StepPiece(ChessPiece):
    # superclass for pieces like Knight and King
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="StepPiece"):
        super().__init__(coordinates, side, boardNo, name)
        self.stepVectors = []  # Needs to inplement the stepVectors in subclasses

    def validNextPositions(self):
        if not self.chessBoard:
            raise Exception("attach piece to ChessBoard Object before calling validMovePosition")
        move = []
        capture = []
        for vector in self.stepVectors:
            position = np.array(self._coordinates) + vector
            if not self.chessBoard.withinBoardBoundaries(position):
                continue
            checkOccupy = self.chessBoard.positionOccupied(position)
            if not checkOccupy[0]:
                move.append(tuple(position))
            else:
                if self.side != checkOccupy[1]:
                    capture.append(tuple(position))

        return move, capture


class King(StepPiece):
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="King"):
        super().__init__(coordinates, side, boardNo, name)
        self._id = 'King'
        self._spriteAddress = ('white-king.png', 'black-king.png')
        self.stepVectors = [(1, 0, 0), (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 0, 1), (0, 0, -1), (0, 1, 0),
                            (0, 1, 1), (0, 1, -1), (0, -1, 0), (0, -1, 1), (0, -1, -1), (-1, 0, 0), (-1, 1, 0),
                            (-1, -1, 0), (-1, 0, 1), (-1, 0, -1)]


class Knight(StepPiece):
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="Knight"):
        super().__init__(coordinates, side, boardNo, name)
        self._id = 'Knight'
        self._spriteAddress = ('white-knight.png', 'black-knight.png')
        self.stepVectors = [(2, 1, 0), (2, -1, 0), (2, 0, 1), (2, 0, -1), (-2, 1, 0), (-2, -1, 0), (-2, 0, 1),
                            (-2, 0, -1), (1, 2, 0), (-1, 2, 0), (0, 2, 1), (0, 2, -1), (1, -2, 0), (-1, -2, 0),
                            (0, -2, 1), (0, -2, -1), (1, 0, 2), (-1, 0, 2), (0, 1, 2), (0, -1, 2), (1, 0, -2),
                            (-1, 0, -2), (0, 1, -2), (0, -1, -2)]


class PawnPiece(ChessPiece):
    # superclass for pieces like Knight and King
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="PawnPiece"):
        super().__init__(coordinates, side, boardNo, name)
        self.advanceVectors = []
        self.captureVectors = []
        self.promotionCoordinateList = []
        self.promotionPieces = []  # List of ChessPiece Class that the pawn can be promoted into

    def generatePromotionCoordinates(self):
        raise Exception("Needs to implement promotion coordinates function in subclasses")


class VortexPawn(PawnPiece):
    def __init__(self, coordinates=(0, 0, 0), side=0, boardNo=8, name="Vortex Pawn"):
        super().__init__(coordinates, side, boardNo, name)
        self._id = 'VortexPawn'
        self._spriteAddress = ('white-pawn.png', 'black-pawn.png')
        self.advanceVectors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.captureVectors = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
        self.promotionCoordinateList = self.generatePromotionCoordinates()
        self.boardNo = 8

    def generatePromotionCoordinates(self):
        coordinateList = []
        for x in range(self.boardNo):
            if not x >= (self.boardNo / 2):
                continue
            for y in range(self.boardNo):
                if not y >= (self.boardNo / 2):
                    continue
                for z in range(self.boardNo):
                    if not z >= (self.boardNo / 2):
                        continue
                    if x == (self.boardNo - 1) or y == (self.boardNo - 1) or z == (self.boardNo - 1):
                        coordinateList += [(x, y, z)]

        return coordinateList

    # def promotion TODO： function for promotion, might need to implement it in ChessBoard

if __name__ == '__main__':
    # section for testing the functions
    # ChessBoard
    testChessBoard = ChessBoard(boardNo=8, dimensions=3)

    # test for validCoordinates method
    valid = [(1, 2, 3), (4, 4, 4), ((1, 2, 3))]
    invalid = [(1, 2), (2, 3, 4, 5), ('1', 2, 3), np.array([1, 2, 3])]
    for coordinates in valid:
        assert (testChessBoard.validCoordinates(coordinates))
    for coordinates in invalid:
        assert (not testChessBoard.validCoordinates(coordinates))

    # test for withinBoardBoundaries method
    invalid = [(-1, 0, 1), (10, 5, 0)]

    for coordinates in valid:
        assert (testChessBoard.withinBoardBoundaries(coordinates))
    for coordinates in invalid:
        assert (not testChessBoard.withinBoardBoundaries(coordinates))

    rook1 = Rook((1, 2, 3))

    rook2 = rook1.createOpposite()

    testChessBoard.addPiece(rook1)
    pawn1 = VortexPawn()
    print(pawn1.generatePromotionCoordinates())
    queent = testChessBoard.transformPiece(pawn1, Queen)
    print(testChessBoard._pieceDict, queent.validNextPositions())


