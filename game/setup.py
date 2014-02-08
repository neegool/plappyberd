# A very simple setup script to create 2 executables.
#
# hello.py is a simple "hello, world" type program, which alse allows
# to explore the environment in which the script runs.
#
# test_wx.py is a simple wxPython program, it will be converted into a
# console-less program.
#
# If you don't have wxPython installed, you should comment out the
#   windows = ["test_wx.py"]
# line below.
#
#
# Run the build process by entering 'setup.py py2exe' or
# 'python setup.py py2exe' in a console prompt.
#
# If everything works well, you should find a subdirectory named 'dist'
# containing some files, among them hello.exe and test_wx.exe.


from distutils.core import setup
import py2exe

sys.argv.append('py2exe')

setup(
     options = {"py2exe": {"compressed": True,
                            "zipfile" = None,
                          "optimize": 1,
                          "ascii": 1,
                          "bundle_files": 1}},
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "0.9",
    description = "A Flappy Bird clone",
    name = "Plappy Berd",

    # targets to build
    windows = ["plappyberd.py"],
    )
