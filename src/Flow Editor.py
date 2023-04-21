#########################
# Flow Editor.py
# Dima Ansel
# 2015-11-22
# --------------
# An editor for making Flow
# files, implemented with Tkinter.
#########################

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

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
BORDER_OFFSET = 5
RULER_WIDTH = 16
CANVAS_WIDTH = NUM_TRIPLETS_X * TRIPLET_WIDTH + RULER_WIDTH
CANVAS_HEIGHT = NUM_TRIPLETS_Y * TRIPLET_HEIGHT + RULER_WIDTH
CANVAS_BG_COLOR = "#CCCCFF"
CANVAS_OFFSET = (BORDER_OFFSET + RULER_WIDTH, BORDER_OFFSET + RULER_WIDTH)

RULER_FILL = "#EEEEEE"
RULER_BORDER_COLOR = "#000000"
RULER_BORDER_WIDTH = 1.0

NORMAL_FILL = ""
NORMAL_BORDER_COLOR = "#888888"
NORMAL_BORDER_WIDTH = 1.0

ACTIVE_FILL = "#FFFFFF"
ACTIVE_BORDER_COLOR = "#555555"
ACTIVE_BORDER_WIDTH = 1.4

SELECTED_FILL = "#8888CC"
SELECTED_BORDER_COLOR = "#555555"
SELECTED_BORDER_WIDTH = 1.4


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
    self._clipboard = {"size": (0, 0)}

    # canvas tracking stuff
    self._canvasitems = {}
    self._grid = {(0, 0): "#> "}
    self._rects = {}
    self._canvastopleft = (0, 0)
    self._rulers = {}

    # setup
    self.createWidgets()
    self._canvas.focus_set()
    self.master.protocol("WM_DELETE_WINDOW", self.closeProgram)
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
    self.initCanvasRulers()

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
    self.editmenu.add_command(label = "Cut     (Ctr-X)", command = self.cut)
    self.editmenu.add_command(label = "Copy  (Ctr-C)", command = self.copy)
    self.editmenu.add_command(label = "Paste  (Ctr-V)", command = self.paste)
    self.editmenu.add_separator()
    self.editmenu.add_command(label = "Find    (Ctr-F)", command = self.find)
    self.editmenu.add_command(label = "Goto   (Ctr-G)", command = self.goto)
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
    self.bind_all("<Control-x>", self.cut)
    self.bind_all("<Control-c>", self.copy)
    self.bind_all("<Control-v>", self.paste)
    self.bind_all("<Control-f>", self.find)
    self.bind_all("<Control-g>", self.goto)
    self.bind_all("<F1>", self.help)

    self._canvas.bind("<Left>", self.moveLeft)
    self._canvas.bind("<Right>", self.moveRight)
    self._canvas.bind("<Up>", self.moveUp)
    self._canvas.bind("<Down>", self.moveDown)

    self._canvas.bind("<Shift-Left>", self.selectLeft)
    self._canvas.bind("<Shift-Right>", self.selectRight)
    self._canvas.bind("<Shift-Up>", self.selectUp)
    self._canvas.bind("<Shift-Down>", self.selectDown)

    self._canvas.bind("<Delete>", self.delText)
    self._canvas.bind("<BackSpace>", self.backspaceText)

  ###############
  # delText
  #   Deletes text in the selected field.
  def delText(self, event = None):
    print("delText called")
    for x in range(self._selection[0][0], self._selection[1][0] + 1):
      for y in range(self._selection[0][1], self._selection[1][1] + 1):
        if (x, y) in self._grid.keys():
          del self._grid[(x, y)]
          self._canvas.delete(self._canvasitems[(x, y)])
          del self._canvasitems[(x, y)]

  ###############
  # backspaceText
  #   Backspaces a character.
  def backspaceText(self, event = None):
    print("backspaceText called")
    self._selection = [self._position, self._position]
    if self._insertindex == 0:
      self.advance(-1)
      if self._position in self._grid.keys():
        self._grid[self._position] = self._grid[self._position][:2] + " "
        self._insertindex = 2
    elif self._insertindex == 1:
      del self._grid[self._position]
      self._canvas.delete(self._canvasitems[self._position])
      del self._canvasitems[self._position]
      self._insertindex = 0
      return # to avoid canvas item set error
    elif self._insertindex == 2:
      if self._position in self._grid.keys():
        self._grid[self._position] = self._grid[self._position][0] + "  "
      self._insertindex = 1
    if self._position in self._grid.keys():
      self._canvas.itemconfig(self._canvasitems[self._position],
                              text = self._grid[self._position])


  ###############
  # cut
  #   Copies selected text to clipboard
  #   and then deletes from file.
  def cut(self, event = None):
    print("cut called")
    self._clipboard = {}
    self._clipboard["size"] = (self._selection[1][0] - self._selection[0][0],
                               self._selection[1][1] - self._selection[0][1])
    for x in range(self._selection[0][0], self._selection[1][0] + 1):
      for y in range(self._selection[0][1], self._selection[1][1] + 1):
        if (x, y) in self._grid.keys():
          pos = (x - self._selection[0][0], y - self._selection[0][1])
          self._clipboard[pos] = self._grid[(x, y)]
          # now delete stuff
          del self._grid[(x, y)]
          self._canvas.delete(self._canvasitems[(x, y)])
          del self._canvasitems[(x, y)]

  ###############
  # copy
  #   Copies selected text to clipboard.
  def copy(self, event = None):
    print("copy called")
    self._clipboard = {}
    self._clipboard["size"] = (self._selection[1][0] - self._selection[0][0],
                               self._selection[1][1] - self._selection[0][1])
    for x in range(self._selection[0][0], self._selection[1][0] + 1):
      for y in range(self._selection[0][1], self._selection[1][1] + 1):
        if (x, y) in self._grid.keys():
          pos = (x - self._selection[0][0], y - self._selection[0][1])
          self._clipboard[pos] = self._grid[(x, y)]

  ###############
  # paste
  #   Pastes selected text from clipboard to
  #   file, starting from top left.
  def paste(self, event = None):
    print("paste called")
    for x in range(self._clipboard["size"][0] + 1):
      for y in range(self._clipboard["size"][1] + 1):
        pos = (self._selection[0][0] + x, self._selection[0][1] + y)
        if (x, y) in self._clipboard.keys(): # replace
          self._grid[pos] = self._clipboard[(x, y)]
          if pos in self._canvasitems.keys():
            self._canvas.itemconfig(self._canvasitems[pos],
                                    text = self._grid[pos])
          else:
            loc = self.getCanvasLoc(pos)
            self._canvasitems[pos] = self._canvas.create_text(loc[0],
                                      loc[1],
                                      text = self._grid[pos],
                                      font = (TRIPLET_FONT, -TRIPLET_HEIGHT),
                                      anchor = NW)
        else: # clear
          if pos in self._grid.keys():
            del self._grid[pos]
            self._canvas.delete(self._canvasitems[pos])
            del self._canvasitems[pos]
    self.raiseRuler()
  ###############
  # b1Action
  #   Performs the left-click action.
  #   Updates the currently position.
  def b1Action(self, event):
    if event.x < CANVAS_OFFSET[0] or event.y < CANVAS_OFFSET[1]:
      return # ignore
    self.colorSelection("normal")

    x = (event.x - CANVAS_OFFSET[0]) // TRIPLET_WIDTH
    y = (event.y - CANVAS_OFFSET[1]) // TRIPLET_HEIGHT
    self._position = (x + self._canvastopleft[0], y + self._canvastopleft[1])
    self._insertindex = 0
    self._selection = [self._position, self._position]

    self.colorSelection("active")

  ###############
  # b1Drag
  #   Performs the left button drag action.
  #   Updates selection and current position.
  def b1Drag(self, event):
    if event.x < CANVAS_OFFSET[0] or event.y < CANVAS_OFFSET[1]:
      return # ignore
    x = (event.x - CANVAS_OFFSET[0]) // TRIPLET_WIDTH
    y = (event.y - CANVAS_OFFSET[1]) // TRIPLET_HEIGHT
    curr = (x + self._canvastopleft[0], y + self._canvastopleft[1])
    
    if self._selection[0][0] > curr[0]: # x
      self._selection[0] = (curr[0], self._selection[0][1])
    elif self._selection[1][0] < curr[0]:
      self._selection[1] = (curr[0], self._selection[1][1])

    if self._selection[0][1] > curr[1]: # y
      self._selection[0] = (self._selection[0][0], curr[1])
    elif self._selection[1][1] < curr[1]:
      self._selection[1] = (self._selection[1][0], curr[1])
    
    self._position = curr # update pos

    # recolor
    self.colorSelection("active")
    self._insertindex = 0

  ###############
  # colorSelection
  #   Colors the selection's rectangles.
  def colorSelection(self, mode):
    if mode == "active":
      mode_fill = SELECTED_FILL
      mode_border_color = SELECTED_BORDER_COLOR
      mode_border_width = SELECTED_BORDER_WIDTH
    elif mode == "normal":
      mode_fill = NORMAL_FILL
      mode_border_color = NORMAL_BORDER_COLOR
      mode_border_width = NORMAL_BORDER_WIDTH
    for x in range(self._selection[0][0], self._selection[1][0] + 1):
      for y in range(self._selection[0][1], self._selection[1][1] + 1):
        if self.isInView(x, y): # valid rectangle
          rect = (x - self._canvastopleft[0], y - self._canvastopleft[1])
          self._canvas.itemconfig(self._rects[rect],
                                  fill = mode_fill,
                                  outline = mode_border_color,
                                  width = mode_border_width)
    if mode == "active" and self.isInView(self._position):
        rect = (self._position[0] - self._canvastopleft[0],
                self._position[1] - self._canvastopleft[1])
        self._canvas.itemconfig(self._rects[rect],
                                fill = ACTIVE_FILL,
                                outline = ACTIVE_BORDER_COLOR,
                                width = ACTIVE_BORDER_WIDTH)




  ###############
  # moveLeft
  #   Moves active cell to left.
  def moveLeft(self, event = None):
    self.colorSelection("normal")
    self._position = (self._position[0] - 1, self._position[1])
    self._selection = [self._position, self._position]
    if not self.isInView(self._position):
      self.shiftView("left")
    self._insertindex = 0
    self.colorSelection("active")


  ###############
  # moveRight
  #   Moves active cell to right.
  def moveRight(self, event = None):
    self.colorSelection("normal")
    self._position = (self._position[0] + 1, self._position[1])
    self._selection = [self._position, self._position]
    if not self.isInView(self._position):
      self.shiftView("right")
    self._insertindex = 0
    self.colorSelection("active")

  ###############
  # moveUp
  #   Moves active cell upwards.
  def moveUp(self, event = None):
    self.colorSelection("normal")
    self._position = (self._position[0], self._position[1] - 1)
    self._selection = [self._position, self._position]
    if not self.isInView(self._position):
      self.shiftView("up")
    self._insertindex = 0
    self.colorSelection("active")

  ###############
  # moveDown
  #   Moves active cell downwards.
  def moveDown(self, event = None):
    self.colorSelection("normal")
    self._position = (self._position[0], self._position[1] + 1)
    self._selection = [self._position, self._position]
    if not self.isInView(self._position):
      self.shiftView("down")
    self._insertindex = 0
    self.colorSelection("active")

  def selectLeft(self, event = None):
    self._position = (self._position[0] - 1, self._position[1])
    
    if self._selection[0][0] > self._position[0]: # x
      self._selection[0] = (self._position[0], self._selection[0][1])

    # recolor
    self.colorSelection("active")
    self._insertindex = 0

  def selectRight(self, event = None):
    self._position = (self._position[0] + 1, self._position[1])

    if self._selection[1][0] < self._position[0]:
      self._selection[1] = (self._position[0], self._selection[1][1])

    # recolor
    self.colorSelection("active")
    self._insertindex = 0

  def selectUp(self, event = None):
    self._position = (self._position[0], self._position[1] - 1)
    
    if self._selection[0][1] > self._position[1]:
      self._selection[0] = (self._selection[0][0], self._position[1])

    # recolor
    self.colorSelection("active")
    self._insertindex = 0

  def selectDown(self, event = None):
    self._position = (self._position[0], self._position[1] + 1)

    if self._selection[1][1] < self._position[1]:
      self._selection[1] = (self._selection[1][0], self._position[1])

    # recolor
    self.colorSelection("active")
    self._insertindex = 0

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
        for x in range(self._selection[0][0], self._selection[1][0] + 1):
          for y in range(self._selection[0][1], self._selection[1][1] + 1):
            if (x,y) != self._position and self.isInView(x, y):
              rect = (x - self._canvastopleft[0], y - self._canvastopleft[1])
              self._canvas.itemconfig(self._rects[rect],
                                      fill = NORMAL_FILL,
                                      outline = NORMAL_BORDER_COLOR,
                                      width = NORMAL_BORDER_WIDTH)
        self._selection = [self._position, self._position]

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
        self.raiseRuler()

      if self._insertindex == 3:
        self.advance()
      elif self._insertindex == 1:
        if event.char == CMD_UP:
          self._direction = "up"
        elif event.char == CMD_DOWN:
          self._direction = "down"
        elif event.char == CMD_LEFT:
          self._direction = "left"
        elif event.char == CMD_RIGHT:
          self._direction = "right"
        else:
          return
        self.advance()
      elif self._grid[self._position][0] == "#" and self._insertindex == 2:
        if event.char == CMD_UP:
          self._direction = "up"
        elif event.char == CMD_DOWN:
          self._direction = "down"
        elif event.char == CMD_LEFT:
          self._direction = "left"
        elif event.char == CMD_RIGHT:
          self._direction = "right"
        else:
          return
        self.advance()


  ###############
  # advance
  #   Moves position in the current direction.
  def advance(self, delta = 1):
    self.colorSelection("normal")
    if self._direction == "up":
      self._position = (self._position[0], self._position[1] - delta)
    elif self._direction == "down":
      self._position = (self._position[0], self._position[1] + delta)
    elif self._direction == "left":
      self._position = (self._position[0] - delta, self._position[1])
    elif self._direction == "right":
      self._position = (self._position[0] + delta, self._position[1])
    rect_idx = (self._position[0] - self._canvastopleft[0],
                self._position[1] - self._canvastopleft[1])
    if not self.isInView(self._position):
      self.shiftView()

    self._selection = [self._position, self._position]
    self._insertindex = 0
    self.colorSelection("active")

  ###############
  # shiftView
  #   Shifts the view in a given direction
  #   in relation to the file data (text).
  def shiftView(self, direction, spaces = 1):
    self.colorSelection("normal")
    if direction == "up":
      self._canvastopleft = (self._canvastopleft[0],
                             self._canvastopleft[1] - 1)
      self.shiftCanvasText("down")
    elif direction == "down":
      self._canvastopleft = (self._canvastopleft[0],
                             self._canvastopleft[1] + 1)
      self.shiftCanvasText("up")
    elif direction == "left":
      self._canvastopleft = (self._canvastopleft[0] - 1,
                             self._canvastopleft[1])
      self.shiftCanvasText("right")
    elif direction == "right":
      self._canvastopleft = (self._canvastopleft[0] + 1,
                             self._canvastopleft[1])
      self.shiftCanvasText("left")

    # renumber rulers
    for x in range(NUM_TRIPLETS_X):
        self._canvas.itemconfig(self._rulers["x"][x],
                                text = str(self._canvastopleft[0] + x))
    for y in range(NUM_TRIPLETS_Y):
        self._canvas.itemconfig(self._rulers["y"][y],
                                text = str(self._canvastopleft[1] + y))
    self.colorSelection("active")

  ###############
  # isInView
  #   True if the given coord is within canvas view.
  def isInView(self, coordorx, y = 0):
    if isinstance(coordorx, int):
      coordorx = (coordorx, y)
    return (self._canvastopleft[0] <= coordorx[0] and
            coordorx[0] < self._canvastopleft[0] + NUM_TRIPLETS_X and
            self._canvastopleft[1] <= coordorx[1] and
            coordorx[1] < self._canvastopleft[1] + NUM_TRIPLETS_Y)
    
  ###############
  # reloadCanvasItems
  #   Reloads canvasitems from the grid.
  def reloadCanvasItems(self):
    self._canvas.delete("all")
    self.initCanvasRects()
    for key in self._grid.keys():
      loc = self.getCanvasLoc(key)
      self._canvasitems[key] = self._canvas.create_text(loc[0], loc[1],
                                text = self._grid[key],
                                font = (TRIPLET_FONT, -TRIPLET_HEIGHT),
                                anchor = NW)
    self.initCanvasRulers() # must be last to keep above other items

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
  # initCanvasRulers
  #   Initializes canvas rulers.
  def initCanvasRulers(self):
    self._rulers["xrect"] = self._canvas.create_rectangle(CANVAS_OFFSET[0],
                              0,
                              CANVAS_WIDTH + BORDER_OFFSET,
                              CANVAS_OFFSET[1],
                              fill = RULER_FILL,
                              outline = RULER_BORDER_COLOR,
                              width = RULER_BORDER_WIDTH)
    self._rulers["yrect"] = self._canvas.create_rectangle(0,
                              CANVAS_OFFSET[1],
                              CANVAS_OFFSET[0],
                              CANVAS_HEIGHT + BORDER_OFFSET,
                              fill = RULER_FILL,
                              outline = RULER_BORDER_COLOR,
                              width = RULER_BORDER_WIDTH)
    self._rulers["square"] = self._canvas.create_rectangle(0,
                              0,
                              CANVAS_OFFSET[0],
                              CANVAS_OFFSET[1],
                              fill = RULER_FILL,
                              outline = RULER_BORDER_COLOR,
                              width = RULER_BORDER_WIDTH)

    self._rulers["x"] = []
    for x in range(self._canvastopleft[0], NUM_TRIPLETS_X + 1):
      text = self._canvas.create_text(CANVAS_OFFSET[0] + (x + 0.5) * TRIPLET_WIDTH,
                                      CANVAS_OFFSET[1] / 2,
                                      text = str(x),
                                      font = (TRIPLET_FONT, -RULER_WIDTH * 4 // 5))
      self._rulers["x"].append(text)
    self._rulers["y"] = []
    for y in range(self._canvastopleft[1], NUM_TRIPLETS_Y + 1):
      text = self._canvas.create_text(CANVAS_OFFSET[0] / 2,
                                      CANVAS_OFFSET[1] + (y + 0.5) * TRIPLET_HEIGHT,
                                      text = str(y),
                                      font = (TRIPLET_FONT, -RULER_WIDTH * 4 // 5))
      self._rulers["y"].append(text)

  ###############
  # raiseRuler
  #   Raises ruler above other elements of canvas.
  def raiseRuler(self):
    self._canvas.tag_raise(self._rulers["xrect"])
    self._canvas.tag_raise(self._rulers["yrect"])
    self._canvas.tag_raise(self._rulers["square"])
    for item in self._rulers["x"]:
      self._canvas.tag_raise(item)
    for item in self._rulers["y"]:
      self._canvas.tag_raise(item)

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
  # shiftCanvasText
  #   Shifts all text elements of the canvas
  #   in given direction by one triplet.
  def shiftCanvasText(self, direction, cells = 1):
    for key, val in self._canvasitems.items():
      if direction == "right":
        self._canvas.move(val, TRIPLET_WIDTH * cells, 0)
      elif direction == "left":
        self._canvas.move(val, -TRIPLET_WIDTH * cells, 0)
      elif direction == "up":
        self._canvas.move(val, 0, -TRIPLET_HEIGHT * cells)
      elif direction == "down":
        self._canvas.move(val, 0, TRIPLET_HEIGHT * cells)

  ##################
  # new
  #   Creates new file. If one is loaded,
  #   prompts user to save.
  def new(self, event = None):
    if self._grid.items() != BASE_GRID.items():
      self.promptSave()
    self._openfile = ""
    self._grid = {(0,0): "#> "}
    self.colorSelection("normal")
    self._position = (0,0)
    self._selection = [(0, 0), (0, 0)]
    self._canvastopleft = (0, 0)
    self.colorSelection("active")
    self._insertindex = 0
    self.reloadCanvasItems()

  ##################
  # promptSave
  #   Prompts user to save file.
  def promptSave(self):
    if messagebox.askquestion("Save","Data will be lost.\nWould you like to save?") == "yes":
      self.save()

  ##################
  # closeProgram
  #   Prompts save, then closes program.
  def closeProgram(self, event = None):
    if self._grid.items() != BASE_GRID.items():
      self.promptSave()
    self.master.destroy()

  ##################
  # open
  #   Initiates dialog to open flow file.
  def open(self, event = None):
    if self._openfile != "":
      self.promptSave()
    self._openfile = filedialog.askopenfilename(
      filetypes = [("Flow files", "*.fl")])
    if self._openfile != "":
      self.loadIn()

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

    self.reloadCanvasItems()


  ##################
  # save
  #   Saves the current file. If file has not
  #   been saved yet, initiates dialog.
  def save(self, event = None):
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

main()