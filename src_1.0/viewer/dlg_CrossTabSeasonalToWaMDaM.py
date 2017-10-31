"""Subclass of dlg_CrossTabSeasonalToWaMDaM, which is generated by wxFormBuilder."""

import wx
import WaMDaMWizard
from Messages_forms.msg_somethigWrong import msg_somethigWrong
from controller.seasonalData_shaper import SeasonalDataShaperFunc

# Implementing dlg_CrossTabSeasonalToWaMDaM
class dlg_CrossTabSeasonalToWaMDaM( WaMDaMWizard.dlg_CrossTabSeasonalToWaMDaM ):
    def __init__( self, parent ):
        WaMDaMWizard.dlg_CrossTabSeasonalToWaMDaM.__init__( self, parent )
        self.cross_file = None

    # Handlers for dlg_CrossTabSeasonalToWaMDaM events.
    def FilePicker_CrossTabulatedraFileOnFileChanged( self, event ):
        # TODO: Implement FilePicker_CrossTabulatedraFileOnFileChanged
        self.cross_file = self.FilePicker_CrossTabSeasonalToWaMDaM.GetPath()
        valid_extension = ['xlsx','xlsm']
        if not (self.cross_file.split('.')[-1] in valid_extension):
            self.Destroy()
            message = msg_somethigWrong(None, msg="A non excel file was selected, \n\n"
                                                  " Please select a valid Excel File")
            message.Show()

    def btn_convertCrossTabulatedSeasonalOnButtonClick( self, event ):
        # TODO: Implement btn_convertCrossTabulatedSeasonalOnButtonClick
        if self.cross_file:
            try:
                SeasonalDataShaperFunc(workbook=self.cross_file)
                self.allDone()
                # self.Destroy()
            except Exception as e:
                message = msg_somethigWrong(None, msg=u'{}, \n\n[*] Could not complete CrossTabulated Task'.format(e))
                message.Show()
        else:
            from Messages_forms.msg_selectWorkbokFirst import msg_selectWorkbokFirst

            instance = msg_selectWorkbokFirst(None)
            result = instance.ShowModal()
            instance.Destroy()
            # instance.Show()

    def btn_cancelOnButtonClick( self, event ):
        self.Destroy()

    def allDone(self):
        from Messages_forms.generalMsgDlg import messageDlg

        instance = messageDlg(None)
        instance.SetTitle(u"Successfully loaded data")
        # instance.Show()
        instance.setMessage(u"\n\nYou successfully loaded '" + self.cross_file.split('\\')[-1] + u"'.")
        result = instance.ShowModal()
        instance.Destroy()
        self.Destroy()
