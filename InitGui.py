#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import sys
import FreeCAD
import FreeCADGui

class gateShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return { 
          'Pixmap': os.path.join(module_path, "icons", "gateAssy.svg"),
          'MenuText': "SluiceGate",
          'ToolTip': "Show/Hide gate"}

    def IsActive(self):
        import gateA
        gateA
        return True

    def Activated(self):
        try:
          import gateA
          gateA.main.d.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")

    def IsActive(self):
        import gateA
        return not FreeCAD.ActiveDocument is None

class gateWorkbench(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join(module_path, "icons", "gateAssy.svg")
        self.__class__.MenuText = "SluiceGate"
        self.__class__.ToolTip = "gate by Pascal"

    def Initialize(self):
        self.commandList = ['gate_Show']
        self.appendToolbar('&gate', self.commandList)
        self.appendMenu("&gate", self.commandList)

    def Activated(self):
        import gateA
        gateA
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
    
FreeCADGui.addWorkbench(gateWorkbench())
FreeCADGui.addCommand("gate_Show", gateShowCommand())    