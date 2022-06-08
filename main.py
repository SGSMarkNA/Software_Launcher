import subprocess
import os
import sys
from pathlib import Path
import Random_Facts_Selector

_this_dir = Path(os.path.dirname(__file__))
os.sys.path.append(str(_this_dir))

# Code Path Collection
_code_base_path = _this_dir.parent
_code_base_name = _code_base_path.name
_ui_folder_path = _this_dir.joinpath("UI")
_site_pak_path  = _code_base_path.joinpath("Python3","Global_Systems","AW_site_packages")



os.sys.path.append(str(_site_pak_path))

from PySide2 import QtCore, QtUiTools, QtWidgets
QtSlot         = QtCore.Slot
QtSignal       = QtCore.Signal
QtProperty     = QtCore.Property

import icons

_UI_Loader = QtUiTools.QUiLoader()
os.sys.path.remove(str(_site_pak_path))

########################################################################
class Modes:
	""""""
	Studio = "Studio"
	Clean  = "Clean"


# made and edit wooho



#----------------------------------------------------------------------
def get_Maya_Versions():
	""""""
	res = []
	p = Path("C:/Program Files/Autodesk")
	for item in p.glob("Maya*/bin/maya.exe"):
		res.append(item.parent.parent.name.replace("Maya",""))
	return res
#----------------------------------------------------------------------
def Maya_Enable_Legacy_Render_Layers(val):
	"""Turns on of off the use of MAYA_ENABLE_LEGACY_RENDER_LAYERS"""
	if val == True:
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
	if "PATH" in os.environ["PATH"]:
		current_sys_paths = os.environ["PATH"].split(";")
		new_sys_path = []
		
		for old_path_item in current_sys_paths:
			
			if not _code_base_name in old_path_item and not "Git_Live_Code" in old_path_item:
				new_sys_path.append(old_path_item)
				
		os.environ["PATH"] = ";".join(new_sys_path)

#----------------------------------------------------------------------
def Setup_Maya_For_Clean():
	""""""
	Remove_Studio_Code_From_Python_Path()
	Remove_Studio_Code_From_Maya_Script_Path()
	Remove_Studio_Code_From_System_Path()
	

#----------------------------------------------------------------------
def Add_Maya_Module_Path(path):
	""""""
	path = str(path)
	if not "MAYA_MODULE_PATH" in os.environ:
		os.environ["MAYA_MODULE_PATH"] = path
	else:
		current_paths = os.environ["MAYA_MODULE_PATH"].split(";")
		if not path in current_paths:
			current_paths.append(path)
		os.environ["MAYA_MODULE_PATH"] = ";".join( current_paths )
#----------------------------------------------------------------------
def Remove_Maya_Module_Path(path):
	""""""
	path = str(path)
	if "MAYA_MODULE_PATH" in os.environ:
		current_paths = os.environ["MAYA_MODULE_PATH"].split(";")
		if path in current_paths:
			current_paths.remove(path)
		os.environ["MAYA_MODULE_PATH"] = ";".join(current_paths)

#----------------------------------------------------------------------
def Add_Path_To_Python_Path(path):
	""""""
	path = str(path)
	if not "PYTHONPATH" in os.environ:
		os.environ["PYTHONPATH"] = path
	else:
		current_paths = os.environ["PYTHONPATH"].split(";")
		
		if not path in current_paths:
			current_paths.append(path)
			
		os.environ["PYTHONPATH"] = ";".join( current_paths )
#----------------------------------------------------------------------
def Remove_Path_From_Python_Path(path):
	""""""
	path = str(path)
	if "PYTHONPATH" in os.environ:
		current_paths = os.environ["PYTHONPATH"].split(";")
		if path in current_paths:
			current_paths.remove(path)
		os.environ["PYTHONPATH"] = ";".join(current_paths)
		
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
	
	#paths_to_add = ";".join( [ _studio_maya_path, _studio_global_systems_path ] )
	
	if "PYTHONPATH" in os.environ:
		os.environ["PYTHONPATH"] = os.environ["PYTHONPATH"] + ";" + _studio_maya_path + ";" + _studio_global_systems_path
	else:
		os.environ["PYTHONPATH"] = _studio_maya_path + ";" + _studio_global_systems_path

#----------------------------------------------------------------------
def Build_Launch_Command(version):
	""""""
	return r'"C:\Program Files\Autodesk\Maya{}\bin\maya.exe"'.format(version)

########################################################################
class Software_Launcher_UI(QtWidgets.QWidget):
	""""""
	#----------------------------------------------------------------------
	def __init__(self,parent=None):
		"""Constructor"""
		super(Software_Launcher_UI,self).__init__(parent)
		self._Random_facts_selector = Random_Facts_Selector.Random_Facts_Selector()
		self.new_random_fact_timer = QtCore.QTimer()
		self.new_random_fact_timer.setInterval(40000)
		self.new_random_fact_timer.timeout.connect(self.update_Random_Fact)
		if False:
			self.legacyRenderLayersCheckBox = QtWidgets.QCheckBox()
			self.legacyViewportCheckBox = QtWidgets.QCheckBox()
			self.userToolsCheckBox = QtWidgets.QCheckBox()
			
			self.Random_Facts_Text = QtWidgets.QTextBrowser()
			self.versionComboBox = QtWidgets.QComboBox()
			self.modeComboBox    = QtWidgets.QComboBox()
			self.pythonComboBox  = QtWidgets.QComboBox()
			self.LaunchButton   = QtWidgets.QPushButton()
			self.AutomotiveButton = QtWidgets.QComboBox()
			self.CleanButton = QtWidgets.QComboBox()
			self.LegoButton = QtWidgets.QComboBox()
	
	#----------------------------------------------------------------------
	def _init(self):
		""""""
		self._orig_html = self.Random_Facts_Text.toHtml()
		self.versionComboBox.clear()
		maya_versions = get_Maya_Versions()
		maya_versions.reverse()
		self.versionComboBox.addItems(maya_versions)
		self.update_Random_Fact()
		self.new_random_fact_timer.start()
	#----------------------------------------------------------------------
	@QtCore.Slot(str)
	def on_versionComboBox_currentIndexChanged(self,val):
		""""""
		val
		if int(self.versionComboBox.currentText()) < 2022:
			self.pythonComboBox.setDisabled(True)
		else:
			self.pythonComboBox.setDisabled(False)
	#----------------------------------------------------------------------
	@QtCore.Slot(str)
	def on_modeComboBox_currentIndexChanged(self,val):
		""""""
		val
		if self.modeComboBox.currentText() == Modes.Clean:
			self.userToolsCheckBox.setDisabled(True)
		else:
			self.userToolsCheckBox.setDisabled(False)
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
		
	#----------------------------------------------------------------------
	def update_Random_Fact(self):
		""""""
		new_fact = self._Random_facts_selector.get_Random_Fact()
		new_html = self._orig_html.replace("REPLACE_CATEGORY",new_fact.category).replace("REPLACE_SUBJECT",new_fact.subject).replace("REPLACE_FACT",new_fact.fact)
		self.Random_Facts_Text.setHtml(new_html)
		
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_AutomotiveButton_clicked(self):
		""""""
		Setup_Maya_For_Studio("2")
		Maya_Enable_Legacy_Render_Layers(True)
		Maya_Enable_Legacy_Viewport(True)
		Enable_User_Tools(True)
		cmd = Build_Launch_Command("2020")
		subprocess.Popen(cmd)
		
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_CleanButton_clicked(self):
		""""""
		Setup_Maya_For_Clean()
		Set_Maya_Python_Version("2")
		Maya_Enable_Legacy_Render_Layers(False)
		Maya_Enable_Legacy_Viewport(True)
		Enable_User_Tools(False)
		cmd = Build_Launch_Command("2020")
		subprocess.Popen(cmd)
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_LegoButton_clicked(self):
		""""""
		Setup_Maya_For_Clean()
		Set_Maya_Python_Version("3")
		Maya_Enable_Legacy_Render_Layers(False)
		Maya_Enable_Legacy_Viewport(True)
		Enable_User_Tools(False)
		Add_Maya_Module_Path( _code_base_path.joinpath("_3rd_Party","LLRToolset","Tools_2022") )
		cmd = Build_Launch_Command("2022")
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
	win._init()
	QtCore.QMetaObject.connectSlotsByName(win)
	#win.setWindowFlags(QtCore.Qt.WindowTitleHint)
	win.show()
	sys.exit(app.exec_())