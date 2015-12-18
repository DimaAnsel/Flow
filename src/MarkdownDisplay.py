##########################
# MarkdownDisplay.py
# Noah Ansel
# 2015-12-16
# --------------
# A tkinter class for displaying
# markdown text in a scrollable window.
#########################

from tkinter import *

class MarkdownDisplay(Frame):

  DEFAULT_HEIGHT = 32
  DEFAULT_WIDTH = 64
  BG_COLOR = "#FFFFFF"

  NORMAL_FONT = ("Helvetica", 12)
  NORMAL_BOLD = ("Helvetica", 12, "bold")
  NORMAL_ITALIC = ("Helvetica", 12, "italic")
  NORMAL_BOLDITALIC = ("Helvetica", 12, "bold", "italic")
  HEADING_1_FONT = ("Helvetica", 42, "bold")
  HEADING_2_FONT = ("Helvetica", 36, "bold")
  HEADING_3_FONT = ("Helvetica", 30, "bold")
  HEADING_4_FONT = ("Helvetica", 24, "bold")
  HEADING_5_FONT = ("Helvetica", 18, "bold")
  HEADING_6_FONT = ("Helvetica", 14, "bold")
  CODE_BLOCK_FONT = ("Courier", 12)


  ###############
  # init
  #   Initializes class and sets up
  #   scrollbar and display classes.
  def __init__(self,
               master = None,
               height = DEFAULT_HEIGHT,
               width = DEFAULT_WIDTH):
    Frame.__init__(self, master, width = width, height = height)

    self.createWidgets()
    self.__text = ""

  ###############
  # createWidgets
  #   Sets up scrollbar and display
  #   widgets. Also, defines font tags.
  def createWidgets(self):
    self.__scrollbar = Scrollbar(self)
    self.__scrollbar.pack(side = "right", fill = Y)
    self.__display = Text(self,
                          bg = MarkdownDisplay.BG_COLOR,
                          yscrollcommand = self.__scrollbar.set)
    self.__display.pack(side = "right", fill = BOTH)
    self.__scrollbar.config(command = self.__display.yview)

    # set up fonts
    self.__display.tag_config("normal", font = MarkdownDisplay.NORMAL_FONT)
    self.__display.tag_config("bold", font = MarkdownDisplay.NORMAL_BOLD)
    self.__display.tag_config("italic", font = MarkdownDisplay.NORMAL_ITALIC)
    self.__display.tag_config("bold-italic", font = MarkdownDisplay.NORMAL_BOLDITALIC)
    self.__display.tag_config("code", font = MarkdownDisplay.CODE_BLOCK_FONT)

    self.__display.tag_config("h1", font = MarkdownDisplay.HEADING_1_FONT)
    self.__display.tag_config("h2", font = MarkdownDisplay.HEADING_2_FONT)
    self.__display.tag_config("h3", font = MarkdownDisplay.HEADING_3_FONT)
    self.__display.tag_config("h4", font = MarkdownDisplay.HEADING_4_FONT)
    self.__display.tag_config("h5", font = MarkdownDisplay.HEADING_5_FONT)
    self.__display.tag_config("h6", font = MarkdownDisplay.HEADING_6_FONT)

  ###############
  # set_text
  #   Reloads the MarkdownDisplay from a new
  #   string of markdown text.
  def set_text(self, text):
    self.__text = text

    self._parseText()

  ###############
  # _parseText
  #   Deletes previous sections and 
  def _parseText(self):
    self.__display.delete(1.0, END)

if __name__ == "__main__":
  root = Tk()
  md = MarkdownDisplay(root)
  md.pack()

  root.mainloop()