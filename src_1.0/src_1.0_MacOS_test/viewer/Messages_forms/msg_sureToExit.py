
import wx
import Validations


class msg_sureToExit(Validations.msg_sureToExit):
    def __init__(self, parent):
        Validations.msg_sureToExit.__init__(self, parent)
        self.parent = None

    def btn_okOnButtonClick(self, event):
        self.Destroy()
        if self.parent:
            self.parent.Destroy()

    def btn_cancelOnButtonClick(self, event):
        self.Destroy()

    def set_parent(self, obj):
        self.parent = obj