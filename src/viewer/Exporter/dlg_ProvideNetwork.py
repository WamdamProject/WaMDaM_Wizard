"""Subclass of dlg_ProvideNetwork, which is generated by wxFormBuilder."""

import wx
import ExportModels

# Implementing dlg_ProvideNetwork
class dlg_ProvideNetwork( ExportModels.dlg_ProvideNetwork ):
	def __init__( self, parent ):
		ExportModels.dlg_ProvideNetwork.__init__( self, parent )
	
	# Handlers for dlg_ProvideNetwork events.
	def FilePicker_ProvideNetworkOnFileChanged( self, event ):
		# TODO: Implement FilePicker_ProvideNetworkOnFileChanged
		pass
	
	def comboBox_SelectNetOnCombobox( self, event ):
		# TODO: Implement comboBox_SelectNetOnCombobox
		pass
	
	def comboBox_SelectScenOnCombobox( self, event ):
		# TODO: Implement comboBox_SelectScenOnCombobox
		pass
	
	def comboBox_timStpOnCombobox( self, event ):
		# TODO: Implement comboBox_timStpOnCombobox
		pass
	
	def StartDtOnText( self, event ):
		# TODO: Implement StartDtOnText
		pass
	
	def EndDtOnTextEnter( self, event ):
		# TODO: Implement EndDtOnTextEnter
		pass
	
	def btn_backOnButtonClick( self, event ):
		# import dlg_SelectModel as fSelectDlg
		# Serv1 = fSelectDlg.dlg_SelectModel(None)
		# Serv1.ShowModal()
		self.Destroy()
	
	def btn_nextOnButtonClick( self, event ):
		import dlg_SpecifyBoundary as fdlg_SpecifyBoundary
		Serv2 = fdlg_SpecifyBoundary.dlg_SpecifyBoundary(None)
		Serv2.ShowModal()

