import wx
import os
import sys
import threading
import ui
from speech.priorities import SpeechPriority

# Añadir el directorio actual al path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
from fuzzywuzzy import fuzz
sys.path.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))


class DialogSearch(wx.Dialog):
	open=False
	def __init__(self,frame, plugin):
		super(DialogSearch,self).__init__(None,title=_("Buscar"))
		self.plugin=plugin
		self.panel=wx.Panel(self)
		search_label=wx.StaticText(self.panel, wx.ID_ANY, label=_("&Busca algo"))
		self.line_search = wx.TextCtrl(self.panel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
		self.line_search.Bind(wx.EVT_TEXT_ENTER, self.on_search)
		self.okBTN=wx.Button(self.panel,label=_("&Aceptar"))
		self.okBTN.Bind(wx.EVT_BUTTON,self.on_search)
		self.cancelBTN=wx.Button(self.panel,label=_("&Cancelar"))
		self.cancelBTN.Bind(wx.EVT_BUTTON,self.on_cancel)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_window)

		sizeV=wx.BoxSizer(wx.VERTICAL)
		sizeH=wx.BoxSizer(wx.HORIZONTAL)
		sizeV.Add(search_label,0,wx.EXPAND)
		sizeV.Add(self.line_search,0,wx.EXPAND)
		sizeH.Add(self.okBTN,2,wx.EXPAND)
		sizeH.Add(self.cancelBTN,2,wx.EXPAND)
		sizeV.Add(sizeH,0,wx.EXPAND)
		self.panel.SetSizer(sizeV)
		self.CenterOnScreen()


	def Close(self):
		#Modifico el comportamiento de self.Close para actualizar booleano open
		super(DialogSearch,self).Close()
		DialogSearch.open=False


	def threadMessage(self):
		def message():
			ui.message(self.plugin.currentText[self.plugin.currentItem],SpeechPriority.NOW)
		thread=threading.Timer(0.1,message)
		thread.start()


	def on_search(self,event):
		search_value=self.line_search.GetValue().strip().lower()
		start_index=self.plugin.currentItem+1
		found=False
		for index in range(start_index,len(self.plugin.currentText)):
			search_result=self.plugin.currentText[index]
			# utilizamos el método partial_ratio para evaluar coincidencias entre las cadenas search_value y search_result
			similarity = fuzz.partial_ratio(search_value, search_result.lower())
			# Si el porcentaje de coincidencia es igual o mayor a 70%, se establece currentItem al balor del index
			if similarity >= 70:
				self.plugin.currentItem = index
				self.threadMessage()
				found=True
				self.Close()
				break

		if not found:
			wx.MessageBox(_('No hay coincidencias'),_('Error'),style=wx.OK | wx.ICON_ERROR)



	def on_cancel(self,event):
		if self.IsModal():
			self.EndModal(wx.ID_CANCEL)
		else:
			self.Close()



	def on_key_window(self,event):
		if event.GetKeyCode()==27:
			if self.IsModal():
				self.EndModal(wx.ID_CANCEL)
			else:
				self.Close()
		else:
			event.Skip()
