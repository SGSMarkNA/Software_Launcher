import subprocess
import os
import sys
from pathlib import Path
import Random_Facts_Selector

_this_dir = Path(os.path.dirname(__file__))
os.sys.path.append(str(_this_dir))

# Code Path Collection
_code_base_path     = _this_dir.parent
isinstance(_code_base_path,Path)

_code_base_name     = _code_base_path.name
_ui_folder_path     = _this_dir.joinpath("UI")
_site_pak_path      = _code_base_path.joinpath("Python3","Global_Systems","AW_site_packages")
_3rd_Party_path     = _code_base_path.joinpath("_3rd_Party")
_winghome_path      = r'v:\SGS_Tools\_3rd_Party\wing-debugger'

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


#def Enable_Remote_DeBugging():
	#os.sys.path.append(_winghome_path)
	#os.environ["WINGHOME"] = _winghome_path

#----------------------------------------------------------------------
def get_Maya_Versions():
	""""""
	res = []
	p = Path("C:/Program Files/Autodesk")
	for item in p.glob("Maya*/bin/maya.exe"):
		res.append(item.parent.parent.name.replace("Maya",""))
	return res

#----------------------------------------------------------------------
def find_Nuke_Versions(version):
	""""""
	p = Path("C:/Program Files")
	items = list(p.glob("Nuke{}*/Nuke*.exe".format(version)))
	if len(items):
		return items[0]
	else:
		return None

#----------------------------------------------------------------------
def Build_Maya_Launch_Command(version):
	""""""
	return r'"C:\Program Files\Autodesk\Maya{}\bin\maya.exe"'.format(version)


########################################################################
class Environment(dict):
	""""""
	##----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		super(Environment,self).__init__(os.environ.copy())
		self.Clear_Legacy_Enviorment()
	#----------------------------------------------------------------------
	def Clear_Legacy_Enviorment(self):
		""""""
		#----------------------------------------------------------------------
		def Remove_Studio_Code_From_Python_Path():
			""""""
			if "PYTHONPATH" in self:
				new_python_path = []
				
				for old_path_item in self["PYTHONPATH"].split(";"):
					if not _code_base_name in old_path_item and not "Git_Live_Code" in old_path_item:
						new_python_path.append(old_path_item)
						
				self["PYTHONPATH"] = ";".join(new_python_path)
				
		#----------------------------------------------------------------------
		def Remove_Studio_Code_From_Maya_Script_Path():
			""""""
			if "MAYA_SCRIPT_PATH" in self:
				new_python_path = []
				for old_path_item in self["MAYA_SCRIPT_PATH"].split(";"):
					if not _code_base_name in old_path_item and not "Git_Live_Code" in old_path_item:
						new_python_path.append(old_path_item)
				self["MAYA_SCRIPT_PATH"] = ";".join(new_python_path)
				
		#----------------------------------------------------------------------
		def Remove_Studio_Code_Nuke_Path_Path():
			""""""
			if "NUKE_PATH" in self:
				self["NUKE_PATH"] = ""
		
		#----------------------------------------------------------------------
		def Remove_Studio_Code_From_System_Path():
			""""""
			if "PATH" in self["PATH"]:
				current_sys_paths = self["PATH"].split(";")
				new_sys_path = []
				
				for old_path_item in current_sys_paths:
					
					if not _code_base_name in old_path_item and not "Git_Live_Code" in old_path_item:
						new_sys_path.append(old_path_item)
						
				self["PATH"] = ";".join(new_sys_path)
		Remove_Studio_Code_From_Python_Path()
		Remove_Studio_Code_From_Maya_Script_Path()
		Remove_Studio_Code_From_System_Path()
		Remove_Studio_Code_Nuke_Path_Path()	
	#----------------------------------------------------------------------
	def Set_Code_Location(self,python_version):
		""""""
		if python_version == "2":
			python_version = "Python2"
		elif python_version == "3":
			python_version = "Python3"
			
		maya_path           = os.path.join(_code_base_path,python_version,"Software","Maya")
		maya_mel_path       = os.path.join(_code_base_path,python_version,"Software","Maya","Mel")
		nuke_path           = os.path.join(_code_base_path,python_version,"Software","Nuke")
		global_systems_path = os.path.join(_code_base_path,python_version,"Global_Systems")
		self.Add_Path_To_Python_Path(maya_path)
		self.Add_Path_To_Python_Path(global_systems_path)
		self.Add_Path_To_Maya_Scripts_Path(maya_mel_path)
		self["NUKE_PATH"] = nuke_path
	#----------------------------------------------------------------------
	def Add_Path_To_Python_Path(self,path):
		""""""
		path = str(path)
		if not "PYTHONPATH" in self:
			self["PYTHONPATH"] = path
		else:
			current_paths = self["PYTHONPATH"].split(";")
			
			if not path in current_paths:
				current_paths.append(path)
				
			self["PYTHONPATH"] = ";".join( current_paths )
	#----------------------------------------------------------------------
	def Remove_Path_From_Python_Path(self,path):
		""""""
		path = str(path)
		if "PYTHONPATH" in self:
			current_paths = self["PYTHONPATH"].split(";")
			if path in current_paths:
				current_paths.remove(path)
			self["PYTHONPATH"] = ";".join(current_paths)
	#----------------------------------------------------------------------
	def Add_Maya_Module_Path(self,path):
		""""""
		path = str(path)
		if not "MAYA_MODULE_PATH" in self:
			self["MAYA_MODULE_PATH"] = path
		else:
			current_paths = self["MAYA_MODULE_PATH"].split(";")
			if not path in current_paths:
				current_paths.append(path)
			self["MAYA_MODULE_PATH"] = ";".join( current_paths )
	#----------------------------------------------------------------------
	def Add_Path_To_Maya_Scripts_Path(self,path):
		""""""
		path = str(path)
		if not "MAYA_SCRIPT_PATH" in self:
			self["MAYA_SCRIPT_PATH"] = path
		else:
			current_paths = self["MAYA_SCRIPT_PATH"].split(";")
			
			if not path in current_paths:
				current_paths.append(path)
				
			self["MAYA_SCRIPT_PATH"] = ";".join( current_paths )
	#----------------------------------------------------------------------
	def Add_Path_To_Maya_XBMLANGPATH(self,path):
		""""""
		path = str(path)
		if not "XBMLANGPATH" in self:
			self["XBMLANGPATH"] = path
		else:
			current_paths = self["XBMLANGPATH"].split(";")
			
			if not path in current_paths:
				current_paths.append(path)
				
			self["XBMLANGPATH"] = ";".join( current_paths )
	#----------------------------------------------------------------------
	def Maya_Enable_Legacy_Render_Layers(self,val):
		"""Turns on of off the use of MAYA_ENABLE_LEGACY_RENDER_LAYERS"""
		if val == True:
			self["MAYA_ENABLE_LEGACY_RENDER_LAYERS"] = "1"
		elif "MAYA_ENABLE_LEGACY_RENDER_LAYERS" in self:
			del self["MAYA_ENABLE_LEGACY_RENDER_LAYERS"] 
	
	
	#----------------------------------------------------------------------
	def Maya_Enable_Legacy_Viewport(self,val):
		"""Turns on of off the use of MAYA_ENABLE_LEGACY_VIEWPORT"""
		if val == True:
			self["MAYA_ENABLE_LEGACY_VIEWPORT"] = "1"
		elif "MAYA_ENABLE_LEGACY_VIEWPORT" in self:
			del self["MAYA_ENABLE_LEGACY_VIEWPORT"]
	#----------------------------------------------------------------------
	def Set_ICIO_Profile_Path(self,path):
		"""Sets the ICIO Env Var"""
		path = str(path)
		self["OCIO"] = path
	#----------------------------------------------------------------------
	def Set_Maya_Color_Management_Policy_File(self,path):
		"""Sets the ICIO Env Var"""
		path = str(path)
		self["MAYA_COLOR_MANAGEMENT_POLICY_FILE"] = path
	#----------------------------------------------------------------------
	def Enable_User_Tools(self,val):
		"""Turns on of off the use of Studio User Tools """
		if val == True :
			self["NO_USER_TOOLS"] = "0"
		else:
			self["NO_USER_TOOLS"] = "1"
	
	#----------------------------------------------------------------------
	def Set_Maya_Python_Version(self,version):
		"""Sets The Version Of Python That Maya Users This Is only Used In Maya 2022"""
		self["MAYA_PYTHON_VERSION"] = str(version)
		
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
			self.Use_Nuke_X_checkBox = QtWidgets.QCheckBox() 
			self.Enable_Remote_Debugging_checkBox = QtWidgets.QCheckBox().to
			self.versionComboBox   = QtWidgets.QComboBox()
			self.modeComboBox      = QtWidgets.QComboBox()
			self.pythonComboBox    = QtWidgets.QComboBox()
			
			self.Maya_2022_aces_Button  = QtWidgets.QComboBox()
			self.Maya_2020_aces_Button  = QtWidgets.QComboBox()
			
			#self.Amsterdam_2018_SRGB_Button   = QtWidgets.QPushButton()
			self.Maya_2022_SRGB_Button         = QtWidgets.QPushButton()
			self.Maya_2020_SRGB_Button         = QtWidgets.QPushButton()
			
			self.Nuke_12_Button    = QtWidgets.QPushButton()
			self.Nuke_13_Button    = QtWidgets.QPushButton()
			self.CleanButton       = QtWidgets.QPushButton()
			self.MayaUSDButton     = QtWidgets.QPushButton()
			self.MayaLaunchButton  = QtWidgets.QPushButton()
	
	#----------------------------------------------------------------------
	def _init(self):
		""""""
		self._nuke_12_exe = find_Nuke_Versions(12)
		self._nuke_13_exe = find_Nuke_Versions(13)
		self._wing_remote_debugging_enabled = False
		self.versionComboBox.clear()
		maya_versions = get_Maya_Versions()
		maya_versions.reverse()
		self.versionComboBox.addItems(maya_versions)
		self._disable_Buttons_Based_On_Found_Content()
	#----------------------------------------------------------------------
	def _disable_Buttons_Based_On_Found_Content(self):
		""""""
		if self._nuke_12_exe == None:
			self.Nuke_12_Button.setEnabled(False)
		if self._nuke_13_exe == None:
			self.Nuke_13_Button.setEnabled(False)
		if not '2023' in get_Maya_Versions():
			self.MayaUSDButton.setEnabled(False)
	#----------------------------------------------------------------------
	@QtCore.Slot(str)
	def on_versionComboBox_currentIndexChanged(self,val):
		""""""
		if int(self.versionComboBox.currentText()) < 2022:
			self.pythonComboBox.setDisabled(True)
		else:
			self.pythonComboBox.setDisabled(False)
	#----------------------------------------------------------------------
	@QtCore.Slot(bool)
	def on_Enable_Remote_Debugging_checkBox_toggled(self,val):
		""""""
		if self._wing_remote_debugging_enabled and not val:
			os.sys.path.remove(str(_winghome_path))
			if "WINGHOME" in os.environ:
				del os.environ["WINGHOME"]
		else:
			os.sys.path.append(str(_winghome_path))
			os.environ["WINGHOME"] = str(_winghome_path)
			
		self._wing_remote_debugging_enabled = val
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
	def on_MayaLaunchButton_clicked(self):
		""""""
		maya_version             = self.versionComboBox.currentText()
		maya_mode                = self.modeComboBox.currentText()
		python_version           = self.pythonComboBox.currentText()
		use_legacy_Render_Layers = self.legacyRenderLayersCheckBox.checkState() == QtCore.Qt.Checked
		use_legacy_Viewport      = self.legacyViewportCheckBox.checkState() == QtCore.Qt.Checked
		use_maya_user_tools      = self.userToolsCheckBox.checkState() == QtCore.Qt.Checked and self.userToolsCheckBox.isEnabled()
		env = Environment()
		#Clear_Legacy_Enviorment()
		
		
		if int(maya_version) <= 2020:
			python_version = "2"
		
		env.Set_Maya_Python_Version(python_version)
		env.Set_Code_Location(python_version)
			
		env.Enable_User_Tools(use_maya_user_tools)
			
		env.Maya_Enable_Legacy_Render_Layers(use_legacy_Render_Layers)
		env.Maya_Enable_Legacy_Viewport(use_legacy_Viewport)
		
		cmd = Build_Maya_Launch_Command(maya_version)
		subprocess.Popen(cmd, env=env)
		
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_Maya_2020_aces_Button_clicked(self):
		""""""
		env = Environment()
		python_version = "2"
		maya_version   = "2020"
		env.Set_Maya_Python_Version(python_version)
		env.Set_Maya_Color_Management_Policy_File("W:/OCIO_Configs/aces_1.2_marks/Maya_2020_Marks_00.xml")
		env.Set_Code_Location(python_version)
		
		env.Add_Path_To_Python_Path(_3rd_Party_path)
		env.Maya_Enable_Legacy_Render_Layers(True)
		env.Maya_Enable_Legacy_Viewport(True)
		env.Enable_User_Tools(True)
		cmd = Build_Maya_Launch_Command(maya_version)
		#subprocess.Popen(args=...,executable=...,cwd=..., env=env)
		subprocess.Popen(cmd, env=env)
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_Maya_2022_aces_Button_clicked(self):
		""""""
		env = Environment()
		python_version = "3"
		maya_version   = "2022"
		env.Set_Maya_Python_Version(python_version)
		env.Set_Maya_Color_Management_Policy_File("W:/OCIO_Configs/aces_1.2_marks/Maya_2020_Marks_00.xml")
		
		env.Set_Code_Location(python_version)
		env.Add_Path_To_Python_Path(_3rd_Party_path)
		env.Maya_Enable_Legacy_Render_Layers(True)
		env.Maya_Enable_Legacy_Viewport(True)
		env.Enable_User_Tools(True)
		cmd = Build_Maya_Launch_Command(maya_version)
		subprocess.Popen(cmd, env=env)
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_Maya_2022_SRGB_Button_clicked(self):
		""""""
		env = Environment()
		python_version = "3"
		maya_version   = "2022"
		env.Set_Maya_Python_Version(python_version)
		env.Set_Maya_Color_Management_Policy_File("W:/OCIO_Configs/Maya_2020_Marks_sRGB_v00.xml")
		
		env.Set_Code_Location(python_version)
		env.Add_Path_To_Python_Path(_3rd_Party_path)
		env.Maya_Enable_Legacy_Render_Layers(True)
		env.Maya_Enable_Legacy_Viewport(True)
		env.Enable_User_Tools(True)
		cmd = Build_Maya_Launch_Command(maya_version)
		subprocess.Popen(cmd, env=env)
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_Maya_2020_SRGB_Button_clicked(self):
		""""""
		env = Environment()
		python_version = "2"
		maya_version   = "2020"
		env.Set_Maya_Python_Version(python_version)
		env.Set_Maya_Color_Management_Policy_File("W:/OCIO_Configs/Maya_2020_Marks_sRGB_v00.xml")
		env.Set_Code_Location(python_version)
		env.Add_Path_To_Python_Path(_3rd_Party_path)
		env.Maya_Enable_Legacy_Render_Layers(True)
		env.Maya_Enable_Legacy_Viewport(True)
		env.Enable_User_Tools(True)
		cmd = Build_Maya_Launch_Command(maya_version)
		#subprocess.Popen(args=...,executable=...,cwd=..., env=env)
		subprocess.Popen(cmd, env=env)
	#----------------------------------------------------------------------
	#@QtCore.Slot()
	#def on_Amsterdam_2018_SRGB_Button_clicked(self):
		#""""""
		#python_version = "2"
		#maya_version   = "2018"
		#env = Environment()
		##Clear_Legacy_Enviorment()
		#env.Set_Maya_Python_Version(python_version)
		#env.Set_Maya_Color_Management_Policy_File("W:/OCIO_Configs/Maya2023_scene-linear-sRGB_v00.xml")
		
		#env.Set_Code_Location(python_version)
		#env.Maya_Enable_Legacy_Render_Layers(True)
		#env.Maya_Enable_Legacy_Viewport(True)
		#env.Enable_User_Tools(True)
		
		#cmd = Build_Maya_Launch_Command(maya_version)
		#subprocess.Popen(cmd, env=env)
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_MayaUSDButton_clicked(self):
		""""""
		python_version = "2"
		maya_version   = "2023"	
		env = Environment()
		env.Set_Maya_Python_Version(python_version)
		env.Set_Maya_Color_Management_Policy_File("")
		env.Maya_Enable_Legacy_Render_Layers(False)
		env.Maya_Enable_Legacy_Viewport(False)
		env.Enable_User_Tools(False)
		env.Add_Path_To_Python_Path(_code_base_path.joinpath("DML_USD","Maya"))
		cmd = Build_Maya_Launch_Command(maya_version)
		subprocess.Popen(cmd, env=env)
	#----------------------------------------------------------------------
	@QtCore.Slot()
	def on_Nuke_12_Button_clicked(self):
		""""""
		python_version = "2"
		env = Environment()
		#Clear_Legacy_Enviorment()
		env.Set_Code_Location(python_version)
		
		cmd = self._nuke_12_exe
		if self.Use_Nuke_X_checkBox.isChecked():
			cmd = str(cmd) + " --nukex"
		subprocess.Popen(cmd, env=env)
		
	@QtCore.Slot()
	def on_Nuke_13_Button_clicked(self):
		""""""
		python_version = "3"
		env = Environment()
		#Clear_Legacy_Enviorment()
		env.Set_Code_Location(python_version)
		
		cmd = self._nuke_13_exe
		if self.Use_Nuke_X_checkBox.isChecked():
			cmd = str(cmd) + " --nukex"
		subprocess.Popen(cmd, env=env)
		
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