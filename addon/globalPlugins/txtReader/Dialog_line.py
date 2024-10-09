import wx
import threading
import ui

class DialogLine(wx.Dialog):
	def __init__(self,frame, plugin):
		super(DialogLine,self).__init__(None,title="Ir a")
		self.plugin=plugin
		self.line=self.plugin.currentItem+1
		self.panel=wx.Panel(self)
		line_label=wx.StaticText(self.panel, wx.ID_ANY, label=_("Número de línea"))
		self.line_num = wx.TextCtrl(self.panel, wx.ID_ANY, value=str(self.line),style=wx.TE_PROCESS_ENTER)
		self.line_num.Bind(wx.EVT_TEXT, self.on_text_change)
		self.line_num.Bind(wx.EVT_TEXT_ENTER, self.on_go)
		self.line_num.Bind(wx.EVT_KEY_DOWN, self.on_key_press)
		self.okBTN=wx.Button(self.panel,label=_("Aceptar"))
		self.okBTN.Bind(wx.EVT_BUTTON,self.on_go)
		self.cancelBTN=wx.Button(self.panel,label=_("Cancelar"))
		self.cancelBTN.Bind(wx.EVT_BUTTON,self.on_cancel)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_window)

		sizeV=wx.BoxSizer(wx.VERTICAL)
		sizeH=wx.BoxSizer(wx.HORIZONTAL)
		sizeV.Add(line_label,0,wx.EXPAND)
		sizeV.Add(self.line_num,0,wx.EXPAND)
		sizeH.Add(self.okBTN,2,wx.EXPAND)
		sizeH.Add(self.cancelBTN,2,wx.EXPAND)
		sizeV.Add(sizeH,0,wx.EXPAND)
		self.panel.SetSizer(sizeV)
		self.CenterOnScreen()

	def threadMessage(self):
		thread=threading.Timer(0.1,self.plugin.speakCurrentLine)
		thread.start()


	def on_text_change(self,event):
		value=self.line_num.GetValue()
		if not value.isdigit() and value != "":
			self.line_num.SetValue(''.join(filter(str.isdigit, value)))
			ui.message(_('Sólo se permite números'))

	def on_go(self,event):
		line_number=int(self.line_num.GetValue())-1
		if 0 <= line_number < len(self.plugin.currentText):
			self.plugin.currentItem=line_number
			self.threadMessage()
			self.Close()
		else:
			wx.MessageBox(_('Número de línea inválido'),_('Error'),style=wx.OK | wx.ICON_ERROR)
			self.line_num.SetFocus()



	def on_cancel(self,event):
		if self.IsModal():
			self.EndModal(wx.ID_CANCEL)
		else:
			self.Close()


	def on_key_press(self,event):
		key_code=event.GetKeyCode()
		if key_code == wx.WXK_DOWN:
			self.increment()
		elif key_code == wx.WXK_UP:
			self.decrement()
		else:
			event.Skip()



	def increment(self):
		current_value=int(self.line_num.GetValue()) if self.line_num.GetValue() else 0
		if current_value < len(self.plugin.currentText):
			self.line_num.SetValue(str(current_value + 1))

	def decrement(self):
		current_value = int(self.line_num.GetValue()) if self.line_num.GetValue() else 0
		if current_value>1:
			self.line_num.SetValue(str(current_value - 1))


	def on_key_window(self,event):
		if event.GetKeyCode()==27:
			if self.IsModal():
				self.EndModal(wx.ID_CANCEL)
			else:
				self.Close()
		else:
			event.Skip()
