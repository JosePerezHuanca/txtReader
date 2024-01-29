# Txt reader add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file LICENSE for more details.
# Copyright (C) 2024 José Perez <perezhuancajose@gmail.com>


import globalPluginHandler;
from scriptHandler import script;
import os;
import wx;
import gui;
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
        self.textContent=[];
        self.currentItem=0;
        self.fileName=None;
        self.reachedLimit={'start': False, 'end': False};

    # Translate
    @script(description=_('Muestra el diálogo para abrir archivo'), gesture='kb:NVDA+alt+f', category='Txt reader')
    def script_open_file(self,gesture):
        def showDialog():
            dialog=wx.FileDialog(None,_("Habrir"), wildcard=_('Archivos de texto (*.txt)|*.txt|Todos los archivos (*.*)|*.*'),style=wx.FD_OPEN);
            try:
                if dialog.ShowModal()== wx.ID_OK:
                    filePat = dialog.GetPath();
                    if os.path.exists(filePat):
                        with codecs.open(filePat,'r',encoding='utf-8') as txtFile:
                            content=[line.strip() for line in txtFile.readlines()];
                            self.textContent.clear();
                            self.textContent.extend(content);
                            tones.beep(300,150);
                            self.fileName=os.path.basename(filePat);
                            self.currentItem=0;
                    else:
                            #translate
                            wx.MessageBox(_('Ese archivo no existe'), 'Error', style=wx.OK | wx.ICON_ERROR);
            except Exception as e:
                wx.MessageBox(str(e));
            finally:
                dialog.Destroy();
        wx.CallAfter(showDialog);

    def speakCurrentLine(self):
        if not self.textContent:
            # Translate
            ui.message(_('Primero selecciona un archivo'));
        else:
            ui.message(self.textContent[self.currentItem]);

    # Translate
    @script(description=_('Navega a la siguiente línea del texto'), gesture='kb:NVDA+alt+downArrow', category='Txt reader')
    def script_next_line(self,gesture):
        self.currentItem=min(len(self.textContent)-1, self.currentItem+1);
        if self.currentItem== len(self.textContent)-1:
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
    @script(description=_('Navega a la línea anterior del texto'),gesture='kb:NVDA+alt+upArrow', category='Txt reader')
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
    @script(description=_('Lee el título del archivo'),gesture='kb:NVDA+alt+t', category='Txt reader')
    def script_title_file(self,gesture):
        if not self.fileName:
            # Translate
            ui.message(_('Primero selecciona un archivo'));
        else:
            ui.message(self.fileName);


    # Translate
    @script(description=_('Lee la línea actual'),gesture='kb:NVDA+alt+space', category='Txt reader')
    def script_current_line(self,gesture):
        self.speakCurrentLine();

    # Translate
    @script(description=_('Ir al principio del texto'),gesture='kb:NVDA+alt+home', category='Txt reader')
    def script_beginText(self,gesture):
        self.currentItem=0;
        self.speakCurrentLine();

    # Translate
    @script(description=_('Ir al final del texto'),gesture='kb:NVDA+alt+end', category='Txt reader')
    def script_endText(self,gesture):
        self.currentItem=len(self.textContent)-1;
        self.speakCurrentLine();

    # Translate
    @script(description=_('Copia la línea actual'),gesture='kb:NVDA+alt+c', category='Txt reader')
    def script_copy_line(self,gesture):
        if not self.textContent:
            # Translate
            ui.message(_('No hay nada para copiar'));
        else:
            # Translate
            api.copyToClip(self.textContent[self.currentItem], _('Copiado'));

    # Translate
    @script(description=_('Si se abrió un archivo previamente, vacía el contenido en memoria'),gesture='kb:NVDA+alt+l', category='Txt reader')
    def script_clearBuffer(self,gesture):
        self.textContent.clear();
        # Translate
        ui.message(_('Se vació el buffer'));
