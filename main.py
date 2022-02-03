import subprocess
import os
import sys
from PySide2 import QtCore,QtWidgets,QtGui,QtUiTools
import icons

_this_dir = os.path.dirname(__file__)
_code_base_path = os.path.realpath(_this_dir+"/..")
_code_base_name = os.path.split(_code_base_path)[-1]
_ui_folder_path = os.path.join(_this_dir, "UI")

_UI_Loader = QtUiTools.QUiLoader()

########################################################################
class Modes:
	""""""
	Studio = "Studio"
	Clean  = "Clean"





#----------------------------------------------------------------------
def Maya_Enable_Legacy_Render_Layers(val):
	"""Turns on of off the use of MAYA_ENABLE_LEGACY_RENDER_LAYERS"""
	if val == True and not "MAYA_ENABLE_LEGACY_RENDER_LAYERS" in os.environ:
		os.environ["MAYA_ENABLE_LEGACY_RENDER_LAYERS"] = "1"
	elif "MAYA_ENABLE_LEGACY_RENDER_LAYERS" in os.environ:
		del os.environ["MAYA_ENABLE_LEGACY_RENDER_LAYERS"] 


#----------------------------------------------------------------------
def Maya_Enable_Legacy_Viewport(val):
	"""Turns on of off the use of MAYA_ENABLE_LEGACY_VIEWPORT"""
	if val == True and not "MAYA_ENABLE_LEGACY_VIEWPORT" in os.environ:
		os.environ["MAYA_ENABLE_LEGACY_VIEWPORT"] = "1"
	elif "MAYA_ENABLE_LEGACY_VIEWPORT" in os.environ:
		del os.environ["MAYA_ENABLE_LEGACY_VIEWPORT"]

#----------------------------------------------------------------------
def Enable_User_Tools(val):
	"""Turns on of off the use of Studio User Tools """
	if val == True :
		os.environ["NO_USER_TOOLS"] = "0"
	else:
		os.environ["NO_USER_TOOLS"] = "1"

#----------------------------------------------------------------------
def Set_Maya_Python_Version(version):
	"""Sets The Version Of Python That Maya Users This Is only Used In Maya 2022"""
	os.environ["MAYA_PYTHON_VERSION"] = str(version)

#----------------------------------------------------------------------
def Remove_Studio_Code_From_Python_Path():
	""""""
	if "PYTHONPATH" in os.environ:
		new_python_path = []
	for old_path_item in os.environ["PYTHONPATH"].split(";"):
		if not _code_base_name in old_path_item and not "Git_Live_Code" in old_path_item:
			new_python_path.append(old_path_item)
	os.environ["PYTHONPATH"] = ";".join(new_python_path)

#----------------------------------------------------------------------
def Remove_Studio_Code_From_Maya_Script_Path():
	""""""
	if "MAYA_SCRIPT_PATH" in os.environ:
		new_python_path = []
		for old_path_item in os.environ["MAYA_SCRIPT_PATH"].split(";"):
			if not _code_base_name in old_path_item and not "Git_Live_Code" in old_path_item:
				new_python_path.append(old_path_item)
		os.environ["MAYA_SCRIPT_PATH"] = ";".join(new_python_path)

#----------------------------------------------------------------------
def Remove_Studio_Code_From_System_Path():
	""""""
	new_python_path = []
	for old_path_item in os.environ["PATH"].split(";"):
		if not _code_base_name in old_path_item and not "Git_Live_Code" in old_path_item:
			new_python_path.append(old_path_item)
	os.environ["PATH"] = ";".join(new_python_path)

#----------------------------------------------------------------------
def Setup_Maya_For_Clean():
	""""""
	Remove_Studio_Code_From_Python_Path()
	Remove_Studio_Code_From_Maya_Script_Path()
	Remove_Studio_Code_From_System_Path()
	
#----------------------------------------------------------------------
def Setup_Maya_For_Studio(python_version):
	""""""
	Remove_Studio_Code_From_Python_Path()
	Remove_Studio_Code_From_Maya_Script_Path()
	Remove_Studio_Code_From_System_Path()
	
	if python_version == "2":
		python_version = "Python2"
	elif python_version == "3":
		python_version = "Python3"
		
	_studio_maya_path           = os.path.join(_code_base_path,python_version,"Software","Maya")
	_studio_global_systems_path = os.path.join(_code_base_path,python_version,"Global_Systems")
	
	paths_to_add = ";".join( [ _studio_maya_path, _studio_global_systems_path ] )
	
	if "PYTHONPATH" in os.environ:
		os.environ["PYTHONPATH"] = os.environ["PYTHONPATH"] + ";" + _studio_maya_path + ";" + _studio_global_systems_path
	else:
		os.environ["PYTHONPATH"] = _studio_maya_path + ";" + _studio_global_systems_path

#----------------------------------------------------------------------
def Build_Launch_Command(version):
	""""""
	return r'"c:\Program Files\Autodesk\Maya{}\bin\maya.exe"'.format(version)

########################################################################
class Software_Launcher_UI(QtWidgets.QWidget):
	""""""
	#----------------------------------------------------------------------
	def __init__(self,parent=None):
		"""Constructor"""
		super(Software_Launcher_UI,self).__init__(parent)
		if False:
			self.legacyRenderLayersCheckBox = QtWidgets.QCheckBox()
			self.legacyViewportCheckBox = QtWidgets.QCheckBox()
			self.userToolsCheckBox = QtWidgets.QCheckBox()

			self.versionComboBox = QtWidgets.QComboBox()
			self.modeComboBox    = QtWidgets.QComboBox()
			self.pythonComboBox  = QtWidgets.QComboBox()
			self.LaunchButton   = QtWidgets.QPushButton()
			self.LaunchButton.clicked
			self.versionComboBox.currentIndexChanged
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_versionComboBox_currentIndexChanged(self):
		""""""
		if self.versionComboBox.currentText() != "2022":
			self.pythonComboBox.setCurrentText("2")
			self.pythonComboBox.setDisabled(True)
		else:
			self.pythonComboBox.setCurrentText("3")
			self.pythonComboBox.setDisabled(False)
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_LaunchButton_clicked(self):
		""""""
		maya_version             = self.versionComboBox.currentText()
		maya_mode                = self.modeComboBox.currentText()
		python_version           = self.pythonComboBox.currentText()
		use_legacy_Render_Layers = self.legacyRenderLayersCheckBox.checkState() == QtCore.Qt.Checked
		use_legacy_Viewport      = self.legacyViewportCheckBox.checkState() == QtCore.Qt.Checked
		use_maya_user_tools      = self.userToolsCheckBox.checkState() == QtCore.Qt.Checked
		
		if maya_mode == Modes.Clean:
			Setup_Maya_For_Clean()
		elif maya_mode == Modes.Studio:
			Setup_Maya_For_Studio(python_version)
			Enable_User_Tools(use_maya_user_tools)
			
		if maya_version == "2022":
			Set_Maya_Python_Version(python_version)
			
		Maya_Enable_Legacy_Render_Layers(use_legacy_Render_Layers)
		Maya_Enable_Legacy_Viewport(use_legacy_Viewport)
		
		cmd = Build_Launch_Command(maya_version)
		subprocess.Popen(cmd)
		
_UI_Loader.registerCustomWidget(Software_Launcher_UI)

def make_ui():
	Qfile = QtCore.QFile(os.path.join(_ui_folder_path,"main.ui"))
	Qfile.open(QtCore.QFile.ReadOnly)
	ui_wig = _UI_Loader.load(Qfile)
	Qfile.close()
	return ui_wig

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	win = make_ui()
	QtCore.QMetaObject.connectSlotsByName(win)
	win.show()
	sys.exit(app.exec_())



subprocess.call(r'"c:\Program Files\Autodesk\Maya2018\bin\maya.exe"')