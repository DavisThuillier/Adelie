import sys
import os
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
import vlc
from glob import glob
import numpy.random as rnd
import music_tag
from shutil import copyfile

from UI.mainWindow import Ui_MainWindow
from UI.editMetadata import Ui_Dialog as Ui_EditMetadata
from UI.editSingleSong import Ui_Dialog as Ui_EditSingleSong
from UI.preferences import Ui_Dialog as Ui_Preferences
from UI.miniMediaPlayer import Ui_Form as Ui_MiniMediaPlayer

import resources_rc

def resource_path(relative_path):
    try:
        base_path = sys.__MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

metaDataDict = {"Title": 0, "Artist": 1,"Album": 4, "Disc": 24}
libraryDict = {"Filename": 0, "DiscAndTrack": 1, "Title": 2, "Album": 3, "Artist": 4, "Genre": 5, "AlbumArtist": 6}

def timeFormat(seconds):
    """
    Formats the time for audio scroll bars to Min:Sec
    """
    minute = abs(seconds)//60
    second = abs(seconds)%60
    return f"{minute:02d}:{second:02d}" 

# Default values for paths
libraryPaths = []
playlistPath = ''

class SongItem(QtWidgets.QListWidgetItem):
    def __init__(self, title, filename = "Unknown"):
        super().__init__(title)
        self.title = title
        self.filename = filename
    def text(self):
        return self.title

class Playlist(QtWidgets.QListWidgetItem):
    def __init__(self, name, filename = "Unknown.m3u"):
        super().__init__(name)
        self.name = name
        self.filename = filename
        #self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

class AlbumItem(QtWidgets.QListWidgetItem):
    def __init__(self, albumName = "Untitled", letter = None, albumDir = "Unknown"):
        super().__init__()
        self.albumName = albumName
        self.letter = letter
        self.albumDir = albumDir

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.musicTabs.setCurrentIndex(0) # Start user at album grid
        self.penguins = [":/images/resources/images/penguin{}.jpg".format(x) for x in range(1,4)] # Placeholder penguins
        self.getSettings()

        self.preferencesDialog = Preferences()
        self.preferencesDialog.accepted.connect(self.setPaths)

        self.miniMediaPlayer = MiniMediaPlayer()
        self.setMiniMediaPlayerActions()

        self.previousSongs = []
        self.playlistActionList = []
        self.tabActionList = []
        self.extraTabListWidgets = []
        self.previousSongIndex = 0

        # Open connection to library database
        self.con = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("library.db")
        self.con.open() # Open a connection to the database

        # Song timer to update info while playing
        self.timer = QtCore.QTimer(self) 
        self.timer.timeout.connect(self.setScrollTimeValues) 

        self.player = vlc.Instance() # VLC instance 
        self.mp = self.player.media_player_new() # Media player
        
        self.currentSong = None
        self.currentAlbum = None
        self.currentPlaylist = None
        self.muted = False
        self.singleSongLoop = False
        self.queueLoop = False
        self.shuffle = False
        self.timeLock = False
        self.songViewState = None
        
        self.setupAdditionalUi()
        self.loadLibraryFromDatabase()

        # Keyboard Shortcuts
        self.playButton.setShortcut(QtGui.QKeySequence("Space"))
        self.shuffleButton.setShortcut(QtGui.QKeySequence("Ctrl+S"))
        self.loopButton.setShortcut(QtGui.QKeySequence("Ctrl+L"))
        self.nextButton.setShortcut(QtGui.QKeySequence("Ctrl+N"))
        self.previousButton.setShortcut(QtGui.QKeySequence("Ctrl+P"))
        self.actionScan_Library.setShortcut(QtGui.QKeySequence("Ctrl+U"))
        self.actionExit.setShortcut(QtGui.QKeySequence("Ctrl+Q"))
        self.actionCurrent_Song.setShortcut(QtGui.QKeySequence("Ctrl+I"))
        
        self.muteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+M"), self)
        self.muteShortcut.activated.connect(lambda: self.toggleMute)

        self.restartShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.restartShortcut.activated.connect(lambda: self.mp.set_position(0))

        self.advanceShortcut = QtWidgets.QShortcut(QtCore.Qt.Key_Right, self)
        self.advanceShortcut.activated.connect(lambda: self.audioScroll.setSliderPosition(self.audioScroll.value() + 5)) 

        self.tabAdvanceShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+F"), self)
        self.tabAdvanceShortcut.activated.connect(self.tabAdvance)
        self.tabRetreatShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+D"), self)
        self.tabRetreatShortcut.activated.connect(lambda: self.tabAdvance(reverse= True))

        self.setActionTriggers()
        self.installEventFilters()

    def setupAdditionalUi(self):
        self.songViewList.doubleClicked.connect(self.songViewOnDoubleClick)
        self.albumListWidget.itemClicked.connect(lambda e: self.loadAlbum(item = e))
        self.albumListWidget.itemDoubleClicked.connect(lambda e: self.loadAlbum(item = e, toQueue=True))
        self.albumArtistDiscographyListWidget.itemClicked.connect(lambda e: self.loadAlbum(item = e, subsetType = "AlbumArtist", subset = self.albumArtistTabAlbumArtistLabel.text()))
        self.albumArtistDiscographyListWidget.itemDoubleClicked.connect(lambda e: self.loadAlbum(item = e, subsetType = "AlbumArtist", subset = self.albumArtistTabAlbumArtistLabel.text(), toQueue=True))
        self.artistDiscographyListWidget.itemClicked.connect(lambda e: self.loadAlbum(item = e, subsetType = "Artist", subset = self.artistTabArtistLabel.text()))
        self.artistDiscographyListWidget.itemDoubleClicked.connect(lambda e: self.loadAlbum(item = e, subsetType = "Artist", subset = self.artistTabArtistLabel.text(),toQueue=True))
        self.genreDiscographyListWidget.itemClicked.connect(lambda e: self.loadAlbum(item = e, subsetType = "Genre", subset = self.genreTabGenreLabel.text()))
        self.genreDiscographyListWidget.itemDoubleClicked.connect(lambda e: self.loadAlbum(item = e, subsetType = "Genre", subset = self.genreTabGenreLabel.text(), toQueue = True))

        self.musicTabs.tabCloseRequested.connect(lambda index: self.musicTabs.removeTab(index)) # Make tabs closable
        for i in range(6): # Make required tabs not closable
            self.musicTabs.tabBar().setTabButton(i, QtWidgets.QTabBar.RightSide,None)

        self.activeQueue.itemDoubleClicked.connect(self.setMediaAndPlay)
        self.searchLineEdit.returnPressed.connect(lambda: self.search(self.searchLineEdit.text()))
        
        self.albumArtistTabAlbumArtistLabel.mousePressEvent = self.albumArtistTabAlbumArtistLabelClick
        self.artistTabArtistLabel.mousePressEvent = self.artistTabArtistLabelClick

        self.genreList.itemClicked.connect(self.onGenreClicked)
        self.genreList.itemDoubleClicked.connect(self.onGenreDoubleClicked)

        self.playlistWidget.itemClicked.connect(self.loadPlaylist)
        self.playlistWidget.itemDoubleClicked.connect(self.onPlaylistDoubleClicked)

        self.artistList.itemClicked.connect(lambda item: self.loadDiscography(item, self.artistDiscographyListWidget))
        self.albumArtistList.itemClicked.connect(lambda item: self.loadDiscography(item, self.albumArtistDiscographyListWidget))
        self.genreList.itemClicked.connect(lambda item: self.loadDiscography(item, self.genreDiscographyListWidget))
        
        self.albumArtistShuffle.clicked.connect(lambda: self.massShuffle("AlbumArtist", self.albumArtistTabAlbumArtistLabel.text()))
        self.artistShuffle.clicked.connect(lambda: self.massShuffle("Artist",self.artistTabArtistLabel.text()))
        self.genreShuffle.clicked.connect(lambda: self.massShuffle("Genre",self.genreTabGenreLabel.text()))

        self.playButton.clicked.connect(self.togglePlay)
        self.shuffleButton.clicked.connect(self.toggleShuffle)
        self.loopButton.clicked.connect(self.toggleLoop)
        self.nextButton.clicked.connect(self.playNextSong)
        self.previousButton.clicked.connect(self.playPreviousSong)
        self.audioScroll.sliderReleased.connect(lambda: self.mp.set_position(self.audioScroll.value()/100) )
        self.audioScroll.sliderPressed.connect(self.toggleScrollLock)
        self.audioScroll.setTracking(True)
        self.volumeDial.valueChanged.connect(lambda: self.mp.audio_set_volume(self.volumeDial.value()) )

        # Tengwar
        #tengwarId = QtGui.QFontDatabase.addApplicationFont(":/fonts/resources/fonts/tngan.ttf")
        #tengwarFamily = QtGui.QFontDatabase.applicationFontFamilies(tengwarId)[0]
        #tngani = QtGui.QFont(tengwarFamily, 20)
        #self.labelThuillier.setFont(tngani)
        #self.labelAudio.setFont(tngani)

    def getSettings(self):
        self.settings=QtCore.QSettings('Adelie', 'Principle')
        if self.settings.value('Library Path') != None:
            global libraryPaths
            libraryPaths = self.settings.value('Library Path') # Load from setting
       
        if self.settings.value('Playlist Path') != None: # Use default is setting has not been set yet
            global playlistPath
            playlistPath = self.settings.value('Playlist Path')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.miniMediaPlayer.close()
        return super().closeEvent(a0)

    def setPaths(self):
        paths = []
        for path in [self.preferencesDialog.pathListWidget.item(index).text() for index in range(self.preferencesDialog.pathListWidget.count())]:
            if path != "":
                paths.append(path)
        self.settings.setValue('Library Path', paths)

        global libraryPaths
        libraryPaths = paths

        global playlistPath
        playlistPath = self.preferencesDialog.playlistPathLineEdit.text()
        if not os.path.isdir(os.path.dirname(playlistPath)) and playlistPath.strip() != '':
            os.makedirs(playlistPath)
        self.settings.setValue('Playlist Path', playlistPath)

    def loadLibraryFromDatabase(self):
        self.createSongView()
        self.generateAlbumGrid()
        self.generatePlaylistList()
        self.generateGenreList()
        self.generateArtistList()
        self.generateAlbumArtistList()

    def reset(self):
        self.reachedEndofQueue()
        self.activeQueue.clear()
        self.miniMediaPlayer.activeQueue.clear()
        self.musicTabs.setCurrentIndex(0) # Return user to album grid
        self.currentSong = None
        self.currentAlbum = None
        self.currentPlaylist = None
        self.muted = False
        self.singleSongLoop = False
        self.queueLoop = False
        self.shuffle = False
        self.timeLock = False
        self.songViewState = None
        self.loadLibraryFromDatabase() 

    def createSongView(self):

        self.songViewModel = QtSql.QSqlQueryModel()
        self.songViewModel.removeColumns(0,2)
        self.songViewModel.setQuery("SELECT * FROM songs ORDER BY Album, DiscAndTrack")
        self.songViewModel.setHeaderData(libraryDict['DiscAndTrack'], QtCore.Qt.Horizontal, " ")
        self.songViewModel.setHeaderData(libraryDict['AlbumArtist'], QtCore.Qt.Horizontal, "Album Artist")

        self.allSongViewModel = QtSql.QSqlQueryModel()
        self.allSongViewModel.removeColumns(0,2)
        self.allSongViewModel.setQuery("SELECT * FROM songs ORDER BY Album, DiscAndTrack")
        self.allSongViewModel.setHeaderData(libraryDict['DiscAndTrack'], QtCore.Qt.Horizontal, " ")
        self.allSongViewModel.setHeaderData(libraryDict['AlbumArtist'], QtCore.Qt.Horizontal, "Album Artist")

        self.songViewList.setModel(self.songViewModel)
        self.songViewList.header().setStyleSheet('font:bold')
        self.songViewList.setSortingEnabled(True)
        self.songViewList.hideColumn(0) # Hide filename
        self.songViewList.hideColumn(1) # Hide discandtrack
        self.songViewList.setColumnWidth(1,800)
        self.songViewList.setColumnWidth(2,800)
        self.songViewList.setColumnWidth(3,800)

        self.allSongViewList.setModel(self.allSongViewModel)
        self.allSongViewList.header().setStyleSheet('font:bold')
        self.allSongViewList.setSortingEnabled(True)
        self.allSongViewList.hideColumn(0) # Hide filename
        self.allSongViewList.hideColumn(1) # Hide discandtrack
        self.allSongViewList.setColumnWidth(1,800)
        self.allSongViewList.setColumnWidth(2,800)
        self.allSongViewList.setColumnWidth(3,800)

    def installEventFilters(self):
        self.playlistWidget.installEventFilter(self)
        self.songViewLabel.installEventFilter(self)
        self.songViewList.installEventFilter(self)
        self.allSongViewList.installEventFilter(self)
        self.albumListWidget.installEventFilter(self)
        self.genreList.installEventFilter(self)
        self.activeQueue.installEventFilter(self)
        self.artistDiscographyListWidget.installEventFilter(self)
        self.albumArtistDiscographyListWidget.installEventFilter(self)
        self.albumArtistList.installEventFilter(self)
        self.artistList.installEventFilter(self)
        self.musicTabs.tabBar().installEventFilter(self)
        self.genreDiscographyListWidget.installEventFilter(self)
        self.albumArtLabel.installEventFilter(self)
        self.titleLabel.installEventFilter(self)
        self.artistLabel.installEventFilter(self)
        self.albumLabel.installEventFilter(self)

        # Mini Media Player Event Filters
        self.miniMediaPlayer.installEventFilter(self)
        self.miniMediaPlayer.albumArtLabel.installEventFilter(self)
        self.miniMediaPlayer.titleLabel.installEventFilter(self)
        self.miniMediaPlayer.artistLabel.installEventFilter(self)
        self.miniMediaPlayer.albumLabel.installEventFilter(self)
        self.miniMediaPlayer.activeQueue.installEventFilter(self)

    def eventFilter(self, source, event):
        """Extend the event filter of QMainWindow for context menus"""       
        if event.type() == QtCore.QEvent.ContextMenu:
            songContexts = [self.songViewList, 
                        self.allSongViewList,
                        self.songViewLabel, 
                        self.albumListWidget,
                        self.artistList,
                        self.albumArtistList, 
                        self.genreList,
                        self.artistDiscographyListWidget,
                        self.albumArtistDiscographyListWidget,
                        self.genreDiscographyListWidget,
                        self.activeQueue,
                        self.miniMediaPlayer.activeQueue,
                        ] + self.extraTabListWidgets + [self.titleLabel, self.artistLabel, self.albumArtLabel, self.albumLabel] + [self.miniMediaPlayer.titleLabel, self.miniMediaPlayer.artistLabel, self.miniMediaPlayer.albumArtLabel, self.miniMediaPlayer.albumLabel]
            if source in songContexts:
                if source is self.songViewList:
                    menu = self.createSongContextMenu(context = 0)
                elif source is self.songViewLabel:
                    menu = self.createSongContextMenu(context = 1)
                elif source is self.albumListWidget:
                    albums = [item for item in self.albumListWidget.selectedItems() if item.albumName != "Not An Album"]
                    if len(albums) < 1: return True
                    menu = self.createSongContextMenu(context = 2, albums = albums)
                elif source is self.genreList:
                    genres = [item.text() for item in self.genreList.selectedItems()]
                    if len(genres) < 1: return True
                    menu = self.createSongContextMenu(context = 3, genres = genres)
                elif source is self.artistDiscographyListWidget:
                    albums = [albumItem.albumName for albumItem in self.artistDiscographyListWidget.selectedItems()]
                    artists = [self.artistTabArtistLabel.text()]
                    if len(albums) < 1: return True
                    menu = self.createSongContextMenu(context = 4, albums = albums, artists = artists)
                elif source is self.albumArtistDiscographyListWidget:
                    albumArtists = [self.albumArtistTabAlbumArtistLabel.text()]
                    albums = [albumItem.albumName for albumItem in self.albumArtistDiscographyListWidget.selectedItems()]
                    if len(albums) < 1: return True
                    menu = self.createSongContextMenu(context = 5, albums = albums, albumArtists = albumArtists)
                elif source in [self.activeQueue, self.miniMediaPlayer.activeQueue]:
                    menu = self.createSongContextMenu(context = 6)
                    if self.activeQueue.count() < 1: return True # Do not show menu if there are no songs in the queue
                elif source is self.artistList:
                    artists = [item.text() for item in self.artistList.selectedItems()]
                    if len(artists) < 1: return True
                    menu = self.createSongContextMenu(context = 8, artists = artists)
                elif source is self.albumArtistList:
                    albumArtists = [item.text() for item in self.albumArtistList.selectedItems()]
                    if len(albumArtists) < 1: return True
                    menu = self.createSongContextMenu(context = 7, albumArtists = albumArtists)
                elif source in self.extraTabListWidgets:
                    menu = self.createSongContextMenu(context = 9, tabListWidget= source)
                elif source is self.genreDiscographyListWidget:
                    albums = [albumItem.albumName for albumItem in self.genreDiscographyListWidget.selectedItems()]
                    if len(albums) < 1: return True
                    genres = [self.genreTabGenreLabel.text()]
                    menu = self.createSongContextMenu(context = 10, albums = albums, genres = genres)
                elif source in [self.titleLabel, self.artistLabel, self.albumArtLabel, self.albumLabel,
                                self.miniMediaPlayer.titleLabel, self.miniMediaPlayer.artistLabel, self.miniMediaPlayer.albumArtLabel, self.miniMediaPlayer.albumLabel]:
                    if self.currentSong != None:
                        menu = self.createSongContextMenu(context = 11)
                    else: return True
                elif source is self.allSongViewList:
                    menu = self.createSongContextMenu(context = 12)
                else: return True
                menu.exec(event.globalPos())
            
            elif source is self.playlistWidget:
                playlistContextMenu = self.createPlaylistContextMenu(self.playlistWidget.itemAt(event.pos()))
                playlistContextMenu.exec(event.globalPos())

            elif source is self.musicTabs.tabBar():
                tabIndex = self.musicTabs.tabBar().tabAt(event.pos())
                if tabIndex > 5:
                    tabContextMenu = self.createTabContextMenu(self.extraTabListWidgets[tabIndex - 6])
                    tabContextMenu.exec(event.globalPos())
            elif source is self.miniMediaPlayer:
                print("Success!")
            return True
    
        return super().eventFilter(source, event)

    def createSongContextMenu(self, context = 0, albums = ["Unknown"], genres = ["Unknown"], artists = ["Unknown"], albumArtists = ["Unknown"], tabListWidget = None):
        songContextMenu = QtWidgets.QMenu()
        selectedSongs = []

        if context == 0: # Context for song view list 
            selectedSongs = [SongItem(self.songViewModel.index(row,libraryDict['Title']).data(),
                            self.songViewModel.index(row,libraryDict['Filename']).data()) 
                            for row in [index.row() for index in self.songViewList.selectionModel().selectedRows()] ]
            tabName = "   " # Name of new tab if created
        elif context == 1: # Context for song view label
            for i in range(self.songViewModel.rowCount()):
                    filename = self.songViewModel.index(i,libraryDict['Filename']).data()  # Get filename from the model
                    title = self.songViewModel.index(i,libraryDict['Title']).data()
                    selectedSongs.append(SongItem(title, filename))
            tabName = self.songViewLabel.text()
        elif context == 2: # Context for album list widget
            getAlbumSongsQuery = QtSql.QSqlQuery()
            getAlbumSongsQueryString = 'SELECT * FROM songs WHERE Album IN ('
            tabName = ""
            firstAlbum = True
            for album in albums:
                if firstAlbum:
                    getAlbumSongsQueryString += '"{}" '.format(album.albumName)
                    tabName += album.albumName; firstAlbum = False
                else:
                    getAlbumSongsQueryString += ', "{}" '.format(album.albumName)
                    tabName += " \u222A {}".format(album.albumName)
                
            getAlbumSongsQueryString += ')'
            getAlbumSongsQuery.exec(getAlbumSongsQueryString)
            while getAlbumSongsQuery.next():
                title = getAlbumSongsQuery.value(libraryDict['Title'])
                filename = getAlbumSongsQuery.value(libraryDict['Filename'])
                selectedSongs.append( SongItem(title, filename) )
            if len(albums) == 0:
                tabName = ""
            else:
                tabName = albums[0].albumName
                for album in albums[1:]:
                    tabName += " \u222A " + album.albumName

        elif context == 3: # Context for genres
            getGenreSongsQuery = QtSql.QSqlQuery()
            getGenreSongsQueryString = 'SELECT * FROM songs WHERE Genre IN ('
            for index, genre in enumerate(genres):
                if index == 0:
                    getGenreSongsQueryString += '"{}" '.format(genre)
                else:
                    getGenreSongsQueryString += ', "{}" '.format(genre)

            getGenreSongsQueryString += ')'
            getGenreSongsQuery.exec(getGenreSongsQueryString)
            while getGenreSongsQuery.next():
                title = getGenreSongsQuery.value(libraryDict['Title'])
                filename = getGenreSongsQuery.value(libraryDict['Filename'])
                selectedSongs.append( SongItem(title, filename) )
            tabName = genres[0]
            for genre in genres[1:]:
                tabName += " \u222A " + genre
        elif context == 4: # Context for artist subset of album
            getArtistSongsQuery = QtSql.QSqlQuery()
            getArtistSongsQuery.exec('SELECT * FROM songs WHERE Album="{}" AND Artist="{}"'.format(albums[0], artists[0]))
            while (getArtistSongsQuery.next()):
                title = getArtistSongsQuery.value(libraryDict['Title'])
                filename = getArtistSongsQuery.value(libraryDict['Filename'])
                selectedSongs.append( SongItem(title, filename) )
            if len(albums) == 0:
                tabName = ""
            else:
                tabName = albums[0] + "\u2229" + artists[0]
        elif context == 5: # Context for album artist subset of album
            getAlbumArtistSongsQuery = QtSql.QSqlQuery()
            getAlbumArtistSongsQueryString = 'SELECT * FROM songs WHERE Album IN ('
            for index, album in enumerate(albums):
                if index == 0:
                    getAlbumArtistSongsQueryString += '"{}" '.format(album)
                else:
                    getAlbumArtistSongsQueryString += ', "{}" '.format(album)
            getAlbumArtistSongsQueryString += ') AND AlbumArtist="{}"'.format(albumArtists[0])
            getAlbumArtistSongsQuery.exec(getAlbumArtistSongsQueryString)
            while (getAlbumArtistSongsQuery.next()):
                title = getAlbumArtistSongsQuery.value(libraryDict['Title'])
                filename = getAlbumArtistSongsQuery.value(libraryDict['Filename'])
                selectedSongs.append( SongItem(title, filename) )
            if len(albums) == 0:
                tabName = ""
            elif len(albums) == 1:
                tabName = albums[0] + " \u2229 " + albumArtists[0]
            else:
                tabName = "(" + albums[0]
                for albums in albums[1:]:
                    tabName += " \u222A " + album
                tabName += ") \u2229 " + albumArtists[0]
        elif context == 6: # Context for active queue
            selectedSongs = [SongItem(item.title, item.filename) for item in self.activeQueue.selectedItems()]
            tabName = "Queue"
        elif context == 7: # Context for multiple album artists
            getAlbumArtistSongsQuery = QtSql.QSqlQuery()
            getAlbumArtistSongsQueryString = 'SELECT * FROM songs WHERE AlbumArtist IN ('
            for index, albumArtist in enumerate(albumArtists):
                if index == 0:
                    getAlbumArtistSongsQueryString += '"{}" '.format(albumArtist)
                else:
                    getAlbumArtistSongsQueryString += ', "{}" '.format(albumArtist)
            getAlbumArtistSongsQueryString += ')'
            getAlbumArtistSongsQuery.exec(getAlbumArtistSongsQueryString)
            while (getAlbumArtistSongsQuery.next()):
                title = getAlbumArtistSongsQuery.value(libraryDict['Title'])
                filename = getAlbumArtistSongsQuery.value(libraryDict['Filename'])
                selectedSongs.append( SongItem(title, filename) )
            tabName = albumArtists[0]
            for artist in albumArtists[1:]:
                tabName += " \u222A " + artist

        elif context == 8: # Context for multiple artists
            getArtistSongsQuery = QtSql.QSqlQuery()
            getArtistSongsQueryString = 'SELECT * FROM songs WHERE Artist IN ('
            for index, artist in enumerate(artists):
                if index == 0:
                    getArtistSongsQueryString += '"{}" '.format(artist)
                else:
                    getArtistSongsQueryString += ', "{}" '.format(artist)

            getArtistSongsQueryString += ')'
            getArtistSongsQuery.exec(getArtistSongsQueryString)
            while (getArtistSongsQuery.next()):
                title = getArtistSongsQuery.value(libraryDict['Title'])
                filename = getArtistSongsQuery.value(libraryDict['Filename'])
                selectedSongs.append( SongItem(title, filename) )
            tabName = artists[0]
            for artist in artists[1:]:
                tabName += " \u222A " + artist
        elif context == 9:
            selectedSongs = [SongItem( song.title, song.filename) for song in tabListWidget.selectedItems()]
        elif context == 10:
            getGenreSongsQuery = QtSql.QSqlQuery()
            getGenreSongsQueryString = 'SELECT * FROM songs WHERE Album IN ('
            firstAlbum = True
            for album in albums:
                if firstAlbum:
                    getGenreSongsQueryString += '"{}" '.format(album); firstAlbum = False
                else:
                    getGenreSongsQueryString += ', "{}" '.format(album)
            getGenreSongsQueryString += ') AND Genre="{}"'.format(genres[0])
            getGenreSongsQuery.exec(getGenreSongsQueryString)
            while (getGenreSongsQuery.next()):
                selectedSongs.append( SongItem(getGenreSongsQuery.value(libraryDict['Title']), getGenreSongsQuery.value(libraryDict['Filename'])) )
            if len(albums) == 0:
                tabName = ""
            elif len(albums) == 1:
                tabName = albums[0] + " \u2229 " + genres[0]
            else:
                tabName = "(" + albums[0]
                for albums in albums[1:]:
                    tabName += " \u222A " + album
                tabName += ") \u2229 " + genres[0]
        elif context == 11:
            selectedSongs = [SongItem( self.titleLabel.text(), self.currentSong)]
            tabName = self.titleLabel.text()
        elif context == 12:
            selectedSongs = [SongItem(self.allSongViewModel.index(row,libraryDict['Title']).data(),
                            self.allSongViewModel.index(row,libraryDict['Filename']).data()) 
                            for row in [index.row() for index in self.allSongViewList.selectionModel().selectedRows()] ]
            tabName = "   " # Name of new tab if created
        else:
            tabName = "New Tab"

        playlistSubMenu = songContextMenu.addMenu("Add To Playlist")
        for playlist in self.playlistList:
            self.createPlaylistAction(playlist, *selectedSongs)
            playlistSubMenu.addAction(self.playlistActionList[-1])
        newPlaylistAction = playlistSubMenu.addAction("New Playlist")
        newPlaylistAction.triggered.connect(lambda: self.newPlaylistDialog(*selectedSongs))
        
        if context != 6:
            addToQueueAction = songContextMenu.addAction("Add to Queue")
            addToQueueAction.triggered.connect(lambda: self.addToQueue(*selectedSongs))
        else:
            removeFromQueueAction = songContextMenu.addAction("Remove from Queue")
            removeFromQueueAction.triggered.connect(self.removeSelectedFromQueue)

        playNowAction = songContextMenu.addAction("Play Now")
        playNowAction.triggered.connect(lambda: self.addToFrontOfQueueAndPlay(*selectedSongs))

        playNextAction = songContextMenu.addAction("Play Next")
        playNextAction.triggered.connect(lambda: self.addToQueue(*selectedSongs, next = True))

        replaceQueueAction = songContextMenu.addAction("Replace Queue")
        replaceQueueAction.triggered.connect(lambda: self.replaceQueue(*selectedSongs))

        replaceAndPlayAction = songContextMenu.addAction("Replace Queue and Play Now")
        replaceAndPlayAction.triggered.connect(lambda: self.replaceQueueAndPlayNow(*selectedSongs))

        if len(selectedSongs) > 0:
            editMetadataAction = songContextMenu.addAction("Edit Metadata")
            editMetadataAction.triggered.connect(lambda: self.editMetadata(*selectedSongs))

        if context in [2]: #[2,4,5,10]
            editAlbumArtAction = songContextMenu.addAction("Edit Album Art")
            editAlbumArtAction.triggered.connect(lambda: self.chooseAlbumArt(albums[0]))
        
        if context != 9:
            newTabAction = songContextMenu.addAction("New Tab")
            newTabAction.triggered.connect(lambda: self.newTab(tabName, *selectedSongs))
        else:
            removeFromTabAction = songContextMenu.addAction("Remove From Tab")
            removeFromTabAction.triggered.connect(lambda: self.removeSelectedFromTab(tabListWidget))

        if self.musicTabs.count() > 6:
            addToTabSubMenu = songContextMenu.addMenu("Add to Tab")
            for i in range(6, self.musicTabs.count()):
                self.makeAddToTabAction(i, *selectedSongs)
                addToTabSubMenu.addAction(self.tabActionList[-1])

        if self.songViewState == 1 and context == 0 : # Corresponds to being in playlist view; provide additional actions
            deleteFromPlaylistAction = songContextMenu.addAction("Delete from {}".format(self.currentPlaylist.name))
            deleteFromPlaylistAction.triggered.connect(lambda: self.deleteFromPlaylist(self.currentPlaylist, *selectedSongs))

        return songContextMenu

    def makeAddToTabAction(self, index, *args):
        selectedSongs = []
        for arg in args:
            if type(arg) == SongItem:
                selectedSongs.append(arg)
        action = QtWidgets.QAction(self.musicTabs.tabText(index))
        action.triggered.connect(lambda: self.addToTab(index, *args))
        self.tabActionList.append(action)
        
    def addToTab(self, index, *args):
        list = self.musicTabs.widget(index).findChild(QtWidgets.QListWidget)
        for arg in args:
            list.addItem(arg)
        
    def editMetadata(self, *args):
        if len(args) == 0:
            return
        elif len(args) == 1:
            try:
                filename = args[0].filename
                f = music_tag.load_file(filename)
            except:
                return
            dialog = EditSingleSongDialog()
            dialog.oldTitleLabel.setText(f['title'].value)
            dialog.oldArtistLabel.setText(f['artist'].value)
            dialog.oldAlbumLabel.setText(f['album'].value)
            dialog.oldGenreLabel.setText(f['genre'].value)

            if dialog.exec():
                newTitle = dialog.newTitleEdit.text()
                newArtist = dialog.newArtistEdit.text()
                newAlbum = dialog.newAlbumEdit.text()
                newGenre = dialog.newGenreEdit.text()
                if newTitle != "":
                    f['title'] = newTitle
                else:
                    newTitle = f['title'].value
                if newArtist != "":
                    f['artist'] = newArtist
                else:
                    newArtist = f['artist'].value
                if newAlbum != "":
                    f['album'] = newAlbum
                else:
                    newAlbum = f['album'].value
                if newGenre != "":
                        f['genre'] = newGenre
                else:
                    newGenre = f['genre'].value
            
                updateMetadata = QtSql.QSqlQuery()
                updateMetadata.exec('''UPDATE songs SET 
                                   Title = "{}", 
                                   Artist = "{}",
                                   Album = "{}", 
                                   Genre = "{}"
                                   WHERE Filename = "{}"
                                '''.format(newTitle, newArtist, newAlbum, newGenre, filename))
                
                f.save()

        else:
            sameGenre = True
            sameArtist = True
            sameAlbumArtist = True 
            sameAlbum = True 
            firstSong = music_tag.load_file(args[0].filename)
            for arg in args:
                f = music_tag.load_file(arg.filename)
                if f['artist'].value != firstSong['artist'].value: sameArtist = False 
                if f['albumartist'].value != firstSong['albumartist'].value: sameAlbumArtist = False
                if f['album'].value != firstSong['album'].value: sameAlbum = False 
                if f['genre'].value != firstSong['genre'].value: sameGenre = False  

            dialog = EditMetadataDialog()
            if sameArtist:
                dialog.oldArtistLabel.setText(f['artist'].value)
            else:
                dialog.oldArtistLabel.setText("Mixed")
            if sameAlbumArtist:
                dialog.oldAlbumArtistLabel.setText(f['albumartist'].value)
            else:
                dialog.oldAlbumArtistLabel.setText("Mixed")
            if sameAlbum:
                dialog.oldAlbumLabel.setText(f['album'].value)
            else:
                dialog.oldAlbumLabel.setText("Mixed")
            if sameGenre:
                dialog.oldGenreLabel.setText(f['genre'].value)
            else:
                dialog.oldGenreLabel.setText("Mixed")
            


            if dialog.exec():
                newArtist = dialog.newArtistEdit.text()
                newAlbum = dialog.newAlbumEdit.text()
                newAlbumArtist = dialog.newAlbumArtistEdit.text()
                newGenre = dialog.newGenreEdit.text()
                for arg in args:
                    filename = arg.filename
                    f = music_tag.load_file(filename)
                    
                    if newArtist != "":
                        f['artist'] = newArtist
                    else:
                        newArtist = f['artist'].value
                    if newAlbum != "":
                        f['album'] = newAlbum
                    else:
                        newAlbum = f['album'].value
                    if newAlbumArtist != "":
                        f['albumartist'] = newAlbumArtist
                    else:
                        newAlbumArtist = f['albumartist'].value
                    if newGenre != "":
                        f['genre'] = newGenre
                    else:
                        newGenre = f['genre'].value
                
                    updateMetadata = QtSql.QSqlQuery()
                    updateMetadata.exec('''UPDATE songs SET 
                                    Artist = "{}",
                                    Album = "{}",
                                    AlbumArtist = "{}",
                                    Genre = "{}"
                                    WHERE Filename = "{}"
                                    '''.format(newArtist, newAlbum, newAlbumArtist, newGenre, filename))
                    f.save()

        if len(self.albumArtistList.selectedItems() ) > 0:
            self.loadDiscography(self.albumArtistList.selectedItems()[0], self.albumArtistDiscographyListWidget)
        if len(self.artistList.selectedItems() ) > 0:
            self.loadDiscography(self.artistList.selectedItems()[0], self.artistDiscographyListWidget)
        
    def createTabContextMenu(self, listWidget):
        tabContextMenu = QtWidgets.QMenu()
        selectedSongs = [SongItem(song.title, song.filename) for song in [listWidget.item(i) for i in range(listWidget.count())] ]

        #tabText = tabText.replace('\u222A', 'UNION').replace('\u2229', 'IN')
        saveTabAction = tabContextMenu.addAction("Save Tab as Playlist")
        saveTabAction.triggered.connect(lambda: self.newPlaylistDialog(*selectedSongs))

        playlistSubMenu = tabContextMenu.addMenu("Add To Playlist")
        for index, playlist in enumerate(self.playlistList):
            self.createPlaylistAction(playlist, *selectedSongs)
            playlistSubMenu.addAction(self.playlistActionList[-1])
        
        addToQueueAction = tabContextMenu.addAction("Add to Queue")
        addToQueueAction.triggered.connect(lambda: self.addToQueue(*selectedSongs))

        playNowAction = tabContextMenu.addAction("Play Now")
        playNowAction.triggered.connect(lambda: self.addToFrontOfQueueAndPlay(*selectedSongs))

        playNextAction = tabContextMenu.addAction("Play Next")
        playNextAction.triggered.connect(lambda: self.addToQueue(*selectedSongs, next = True))

        replaceQueueAction = tabContextMenu.addAction("Replace Queue")
        replaceQueueAction.triggered.connect(lambda: self.replaceQueue(*selectedSongs))

        replaceAndPlayAction = tabContextMenu.addAction("Replace Queue and Play Now")
        replaceAndPlayAction.triggered.connect(lambda: self.replaceQueueAndPlayNow(*selectedSongs))

        editMetadataAction = tabContextMenu.addAction("Edit Metadata")
        editMetadataAction.triggered.connect(lambda: self.editMetadata(*selectedSongs))

        return tabContextMenu

    def createPlaylistContextMenu(self, playlist = None):
        playlistContextMenu = QtWidgets.QMenu()

        if playlist != None:
            playlistFilename = playlist.filename
            playlistName = playlist.name
            playlistSongs = []

            with open(playlist.filename) as p: 
                songList = p.readlines() # Read song filenames into list
            for file in songList:
                if os.path.isfile(file.strip()):
                    filename = file.strip() # Remove newline character and add to library path
                    media = self.player.media_new(filename) 
                    media.parse()
                    title = media.get_meta(metaDataDict['Title'])
                    playlistSongs.append(SongItem(title, filename))

            playlistSubMenu = playlistContextMenu.addMenu("Add To Playlist")
            for index, playlist in enumerate(self.playlistList):
                self.createPlaylistAction(playlist, *playlistSongs)
                playlistSubMenu.addAction(self.playlistActionList[-1])
            newPlaylistAction = playlistSubMenu.addAction("New Playlist")
            newPlaylistAction.triggered.connect(self.newPlaylistDialog)

            renamePlaylistAction = playlistContextMenu.addAction("Rename {}".format(playlistName))
            renamePlaylistAction.triggered.connect(lambda: self.renamePlaylistDialog(playlistName, playlistFilename))

            addToQueueAction = playlistContextMenu.addAction("Add to Queue")
            addToQueueAction.triggered.connect(lambda: self.addToQueue(*playlistSongs))

            playNowAction = playlistContextMenu.addAction("Play Now")
            playNowAction.triggered.connect(lambda: self.addToFrontOfQueueAndPlay(*playlistSongs))

            playNextAction = playlistContextMenu.addAction("Play Next")
            playNextAction.triggered.connect(lambda: self.addToQueue(*playlistSongs, next = True))

            replaceQueueAction = playlistContextMenu.addAction("Replace Queue")
            replaceQueueAction.triggered.connect(lambda: self.replaceQueue(*playlistSongs))

            replaceAndPlayAction = playlistContextMenu.addAction("Replace Queue and Play Now")
            replaceAndPlayAction.triggered.connect(lambda: self.replaceQueueAndPlayNow(*playlistSongs))

            deletePlaylistAction = playlistContextMenu.addAction("Delete {}".format(playlistName))
            deletePlaylistAction.triggered.connect(lambda: self.deletePlaylistDialog(playlistName, playlistFilename))
        else:
            newPlaylistAction = playlistContextMenu.addAction("New Playlist")
            newPlaylistAction.triggered.connect(self.newPlaylistDialog)

        return playlistContextMenu       

    def setActionTriggers(self, *args):
        self.actionScan_Library.triggered.connect(lambda: self.updateDatabase(completeUpdate=True))
        self.actionReset.triggered.connect(self.reset)
        self.actionExit.triggered.connect(self.close)
        self.actionPreferences.triggered.connect(self.preferencesDialog.show)
        self.actionCurrent_Song.triggered.connect(lambda: self.editMetadata(SongItem(self.titleLabel.text(), self.currentSong)))
        self.actionCurrent_Album.triggered.connect(self.currentAlbumTrigger)
        self.actionCurrent_Artist.triggered.connect(self.currentArtistTrigger)
        self.actionAll_Songs_in_Queue.triggered.connect(lambda: self.editMetadata(*[self.activeQueue.item(i) for i in range(self.activeQueue.count())]))
        self.actionMini_Media_Player.triggered.connect(self.openMiniMediaPlayer)

    def currentAlbumTrigger(self):
        selectedSongs = []
        album = self.albumLabel.text()
        getAlbumSongsQuery = QtSql.QSqlQuery()
        getAlbumSongsQueryString = 'SELECT * FROM songs WHERE Album="{}"'.format(album)
        getAlbumSongsQuery.exec(getAlbumSongsQueryString)
        while getAlbumSongsQuery.next():
            title = getAlbumSongsQuery.value(libraryDict['Title'])
            filename = getAlbumSongsQuery.value(libraryDict['Filename'])
            selectedSongs.append( SongItem(title, filename) )

        self.editMetadata(*selectedSongs)

    def currentArtistTrigger(self):
        selectedSongs = []
        artist = self.artistLabel.text()
        getArtistSongsQuery = QtSql.QSqlQuery()
        getArtistSongsQueryString = 'SELECT * FROM songs WHERE Artist="{}"'.format(artist)
        getArtistSongsQuery.exec(getArtistSongsQueryString)
        while getArtistSongsQuery.next():
            title = getArtistSongsQuery.value(libraryDict['Title'])
            filename = getArtistSongsQuery.value(libraryDict['Filename'])
            selectedSongs.append( SongItem(title, filename) )

        self.editMetadata(*selectedSongs)

    def createPlaylistAction(self, playlist, *args):
        selectedSongs = []
        for arg in args:
            if type(arg) == SongItem:
                selectedSongs.append(arg)

        action = QtWidgets.QAction(playlist.name)
        action.triggered.connect(lambda: self.addToPlaylist(playlist, *args))
        self.playlistActionList.append(action)

    def togglePlay(self):
        if self.currentSong == None:
            if self.activeQueue.count() < 1:
                if self.currentAlbum == None:
                    albumName = "Not An Album" # Name to assign to non-album markers items inside album grid
                    while albumName == "Not An Album":
                        if self.albumListWidget.count() < 1:
                            message = "Either your music library is empty or the library database has not yet been populated. Go to 'File>Preferences' to add paths to your music. Then, click on 'File>Scan Library' to update the database."
                            QtWidgets.QMessageBox.about(self, 
                                              "Empty Library Warning", 
                                              message)
                            return
                        else:
                            index = rnd.randint(0, self.albumListWidget.count())
                            albumName = self.albumListWidget.item(index).albumName
                else:
                    albumName = self.currentAlbum
                self.loadAlbum(loadByName=True, name = albumName)
                self.loadQueueFromSongView()
                
            self.activeQueue.setCurrentRow(0)
            self.miniMediaPlayer.activeQueue.setCurrentRow(0)
            self.setMedia(self.activeQueue.currentItem().filename)
            sleep(0.5)      

        if self.mp.is_playing():
            self.mp.pause()
        else:
            self.mp.play()

    def toggleMute(self):
        if self.muted:
                self.volumeDial.setSliderPosition(self.volume) # Restore previous volume 
        else:
            self.volume = self.volumeDial.value() # Save volume value before muting
            self.volumeDial.setSliderPosition(0) # Set slider position to 0 to mute
        self.muted = not self.muted

    def toggleScrollLock(self):
        self.timeLock = not self.timeLock

    def toggleLoop(self):
        if not (self.queueLoop or self.singleSongLoop):
                self.queueLoop = True
        elif self.queueLoop:
            self.queueLoop = False
            self.singleSongLoop = True
            self.loopButton.setIcon(QtGui.QIcon(':/images/resources/images/loopone.png'))
        elif self.singleSongLoop:
            self.singleSongLoop = False
            self.loopButton.setIcon(QtGui.QIcon(':/images/resources/images/loop.png'))

    def toggleShuffle(self):
        self.shuffle = not self.shuffle
            
    def setMedia(self, filename):
        if filename != None:
            self.currentSong = filename
            self.media = self.player.media_new(filename) 
            self.media.parse() # Parse the media to obtain metadata
            self.mp.set_media(self.media)
            self.titleLabel.setText(self.media.get_meta(metaDataDict['Title']))
            self.artistLabel.setText(self.media.get_meta(metaDataDict['Artist']))
            self.albumLabel.setText(self.media.get_meta(metaDataDict['Album']))
            self.miniMediaPlayer.titleLabel.setText(self.media.get_meta(metaDataDict['Title']))
            self.miniMediaPlayer.artistLabel.setText(self.media.get_meta(metaDataDict['Artist']))
            self.miniMediaPlayer.albumLabel.setText(self.media.get_meta(metaDataDict['Album']))
            self.getAlbumArt(os.path.dirname(filename))
            self.audioScroll.setValue(0)
            self.timer.start(300)

    def setMediaAndPlay(self, song):
        if type(song) == SongItem:
            filename = song.filename
        else:
            filename = song
        if self.currentSong != None and len(self.previousSongs) == self.previousSongIndex-1:
            self.previousSongs.append(self.currentSong)
        self.setMedia(filename)
        sleep(0.5)
        self.mp.play()

    def setScrollTimeValues(self):
        for player in [self, self.miniMediaPlayer]:
            player.timeRemaining.setText( "-" + timeFormat((self.media.get_duration() - self.mp.get_time())//1000 ) )
            if self.mp.get_time() > 0:
                player.timeElapsed.setText( timeFormat(self.mp.get_time()//1000 )  )
                if not self.timeLock:
                    player.audioScroll.setSliderPosition(int(100 * self.mp.get_time()/self.media.get_duration()))
            else:
                player.timeElapsed.setText("00:00")

            if self.media.get_duration() - self.mp.get_time() < 2000: # Within last 2 seconds of song
                    self.playNextSong()

    def playPreviousSong(self):
        if self.previousSongIndex > 0:
            self.previousSongIndex -= 1
            filename = self.previousSongs[self.previousSongIndex]
        elif self.currentSong == None:
            return 
        else:
            filename = self.currentSong
                
        self.setMediaAndPlay(filename)

    def playNextSong(self):
        queueLength = self.activeQueue.count() # Get length of queue
        queueIndex = self.activeQueue.currentRow() # Get current index

        if queueLength < 1:
            return # Don't attempt to play the next song if there are no songs in the queue
        if self.previousSongIndex < len(self.previousSongs) - 1:
            self.setMediaAndPlay(self.previousSongs[self.previousSongIndex])
            self.previousSongIndex += 1
        else:
            self.previousSongIndex += 1
            if self.singleSongLoop:
                index = queueIndex
            elif self.shuffle: # Choose random integer in range of queue
                if queueLength == 1:
                    index = queueIndex
                else:
                    availableIndices = list(range(queueLength))
                    availableIndices.remove(queueIndex) # Create list of current queue indices and remove the current index
                    index = rnd.choice(availableIndices)
            elif self.queueLoop:
                index = (queueIndex + 1 ) % queueLength
            else:
                index = queueIndex + 1

            if index < queueLength: 
                self.activeQueue.setCurrentRow(index)
                self.miniMediaPlayer.activeQueue.setCurrentRow(index)
                self.setMediaAndPlay(self.activeQueue.currentItem().filename)
            else:
                self.reachedEndofQueue() 

    def reachedEndofQueue(self):
        self.mp.stop() # Stop Playing music
        self.activeQueue.setCurrentRow(0)
        self.miniMediaPlayer.activeQueue.setCurrentRow(0)
        self.previousSongs = []
        self.currentSong = None
        self.artistLabel.clear()
        self.titleLabel.clear()
        self.albumLabel.clear()
        self.albumArtLabel.clear()
        self.timer.stop()
        self.timeRemaining.setText("00:00")
        self.timeElapsed.setText("00:00")
        self.audioScroll.setSliderPosition(0)

    def songViewOnDoubleClick(self, index):
        row = index.row()
        filename = self.songViewModel.index(row,libraryDict['Filename']).data()  # Get filename from the model
        title = self.songViewModel.index(row,libraryDict['Title']).data()
        self.addToFrontOfQueueAndPlay(**{'Filename' : filename, 'Title': title})

    def loadDiscography(self, item, target):
        """Load albums associated to the item object into the album grid at target"""
        if target == self.artistDiscographyListWidget:
            label = self.artistTabArtistLabel 
            column = "Artist"
        elif target == self.albumArtistDiscographyListWidget:
            label = self.albumArtistTabAlbumArtistLabel
            column = "AlbumArtist" 
        elif target == self.genreDiscographyListWidget:
            label = self.genreTabGenreLabel
            column = "Genre"
        else:
            return
        name = item.text()
        label.setText(name)
        target.clear()

        query = QtSql.QSqlQuery()
        query.exec('SELECT * FROM songs WHERE {}="{}"'.format(column, name))
        artistAlbumList = []
        while (query.next()):
            albumName = query.value(libraryDict['Album'])
            if albumName not in artistAlbumList:
                artistAlbumList.append(albumName)
                albumDir = os.path.dirname(query.value(libraryDict['Filename']))
                albumItem = self.createAlbumItem(albumName, albumDir)
                target.addItem(albumItem)

    def massShuffle(self, column, name):
        selectedSongs = []
        query = QtSql.QSqlQuery()
        query.exec('SELECT * FROM songs WHERE {}="{}"'.format(column, name))
        while (query.next()):
            title = query.value(libraryDict['Title'])
            filename = query.value(libraryDict['Filename'])
            selectedSongs.append( SongItem(title, filename) )
        self.replaceQueueAndPlayNow(*selectedSongs)
        if not self.shuffle:
            self.shuffleButton.click()
        self.playNextSong() # Gives random song instead of first song in queue

    #######################
    #### Album Methods ####
    #######################

    def getAlbumArt(self, path):
        try:
            picList = glob(path + "/cover*") + glob(path + "/AlbumArt*") 
            albumArt = picList[0]
        except:
            albumArt = rnd.choice(self.penguins)
        pixMap = QtGui.QPixmap(albumArt)
        smallPixMap = pixMap.scaled(400, 400)
        largePixMap = pixMap.scaled(600, 600)
        self.albumArtLabel.setPixmap(smallPixMap)
        self.miniMediaPlayer.albumArtLabel.setPixmap(largePixMap)

    def generateAlbumGrid(self, order = "Album"):
        self.albumListWidget.clear()
        queryAlbumsQuery = QtSql.QSqlQuery()
        queryAlbumsQuery.exec("""SELECT *
                               FROM (
                                     SELECT *, 
                                     ROW_NUMBER() OVER(PARTITION BY Album ORDER BY Filename) AS row_number
                                     FROM songs
                                     )
                                WHERE row_number = 1
                                ORDER BY {}
                                """.format(order))
        
        currentLetter = None
        firstTime = True
        while (queryAlbumsQuery.next()):
            if firstTime and queryAlbumsQuery.value(libraryDict['Album']).strip()[0].isnumeric():
                firstTime = False
                currentLetter = '#'
                letterItem = self.createAlbumItem("Not An Album", "Not An AlbumDir", letter = currentLetter)
                letterItem.setTextAlignment(QtCore.Qt.AlignVCenter)
                self.albumListWidget.addItem(letterItem)
            albumDir = os.path.dirname(queryAlbumsQuery.value(libraryDict['Filename']))
            albumName = queryAlbumsQuery.value(libraryDict['Album'])
            potentialLetter = albumName.strip()[0]
            if not potentialLetter.isnumeric() and potentialLetter != currentLetter:
                currentLetter = potentialLetter
                letterItem = self.createAlbumItem("Not An Album", "Not An AlbumDir", letter = currentLetter)
                self.albumListWidget.addItem(letterItem)
            albumItem = self.createAlbumItem(albumName, albumDir)
            self.albumListWidget.addItem(albumItem)

    def createAlbumItem(self, albumName, albumDir, letter = None):
        albumItem = AlbumItem(albumName = albumName, letter = letter, albumDir = albumDir)
        try:
            picList = glob(albumDir + "/cover*") + glob(albumDir + "/AlbumArt*")
            albumArt = picList[0]
        except:
            
            albumArt = rnd.choice(self.penguins)
        if letter == None:
            albumItem.albumArt = albumArt
            pixMap = QtGui.QPixmap(albumArt)
            pixMap = pixMap.scaled(400, 400)
            albumIcon = QtGui.QIcon(pixMap)
            albumItem.setIcon(albumIcon)
        else:
            albumItem.setText(letter)
        return albumItem
        
    def loadAlbum(self, item = None, subset = None, subsetType = None, toQueue = False, loadByName = False, name = "Unknown"):
        if loadByName: 
            albumName = name
        else:
            letter = item.letter
            if item == None: 
                return # Return if not loading by name, but no item was provided
            albumName = item.albumName
        if albumName != "Not An Album":
            if not toQueue:
                self.songViewState = 0
                if subset == None:
                    self.songViewModel.setQuery('SELECT * FROM songs WHERE Album="{}" ORDER BY DiscAndTrack'.format(albumName))
                    self.songViewLabel.setText(albumName)
                else:
                    self.songViewModel.setQuery('SELECT * FROM songs WHERE Album="{}" AND {}="{}" ORDER BY DiscAndTrack'.format(albumName, subsetType, subset))
                    self.songViewLabel.setText(albumName + " \u2229 " + subset)
                self.songViewList.showColumn(1)
                self.songViewList.setColumnWidth(1,150)
                self.currentPlaylist = None
                self.currentAlbum = albumName
            else:
                albumQuery = QtSql.QSqlQuery()
                if subset == None:
                    albumQuery.exec('SELECT * FROM songs WHERE Album="{}" ORDER BY DiscAndTrack'.format(albumName) )
                else:
                    albumQuery.exec('SELECT * FROM songs WHERE Album="{}" AND {}="{}" ORDER BY DiscAndTrack'.format(albumName, subsetType, subset))
                songs = []
                while albumQuery.next():
                    title = albumQuery.value(libraryDict['Title'])
                    filename = albumQuery.value(libraryDict['Filename'])
                    songs.append(SongItem( title, filename))
                self.replaceQueueAndPlayNow(*songs)
        else:
            if not toQueue:
                self.songViewState = 0
                if letter == '#':
                    self.songViewModel.setQuery('SELECT * FROM songs WHERE Album LIKE "{}%" ORDER BY Album, DiscAndTrack'.format(letter))
                else:
                    self.songViewModel.setQuery('SELECT * FROM songs WHERE Album LIKE "{}%" ORDER BY Album, DiscAndTrack'.format(letter))
                self.songViewLabel.setText("Albums Beginning With {}".format(letter))
                self.songViewList.showColumn(1)
                self.songViewList.setColumnWidth(1,150)
                self.currentPlaylist = None
                self.currentAlbum = None
            else:
                albumQuery = QtSql.QSqlQuery()
                albumQuery.exec('SELECT Title, Filename FROM songs WHERE Album LIKE"{}%" ORDER BY Album, DiscAndTrack'.format(letter) )
                songs = []
                while albumQuery.next():
                    title = albumQuery.value(0)
                    filename = albumQuery.value(1)
                    songs.append(SongItem( title, filename))
                self.replaceQueueAndPlayNow(*songs)
        
    def chooseAlbumArt(self, album):
        sourceFile = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', album.albumDir, "All Files (*)")
        if sourceFile[0] != "":
            destinationFile = album.albumDir + "/AlbumArt" + os.path.splitext(sourceFile[0])[-1]
            try:
                copyfile(sourceFile[0], destinationFile) # Copy album art to album directory
            except: pass 
            else:
                os.remove(sourceFile[0])
            
            albumIcon = QtGui.QIcon(destinationFile)
            album.setIcon(albumIcon)
        self.generateAlbumGrid()

    ##########################
    #### Playlist methods ####
    ##########################

    def generatePlaylistList(self):
        self.playlistWidget.clear()
        self.playlistList = []
        for playlist in glob(playlistPath + "/*.m3u"):
            name = os.path.basename(playlist)[:-4] # Removes rest of path name and extension
            playlistItem = Playlist(name, playlist)
            self.playlistWidget.addItem(playlistItem)
            self.playlistList.append(playlistItem)
            
    def loadPlaylist(self, playlist, queue = "Song View"):
        self.currentAlbum = None
        self.currentPlaylist = playlist
        self.songViewList.hideColumn(1)
        self.songViewState = 1 # In playlist view state
        loadPlaylistQuery = 'SELECT * FROM songs WHERE Filename IN ('

        with open(playlist.filename) as p: 
            songList = p.readlines() # Read song filenames into list

        index = 0

        for file in songList:
            if os.path.isfile(file.strip()):
                filename = file.strip() # Remove newline character and add to library path
                if index == 0:
                    loadPlaylistQuery += '"{}" '.format(filename)
                else:
                    loadPlaylistQuery += ', "{}" '.format(filename)
                index += 1

        loadPlaylistQuery += ") ORDER BY Album, DiscAndTrack"
        self.songViewModel.setQuery(loadPlaylistQuery)
        self.songViewLabel.setText(playlist.name)                  

    def onPlaylistDoubleClicked(self,playlist):
        self.loadPlaylist(playlist)
        if self.songViewModel.rowCount() > 0:
            self.loadQueueFromSongViewAndPlay()

    def addToPlaylist(self, playlist, *args):
        linesToAdd = []
        for arg in args:
            if type(arg) == SongItem:
                lineToAdd = arg.filename
                linesToAdd.append(lineToAdd)
        
        with open(playlist.filename, "r") as file:
            for line in file.readlines():
                if line.strip() in linesToAdd:
                    linesToAdd.remove(line.strip())
                
        with open(playlist.filename, "a") as file:
            for line in linesToAdd:
                file.write('\n' + line)

    def updatePlaylistFileName(self, playlist):
        newFilename = playlistPath + "/{}.m3u".format(playlist.text())
        os.rename(playlist.filename, newFilename)
        playlist.filename = newFilename

    def deleteFromPlaylist(self, playlist, *args):
        linesToDelete = []
        for arg in args:
            if type(arg) == SongItem: # Check is argument passed is a song
                lineToDelete = arg.filename
                linesToDelete.append(lineToDelete)

        with open(playlist.filename, "r") as file:
            lines = file.readlines()
        with open(playlist.filename, "w") as file:
            for line in lines:
                if line.strip() not in linesToDelete:
                    file.write(line)

        self.loadPlaylist(playlist)

    def newPlaylistDialog(self, *args):
        name, ok = QtWidgets.QInputDialog().getText(self, "New Playlist",
                                     "Playlist Name:", QtWidgets.QLineEdit.Normal)
        if name and ok:
            while name in [playlist.name for playlist in self.playlistList]:
                name = name + "_" # Rename playlist if playlist name already exists

            filename = playlistPath + "/{}.m3u".format(name)
            with open(filename, "w") as file:
                for index, arg in enumerate(args):
                    if type(arg) == SongItem:
                        lineToAdd = arg.filename
                        if index == 0:
                            file.write(lineToAdd)
                        else:
                            file.write('\n' + lineToAdd)
        
        self.generatePlaylistList()

    def renamePlaylistDialog(self, playlistName, playlistFilename, *args):
        name, ok = QtWidgets.QInputDialog().getText(self, "Rename {}".format(playlistName),
                                     "New Name:", QtWidgets.QLineEdit.Normal)
        if name and ok:
            while name in [playlist.name for playlist in self.playlistList]:
                name = name + "_" # Rename playlist if playlist name already exists

            newFilename = playlistPath + "/{}.m3u".format(name)
            os.rename(playlistFilename, newFilename)
        
        self.generatePlaylistList()

    def deletePlaylistDialog(self, playlistName, filename):
        dialog = QtWidgets.QDialog()
        dialog.setModal(True)
        layout = QtWidgets.QVBoxLayout(dialog)
        dialog.setWindowTitle("Delete Playlist")
        label = QtWidgets.QLabel("Delete {}?".format(playlistName))
        label.setAlignment(QtCore.Qt.AlignCenter)
        dialog.resize(400,200)
        buttonBox = QtWidgets.QDialogButtonBox()
        layout.addWidget(label)
        layout.addWidget(buttonBox)
        buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        if dialog.exec():
            os.remove(filename)
            self.generatePlaylistList()

    #######################
    #### Artist Methods ###
    #######################

    def generateArtistList(self):
        self.artistList.clear()
        queryArtistsQuery = QtSql.QSqlQuery()
        queryArtistsQuery.exec("""SELECT * 
                               FROM (
                                     SELECT *, 
                                     ROW_NUMBER() OVER(PARTITION BY Artist ORDER BY Filename) AS row_number
                                     FROM songs
                                     )
                                WHERE row_number = 1
                                """)
        while (queryArtistsQuery.next()):
            artist = queryArtistsQuery.value(libraryDict['Artist'])
            self.addArtistItem(artist)

    def addArtistItem(self, artist):
        item = QtWidgets.QListWidgetItem(artist)
        self.artistList.addItem(item)

    def artistTabArtistLabelClick(self, event):
        self.songViewModel.setQuery('SELECT * FROM songs WHERE Artist="{}"'.format(self.artistTabArtistLabel.text()))
        self.songViewLabel.setText(self.artistTabArtistLabel.text())

    ##############################
    #### Album Artist Methods ####
    ##############################

    def generateAlbumArtistList(self):
        self.albumArtistList.clear()
        queryAlbumArtistsQuery = QtSql.QSqlQuery()
        queryAlbumArtistsQuery.exec("""SELECT * 
                               FROM (
                                     SELECT *, 
                                     ROW_NUMBER() OVER(PARTITION BY AlbumArtist ORDER BY Filename) AS row_number
                                     FROM songs
                                     )
                                WHERE row_number = 1
                                """)
        while (queryAlbumArtistsQuery.next()):
            albumArtist = queryAlbumArtistsQuery.value(libraryDict['AlbumArtist'])
            self.addAlbumArtistItem(albumArtist)

    def addAlbumArtistItem(self, albumArtist):
        item = QtWidgets.QListWidgetItem(albumArtist)
        self.albumArtistList.addItem(item)

    def albumArtistTabAlbumArtistLabelClick(self, event):
        self.songViewModel.setQuery('SELECT * FROM songs WHERE AlbumArtist="{}"'.format(self.albumArtistTabAlbumArtistLabel.text()))
        self.songViewLabel.setText(self.albumArtistTabAlbumArtistLabel.text())

    #######################
    #### Genre Methods ####
    #######################

    def generateGenreList(self):
        self.genreList.clear()
        queryGenresQuery = QtSql.QSqlQuery()
        queryGenresQuery.exec("""SELECT * 
                               FROM (
                                     SELECT *, 
                                     ROW_NUMBER() OVER(PARTITION BY Genre ORDER BY Filename) AS row_number
                                     FROM songs
                                     )
                                WHERE row_number = 1
                                """)
        while (queryGenresQuery.next()):
            genre = queryGenresQuery.value(libraryDict['Genre'])
            self.addGenreItem(genre)
            
    def addGenreItem(self, genre):
        item = QtWidgets.QListWidgetItem(genre)
        self.genreList.addItem(item)

    def onGenreClicked(self,item):
        self.songViewLabel.setText(item.text())
        self.songViewModel.setQuery('SELECT * FROM songs WHERE Genre="{}"'.format(item.text()))
        self.songViewList.hideColumn(1)
        self.songViewState = 2

    def onGenreDoubleClicked(self,item):
        self.onGenreClicked(item)
        self.loadQueueFromSongViewAndPlay()

    #######################
    #### Queue Methods ####
    #######################

    def addToQueue(self, *args, front = False, next = False, **kwargs):
        for index, arg in enumerate(args):
            if type(arg) == SongItem:
                anotherSongItem = SongItem(arg.title, arg.filename) # Copy to add to mini queue
                if front == True:
                    self.activeQueue.insertItem(index, arg)
                    self.miniMediaPlayer.activeQueue.insertItem(index, anotherSongItem)
                elif next == True:
                    self.activeQueue.insertItem(index + 1, arg)
                    self.miniMediaPlayer.activeQueue.insertItem(index + 1, anotherSongItem)
                else:
                    self.activeQueue.addItem(arg)
                    self.miniMediaPlayer.activeQueue.addItem(anotherSongItem)

        songItem = SongItem(kwargs.get('Title', 'Unknown'), 
                            kwargs.get('Filename', 'Unknown'))
        anotherSongItem = SongItem(kwargs.get('Title', 'Unknown'), 
                            kwargs.get('Filename', 'Unknown'))

        if songItem.filename != 'Unknown':
            if front == True:
                self.activeQueue.insertItem(0, songItem)
                self.miniMediaPlayer.activeQueue.insertItem(0, anotherSongItem)
            elif next == True:
                self.activeQueue.insertItem(1, songItem)
                self.miniMediaPlayer.activeQueue.insertItem(1, anotherSongItem)
            else:
                self.activeQueue.addItem(songItem)
                self.miniMediaPlayer.activeQueue.addItem(anotherSongItem)

    def removeSelectedFromQueue(self):
        for index in [item.row() for item in self.activeQueue.selectedIndexes()]:
            self.activeQueue.takeItem(index)
            self.miniMediaPlayer.activeQueue.takeItem(index)
        
    def addToFrontOfQueueAndPlay(self, *args, **kwargs):
        self.addToQueue(front = True, **kwargs)
        self.addToQueue(*[song for song in args if type(song) == SongItem], front = True)
        self.activeQueue.setCurrentRow(0)
        self.miniMediaPlayer.activeQueue.setCurrentRow(0)
        self.setMediaAndPlay(self.activeQueue.currentItem().filename)
        self.previousSongIndex = len(self.previousSongs)

    def replaceQueue(self, *args, **kwargs):
        self.activeQueue.clear()
        self.miniMediaPlayer.activeQueue.clear()
        self.addToQueue(*args, **kwargs)

    def replaceQueueAndPlayNow(self, *args, **kwargs):
        self.replaceQueue(*args, **kwargs)
        self.activeQueue.setCurrentRow(0)
        self.miniMediaPlayer.activeQueue.setCurrentRow(0)
        if self.activeQueue.currentItem() != None:
            self.setMediaAndPlay(self.activeQueue.currentItem().filename)

    def loadQueueFromSongView(self):
        self.activeQueue.clear()
        self.miniMediaPlayer.activeQueue.clear()
        for i in range(self.songViewModel.rowCount()):
            filename = self.songViewModel.index(i,libraryDict['Filename']).data()  # Get filename from the model
            title = self.songViewModel.index(i,libraryDict['Title']).data()
            self.addToQueue(**{'Filename' : filename, 'Title': title})

    def loadQueueFromSongViewAndPlay(self):
        self.loadQueueFromSongView()
        self.activeQueue.setCurrentRow(0)
        self.miniMediaPlayer.activeQueue.setCurrentRow(0)
        self.setMediaAndPlay(self.activeQueue.currentItem().filename)

    def newTab(self, tabName, *args):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        tabInt = self.musicTabs.addTab(widget, tabName)
        songList = QtWidgets.QListWidget()
        songList.installEventFilter(self)
        self.extraTabListWidgets.append(songList)
        layout.addWidget(songList)
        for arg in args:
            songList.addItem(arg)

        songList.setStyleSheet("color:white")
        songList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        songList.itemDoubleClicked.connect(lambda e: self.addToFrontOfQueueAndPlay(**{'Title' : e.title, 'Filename': e.filename}))

    def tabAdvance(self, reverse = False):
        if not reverse:
            self.musicTabs.setCurrentIndex( (self.musicTabs.currentIndex() + 1 ) % self.musicTabs.count() )
        else:
            self.musicTabs.setCurrentIndex( (self.musicTabs.currentIndex() + 1 ) % self.musicTabs.count() )

    def removeSelectedFromTab(self, listWidget):
        selectedRows = [index.row() for index in listWidget.selectedIndexes()]
        for row in selectedRows:
            listWidget.takeItem(row)

    def search(self,text):
        self.songViewLabel.setText("Search: " + text)
        queryString = '''SELECT * FROM songs WHERE 
                         Title LIKE "%{0}%" OR
                         Album LIKE "%{0}%" OR
                         Artist LIKE "%{0}%" OR
                         AlbumArtist LIKE "%{0}%" OR
                         Genre LIKE "%{0}%"
        '''.format(text)
        self.songViewModel.setQuery(queryString)

    ##################
    #### Database ####
    ##################

    def updateDatabase(self, completeUpdate = False, add = False, delete = False, paths = []):
        self.thread = QtCore.QThread()
        self.worker = DatabaseWorker(self.con)
        self.worker.moveToThread(self.thread)
        if completeUpdate:
            self.thread.started.connect(self.worker.completeUpdate)
        elif add:
            self.thread.started.connect(lambda: self.worker.addNewPaths(paths))
        elif delete:
            self.thread.started.connect(lambda: self.worker.deleteOldPaths(paths))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.loadLibraryFromDatabase)
        self.thread.start()
            
    ###########################
    #### Mini Media Player ####
    ###########################

    def setMiniMediaPlayerActions(self):
        self.miniMediaPlayer.playButton.setShortcut(QtGui.QKeySequence("Space"))
        self.miniMediaPlayer.shuffleButton.setShortcut(QtGui.QKeySequence("Ctrl+S"))
        self.miniMediaPlayer.loopButton.setShortcut(QtGui.QKeySequence("Ctrl+L"))
        self.miniMediaPlayer.nextButton.setShortcut(QtGui.QKeySequence("Ctrl+N"))
        self.miniMediaPlayer.previousButton.setShortcut(QtGui.QKeySequence("Ctrl+P"))

        self.miniMediaPlayer.playButton.clicked.connect(self.togglePlay)
        self.miniMediaPlayer.shuffleButton.clicked.connect(self.toggleShuffle)
        self.miniMediaPlayer.loopButton.clicked.connect(self.toggleLoop)
        self.miniMediaPlayer.nextButton.clicked.connect(self.playNextSong)
        self.miniMediaPlayer.previousButton.clicked.connect(self.playPreviousSong)
        self.miniMediaPlayer.audioScroll.sliderReleased.connect(lambda: self.mp.set_position(self.miniMediaPlayer.audioScroll.value()/100) )
        self.miniMediaPlayer.audioScroll.sliderPressed.connect(self.toggleScrollLock)
        self.miniMediaPlayer.audioScroll.setTracking(True)
        
        self.miniMediaPlayer.activeQueue.itemDoubleClicked.connect(self.setMediaAndPlay)

        self.miniMediaPlayer.albumArtLabel.enterEvent = self.miniMediaPlayer.onHover
        
    def openMiniMediaPlayer(self):
        self.miniMediaPlayer.show()
        self.showMinimized()

class DatabaseWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def __init__(self, sqlconnection):
        super().__init__()
        self.con = sqlconnection
        self.query = QtSql.QSqlQuery(self.con)
        self.creationMessage = """ CREATE TABLE IF NOT EXISTS songs (
            Filename text NOT NULL PRIMARY KEY,
            DiscAndTrack text,
            Title text NOT NULL,
            Album text,
            Artist text,
            Genre text,
            AlbumArtist text
            );
            """
        self.query.exec(self.creationMessage) #Ensure that the database and song table exists

    def completeUpdate(self):
        self.query.exec("DELETE From songs")
        self.addPaths(libraryPaths)
        self.finished.emit()

    def addNewPaths(self, paths):
        self.addPaths(paths)
        self.finished.emit()

    def deleteOldPaths(self, paths):
        self.deletePaths(paths)
        self.finished.emit()
    
    def deletePaths(self, paths):
        for path in paths:
                if path != "":
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file[-3:] in ["m4a", "mp3"]:
                                filename = root + "\\" + file
                                try:
                                    f = music_tag.load_file(filename)
                                    self.query.exec("DELETE * FROM songs WHERE Filename={}".format(filename))
                                except:
                                    pass

    def addPaths(self, paths):
        for path in paths:
                if path != "":
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file[-3:] in ["m4a", "mp3"]:
                                filename = root + "\\" + file
                                try:
                                    f = music_tag.load_file(filename)
                                    self.query.prepare("INSERT INTO songs(DiscAndTrack, Title, Album, Artist, Genre, AlbumArtist, Filename)" "VALUES(?,?,?,?,?,?,?)")
                                    self.query.bindValue(0, f"{f['discnumber'].value:02d}-{f['tracknumber'].value:02d}" )
                                    self.query.bindValue(1, f['title'].value)
                                    self.query.bindValue(2, f['album'].value)
                                    self.query.bindValue(3, f['artist'].value)
                                    self.query.bindValue(4, f['genre'].value)
                                    self.query.bindValue(5, f['albumartist'].value)
                                    self.query.bindValue(6, filename)
                                    self.query.exec_()
                                except:
                                    pass

class Preferences(QtWidgets.QDialog, Ui_Preferences):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.addPathButton.clicked.connect(self.addPath)
        self.pathListWidget.installEventFilter(self)
        
        
    def eventFilter(self, source, event) -> bool:
        if event.type() == QtCore.QEvent.ContextMenu and source == self.pathListWidget:
            item = self.pathListWidget.itemAt(event.pos())
            pathContextMenu = QtWidgets.QMenu()
            pathContextMenu.addAction("Remove from paths")
            pathContextMenu.triggered.connect(lambda: self.pathListWidget.takeItem(self.pathListWidget.currentRow()))
            pathContextMenu.exec(event.globalPos())
            return True

        return super().eventFilter(source, event)
    
    def addPath(self):
        item = QtWidgets.QListWidgetItem("New Path")
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.pathListWidget.addItem(item)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.pathListWidget.clear()
        for path in libraryPaths:
            if path != "":
                item = QtWidgets.QListWidgetItem(path)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                self.pathListWidget.addItem(item)

        self.playlistPathLineEdit.setText(playlistPath)
        return super().showEvent(a0)

class EditSingleSongDialog(QtWidgets.QDialog, Ui_EditSingleSong):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setModal(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

class EditMetadataDialog(QtWidgets.QDialog, Ui_EditMetadata):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setModal(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

class MiniMediaPlayer(QtWidgets.QWidget, Ui_MiniMediaPlayer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def onHover(self, event):
        print("Test")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    pfefferId = QtGui.QFontDatabase.addApplicationFont(":/fonts/resources/fonts/PfefferMediaeval.otf")
    pfefferFamily = QtGui.QFontDatabase.applicationFontFamilies(pfefferId)[0]
    pfeffer = QtGui.QFont(pfefferFamily, 10)
    app.setFont(pfeffer)
    window.showMaximized()
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()

