import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import sip
import windowcontrol
import os


if __name__ == "__main__":
    #https://github.com/NVlabs/instant-ngp/discussions/300#discussioncomment-5353810
    #pip install --no-binary opencv-python opencv-python
    #na wypadek problemów konfliktu pluginów w qt i opencv
    #ci_build_and_not_headless = False
    #try:
    #    from cv2.version import ci_build, headless
    #    ci_and_not_headless = ci_build and not headless
    #except:
    #    pass
    #if sys.platform.startswith("linux") and ci_and_not_headless:
    #    os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
    #if sys.platform.startswith("linux") and ci_and_not_headless:
    #    os.environ.pop("QT_QPA_FONTDIR")
    app = QApplication(sys.argv)
    form = windowcontrol.MainDialog(app)
    form.show()
    app.exec_()
