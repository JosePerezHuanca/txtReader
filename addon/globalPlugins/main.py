#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2024 José Perez <perezhuancajose@gmail.com>


import globalPluginHandler;
from scriptHandler import script;
import os;
import wx;
import gui;
import codecs;
import api;
import ui;
import tones;


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__();
        self.textContent=[];
        self.currentItem=0;
        self.fileName=None;
        self.reachedLimit={'start': False, 'end': False};


    @script(description='Muestra el diálogo para habrir archivo', gesture='kb:NVDA+alt+f', category='Txt reader')
    def script_open_file(self,gesture):
        def showDialog():
            dialog=wx.FileDialog(None,"Habrir", wildcard='Archivos de texto (*.txt)|*.txt|Todos los archivos (*.*)|*.*',style=wx.FD_OPEN);
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
                            wx.MessageBox('Ese archivo no existe', 'Error', style=wx.OK | wx.ICON_ERROR);
            except Exception as e:
                wx.MessageBox(str(e));
            finally:
                dialog.Destroy();
        wx.CallAfter(showDialog);

    def speakCurrentLine(self):
        if not self.textContent:
            ui.message('Primero selecciona un archivo');
        else:
            ui.message(self.textContent[self.currentItem]);

    @script(description='Ba a la siguiente línea del texto', gesture='kb:NVDA+alt+downArrow', category='Txt reader')
    def script_next_line(self,gesture):
        self.currentItem=min(len(self.textContent)-1, self.currentItem+1);
        if self.currentItem== len(self.textContent)-1:
            if self.reachedLimit['end']:
                tones.beep(400,150);
                self.speakCurrentLine();
            else:
                self.reachedLimit['end']=True;
                self.speakCurrentLine();
        else:
            self.reachedLimit['start']=False;
            self.speakCurrentLine();


    @script(description='Ba a la línea anterior del texto',gesture='kb:NVDA+alt+upArrow', category='Txt reader')
    def script_previous_line(self,gesture):
        self.currentItem=max(0, self.currentItem-1);
        if self.currentItem==0:
            if self.reachedLimit['start']:
                tones.beep(200,150);
                self.speakCurrentLine();
            else:
                self.reachedLimit['start']=True;
                self.speakCurrentLine();
        else:
            self.reachedLimit['end']=False;
            self.speakCurrentLine();


    @script(description='Anuncia el título del archivo',gesture='kb:NVDA+alt+t', category='Txt reader')
    def script_title_file(self,gesture):
        if not self.fileName:
            ui.message('Primero selecciona un archivo');
        else:
            ui.message(self.fileName);


    @script(description='Lee la línea actual',gesture='kb:NVDA+alt+space', category='Txt reader')
    def script_current_line(self,gesture):
        self.speakCurrentLine();

    @script(description='Ba al principio del texto',gesture='kb:NVDA+alt+home', category='Txt reader')
    def script_beginText(self,gesture):
        self.currentItem=0;
        self.speakCurrentLine();

    @script(description='Ba al final del texto',gesture='kb:NVDA+alt+end', category='Txt reader')
    def script_endText(self,gesture):
        self.currentItem=len(self.textContent)-1;
        self.speakCurrentLine();

    @script(description='Copia la línea actual',gesture='kb:NVDA+alt+c', category='Txt reader')
    def script_copy_line(self,gesture):
        if not self.textContent:
            ui.message('No hay nada para copiar');
        else:
            api.copyToClip(self.textContent[self.currentItem], 'Copiado');


    @script(description='Vacía el bufer actual',gesture='kb:NVDA+alt+l', category='Txt reader')
    def script_clearBufer(self,gesture):
        self.textContent.clear();
        ui.message('Se vació el bufer');
