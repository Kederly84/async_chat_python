from cx_Freeze import setup, Executable

build_exe_options = {
      'packages': ['common', 'logs', 'server']
}
setup(name='message_server',
      version='1.0',
      description='message_server',
      options={
            'build_exe': build_exe_options
      },
      executables=[Executable('server.py',
                              targetName='server.exe',
                              )]
      )