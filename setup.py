from distutils.core import setup
import py2exe

data_config = [(".", ["exList.txt", "oui.txt", "data.xml"]),
              ("icons", ["winSetup.ico", "main.ico"]),
    ]

console_config = [{"script":"winSetup.py", "icon_resources":[(1, "winSetup.ico")]},
                  {"script":"main.py", "icon_resources":[(1, "main.ico")]},
                  ]

setup(console = console_config,
      data_files = data_config,
      )
