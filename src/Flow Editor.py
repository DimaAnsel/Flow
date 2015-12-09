#########################
# Flow Editor.py
# Noah Ansel
# 2015-11-22
# --------------
# An editor for making Flow
# files, implemented with Tkinter.
#########################

from tkinter import *
from tkinter import filedialog

"███████████████████████████████   Constants   ████████████████████████████████"

# Window attributes
EDITOR_TITLE = "Flow Editor"
ICON_FILE = "flow_icon.gif"

TRIPLET_HEIGHT = 16
TRIPLET_WIDTH = 2 * TRIPLET_HEIGHT
TRIPLET_FONT = "Courier"

NUM_TRIPLETS_X = 24
NUM_TRIPLETS_Y = 32

# Canvas attributes
CANVAS_WIDTH = NUM_TRIPLETS_X * TRIPLET_WIDTH
CANVAS_HEIGHT = NUM_TRIPLETS_Y * TRIPLET_HEIGHT
CANVAS_BG_COLOR = "#CCCCFF"
CANVAS_OFFSET = (5, 5)

NORMAL_FILL = ""
NORMAL_BORDER_COLOR = "#888888"
NORMAL_BORDER_WIDTH = 1

ACTIVE_FILL = "#FFFFFF"
ACTIVE_BORDER_COLOR = "#555555"
ACTIVE_BORDER_WIDTH = 1.4


# Flow commands
CMD_START = '#'
CMD_COMP  = '?'
CMD_LEFT  = '<'
CMD_RIGHT = '>'
CMD_DOWN  = 'v'
CMD_UP    = '^'

CMD_LOAD  = '@'
CMD_SET   = ':'
CMD_ADD   = '+'
CMD_SUB   = '-'
CMD_MUL   = '*'
CMD_DIV   = '/'
CMD_MOD   = '%'
CMD_IN    = '~'
CMD_OUT   = '"'

# Defaults
BASE_GRID = {(0,0): "#> "}

"████████████████████████████████   Tkinter   █████████████████████████████████"


######################
# Editor
#   Main class for the editor.
#   Houses all other classes.
######################
class Editor(Frame):

  ##############
  # init
  #   Initializes the editor class
  #   and all subclasses.
  def __init__(self, master):
    Frame.__init__(self, master)
    
    # loaded file
    self._openfile = ""
    self._grid = {(0,0): "#> "}

    # current item
    self._position = (0,0) # currently active cell
    self._insertindex = 0 # position in cell to insert
    self._selection = [(0,0), (0,0)] # topleft and botright corners of selection
    self._direction = "right" # direction (defaults to right)

    # canvas tracking stuff
    self._canvasitems = {}
    self._grid = {}
    self._rects = {}
    self._canvastopleft = (0, 0)

    self.createWidgets()
    self._canvas.focus_set()
    self.pack()

    self.new()

  ###############
  # createWidgets
  #   Initializes all subclasses.
  def createWidgets(self):
    # Canvas
    self._canvas = Canvas(self,
                         width = CANVAS_WIDTH,
                         height = CANVAS_HEIGHT,
                         bg = CANVAS_BG_COLOR,
                         bd = 2,
                         relief = SUNKEN)
    self._canvas.pack()

    self.initCanvasRects()

    # Menu bar
    self.menubar = Menu(self.master)

    self.filemenu = Menu(self.menubar, tearoff = 0)
    self.filemenu.add_command(label = "New              (Ctr-N)", command = self.new)
    self.filemenu.add_command(label = "Open            (Ctr-O)", command = self.open)
    self.filemenu.add_command(label = "Save              (Ctr-S)", command = self.save)
    self.filemenu.add_command(label = "Save As   (Ctr-Sh-S)", command = self.saveAs)
    self.filemenu.add_separator()
    self.filemenu.add_command(label = "Exit", command = self.exit)
    self.menubar.add_cascade(label = "File",  menu = self.filemenu)

    self.editmenu = Menu(self.menubar, tearoff = 0)
    self.editmenu.add_command(label = "Find    (Ctr-F)", command = self.find)
    self.editmenu.add_command(label = "Goto  (Ctr-G)", command = self.goto)
    self.menubar.add_cascade(label = "Edit",  menu = self.editmenu)

    self.menubar.add_command(label = "Help",  command = self.help)

    self.master.config(menu = self.menubar)

    self.bindKeys()

  ###############
  # bindKeys
  #   Binds keyboard shortcuts
  def bindKeys(self):
    self._canvas.bind("<Key>", self.keyPress)
    self._canvas.bind("<Button-1>", self.b1Action)
    self._canvas.bind("<B1-Motion>", self.b1Drag)

    self.bind_all("<Control-n>", self.new)
    self.bind_all("<Control-o>", self.open)
    self.bind_all("<Control-s>", self.save)
    self.bind_all("<Control-S>", self.saveAs)
    self.bind_all("<Control-f>", self.find)
    self.bind_all("<Control-g>", self.goto)
    self.bind_all("<F1>", self.help)

    self._canvas.bind("<Shift-Left>", self.selectLeft)
    self._canvas.bind("<Shift-Right>", self.selectRight)
    self._canvas.bind("<Shift-Up>", self.selectUp)
    self._canvas.bind("<Shift-Down>", self.selectDown)

  ###############
  # b1Action
  #   Performs the left-click action.
  #   Updates the currently selected item.
  def b1Action(self, event):
    for x in range(self._selection[0][0], self._selection[1][0] + 1):
      for y in range(self._selection[0][1], self._selection[1][1] + 1):
        self._canvas.itemconfig(self._rects[(x, y)],
                                fill = NORMAL_FILL,
                                outline = NORMAL_BORDER_COLOR,
                                width = NORMAL_BORDER_WIDTH)

    x = (event.x - CANVAS_OFFSET[0]) // TRIPLET_WIDTH + self._canvastopleft[0]
    y = (event.y - CANVAS_OFFSET[1]) // TRIPLET_HEIGHT + self._canvastopleft[1]
    self._position = (x, y)
    self._canvas.itemconfig(self._rects[self._position],
                            fill = ACTIVE_FILL,
                            outline = ACTIVE_BORDER_COLOR,
                            width = ACTIVE_BORDER_WIDTH)
    self._insertindex = 0
    self._selection = ((x, y), (x, y))

  def b1Drag(self, event):
    print("b1Drag called")

  def selectLeft(self, event = None):
    print("selectLeft called")

  def selectRight(self, event = None):
    print("selectRight called")

  def selectUp(self, event = None):
    print("selectUp called")

  def selectDown(self, event = None):
    print("selectDown called")

  ###############
  # keyPress
  #   If a character is valid input, enters that
  #   character at the current pointer
  def keyPress(self, event):
    print("'{}' pressed: char is '{}', type is '{}', state is '{}'".format(event.keysym,event.char, event.type, event.state))

    if (event.char != "" and event.char != "\t" and
        event.keysym != "Return" and
        (0 <= event.state and event.state < 4 or
         8 <= event.state and event.state < 12)): # valid key entry, not a shortcut
      print("char should be entered")

      # reset selection
      if (self._selection[0] != self._selection[1]):
        self._selection = (self._position, self._position)

      # update text
      if self._insertindex == 0:
        self._grid[self._position] = event.char + "  "
      elif self._insertindex == 1:
        self._grid[self._position] = self._grid[self._position][0] + event.char + " "
      elif self._insertindex == 2:
        self._grid[self._position] = self._grid[self._position][0:2] + event.char
      self._insertindex += 1

      if self._position in self._canvasitems.keys():
        self._canvas.itemconfig(self._canvasitems[self._position],
                                text = self._grid[self._position])
      else:
        loc = self.getCanvasLoc(self._position)
        self._canvasitems[self._position] = self._canvas.create_text(loc[0],
                                              loc[1],
                                              text = self._grid[self._position],
                                              font = (TRIPLET_FONT, -TRIPLET_HEIGHT),
                                              anchor = NW)

      if self._insertindex == 3:
        self.advance()


  ###############
  # advance
  #   Moves position in the current direction.
  def advance(self):
    self._canvas.itemconfig(self._rects[self._position],
                            fill = NORMAL_FILL,
                            outline = NORMAL_BORDER_COLOR,
                            width = NORMAL_BORDER_WIDTH)
    if self._direction == "up":
      self._position = (self._position[0], self._position[1] - 1)
    elif self._direction == "down":
      self._position = (self._position[0], self._position[1] + 1)
    elif self._direction == "left":
      self._position = (self._position[0] - 1, self._position[1])
    elif self._direction == "right":
      self._position = (self._position[0] + 1, self._position[1])
    rect_idx = (self._position[0] - self._canvastopleft[0],
                self._position[1] - self._canvastopleft[1])
    self._canvas.itemconfig(self._rects[self._position],
                            fill = ACTIVE_FILL,
                            outline = ACTIVE_BORDER_COLOR,
                            width = ACTIVE_BORDER_WIDTH)

    self._selection = (self._position, self._position)
    self._insertindex = 0

  ###############
  # updateCanvasItems
  #   Updates canvasitems of a given grid cell.
  def updateCanvasItems(self):
    self._canvas.delete("all")
    self.initCanvasRects()
    for key in self._grid.keys():
      loc = self.getCanvasLoc(key)
      self._canvasitems[key] = self._canvas.create_text(loc[0], loc[1],
                                text = self._grid[key],
                                font = (TRIPLET_FONT, -TRIPLET_HEIGHT),
                                anchor = NW)

  ###############
  # initCanvasRects
  #   Initializes canvas cells.
  def initCanvasRects(self):
    for x in range(NUM_TRIPLETS_X):
      for y in range(NUM_TRIPLETS_Y):
        loc = self.getCanvasLoc(x,y)
        self._rects[(x,y)] = self._canvas.create_rectangle(loc[0], loc[1],
                                loc[0] + TRIPLET_WIDTH,
                                loc[1] + TRIPLET_HEIGHT,
                                fill = NORMAL_FILL,
                                outline = NORMAL_BORDER_COLOR,
                                width = NORMAL_BORDER_WIDTH)
    
    rect = (self._position[0] - self._canvastopleft[0],
            self._position[1] - self._canvastopleft[1])
    self._canvas.itemconfig(self._rects[(0, 0)],
                            fill = ACTIVE_FILL,
                            outline = ACTIVE_BORDER_COLOR,
                            width = ACTIVE_BORDER_WIDTH)

  ###############
  # findByData
  #   Returns all positions in grid that
  #   contain a given string.
  def findByData(self, data):
    locs = []
    for key, val in self._grid.items():
      if data in val:
        locs.append(key)
    return locs

  ###############
  # findByX
  #   Returns all positions in grid with given x loc.
  def findByX(self, xVal):
    locs = []
    for key in self._grid.keys():
      if key[0] == xVal:
        locs.append(key)
    return locs

  ##############
  # findByY
  #   Returns all positions in grid with given y loc.
  def findByY(self, yVal):
    locs = []
    for key in self._grid.keys():
      if key[1] == yVal:
        locs.append(key)
    return locs

  ###############
  # dimensions
  #   Returns the width and height
  #   of the current flow program.
  def dimensions(self):
    minX = 0
    minY = 0
    maxX = 0
    maxY = 0
    for key in self._grid.keys():
      if key[0] < minX:
        minX = key[0]
      if key[1] < minY:
        minY = key[1]
      if key[0] > maxX:
        maxX = key[0]
      if key[1] > maxY:
        maxY = key[1]
    return (maxX - minX, maxY - minY)

  ################
  # getTopLeft
  #   Gets the leftmost and upmost coordinates
  #   in the current flow program.
  def getTopLeft(self):
    minX = 0
    minY = 0
    for key in self._grid.keys():
      if key[0] < minX:
        minX = key[0]
      if key[1] < minY:
        minY = key[1]
    return (minX, minY)


  ##################
  # getCanvasLoc
  #   Gets location of a coordinate on canvas
  def getCanvasLoc(self, coordorx, y = -1):
    if isinstance(coordorx, int):
      return ((coordorx - self._canvastopleft[0]) * TRIPLET_WIDTH + CANVAS_OFFSET[0],
              (y - self._canvastopleft[1]) * TRIPLET_HEIGHT + CANVAS_OFFSET[0])
    else:
      return ((coordorx[0] - self._canvastopleft[0]) * TRIPLET_WIDTH + CANVAS_OFFSET[0],
              (coordorx[1] - self._canvastopleft[1]) * TRIPLET_HEIGHT + CANVAS_OFFSET[1])

  ##################
  # shiftCanvas
  #   Shifts all elements of the canvas
  #   in given direction by one triplet.
  def shiftCanvas(self, direction):
    for item in self._canvas.find_all():
      if direction == "right":
        self._canvas.move(item, -TRIPLET_WIDTH, 0)
      elif direction == "left":
        self._canvas.move(item, TRIPLET_WIDTH, 0)
      elif direction == "up":
        self._canvas.move(item, 0, -TRIPLET_HEIGHT)
      elif direction == "down":
        self._canvas.move(item, 0, TRIPLET_HEIGHT)

  ##################
  # new
  #   Creates new file. If one is loaded,
  #   prompts user to save.
  def new(self, event = None):
    print("new called")

    if self._grid != BASE_GRID:
      self.promptSave()
      self._openfile = ""
      self._grid = {(0,0): "#> "}
      self._position = (0,0)
      self._insertindex = 0
      self.updateCanvasItems()

  ##################
  # promptSave
  #   Prompts user to save file.
  def promptSave(self):
    print("promptSave called")

  ##################
  # open
  #   Initiates dialog to open flow file.
  def open(self, event = None):
    print("open called")
    if self._openfile != "":
      self.promptSave()
    self._openfile = filedialog.askopenfilename(
      filetypes = [("Flow files", "*.fl")])
    if self._openfile != "":
      self.loadIn()
      self.updateCanvasItems()

  ##################
  # loadIn
  #   Loads a file in.
  def loadIn(self):
    f = open(self._openfile,'r')
    lineList = f.readlines()
    f.close()

    x = 0
    y = 0
    for line in lineList:
      for i in range(0,len(line),3):
        if i + 3 < len(line):
          triplet = line[i:i + 3]
          self._grid[(x,y)] = triplet.replace("\n","")
        else:
          triplet = line[i:]
          self._grid[(x,y)] = triplet.replace("\n","") + " "*(3 - len(triplet))
        x += 1
      x = 0
      y += 1

    self.updateCanvasItems()


  ##################
  # save
  #   Saves the current file. If file has not
  #   been saved yet, initiates dialog.
  def save(self, event = None):
    print("save called")
    if self._openfile == "":
      self.saveAs()
    else:
      outfile = open(self._openfile, 'w')
      outfile.write(self.convertToStr())
      outfile.close()

  ##################
  # saveAs
  #   Initiates dialog to save current file.
  def saveAs(self, event = None):
    self._openfile = filedialog.asksaveasfilename(
      filetypes = [("Flow files", "*.fl")])
    if self._openfile != "" and self._openfile[-3:] != ".fl":
      self._openfile += ".fl"
    if self._openfile != "":
      outfile = open(self._openfile, 'w')
      outfile.write(self.convertToStr())
      outfile.close()

  ##################
  # convertToStr
  #   Converts the grid to a string
  def convertToStr(self):
    retStr = ""
    topLeft = self.getTopLeft()
    dim = self.dimensions()
    for y in range(topLeft[1],topLeft[1] + dim[1] + 1):
      for x in range(topLeft[0], topLeft[0] + dim[0] + 1):
        if (x,y) in self._grid.keys():
          retStr += self._grid[(x,y)]
        else:
          retStr += "   "
      retStr += "\n"
    return retStr

  ##################
  # exit
  #   Exits the application.
  def exit(self):
    if self._openfile != "":
      self.promptSave()
    print("exiting")
    self.master.quit()

  ##################
  # find
  #   Initiates dialog to find a string in the file.
  def find(self, event = None):
    print("find called")

  ##################
  # goto
  #   Initiates dialog to goto a coordinate in the file.
  def goto(self, event = None):
    print("goto called")

  ##################
  # help
  #   Initiates help dialog.
  def help(self, event = None):
    print("help called")


"██████████████████████████████████   Main   ██████████████████████████████████"

def main():
  root = Tk()
  root.title(EDITOR_TITLE)
  img = PhotoImage(file = ICON_FILE)
  root.tk.call('wm','iconphoto',root._w,img)

  editor = Editor(root)

  root.mainloop()
  root.destroy()

main()