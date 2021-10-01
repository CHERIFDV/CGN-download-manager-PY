import sys
import os



import threading
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtGui
import urllib.request
from os import path
import pafy

FROM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MyApp(QMainWindow, FROM_CLASS):
    def __init__(self, parent=None):
        super(MyApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        QMainWindow.setWindowTitle(self,"CGN Download manager")
        self.window2 = MyApp2()
        self.Handel_Buton()
        self.path_of_file=""


    def Button_stoping(self):
        if os.path.exists(self.path_of_file):
              os.remove(self.path_of_file)
              os.execl(sys.executable, *([sys.executable] + sys.argv))
        else:
            QMessageBox.warning(self, "Download Information", "no downloads exist")
    def Handel_browse(self):
        save=QFileDialog.getExistingDirectory(self,"select download directory ")
        self.lineEdit.setText(save)
        return save
    def Handel_browseyoutube(self):
        save=QFileDialog.getExistingDirectory(self,"select download directory ")
        self.lineEdit_6.setText(save)
        return save

    def Handel_browseyoutubelist(self):
        save = QFileDialog.getExistingDirectory(self, "select download directory ")
        self.lineEdit_8.setText(save)

    def Handel_Buton(self):
        self.pushButton.clicked.connect(self.dowenload_file)
        self.pushButton_2.clicked.connect(self.Handel_browse)
        self.pushButton_4.clicked.connect(self.search_video)
        self.pushButton_5.clicked.connect(self.search_list)
        self.pushButton_6.clicked.connect(self.dowenload_video)
        self.pushButton_3.clicked.connect(self.Handel_browseyoutube)
        self.pushButton_7.clicked.connect(self.Handel_browseyoutubelist)
        self.pushButton_8.clicked.connect(self.Button_stoping)
        self.pushButton_9.clicked.connect(self.window2.showlist)
        self.pushButton_10.clicked.connect(self.about)
    def about(self):
        QMessageBox.about(self, "Download Information", "CGN Download Manager is application download any file from site and download videos MP4 or MP3 ")
    def progress_Bar(self,blocknum,blocksize,totalsize):
        read=blocknum*blocksize
        if totalsize > 0:
            porsent=read*100/totalsize
            self.progressBar.setValue(porsent)
        QApplication.processEvents()

    def download_file_thred(self,url,save_location):
        try:
            urllib.request.urlretrieve(url,save_location, self.progress_Bar)
        except Exception:
             QMessageBox.warning(self, "Download Information", "Download Failed")
             return
        except ValueError:
            QMessageBox.warning(self, "Download Information", "set the link")
            return
        QMessageBox.information(self, "Download Information", "the Download complete ")
        self.progressBar.setValue(0)
        self.lineEdit_2.setText('')
        self.lineEdit.setText('')
        self.label_10.setText('')
        self.path_of_file = ""
    def dowenload_file(self):
        url=self.lineEdit_2.text()
        save_location=self.lineEdit.text()
        save_location=str(save_location)+"/"+(url.split("/")[-1].split("?")[0])
        self.path_of_file=save_location
        self.label_10.setText(str("downloading :"+(url.split("/")[-1].split("?")[0])))
        self.download_thred=threading.Thread(target=self.download_file_thred,args=(url,save_location))
        self.download_thred.start()



    def search_list(self):
        self.download_thredp = threading.Thread(target=self.search_list_thread)
        self.download_thredp.start()

    def search_list_thread(self):
            save = self.lineEdit_8.text()
            if save=="":
                QMessageBox.information(self ,"Download Information" ,"Set the diractory ")
                save=self.lineEdit_8.text()
            else:
                link = self.lineEdit_7.text()
                type = self.radioButton_7.isChecked()
                QApplication.processEvents()
                self.window2.setlink(link)
                self.window2.settype(type)
                self.window2.setsave(save)
                self.label_3.setText("Please wait for search ...")
                QApplication.processEvents()
                try:
                    self.window2.cherche_playlit()
                except ValueError:
                    QMessageBox.warning(self, "Download Information", "Please set link ;)")
                    self.label_3.setText("Error 404: Link Not Found")
                    return
                self.label_3.setText("search completed press show ---->")


    def gettype(self):
     if    self.radioButton_7.isChecked():
         return "MP3"
     elif self.radioButton_8.ischecked():
         return "MP4"

    def cherche_dans_table_qualite(self):
         qualite = str(self.comboBox.currentText())
         return self.tabelem.index(qualite)

    def search_video(self):
        self.download_threds=threading.Thread(target=self.search_video_thread)
        self.download_threds.start()

    def search_video_thread(self):
        self.label_4.setText("start searching....")
        link=self.lineEdit_5.text()
        if link=="":
            self.label_4.setText("searching error....")
            QMessageBox.warning(self, "Download Information", "set link please ;)")
            return
        self.comboBox.clear()
        if self.radioButton_5.isChecked():
            v = pafy.new(link)
            steams = v.audiostreams
            for steam in steams:
                self.comboBox.addItem(str(steam))
        elif self.radioButton_6.isChecked():
            v=pafy.new(link)
            steams=v.streams
            for steam in steams:
                 self.comboBox.addItem(str(steam))
                 QApplication.processEvents()
        self.label_4.setText("searching complete")

    def progress_Barv(self,blocknum,blocksize,totalsize):
        read=blocknum*blocksize
        if totalsize > 0:
            porsent=read*100/totalsize
        self.progressBar_3.setValue(porsent)
        QApplication.processEvents()

    def dowenload_video(self):
        if self.lineEdit_5.text()!="" and self.lineEdit_6.text()!="":
            self.download_thredv=threading.Thread(target=self.download_video_thred)
            self.download_thredv.start()
        else:
            QMessageBox.warning(self, "Download Information", "enter the link and directory")
            pass
    def download_video_thred(self):
        self.label_4.setText("start download...")
        link = self.lineEdit_5.text()
        if self.lineEdit_6.text() == "":
            save = self.Handel_browseyoutube()
        else:
            save = self.lineEdit_6.text()
        v = pafy.new(link)
        print("f")
        data = self.comboBox.currentIndex()
        if self.radioButton_5.isChecked():
            v = v.audiostreams
            try:
                 self.path_of_file=save + "/" + v[data].title + ".mp3"
                 urllib.request.urlretrieve(v[data].url, save + "/" + v[data].title + ".mp3", self.progress_Barv)

            except Exception:
                QMessageBox.warning(self, "Download Information", "Download Failed")
                return
        elif self.radioButton_6.isChecked():
            v = v.streams
            try:
                self.path_of_file = save + "/" + v[data].title + ".mp4"
                urllib.request.urlretrieve(v[data].url, save + "/" + v[data].title + ".mp4", self.progress_Barv)
            except Exception:
                  QMessageBox.warning(self, "Download Information", "Download Failed")
                  return

        QMessageBox.information(self ,"Download Information" ,"the Download complete ")
        self.progressBar_3.setValue(0)
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')
        self.label_4.setText("")
        self.comboBox.clear()
        self.path_of_file = ""
#class 2 window2:

FROM_CLASS1,_ = loadUiType(path.join(path.dirname(__file__),"main2.ui"))

class MyApp2(QMainWindow, FROM_CLASS1,):
    def __init__(self, parent=None):
        super(MyApp2,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        QMainWindow.setWindowTitle(self, "CGN Download manager")
        self.handel_button()
        self.tabelem = []
        self.tabtitle=[]
        self.tablecelection=[]
        self.widget = QWidget()
        self.path_of_file = ""


    def handel_button(self):
        self.pushButton.clicked.connect(self.dowenload_video)
        self.pushButton_2.clicked.connect(self.chekall)

    def settype(self,type):
         self.type=type
    def setsave(self,save):
         self.save=save
    def setlink(self,link):
         self.link=link


    def cherche_playlit(self):
         del self.tablecelection[:]
         del self.tabtitle[:]
         del self.tabelem[:]
         self.comboBox.clear()
         v = pafy.get_playlist(self.link)
         nbv=len(v['items'])
         type=self.type
         message="the list have : "+str(nbv)+" videos"
         self.label_2.setText(str(message))
         if type :
             self.comboBox.addItem('audio:webm@50k')
             self.comboBox.addItem('audio:webm@70k')
             self.comboBox.addItem('audio:m4a@128k')
             self.comboBox.addItem('audio:webm@160k')
             for i in range(0,nbv):
                 try:
                      element=v['items'][i]['pafy'].audiostreams
                      self.tabtitle.append(v['items'][i]['pafy'].audiostreams[0].title)
                      element=str(element).replace("[","").replace("]","").replace(" ","").split(",")
                      self.tabelem.append(element)
                 except OSError :
                        self.tabtitle.append("erreur")
                        pass
         else:
             self.tab=[]
             self.comboBox.addItem('normal:webm@640x360')
             self.comboBox.addItem('normal:mp4@640x360')
             self.comboBox.addItem('normal:flv@320x240')
             self.comboBox.addItem('normal:3gp@320x240')
             self.comboBox.addItem('normal:3gp@176x144')
             self.comboBox.addItem('normal:mp4@1280x720')
             for i in range(0,nbv):
                 try:
                     element=v['items'][i]['pafy'].streams
                     print(element)
                     self.tabtitle.append(v['items'][i]['pafy'].streams[0].title)
                     element=str(element).replace("[","").replace("]","").replace(" ","").split(",")
                     self.tabelem.append(element)
                     print(self.tabelem)
                 except OSError :
                        self.tabtitle.append("erreur")
                        pass
         self.progressBar.setValue(0)

    def showlist(self):
         self.diplay_choix()

    def cherche_dans_table_qualite(self,i):
        qualite=str(self.comboBox.currentText())
        try:
           return self.tabelem[i].index(qualite)
        except ValueError:
             QMessageBox.warning(self,"Download Information", "the qualite is not execute change qualite ;)")

    def progress_Bar(self,blocknum,blocksize,totalsize):
        read=blocknum*blocksize
        if totalsize > 0:
            porsent=read*100/totalsize
        self.progressBar.setValue(porsent)
        QApplication.processEvents()


    def dowenload_video(self):
        if self.path_of_file!="":
            os.remove(self.path_of_file)
            os.execl(sys.executable, *([sys.executable] + sys.argv))
        else:
             self.download_thredvp=threading.Thread(target=self.dowenload_videop_thread)
             self.download_thredvp.start()

    def dowenload_videop_thread(self):
        v = pafy.get_playlist(self.link)
        saver=self.save
        self.tablecelection=self.envoye()
        print(self.tablecelection)
        nbv = len(v['items'])
        self.pushButton.setText("cancel download")
        if self.type:
             for i in range(len(self.tablecelection)):
                  if self.tablecelection[i]!=False:
                       if self.cherche_dans_table_qualite(i) == None:
                           return
                       savef=str(saver+"/"+v['items'][i]['pafy'].audiostreams[self.cherche_dans_table_qualite(i)].title+".mp3")
                       print(savef)
                       self.label.setText("Try Download : " +str(i+1)  + "/" +str(len(self.tabtitle)))
                       try:
                           self.label_3.setText("Audio name : : " + str(v['items'][i]['pafy'].audiostreams[self.cherche_dans_table_qualite(i)].title))
                           self.path_of_file = savef
                           urllib.request.urlretrieve(v['items'][i]['pafy'].audiostreams[self.cherche_dans_table_qualite(i)].url,savef,self.progress_Bar)
                       except Exception:
                           QMessageBox.warning(self,"Download Information","Download Failed")
                           return
                  else:
                      pass
        else:
            for i in range(len(self.tablecelection)):
                if self.tablecelection[i] != False:
                      QApplication.processEvents()
                      if self.cherche_dans_table_qualite(i)==None:
                           return
                      savef = str(saver+"/"+v['items'][i]['pafy'].streams[self.cherche_dans_table_qualite(i)].title+".mp4")

                      self.label.setText("Try Download : " +str(i+1)+ "/" +str(len(self.tabtitle)))
                      try:
                           self.path_of_file = savef
                           self.label_3.setText("Video name : " + str(v['items'][i]['pafy'].streams[self.cherche_dans_table_qualite(i)].title))
                           urllib.request.urlretrieve(v['items'][i]['pafy'].streams[self.cherche_dans_table_qualite(i)].url,savef,self.progress_Bar)

                      except Exception:
                           QMessageBox.warning(self, "Download Information", "Download Failed")
                           return
                else:
                    pass
        QMessageBox.information(self, "Download Information", "the Download complete ")
        self.label.setText("Download complete : " + str(nbv) + "/" + str(nbv))
        del self.tablecelection[:]
        del self.tabtitle[:]
        del self.tabelem [:]
        self.window().close()

    def envoye(self):
        tabcelection=[]
        for i in range(1,len(self.tabelem)*2,2):
              QApplication.processEvents()
              tabcelection.append(self.verticalLayout_2.itemAt(i).widget().isChecked())

        return tabcelection

    def chekall(self):
        for i in range(1, len(self.tabelem) * 2, 2):
            QApplication.processEvents()
            if self.verticalLayout_2.itemAt(i).widget().isEnabled() == True:
                QApplication.processEvents()
                self.verticalLayout_2.itemAt(i).widget().setCheckState(True)

    def clearLayout(self,layout):
        while layout.count():
            QApplication.processEvents()
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def diplay_choix(self):
        self.afichelayout()
        self.clearLayout(self.verticalLayout_2)
        for i in range(len(self.tabtitle)):
            QApplication.processEvents()
            self.labelB = QtWidgets.QLabel(self)
            if  self.tabtitle[i]!="erreur":
                self.labelB.setText( self.tabtitle[i])
                checkBox = QCheckBox(self)
                QApplication.processEvents()
            else :
                self.labelB.setText("that video not found sorry :(")
                checkBox = QCheckBox(self)
                checkBox.setEnabled(False)
            checkBox.setGeometry(i, 150, 20, 20)
            self.verticalLayout_2.addWidget(self.labelB)
            self.verticalLayout_2.addWidget(checkBox)
            self.show()
    def afichelayout(self):
        self.setCentralWidget(self.realmScroll)
        self.window().setFixedWidth(700)

def main():
    app=QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())


if  __name__ == "__main__":
         main()
