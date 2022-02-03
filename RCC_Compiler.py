import os

def compile_rcc_file(rcc_file, dest_foulder=None, dest_name=None):
    if not os.path.exists(rcc_file):
        raise IOError("File %r Does Not Exist" % str(rcc_file))

    if dest_foulder is None:
        dest_foulder = os.path.dirname(rcc_file)
    else:
        dest_foulder = dest_foulder

    if dest_name is None:
        dest_name = os.path.basename(rcc_file).replace(".qrc",".py")
    dest_path =  os.path.join(dest_foulder, dest_name)

    command = 'C:/Python39/Lib/site-packages/PySide2/rcc.exe -g python -o "%s" "%s"' % (dest_path, rcc_file)
    os.system(command)

if __name__ == "__main__":
    compile_rcc_file(r"c:\Users\drew.loveridge\Documents\SGS_Tools\Global_Systems\PYQT\RESOURCES\Maya_Innerface_Icons\Maya_Innerface_Icons.qrc", dest_foulder=r"c:\Users\drew.loveridge\Documents\SGS_Tools\Global_Systems\PYQT\RESOURCES",dest_name="Maya_Innerface_Icons_p3.py" )
