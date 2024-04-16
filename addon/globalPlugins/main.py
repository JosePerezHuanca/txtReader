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
import ui;
import tones;
import globalVars;
import addonHandler;

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
        self.selectedItemIndex=None
        self.currentText=[];
        self.fileName=None;
        self.reachedLimit={'start': False, 'end': False};
    
    # Translators: script category for add-on gestures
    scriptCategory=_('Txt reader');

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
                            tones.beep(300,150);
                            self.fileName=os.path.basename(filePat);
                            fileDic={
                                "title": self.fileName,
                                "text": content
                            }
                            self.content.append(fileDic)
                            self.currentItem=0;
                            self.selectedItemIndex = len(self.content) - 1
                            self.currentText=content
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
        elif 0 <= self.currentItem < len(self.currentText):
            ui.message(self.currentText[self.currentItem])
        else:
            ui.message(self.currentText[-1])

    # Translate
    @script(description=_('Navega a la siguiente línea del texto'), gesture='kb:NVDA+alt+downArrow', category=scriptCategory)
    def script_next_line(self,gesture):
        self.currentItem=min(len(self.currentText)-1, self.currentItem+1);
        if self.currentItem== len(self.currentText)-1:
            if self.reachedLimit['end']:
                tones.beep(400,150);
                # Translate
                ui.message(_('Fin.'));
                self.speakCurrentLine();
            else:
                self.reachedLimit['end']=True;
                self.speakCurrentLine();
        else:
            self.reachedLimit['start']=False;
            self.speakCurrentLine();

    # Translate
    @script(description=_('Navega a la línea anterior del texto'),gesture='kb:NVDA+alt+upArrow', category=scriptCategory)
    def script_previous_line(self,gesture):
        self.currentItem=max(0, self.currentItem-1);
        if self.currentItem==0:
            if self.reachedLimit['start']:
                tones.beep(200,150);
                # Translate
                ui.message(_('Inicio.'));
                self.speakCurrentLine();
            else:
                self.reachedLimit['start']=True;
                self.speakCurrentLine();
        else:
            self.reachedLimit['end']=False;
            self.speakCurrentLine();


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
    def script_beginText(self,gesture):
        self.currentItem=0;
        self.speakCurrentLine();

    # Translate
    @script(description=_('Ir al final del texto'),gesture='kb:NVDA+alt+end', category=scriptCategory)
    def script_endText(self,gesture):
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
            api.copyToClip(self.textContent[self.currentItem], _('Copiado'));

    # Translate
    @script(description=_('Si se abrió un archivo previamente, vacía el contenido en memoria'),gesture='kb:NVDA+alt+l', category=scriptCategory)
    def script_clearBuffer(self,gesture):
        self.content.clear();
        self.currentText.clear();
        # Translate
        ui.message(_('Se vació el buffer'));



    @script(description=_('Siguiente texto'), gesture='kb:NVDA+alt+rightArrow', category=scriptCategory)
    def script_nextText(self, gesture):
        if self.content:
            if self.selectedItemIndex is not None:
                next_index = (self.selectedItemIndex + 1) % len(self.content)
                next_item = self.content[next_index]
                if next_index == 0 or "title" not in next_item:
                    ui.message("Fin")
                else:
                    self.fileName = next_item["title"]
                    self.currentText = next_item["text"]
                    self.selectedItemIndex = next_index
                    self.speakCurrentLine()
            else:
                ui.message('No se ha seleccionado un archivo');
        else:
            ui.message(_('Primero selecciona un archivo.'))

    @script(description=_('Texto anterior'), gesture='kb:NVDA+alt+leftArrow', category=scriptCategory)
    def script_previous_text(self, gesture):
        if self.content:
            if self.selectedItemIndex is not None:
                previous_index = (self.selectedItemIndex - 1) % len(self.content)
                previous_item = self.content[previous_index]
                if previous_index == len(self.content) - 1 or "title" not in previous_item:
                    ui.message("Inicio")
                else:
                    self.fileName = previous_item["title"]
                    self.currentText = previous_item["text"]
                    self.selectedItemIndex = previous_index
                    self.speakCurrentLine()
            else:
                ui.message('No se ha seleccionado un archivo')
        else:
            ui.message(_('Primero selecciona un archivo.'))

    @script(description='Borrar texto actual', gesture='kb:NVDA+alt+backSpace')
    def script_removeCurrentText(self, gesture):
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
