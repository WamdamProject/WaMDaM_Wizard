"""Subclass of dlg_License, which is generated by wxFormBuilder."""

import wx
import WaMDaMWizard

# Implementing dlg_License
class dlg_License( WaMDaMWizard.dlg_License ):
	def __init__( self, parent ):
		WaMDaMWizard.dlg_License.__init__( self, parent )
	
	# Handlers for dlg_License events.
	def sdbSizer_AboutOKOnOKButtonClick( self, event ):
		self.Destroy()
	
