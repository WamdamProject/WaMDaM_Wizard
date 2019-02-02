"""Subclass of dlg_Publish, which is generated by wxFormBuilder."""

import wx
import Publish_Viz
from controller.ConnectDB_ParseExcel import DB_Setup
from viewer.Messages_forms.msg_somethigWrong import msg_somethigWrong
# from hs_restclient import HydroShare, HydroShareAuthBasic
from hs_restclient import HydroShare, HydroShareAuthBasic
from controller.HydroShare.PublishWaMDaM import publishOnHydraShare

class dlg_Publish( Publish_Viz.dlg_Publish ):
	def __init__( self, parent ):
		Publish_Viz.dlg_Publish.__init__( self, parent )

		# self.m_textCtrl7.Value
		# self.m_textCtrl8.Value

	# Handlers for dlg_Publish events.
	def btn_loginOnButtonClick( self, event ):
		# TODO: Implement btn_loginOnButtonClick
		userName = self.m_textCtrl7.Value
		password = self.m_textCtrl8.Value

		auth = HydroShareAuthBasic(username=userName, password=password)
		# hs = HydroShare(auth=auth)
		# hs = HydroShare(auth=auth, hostname='beta.hydroshare.org')
		# hs is the login resposne
		hs = HydroShare(auth=auth, hostname='hydroshare.org')
		try:
			for resource in hs.resources():
				print("success")
                # self.Btn_Login.Enabled = False
				break
			pass
		except:
			from viewer.Messages_forms.msg_somethigWrong import msg_somethigWrong

			msg = "\n\nThe provided username and password do not match yours in OpenAgua"
			msg_somethigWrong(None, msg=msg).Show()


	# Handlers for dlg_Publish events.
	def btn_PublishOnButtonClick( self, event ):
		self.btn_Publish.Enabled = False
		# TODO: Implement btn_PublishOnButtonClick
		if not self.checkConnectingToSqlite():
			msg = "\n\nWarning: Please connect to sqlite first."
			msg_somethigWrong(self, msg).Show()
		else:
			err_msg = self.checkValidatingOfUserInformation()
			if err_msg != '':
				msg_somethigWrong(self, err_msg).Show()
				self.btn_Publish.Enabled = True
			else:
				userName = self.m_textCtrl7.Value
				password = self.m_textCtrl8.Value
				title = self.m_textCtrl9.Value
				abstract = self.m_textCtrl10.Value


				author = self.m_textCtrl81.Value
				db_setup = DB_Setup()
				fullPathOfSqlite = db_setup.get_dbpath()

				# connect to te server and create a resource
				resource_id= publishOnHydraShare(userName, password, fullPathOfSqlite, title, abstract, author)


				if resource_id:
					from viewer.Messages_forms.msg_connSQLiteSuccs import msg_connSQLiteSuccs
					msgdlg = msg_connSQLiteSuccs(self)
					msgdlg.setMessage("\n\nSuccessfully, uploaded Sqlite file.")
					msgdlg.ShowModal()

					# options = {"file_path": 'WEAP_WASH.sqlite', "hs_file_type": "SingleFile"}
					# result = hs.resource(return_value).functions.set_file_type(options)

					self.Destroy()
				else:
					msg_somethigWrong(self,
									  msg='\n\nError: Sorry, failed uploading the sqlite file.').Show()
				self.btn_Publish.Enabled = True
		pass
	
	def btn_cancelOnButtonClick( self, event ):
		# TODO: Implement btn_cancelOnButtonClick
		self.Destroy()

	# this function is to check if user name or password id empty
	def checkValidatingOfUserInformation(self):
		userName = self.m_textCtrl7.Value
		msg = ''
		if not userName or userName == '' :
			msg = '\n\nError: User name can not be empty.\n Please input user name.'
			return msg

		password = self.m_textCtrl8.Value
		if not password or password == '':
			msg = '\n\nError: Password can not be empty.\n Please input password.'
			return msg

		title = self.m_textCtrl9.Value
		if not title or title == '' :
			msg = '\n\nError: Title can not be empty.\n Please input title.'
			return msg

		abstract = self.m_textCtrl10.Value
		if not abstract or abstract == '':
			msg = '\n\nError: Abstract can not be empty.\n Please input abstract.'
			return msg

		author = self.m_textCtrl81.Value
		if not author or author == '' :
			msg = '\n\nError: Authors can not be empty.\n Please provide an author name.'
			return msg
		return msg
	#this function is to check if connecting to sqlite.
	def checkConnectingToSqlite(self):
		db_setup = DB_Setup()
		if not db_setup.get_session():
			return False
		return True

	
	
