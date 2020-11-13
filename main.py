import numpy as np
import time
import sys
import os
import requests

class Puzzles:
  sudokuUS = [[5,0,0,3,0,7,0,0,9], 
              [3,4,0,8,0,1,0,2,6],
              [0,0,0,0,9,0,0,0,0],
              [0,9,5,7,0,3,8,0,0],
              [0,1,0,0,8,0,0,3,5],
              [0,0,3,5,0,9,6,7,0],
              [0,0,0,0,6,0,0,0,0],
              [4,2,0,1,0,8,0,9,3],
              [8,0,0,9,0,4,0,0,1]]
  sudokuUS2 = [[5,0,0,3,0,7,0,0,9], 
               [3,4,0,8,0,1,0,2,6],
               [0,0,0,0,9,0,0,0,0],
               [0,9,5,7,0,3,8,0,0],
               [0,1,0,0,8,0,0,3,5],
               [0,0,3,5,0,9,6,7,0],
               [0,0,0,0,6,0,0,0,0],
               [4,2,0,1,0,8,0,9,3],
               [8,0,0,9,0,4,0,0,1]]
  puzzleDif = "easy"
  def makePuzzle(difficulty):
    f = open("myPuzzle.txt", "w")
    Puzzles.puzzleDif = difficulty
    url = 'https://1sudoku.com/sudoku/' + difficulty
    #print(url)
    r = requests.get(url)
    theText = r.text
    for i in range(len(theText)):
      if theText[i:i+20] == "<div id=\"grilleJeu\">":
        boardStart = i+20
      if theText[i:i+16] == "<div id=\"pause\">":
        boardEnd = i
    theText = theText[boardStart:boardEnd]
    for i in range(len(theText)):
      if theText[i:i+3] == "id=":
        checker = True
        j = i+3
        while checker:
          if theText[j:j+len('v="')] == 'v="':
            f.write(theText[j+3:j+4])
            break
          if theText[j:j+len("</div>")] == "</div>":
            f.write(str(0))
            break
          j += 1
    f.close()
	
  def writePuzzle():
    f = open("myPuzzle.txt", "r")
    theText = f.read()
    z = 0
    for i in range(0, len(theText)): 
      row = z//9
      col = z%9
      Puzzles.sudokuUS[row][col] = int(theText[i])
      z+=1
    f.close()
	
  def getStringer():
    return (str(Puzzles.puzzleDif + " Count: " + str(counter.count) + " Time: " + str(Timer.getTime())[0:6]))
  

class Timer:
  start = 0
  end = 0
  def startTime():
    Timer.timerReset()
    Timer.start = time.time()
  def endTime():
    Timer.end = time.time()
  def getTime():
    Timer.endTime()
    return Timer.end - Timer.start
  def timerReset():
    Timer.start = 0
    Timer.end = 0

class counter:
  count = 0
  def addCount():
    counter.count += 1

class Algorithm:
  def getRow(row, num):
    """Returns True if a number works in a given row, False otherwise"""
    aRow = Puzzles.sudokuUS[row]
    if num in aRow:
      return False
    return True

  def getColumn(col, num):
    """Returns True if a number works in a given colum, False otherwise"""
    thisCol = [row[col] for row in Puzzles.sudokuUS]
    if num in thisCol:
      return False
    return True

  def getBox(row, column, num):
    """Returns True if a number works in a given spot of a given 3x3 matrix, False other wise"""
    box = [0,0,0,0,0,0,0,0,0]
    matrix = Puzzles.sudokuUS
    if row < 3:
      if column < 3:
        box = [matrix[0][0], matrix[0][1], matrix[0][2], matrix[1][0], matrix[1][1], matrix[1][2], matrix[2][0], matrix[2][1], matrix[2][2]]
    if row < 6 and row > 2:
      if column < 6 and column > 2:
        box = [matrix[3][3], matrix[3][4], matrix[3][5], matrix[4][3], matrix[4][4], matrix[4][5], matrix[5][3], matrix[5][4], matrix[5][5]]
    if row < 9 and row > 5:
      if column < 9 and column > 5:
        box = [matrix[6][6], matrix[6][7], matrix[6][8], matrix[7][6], matrix[7][7], matrix[7][8], matrix[8][6], matrix[8][7], matrix[8][8]]

    if num in box:
      return False
    return True

  def checkNum(row, col, num):
    """Checks if a number works in a given spot"""
    
    if Algorithm.getBox(row, col, num) == False:
      return False
    if Algorithm.getColumn(col, num) == False:
      return False
    if Algorithm.getRow(row, num) == False:
      return False
    return True

  def hasEmpty():
    for i in range(9):
      for j in range(9):
        if Puzzles.sudokuUS[i][j] == 0:
          return True
    return False

  def isPossible(row, col, num):
    #Tests if a given number(num) can go in a given coordinate
    return Algorithm.checkNum(row, col, num)

  def findPossible(row, col):
    """Returns an array with all possible numbers for a given coordinate"""
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    for i in arr:
      if Algorithm.isPossible(row, col, i) == False:
        index = 0;
        for x in arr:
          index = index + 1
          if x == i:       
            arr = np.delete(arr, index-1)
    
    return arr

  def finished():
    puz = ""
    for row in Puzzles.sudokuUS:
      for elem in row:
        puz = puz + str(elem) + " "
      puz = puz + "\n"
    return (puz + (str("Solved: " + str(Algorithm.isSolved()) + " Count: " + str(counter.count) + " Time: " + str(Timer.getTime())[0:8]))), (str(Puzzles.puzzleDif) + ":" + str(counter.count) + ":" + (str(Timer.getTime())[0:4]))

  def isSolved():
    """Checks if the board is solved."""
    for i in range(1,10):
      for row in range(0, 9):
        for col in range(0,9):
          if Algorithm.getRow(row, i) == True: 
            return False
          if Algorithm.getColumn(col, i) == True:
            return False
          # add box check
    return True

  def setKnowns():
    for i in range(0,81):
      row = i//9
      col = i%9
      if Puzzles.sudokuUS[row][col] == 0:
          possibleNums = Algorithm.findPossible(row, col)
          if possibleNums.size == 1:
            Puzzles.sudokuUS[row][col] = possibleNums[0]

  def recursiveSolver():
    """Solves the board with recursion.."""
    counter.addCount()
    sys.stdout.write("\r" + str(Puzzles.getStringer()))
    for i in range(0,81):
      row = i//9
      col = i%9
      if Puzzles.sudokuUS[row][col] == 0:
          #print(Puzzles.sudokuUS[row][col])
          #time.sleep(2)
          for num in range(1,10):
            if Algorithm.checkNum(row, col, num):
              Puzzles.sudokuUS[row][col] = num
              if Algorithm.isSolved():
                return True
              else:
                if Algorithm.recursiveSolver():
                  return True
          break
    Puzzles.sudokuUS[row][col] = 0

def runSolvers():
  os.system('clear')
 
  Puzzles.writePuzzle()

  f = open('results.txt', 'a')
  counter.count = 0
  Timer.startTime()
  Algorithm.setKnowns()
  Algorithm.recursiveSolver()
  Timer.endTime()
  alg1, alg1Info = Algorithm.finished()
  f.write("alg1:" + str(alg1Info) + "\n")
  os.system('clear')
	
  Puzzles.writePuzzle()
  counter.count = 0
  Timer.startTime()
  Algorithm.recursiveSolver()
  Timer.endTime()
  alg2, alg2Info = Algorithm.finished()
  f.write("alg2:" + str(alg2Info) + "\n")
  os.system('clear')
  f.close()
  print("Alg 1\n" + str(alg1))
  print("Alg 2\n" + str(alg2))

from Data import readFile, plotter
import Data
choice = "";

while choice != "x":
  choice = input("Type 't' to run tests (5 easy, 5 medium), 'e' to run one easy test, or 'd' for data. Press 'x' to exit.")

  if(choice == "t"):
    for i in range(5):
      Puzzles.makePuzzle("easy")
      runSolvers()
    for i in range(5):
      Puzzles.makePuzzle("medium")
      runSolvers()
  if(choice == "e"):
    Puzzles.makePuzzle("easy")
    runSolvers()
  if(choice == 'd'):
    cho = input("Input 1, 2, 3, 4 or 5 for Algorithm 1 Easy, Algorithm 1 Medium, Algorithm 2 Easy, Algorithm 2 Medium, or Plot of All Data respectively")
    plotter(cho)

