from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('1aact.py', base=base, target_name = 'aact')
]

setup(name='Approach Avoidance Conflict Task',
      version = '1.0',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
