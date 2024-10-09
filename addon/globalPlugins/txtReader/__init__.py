# Txt reader add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file LICENSE for more details.
# Copyright (C) 2024 José Perez <perezhuancajose@gmail.com>


import globalPluginHandler;
from scriptHandler import script;
import os;
import wx;
import codecs;
import api;
import threading
import ui;
from speech.priorities import SpeechPriority
import tones;
import globalVars;
import addonHandler;
import gui
from .Dialog_line import DialogLine
from .Dialog_search import DialogSearch

def disableInSecureMode(decoratedCls):
    if globalVars.appArgs.secure:
        return globalPluginHandler.GlobalPlugin;
    return decoratedCls;

# For translators
try:
    addonHandler.initTranslation();
except addonHandler.AddonError:
    from logHandler import log;
    log.warning('Unable to initialise translations. This may be because the addon is running from NVDA scratchpad.');

@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__();
        self.content=[];
        self.currentItem=0;
        self.selectedItemIndex=0
        self.currentText=[];
        self.fileName=None;
    
    # Translators: script category for add-on gestures
    scriptCategory=_('Txt reader');

    def threadMessage(self,message):
        def displayMessage():
            tones.beep(300,150);
            ui.message(message,SpeechPriority.NOW)
        thread = threading.Timer(0.02,displayMessage)
        thread.start()


    # Translate
    @script(description=_('Muestra el diálogo para abrir archivo'), gesture='kb:NVDA+alt+f', category=scriptCategory)
    def script_open_file(self,gesture):
        def showDialog():
            dialog=wx.FileDialog(None,_("Habrir"), wildcard=_('Archivos de texto (*.txt)|*.txt|Todos los archivos (*.*)|*.*'),style=wx.FD_OPEN);
            try:
                if dialog.ShowModal()== wx.ID_OK:
                    filePat = dialog.GetPath();
                    if os.path.exists(filePat):
                        with codecs.open(filePat,'r',encoding='utf-8') as txtFile:
                            content=[line.strip() for line in txtFile.readlines()];
                            self.fileName=os.path.basename(filePat);
                            fileDic={
                                "title": self.fileName,
                                "text": content
                            }
                            if not any(fileDic["title"] == self.fileName for fileDic in self.content):
                                self.content.append(fileDic)
                                self.currentItem=0;
                                self.selectedItemIndex = len(self.content) - 1
                                self.currentText=content
                                self.threadMessage(_(f'Lellendo {self.fileName}'))
                            else:
                                wx.MessageBox(_('Ese archivo ya fue cargado'), _('Error'), style=wx.OK | wx.ICON_ERROR)
                    else:
                            #translate
                            wx.MessageBox(_('Ese archivo no existe'), _('Error'), style=wx.OK | wx.ICON_ERROR);
            except Exception as e:
                wx.MessageBox(str(e));
            finally:
                dialog.Destroy();
        wx.CallAfter(showDialog);

    def speakCurrentLine(self):
        if not self.currentText:
            # Translate
            ui.message(_('Primero selecciona un archivo'));
        else:
            ui.message(self.currentText[self.currentItem],SpeechPriority.NOW)



    # Translate
    @script(description=_('Navega a la siguiente línea del texto'), gesture='kb:NVDA+alt+downArrow', category=scriptCategory)
    def script_next_line(self,gesture):
        if self.currentItem< len(self.currentText)-1:
            self.currentItem+=1
            # Translate
            self.speakCurrentLine();
        else:
            self.currentItem=len(self.currentText)-1
            ui.message(_('Fin'))
            self.speakCurrentLine();
            tones.beep(400,150);

    # Translate
    @script(description=_('Navega a la línea anterior del texto'),gesture='kb:NVDA+alt+upArrow', category=scriptCategory)
    def script_previous_line(self,gesture):
        if self.currentItem>0:
            self.currentItem-=1
            # Translate
            self.speakCurrentLine();
        else:
            self.currentItem=0
            ui.message(_('Inicio.'));
            self.speakCurrentLine();
            tones.beep(200,150);


    # Translate
    @script(description=_('Lee el título del archivo'),gesture='kb:NVDA+alt+t', category=scriptCategory)
    def script_title_file(self,gesture):
        if not self.fileName:
            # Translate
            ui.message(_('Primero selecciona un archivo'));
        else:
            ui.message(self.fileName);


    # Translate
    @script(description=_('Lee la línea actual'),gesture='kb:NVDA+alt+space', category=scriptCategory)
    def script_current_line(self,gesture):
        self.speakCurrentLine();

    # Translate
    @script(description=_('Ir al principio del texto'),gesture='kb:NVDA+alt+home', category=scriptCategory)
    def script_begin_text(self,gesture):
        self.currentItem=0;
        self.speakCurrentLine();

    # Translate
    @script(description=_('Ir al final del texto'),gesture='kb:NVDA+alt+end', category=scriptCategory)
    def script_end_text(self,gesture):
        self.currentItem=len(self.currentText)-1;
        self.speakCurrentLine();

    # Translate
    @script(description=_('Copia la línea actual'),gesture='kb:NVDA+alt+c', category=scriptCategory)
    def script_copy_line(self,gesture):
        if not self.currentText:
            # Translate
            ui.message(_('No hay nada para copiar'));
        else:
            # Translate
            api.copyToClip(self.currentText[self.currentItem], notify=True);

    # Translate
    @script(description=_('Si se abrió uno o mas archivos previamente, vacía el contenido en memoria'),gesture='kb:NVDA+alt+l', category=scriptCategory)
    def script_clear_list(self,gesture):
        self.content.clear();
        self.currentText.clear();
        # Translate
        ui.message(_('Se vació la lista'));

    # Translate
    @script(description=_('Muestra el diálogo para ir a una línea específica'),gesture='kb:NVDA+alt+g',category=scriptCategory)
    def script_got_to_line(self,gesture):
        def show_dialog():
            if self.currentText:
                dialog=DialogLine(gui.mainFrame,self)
                gui.mainFrame.prePopup()
                dialog.Show()
                dialog.CentreOnScreen()
                gui.mainFrame.postPopup()
            else:
                wx.MessageBox(_('Primero selecciona un archivo'),_('Error'),style=wx.OK | wx.ICON_ERROR)
        wx.CallAfter(show_dialog)


    # Translate
    @script(description=_('Muestra un diálogo para buscar en el texto actual'),gesture='kb:NVDA+alt+b',category=scriptCategory)
    def script_search(self,gesture):
        def show_dialog():
            if self.currentText:
                dialog=DialogSearch(gui.mainFrame,self)
                gui.mainFrame.prePopup()
                dialog.Show()
                dialog.CentreOnScreen()
                gui.mainFrame.postPopup()
            else:
                wx.MessageBox(_('Primero selecciona un archivo'),_('Error'),style=wx.OK | wx.ICON_ERROR)
        wx.CallAfter(show_dialog)


    # Translate
    @script(description=_('Si se abrió mas de un archivo, navega al siguiente texto en la lista'), gesture='kb:NVDA+alt+rightArrow', category=scriptCategory)
    def script_next_text(self, gesture):
        if self.content:
            if self.selectedItemIndex < len(self.content)-1:
                next_index=self.selectedItemIndex+1
                next_item = self.content[next_index]
                self.fileName = next_item["title"]
                self.currentText = next_item["text"]
                self.selectedItemIndex = next_index
                #Me aseguro que currentItem no exceda el número de líneas del nuevo texto
                self.currentItem = min(self.currentItem, len(self.currentText) - 1)
                self.speakCurrentLine()
            else:
                last=self.content[-1]
                self.fileName=last["title"]
                self.currentText=last["text"]
                ui.message(_('Fin'))
                self.speakCurrentLine()
        else:
            ui.message(_('Primero selecciona un archivo.'))

    # Translate
    @script(description=_('Si se abrió mas de un archivo, navega al texto anterior en la lista'), gesture='kb:NVDA+alt+leftArrow', category=scriptCategory)
    def script_previous_text(self, gesture):
        if self.content:
            if self.selectedItemIndex>0:
                previous_index=self.selectedItemIndex-1
                previous_item = self.content[previous_index]
                self.fileName = previous_item["title"]
                self.currentText = previous_item["text"]
                self.selectedItemIndex = previous_index
                self.currentItem = min(self.currentItem, len(self.currentText) - 1)
                self.speakCurrentLine()
            else:
                first=self.content[0]
                self.fileName=first["title"]
                self.currentText=first["text"]
                ui.message(_('Inicio'))
                self.speakCurrentLine()
        else:
            ui.message(_('Primero selecciona un archivo.'))

    # Translate
    @script(description=_('Elimina el texto actual de la lista'), gesture='kb:NVDA+alt+backSpace')
    def script_remove_current_text(self, gesture):
        if self.fileName:
            for item in self.content:
                if "title" in item and item["title"] == self.fileName:
                    self.content.remove(item)
                    break
            self.currentText.clear()
            self.fileName = None
            if self.content:
                self.selectedItemIndex = (self.selectedItemIndex - 1) % len(self.content)
                current_item = self.content[self.selectedItemIndex]
                self.fileName = current_item["title"]
                self.currentText = current_item["text"]
            self.speakCurrentLine()
        else:
            ui.message('Primero selecciona un archivo')
