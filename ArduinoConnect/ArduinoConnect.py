import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import serial.tools.list_ports

#
# ArduinoAppTemplate
#

class ArduinoAppTemplate():
  """ Template class for writing code on top of Arduino Connector
  """
  def __init__(self):
    self.ArduinoNode = slicer.mrmlScene.GetFirstNodeByName("arduinoNode")
    sceneModifiedObserverTag = self.ArduinoNode.AddObserver(vtk.vtkCommand.ModifiedEvent, self.doSomethingWhenNewDataIsRead)

  def doSomethingWhenNewDataIsRead(self, caller, event):
    print("FIRED! %s" % (self.ArduinoNode.GetParameter("Data")))

#
# ArduinoConnect
#

class ArduinoConnect(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Arduino Connect" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Developer Tools"]
    self.parent.dependencies = []
    self.parent.contributors = ["Paolo Zaffino (Magna Graecia University of Catanzaro, Italy)", "Domenico Leuzzi (Magna Graecia University of Catanzaro, Italy)", "Virgilio Sabatino (Magna Graecia University of Catanzaro, Italy)", "Andras Lasso (PerkLab, Queen's)", "Maria Francesca Spadea (Magna Graecia University of Catanzaro, Italy)"]
    self.parent.helpText = """
    This module allows to connect and transmit/receive data from Arduino board. On top of this users can build applications.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """ """ # replace with organization, grant and thanks.

    # If needed install serial pylibrary before imporing. If already installed, just import it.
    try:
      import serial
    except ModuleNotFoundError:
      slicer.util.pip_install("pyserial")
      import serial


#
# ArduinoConnectWidget
#

class ArduinoConnectWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    self.logic = ArduinoConnectLogic()
    arduinoApp = ArduinoAppTemplate()

    # Load widget from .ui file (created by Qt Designer)
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/ArduinoConnect.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # connections
    self.ui.portSelectorComboBox.setEnabled(False)
    self.ui.detectDevice.connect('clicked(bool)', self.onDetectDeviceButton)
    self.ui.connectButton.connect('toggled(bool)', self.onConnectButton)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onConnectButton(self, toggle):

    # clicked connect and the device list has elements
    if toggle and self.ui.portSelectorComboBox.currentText != "":

        self.connected = self.logic.connect(self.ui.portSelectorComboBox.currentText,self.ui.baudSelectorComboBox.currentText)

        if self.connected:
          self.ui.connectButton.setText("Disconnect")
          self.ui.connectButton.setStyleSheet("background-color:#ff0000")
        else:
          self.deviceError("Device not found", "Impssible to connect the selected device.", "critical")
          self.ui.connectButton.setChecked(False)
          self.ui.connectButton.setText("Connect")
          self.ui.connectButton.setStyleSheet("background-color:#f1f1f1;")

    # clicked connect but device list has no elements
    elif toggle and self.ui.portSelectorComboBox.currentText == "":
        self.deviceError("Ports scan", "Any device has been set!", "warning")
        self.ui.connectButton.setChecked(False)
        return

    # clicked disconnect with a running connection
    elif not toggle and self.logic.arduinoConnection is not None and self.connected:
      self.logic.disconnect()
      self.ui.connectButton.setText("Connect")
      self.ui.connectButton.setStyleSheet("background-color:#f1f1f1;")

  def onDetectDeviceButton(self, clicked):

    self.ui.portSelectorComboBox.setEnabled(True)
    self.ui.portSelectorComboBox.clear()

    devices = [port.device for port in serial.tools.list_ports.comports() if port[2] != 'n/a']

    if len(devices)==0:
        self.deviceError("Ports scan", "Any device has been found!", "warning")
    elif len(devices)>0:
        for device in devices:
            self.ui.portSelectorComboBox.addItem(device)

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

class ArduinoConnectLogic(ScriptedLoadableModuleLogic):
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

      self.arduinoConnection = None

  def connect(self, port,baud):

      slicer.arduinoData = {}
      slicer.arduinoData["lastMessage"] = None

      try:
        self.arduinoConnection = serial.Serial(port,baud)
      except serial.serialutil.SerialException:
        return False

      self.arduinoEndOfLine = '\n'
      self.arduinoRefreshRateFps = 10.0
      qt.QTimer.singleShot(1000/self.arduinoRefreshRateFps, self.pollSerialDevice)
      return True

  def disconnect(self):
      self.arduinoConnection.close()
      self.arduinoConnection = None

  def pollSerialDevice(self):

      if self.arduinoConnection is None:
        return

      if self.arduinoConnection.isOpen() and self.arduinoConnection.in_waiting == 0: # No messages from arduino
          qt.QTimer.singleShot(1000/self.arduinoRefreshRateFps, self.pollSerialDevice)
      elif self.arduinoConnection.isOpen() and self.arduinoConnection.in_waiting > 0: # Some messages from arduino
          arduinoReceiveBuffer = self.arduinoConnection.readline().decode('ascii')
          if self.arduinoEndOfLine in arduinoReceiveBuffer: # Valid message
              message = arduinoReceiveBuffer.split(self.arduinoEndOfLine)[0]
              message = self.processMessage(message)
              if len(message) >= 1:

                  slicer.arduinoData["lastMessage"] = message

                  print("FROM LOGIC: %s" % (str(slicer.arduinoData["lastMessage"])))

                  # Fire a message even if the message is unchanged
                  if message == self.parameterNode.GetParameter("Data"):
                    self.parameterNode.Modified()
                  else:
                    self.parameterNode.SetParameter("Data", message)

          qt.QTimer.singleShot(1000/self.arduinoRefreshRateFps, self.pollSerialDevice)

  def processMessage(self, msg):
      return msg


class ArduinoConnectTest(ScriptedLoadableModuleTest):
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
    self.test_ArduinoConnect1()

  def test_ArduinoConnect1(self):
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
    logic = ArduinoConnectLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
