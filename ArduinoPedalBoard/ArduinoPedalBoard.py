import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import shutil, subprocess, json

# If needed install serial pylibrary before imporing. If already installed, just import it.
try:
  import serial
  import serial.tools.list_ports
except ModuleNotFoundError:
  slicer.util.pip_install("pyserial")
  import serial
  import serial.tools.list_ports


#
# ArduinoPedalBoard Class dev. Domenico Leuzzi
#


class ArduinoPedalBoardViews(ScriptedLoadableModule):
    
    
  def __init__(self):
    
    self.ArduinoNode = slicer.mrmlScene.GetFirstNodeByName("arduinoNode")
    sceneModifiedObserverTag = self.ArduinoNode.AddObserver(vtk.vtkCommand.ModifiedEvent, self.button3IsPushed)
    
    # Get Slice Node from Scene
    self.red_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    self.yellow_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    self.green_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    
    self.c=0 #Counter Check Value for change views
        
  def button3IsPushed(self, caller, event):
  
    message = self.ArduinoNode.GetParameter("Data")
    #self.monitor.insertPlainText(message)
       
    #
    # Control Button Pressed From Arduino
    
    if(message>str(19) and message <str(21)): #N.B. Serial Value == 20    

        # Counter Check Value Increase
        self.c+=1
        
        if(self.c==1):   
            # Set Slice Node from Scene (Red)
            
            self.red_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed").GetID(),"\n")  
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())           
       
        if(self.c==2):
            # Set Slice Node from Scene (Yellow)
            self.yellow_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow").GetID(),"\n")
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpYellowSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())
            
        if(self.c==3):
            # Set Slice Node from Scene (Green)
            self.green_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")   
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen").GetID(),"\n")
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpGreenSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())
            
        if(self.c==4):
            # Default LayoutUpView
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
            
            self.c=0    #Reset Counter Check value 
 
        
    if((message>=str(0) and message<str(1)) and self.c==1):   #Red Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.red_Slice.SetSliceOffset(self.red_Slice.GetSliceOffset()-0.5)    
                
        # Print Slice Node Offset
        print("Offset Red Slice:",self.red_Slice.GetSliceOffset())            
        
        
    if((message>=str(0) and message<str(1)) and self.c==2):  #Yellow Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.yellow_Slice.SetSliceOffset(self.yellow_Slice.GetSliceOffset()-0.5)    
                
        # Print Slice Node Offset
        print("Offset Yellow Slice:",self.yellow_Slice.GetSliceOffset()) 
        
        
    if((message>=str(0) and message<str(1)) and self.c==3):  #Green Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.green_Slice.SetSliceOffset(self.green_Slice.GetSliceOffset()-0.5)   
                
        # Print Slice Node Offset
        print("Offset Green Slice:",self.green_Slice.GetSliceOffset()) 
          
        
    if((message>=str(5) and message<str(6)) and self.c==1): #N.B. Serial Value == 5 #Red Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.red_Slice.SetSliceOffset(self.red_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Red Slice:",self.red_Slice.GetSliceOffset()) 
        
        
    if((message>=str(5) and message<str(6)) and self.c==2):  #Yellow Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.yellow_Slice.SetSliceOffset(self.yellow_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Yellow Slice:",self.yellow_Slice.GetSliceOffset())        
        
        
    if((message>=str(5) and message<str(6)) and self.c==3):  #Green Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.green_Slice.SetSliceOffset(self.green_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Green Slice:",self.green_Slice.GetSliceOffset())          
     
     

#--------------- Second Class (Arduino Button Central)

class ArduinoPedalBoardViewsButtonCentral(ScriptedLoadableModule):


  def __init__(self):
  
    self.ArduinoNode = slicer.mrmlScene.GetFirstNodeByName("arduinoNode")
    sceneModifiedObserverTag = self.ArduinoNode.AddObserver(vtk.vtkCommand.ModifiedEvent, self.button2IsPushed)
    
    # Get Slice Node from Scene
    self.red_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    self.yellow_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    self.green_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    
    self.c=0 #Counter Check Value for change views
        
  def button2IsPushed(self, caller, event):
  
    message = self.ArduinoNode.GetParameter("Data")
       
    #
    # Control Button Pressed From Arduino
    
    if(message>=str(0) and message <str(1)): #N.B. Serial Value == 0    

        # Counter Check Value Increase
        self.c+=1
        
        if(self.c==1):   
            # Set Slice Node from Scene (Red)
            
            self.red_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed").GetID(),"\n")  
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())           
       
        if(self.c==2):
            # Set Slice Node from Scene (Yellow)
            self.yellow_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow").GetID(),"\n")
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpYellowSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())
            
        if(self.c==3):
            # Set Slice Node from Scene (Green)
            self.green_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")   
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen").GetID(),"\n")
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpGreenSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())
            
        if(self.c==4):
            # Default LayoutUpView
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
            
            self.c=0    #Reset Counter Check value 
 
        
    if((message>=str(20) and message<str(21)) and self.c==1):   #Red Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.red_Slice.SetSliceOffset(self.red_Slice.GetSliceOffset()-0.5)    
                
        # Print Slice Node Offset
        print("Offset Red Slice:",self.red_Slice.GetSliceOffset())            
        
        
    if((message>=str(20) and message<str(21)) and self.c==2):  #Yellow Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.yellow_Slice.SetSliceOffset(self.yellow_Slice.GetSliceOffset()-0.5)    
                
        # Print Slice Node Offset
        print("Offset Yellow Slice:",self.yellow_Slice.GetSliceOffset()) 
        
        
    if((message>=str(20) and message<str(21)) and self.c==3):  #Green Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.green_Slice.SetSliceOffset(self.green_Slice.GetSliceOffset()-0.5)   
                
        # Print Slice Node Offset
        print("Offset Green Slice:",self.green_Slice.GetSliceOffset()) 
          
        
    if((message>=str(5) and message<str(6)) and self.c==1): #N.B. Serial Value == 5 #Red Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.red_Slice.SetSliceOffset(self.red_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Red Slice:",self.red_Slice.GetSliceOffset()) 
        
        
    if((message>=str(5) and message<str(6)) and self.c==2):  #Yellow Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.yellow_Slice.SetSliceOffset(self.yellow_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Yellow Slice:",self.yellow_Slice.GetSliceOffset())        
        
        
    if((message>=str(5) and message<str(6)) and self.c==3):  #Green Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.green_Slice.SetSliceOffset(self.green_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Green Slice:",self.green_Slice.GetSliceOffset())          


#--------------- Third Class (Arduino Button Right)

class ArduinoPedalBoardViewsButtonRight(ScriptedLoadableModule):


  def __init__(self):
  
    self.ArduinoNode = slicer.mrmlScene.GetFirstNodeByName("arduinoNode")
    sceneModifiedObserverTag = self.ArduinoNode.AddObserver(vtk.vtkCommand.ModifiedEvent, self.button1IsPushed)
    
    # Get Slice Node from Scene
    self.red_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    self.yellow_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    self.green_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    
    self.c=0 #Counter Check Value for change views
        
  def button1IsPushed(self, caller, event):
  
    message = self.ArduinoNode.GetParameter("Data")
       
    #
    # Control Button Pressed From Arduino
    
    if(message>=str(5) and message <str(6)): #N.B. Serial Value == 5    

        # Counter Check Value Increase
        self.c+=1
        
        if(self.c==1):   
            # Set Slice Node from Scene (Red)
            
            self.red_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed").GetID(),"\n")  
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())           
       
        if(self.c==2):
            # Set Slice Node from Scene (Yellow)
            self.yellow_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow").GetID(),"\n")
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpYellowSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())
            
        if(self.c==3):
            # Set Slice Node from Scene (Green)
            self.green_Slice = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")   
            print(slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen").GetID(),"\n")
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpGreenSliceView)
            print(slicer.app.layoutManager().layoutLogic().GetLayoutNode().GetID())
            
        if(self.c==4):
            # Default LayoutUpView
            slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
            
            self.c=0    #Reset Counter Check value 
 
        
    if((message>=str(20) and message<str(21)) and self.c==1):   #Red Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.red_Slice.SetSliceOffset(self.red_Slice.GetSliceOffset()-0.5)    
                
        # Print Slice Node Offset
        print("Offset Red Slice:",self.red_Slice.GetSliceOffset())            
        
        
    if((message>=str(20) and message<str(21)) and self.c==2):  #Yellow Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.yellow_Slice.SetSliceOffset(self.yellow_Slice.GetSliceOffset()-0.5)    
                
        # Print Slice Node Offset
        print("Offset Yellow Slice:",self.yellow_Slice.GetSliceOffset()) 
        
        
    if((message>=str(20) and message<str(21)) and self.c==3):  #Green Case
    
        print("Button DOWN Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.green_Slice.SetSliceOffset(self.green_Slice.GetSliceOffset()-0.5)   
                
        # Print Slice Node Offset
        print("Offset Green Slice:",self.green_Slice.GetSliceOffset()) 
          
        
    if((message>=str(0) and message<str(1)) and self.c==1): #N.B. Serial Value == 0 #Red Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.red_Slice.SetSliceOffset(self.red_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Red Slice:",self.red_Slice.GetSliceOffset()) 
        
        
    if((message>=str(0) and message<str(1)) and self.c==2):  #Yellow Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.yellow_Slice.SetSliceOffset(self.yellow_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Yellow Slice:",self.yellow_Slice.GetSliceOffset())        
        
        
    if((message>=str(0) and message<str(1)) and self.c==3):  #Green Case
    
        print("Button UP Pressed, [Operation num.]:",message)
        
        # Changing Slice Node Offset 
        self.green_Slice.SetSliceOffset(self.green_Slice.GetSliceOffset()+0.5)    
                
        # Print Slice Node Offset
        print("Offset Green Slice:",self.green_Slice.GetSliceOffset())          


#
# Class ArduinoPedalBoard
#

class ArduinoPedalBoard(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ArduinoPedalBoard" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Developer Tools"]
    self.parent.dependencies = []
    self.parent.contributors = ["Paolo Zaffino (Magna Graecia University of Catanzaro, Italy)", "Domenico Leuzzi (Magna Graecia University of Catanzaro, Italy)", "Virgilio Sabatino (Magna Graecia University of Catanzaro, Italy)", "Andras Lasso (PerkLab, Queen's)", "Maria Francesca Spadea (Magna Graecia University of Catanzaro, Italy)"]
    self.parent.helpText = """
    This module allows to connect and transmit/receive data from Arduino board. On top of this users can build applications.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """ """ # replace with organization, grant and thanks. 


#
# ArduinoConnectWidget
#

class ArduinoPedalBoardWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Plotter
    self.plotter = None

    # Configuration
    self.configFileName = __file__.replace("ArduinoPedalBoard.py", "Resources%sArduinoPedalBoardConfig.json" % (os.sep))
    with open(self.configFileName) as f:
      self.config = json.load(f)

    self.logic = ArduinoPedalBoardLogic()

    # Load widget from .ui file (created by Qt Designer)
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/ArduinoPedalBoard.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)
    
    #Edit By Domenico Leuzzi
    #(NEW BUTTONS)
    self.ui.SetButton1.connect('clicked(bool)', self.onSetButton1) 
    self.ui.SetButton2.connect('clicked(bool)', self.onSetButton2)
    self.ui.SetButton3.connect('clicked(bool)', self.onSetButton3)

    # Add vertical spacer
    self.layout.addStretch(1)
    

  def cleanup(self):
    pass

  def writeConfig(self):
    with open(self.configFileName, 'w') as json_file:
      json.dump(self.config, json_file)

  def autoFindIDEExe(self):
    arduinoIDEExe = shutil.which("arduino")
    if arduinoIDEExe is None:
      return ""
    else:
      return arduinoIDEExe
      
      
      
  def onSetButton1(self, clicked): 

    # Alert
    if(((self.ui.button1_Choice.currentText=="Change Viewer") and (self.ui.button2_Choice.currentText=="Change Viewer")) or ((self.ui.button2_Choice.currentText=="Change Viewer") and (self.ui.button3_Choice.currentText=="Change Viewer")) or ((self.ui.button1_Choice.currentText=="Change Viewer") and (self.ui.button3_Choice.currentText=="Change Viewer"))):
        
        self.deviceError("Operation Not Valid.", "Changer Views are duplicate. You must choise only one 'Changer'.", "critical")
               
    elif(self.ui.button1_Choice.currentText=="Change Viewer"):
 
        ArduinoPedalBoardViewsButtonRight()

        self.ui.button1_Choice.setEnabled(False)
        self.ui.button2_Choice.setEnabled(False)
        self.ui.button3_Choice.setEnabled(False)

        #Change Text in combobox
        self.ui.button2_Choice.setCurrentText("Slice Offset +")
        self.ui.button3_Choice.setCurrentText("Slice Offset -")
        
    # Warning Error    
    elif((self.ui.button1_Choice.currentText=="Select Option") or (self.ui.button2_Choice.currentText=="Select Option") or (self.ui.button3_Choice.currentText=="Select Option")):
    
        self.deviceError("Missed Option", "Changer Viewer not found!", "warning")
          
          
    #
    # Method Button2
    #
 
  def onSetButton2(self, clicked):  
   
    # Critical Error
    if(((self.ui.button2_Choice.currentText=="Change Viewer") and (self.ui.button1_Choice.currentText=="Change Viewer")) or ((self.ui.button2_Choice.currentText=="Change Viewer") and (self.ui.button3_Choice.currentText=="Change Viewer")) or ((self.ui.button1_Choice.currentText=="Change Viewer") and (self.ui.button3_Choice.currentText=="Change Viewer"))):
        
        self.deviceError("Operation Not Valid.", "Changer Views are duplicate. You must choise only one 'Changer'.", "critical")
               
    elif(self.ui.button2_Choice.currentText=="Change Viewer"):
 
        ArduinoPedalBoardViewsButtonCentral()

        self.ui.button1_Choice.setEnabled(False)
        self.ui.button2_Choice.setEnabled(False)
        self.ui.button3_Choice.setEnabled(False)

        #Change Text in combobox
        self.ui.button1_Choice.setCurrentText("Slice Offset +")
        self.ui.button3_Choice.setCurrentText("Slice Offset -")       
        
    # Warning Error    
    elif((self.ui.button1_Choice.currentText=="Select Option") or (self.ui.button2_Choice.currentText=="Select Option") or (self.ui.button3_Choice.currentText=="Select Option")):
    
        self.deviceError("Missed Option", "Changer Viewer not found!", "warning")  
       
       
    #
    # Method Button3
    #          
           
  def onSetButton3(self, clicked):
  
    # Alert
    if(((self.ui.button3_Choice.currentText=="Change Viewer") and (self.ui.button1_Choice.currentText=="Change Viewer")) or ((self.ui.button2_Choice.currentText=="Change Viewer") and (self.ui.button3_Choice.currentText=="Change Viewer")) or ((self.ui.button2_Choice.currentText=="Change Viewer") and (self.ui.button3_Choice.currentText=="Change Viewer"))):
        
        self.deviceError("Operation Not Valid.", "Changer Views are duplicate. You must choise only one 'Changer'.", "critical")
                
    elif(self.ui.button3_Choice.currentText=="Change Viewer"):

        ArduinoPedalBoardViews()

        self.ui.button1_Choice.setEnabled(False)
        self.ui.button2_Choice.setEnabled(False)
        self.ui.button3_Choice.setEnabled(False)

        #Change Text in combobox
        self.ui.button1_Choice.setCurrentText("Slice Offset +")
        self.ui.button2_Choice.setCurrentText("Slice Offset -")           
            
    # Warning Error    
    elif((self.ui.button1_Choice.currentText=="Select Option") or (self.ui.button2_Choice.currentText=="Select Option") or (self.ui.button3_Choice.currentText=="Select Option")):
    
        self.deviceError("Missed Option", "Changer Viewer not found!", "warning")
             
        
  def deviceError(self, title, message, error_type="warning"):
    deviceMBox = qt.QMessageBox()
    if error_type == "warning":
      deviceMBox.setIcon(qt.QMessageBox().Warning)
    elif error_type == "critical":
      deviceMBox.setIcon(qt.QMessageBox().Critical)
    deviceMBox.setWindowTitle(title)
    deviceMBox.setText(message)
    deviceMBox.exec()

#
# ArduinoConnectLogic
#

class ArduinoPedalBoardLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
      ScriptedLoadableModuleLogic.__init__(self)

      import serial

      self.parameterNode=slicer.vtkMRMLScriptedModuleNode()
      self.parameterNode.SetName("arduinoNode")
      slicer.mrmlScene.AddNode(self.parameterNode)



class ArduinoPedalBoardTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    self.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ArduinoPedalBoard1()

  def test_ArduinoPedalBoard11(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://self.kitware.com/midas3/download?items=5767',
      checksums='SHA256:12d17fba4f2e1f1a843f0757366f28c3f3e1a8bb38836f0de2a32bb1cd476560')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = ArduinoPedalBoardLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
