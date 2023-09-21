from cx_Freeze import setup, Executable

build_exe_options = {"include_files" : ["utils.py","plus_symbol.png","beep.mp3"]}

setup(name = "AACT",
      version = "0.1",
      description = "",
      options = { "build_exe" : build_exe_options },
      executables = [Executable("aact.py")]) # Program name