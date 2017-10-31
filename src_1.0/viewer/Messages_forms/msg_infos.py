#[[[Explain more (one or two sentences) of what it does]]]
import Validations
import wx

# Implementing msg_duplicateEnties
class msg_infos( Validations.msg_infos ):
	def __init__( self, parent, msg):
		Validations.msg_infos.__init__( self, parent, msg)
		self.MakeModal(True)
		self.parent = parent

	# Handlers for msg_duplicateEnties events.
	def btn_okOnButtonClick( self, event ):
		self.MakeModal(False)
		if self.parent:
			self.parent.Show()
		self.Close()

	def set_parent(self, obj):
		self.parent = obj