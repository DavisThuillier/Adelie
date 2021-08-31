# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/ThuillierAudiov2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2165, 1036)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/resources/play_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setStyleSheet("\n"
"background-color: #415466")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(-1, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_10.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.splitter = QtWidgets.QSplitter(self.layoutWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.musicTabs = QtWidgets.QTabWidget(self.splitter)
        self.musicTabs.setAutoFillBackground(False)
        self.musicTabs.setStyleSheet("QTabWidget::pane { border: 0;\n"
"}\n"
"\n"
"QTabBar::tab  {\n"
"    font-weight: bold;\n"
"    background-color: rgb(189, 189, 189);\n"
"    border: 2px solid rgb(189, 189, 189);\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    margin-left: 2px;\n"
"    margin-right: 2px;\n"
"    padding: 6px;\n"
"}\n"
"QTabBar::tab:!selected  {\n"
"    font-weight: bold;\n"
"    background-color: rgb(65, 84, 102);\n"
"    color: white;\n"
"    border: 1px solid rgb(189,189,189);\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    margin-left: 2px;\n"
"    margin-right: 2px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"")
        self.musicTabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.musicTabs.setTabsClosable(True)
        self.musicTabs.setMovable(False)
        self.musicTabs.setObjectName("musicTabs")
        self.albumTab = QtWidgets.QWidget()
        self.albumTab.setAutoFillBackground(False)
        self.albumTab.setStyleSheet("background-image: url(:/images/resources/images/deepfield.jpg)")
        self.albumTab.setObjectName("albumTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.albumTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.albumListWidget = QtWidgets.QListWidget(self.albumTab)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.albumListWidget.setFont(font)
        self.albumListWidget.setStyleSheet("\n"
"color:white")
        self.albumListWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.albumListWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.albumListWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.albumListWidget.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.albumListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.albumListWidget.setIconSize(QtCore.QSize(300, 300))
        self.albumListWidget.setFlow(QtWidgets.QListView.LeftToRight)
        self.albumListWidget.setProperty("isWrapping", True)
        self.albumListWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.albumListWidget.setGridSize(QtCore.QSize(330, 320))
        self.albumListWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.albumListWidget.setItemAlignment(QtCore.Qt.AlignCenter)
        self.albumListWidget.setObjectName("albumListWidget")
        self.verticalLayout_3.addWidget(self.albumListWidget)
        self.musicTabs.addTab(self.albumTab, "")
        self.albumArtistsTab = QtWidgets.QWidget()
        self.albumArtistsTab.setStyleSheet("")
        self.albumArtistsTab.setObjectName("albumArtistsTab")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.albumArtistsTab)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.splitter_3 = QtWidgets.QSplitter(self.albumArtistsTab)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.albumArtistList = QtWidgets.QListWidget(self.splitter_3)
        self.albumArtistList.setStyleSheet("color: white")
        self.albumArtistList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.albumArtistList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.albumArtistList.setObjectName("albumArtistList")
        self.widget = QtWidgets.QWidget(self.splitter_3)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.albumArtistTabAlbumArtistLabel = QtWidgets.QLabel(self.widget)
        self.albumArtistTabAlbumArtistLabel.setStyleSheet("font-weight: bold;\n"
"color: white")
        self.albumArtistTabAlbumArtistLabel.setText("")
        self.albumArtistTabAlbumArtistLabel.setWordWrap(True)
        self.albumArtistTabAlbumArtistLabel.setObjectName("albumArtistTabAlbumArtistLabel")
        self.horizontalLayout_5.addWidget(self.albumArtistTabAlbumArtistLabel)
        self.albumArtistShuffle = QtWidgets.QToolButton(self.widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/resources/images/shufflewhite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.albumArtistShuffle.setIcon(icon1)
        self.albumArtistShuffle.setIconSize(QtCore.QSize(40, 40))
        self.albumArtistShuffle.setObjectName("albumArtistShuffle")
        self.horizontalLayout_5.addWidget(self.albumArtistShuffle)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.albumArtistDiscographyListWidget = QtWidgets.QListWidget(self.widget)
        self.albumArtistDiscographyListWidget.setStyleSheet("")
        self.albumArtistDiscographyListWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.albumArtistDiscographyListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.albumArtistDiscographyListWidget.setIconSize(QtCore.QSize(300, 300))
        self.albumArtistDiscographyListWidget.setProperty("isWrapping", True)
        self.albumArtistDiscographyListWidget.setGridSize(QtCore.QSize(330, 320))
        self.albumArtistDiscographyListWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.albumArtistDiscographyListWidget.setObjectName("albumArtistDiscographyListWidget")
        self.verticalLayout_4.addWidget(self.albumArtistDiscographyListWidget)
        self.verticalLayout_9.addWidget(self.splitter_3)
        self.musicTabs.addTab(self.albumArtistsTab, "")
        self.genreTab = QtWidgets.QWidget()
        self.genreTab.setStyleSheet("")
        self.genreTab.setObjectName("genreTab")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.genreTab)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.splitter_5 = QtWidgets.QSplitter(self.genreTab)
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.genreList = QtWidgets.QListWidget(self.splitter_5)
        self.genreList.setStyleSheet("color: white")
        self.genreList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.genreList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.genreList.setObjectName("genreList")
        self.widget_3 = QtWidgets.QWidget(self.splitter_5)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.genreTabGenreLabel = QtWidgets.QLabel(self.widget_3)
        self.genreTabGenreLabel.setStyleSheet("font-weight: bold;\n"
"color: white")
        self.genreTabGenreLabel.setText("")
        self.genreTabGenreLabel.setWordWrap(True)
        self.genreTabGenreLabel.setObjectName("genreTabGenreLabel")
        self.horizontalLayout_6.addWidget(self.genreTabGenreLabel)
        self.genreShuffle = QtWidgets.QToolButton(self.widget_3)
        self.genreShuffle.setIcon(icon1)
        self.genreShuffle.setIconSize(QtCore.QSize(40, 40))
        self.genreShuffle.setObjectName("genreShuffle")
        self.horizontalLayout_6.addWidget(self.genreShuffle)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.genreDiscographyListWidget = QtWidgets.QListWidget(self.widget_3)
        self.genreDiscographyListWidget.setStyleSheet("")
        self.genreDiscographyListWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.genreDiscographyListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.genreDiscographyListWidget.setIconSize(QtCore.QSize(300, 300))
        self.genreDiscographyListWidget.setGridSize(QtCore.QSize(330, 320))
        self.genreDiscographyListWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.genreDiscographyListWidget.setObjectName("genreDiscographyListWidget")
        self.verticalLayout_8.addWidget(self.genreDiscographyListWidget)
        self.verticalLayout_13.addWidget(self.splitter_5)
        self.musicTabs.addTab(self.genreTab, "")
        self.ArtistsTab = QtWidgets.QWidget()
        self.ArtistsTab.setStyleSheet("")
        self.ArtistsTab.setObjectName("ArtistsTab")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.ArtistsTab)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.splitter_4 = QtWidgets.QSplitter(self.ArtistsTab)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.artistList = QtWidgets.QListWidget(self.splitter_4)
        self.artistList.setStyleSheet("color: white")
        self.artistList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.artistList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.artistList.setObjectName("artistList")
        self.widget_2 = QtWidgets.QWidget(self.splitter_4)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.artistTabArtistLabel = QtWidgets.QLabel(self.widget_2)
        self.artistTabArtistLabel.setStyleSheet("font-weight: bold;\n"
"color: white")
        self.artistTabArtistLabel.setText("")
        self.artistTabArtistLabel.setWordWrap(True)
        self.artistTabArtistLabel.setObjectName("artistTabArtistLabel")
        self.horizontalLayout_3.addWidget(self.artistTabArtistLabel)
        self.artistShuffle = QtWidgets.QToolButton(self.widget_2)
        self.artistShuffle.setText("")
        self.artistShuffle.setIcon(icon1)
        self.artistShuffle.setIconSize(QtCore.QSize(40, 40))
        self.artistShuffle.setObjectName("artistShuffle")
        self.horizontalLayout_3.addWidget(self.artistShuffle)
        self.verticalLayout_11.addLayout(self.horizontalLayout_3)
        self.artistDiscographyListWidget = QtWidgets.QListWidget(self.widget_2)
        self.artistDiscographyListWidget.setStyleSheet("")
        self.artistDiscographyListWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.artistDiscographyListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.artistDiscographyListWidget.setIconSize(QtCore.QSize(300, 300))
        self.artistDiscographyListWidget.setGridSize(QtCore.QSize(330, 320))
        self.artistDiscographyListWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.artistDiscographyListWidget.setObjectName("artistDiscographyListWidget")
        self.verticalLayout_11.addWidget(self.artistDiscographyListWidget)
        self.verticalLayout_12.addWidget(self.splitter_4)
        self.musicTabs.addTab(self.ArtistsTab, "")
        self.playlistTab = QtWidgets.QWidget()
        self.playlistTab.setStyleSheet("")
        self.playlistTab.setObjectName("playlistTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.playlistTab)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.playlistWidget = QtWidgets.QListWidget(self.playlistTab)
        self.playlistWidget.setStyleSheet("color: white")
        self.playlistWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.playlistWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.playlistWidget.setObjectName("playlistWidget")
        self.verticalLayout_5.addWidget(self.playlistWidget)
        self.musicTabs.addTab(self.playlistTab, "")
        self.allSongsTab = QtWidgets.QWidget()
        self.allSongsTab.setObjectName("allSongsTab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.allSongsTab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.allSongViewList = QtWidgets.QTreeView(self.allSongsTab)
        self.allSongViewList.setStyleSheet("QHeaderView::section\n"
"{\n"
"   background-color: rgb(189, 189, 189)\n"
"}\n"
"QTreeView::item\n"
"{\n"
"    color: white;\n"
"}\n"
"")
        self.allSongViewList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.allSongViewList.setFrameShadow(QtWidgets.QFrame.Plain)
        self.allSongViewList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.allSongViewList.setObjectName("allSongViewList")
        self.verticalLayout_7.addWidget(self.allSongViewList)
        self.musicTabs.addTab(self.allSongsTab, "")
        self.songViewWidget = QtWidgets.QWidget(self.splitter)
        self.songViewWidget.setObjectName("songViewWidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.songViewWidget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.songViewLabel = QtWidgets.QLabel(self.songViewWidget)
        self.songViewLabel.setStyleSheet("color: white;\n"
"font-weight: bold")
        self.songViewLabel.setText("")
        self.songViewLabel.setObjectName("songViewLabel")
        self.verticalLayout_6.addWidget(self.songViewLabel)
        self.songViewList = QtWidgets.QTreeView(self.songViewWidget)
        self.songViewList.setStyleSheet("QHeaderView::section\n"
"{\n"
"     background-color: rgb(189, 189, 189)\n"
"}\n"
"QTreeView::item\n"
"{\n"
"    color: white;\n"
"}")
        self.songViewList.setFrameShadow(QtWidgets.QFrame.Raised)
        self.songViewList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.songViewList.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.songViewList.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.songViewList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.songViewList.setUniformRowHeights(True)
        self.songViewList.setSortingEnabled(True)
        self.songViewList.setObjectName("songViewList")
        self.verticalLayout_6.addWidget(self.songViewList)
        self.verticalLayout_10.addWidget(self.splitter)
        self.sideBar = QtWidgets.QWidget(self.splitter_2)
        self.sideBar.setMinimumSize(QtCore.QSize(200, 0))
        self.sideBar.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.sideBar.setStyleSheet("background-color: rgb(189, 189, 189)")
        self.sideBar.setObjectName("sideBar")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sideBar)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelThuillier = QtWidgets.QLabel(self.sideBar)
        self.labelThuillier.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelThuillier.setObjectName("labelThuillier")
        self.horizontalLayout_2.addWidget(self.labelThuillier)
        self.labelAudio = QtWidgets.QLabel(self.sideBar)
        self.labelAudio.setObjectName("labelAudio")
        self.horizontalLayout_2.addWidget(self.labelAudio)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.shuffleButton = QtWidgets.QPushButton(self.sideBar)
        self.shuffleButton.setStyleSheet("QPushButton {background-color: rgb(156, 175, 169)}\n"
"QPushButton::checked {background-color: }")
        self.shuffleButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/resources/images/shuffle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shuffleButton.setIcon(icon2)
        self.shuffleButton.setIconSize(QtCore.QSize(60, 60))
        self.shuffleButton.setCheckable(True)
        self.shuffleButton.setFlat(True)
        self.shuffleButton.setObjectName("shuffleButton")
        self.horizontalLayout_7.addWidget(self.shuffleButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.previousButton = QtWidgets.QPushButton(self.sideBar)
        self.previousButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/resources/images/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previousButton.setIcon(icon3)
        self.previousButton.setIconSize(QtCore.QSize(60, 80))
        self.previousButton.setFlat(True)
        self.previousButton.setObjectName("previousButton")
        self.horizontalLayout_7.addWidget(self.previousButton)
        self.playButton = QtWidgets.QPushButton(self.sideBar)
        self.playButton.setMinimumSize(QtCore.QSize(60, 60))
        self.playButton.setMaximumSize(QtCore.QSize(100, 100))
        self.playButton.setStyleSheet("QPushButton {background-color: rgb(156, 175, 169)}\n"
"QPushButton::checked {background-color: }")
        self.playButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/resources/images/play_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon4)
        self.playButton.setIconSize(QtCore.QSize(80, 80))
        self.playButton.setCheckable(False)
        self.playButton.setAutoDefault(False)
        self.playButton.setFlat(True)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_7.addWidget(self.playButton)
        self.nextButton = QtWidgets.QPushButton(self.sideBar)
        self.nextButton.setStyleSheet("QPushButton {background-color: rgb(156, 175, 169)}\n"
"QPushButton::checked {background-color: }")
        self.nextButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/resources/images/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextButton.setIcon(icon5)
        self.nextButton.setIconSize(QtCore.QSize(60, 80))
        self.nextButton.setCheckable(False)
        self.nextButton.setFlat(True)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout_7.addWidget(self.nextButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.loopButton = QtWidgets.QPushButton(self.sideBar)
        self.loopButton.setStyleSheet("QPushButton {background-color: rgb(156, 175, 169)}\n"
"QPushButton::checked {background-color: }")
        self.loopButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/resources/images/loop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loopButton.setIcon(icon6)
        self.loopButton.setIconSize(QtCore.QSize(60, 60))
        self.loopButton.setCheckable(False)
        self.loopButton.setFlat(True)
        self.loopButton.setObjectName("loopButton")
        self.horizontalLayout_7.addWidget(self.loopButton)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.audioScroll = QtWidgets.QScrollBar(self.sideBar)
        self.audioScroll.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(156, 175, 169)")
        self.audioScroll.setMaximum(100)
        self.audioScroll.setOrientation(QtCore.Qt.Horizontal)
        self.audioScroll.setInvertedAppearance(False)
        self.audioScroll.setObjectName("audioScroll")
        self.verticalLayout.addWidget(self.audioScroll)
        self.audioTimeLayout = QtWidgets.QHBoxLayout()
        self.audioTimeLayout.setObjectName("audioTimeLayout")
        self.timeElapsed = QtWidgets.QLabel(self.sideBar)
        self.timeElapsed.setStyleSheet("font:bold")
        self.timeElapsed.setObjectName("timeElapsed")
        self.audioTimeLayout.addWidget(self.timeElapsed)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.audioTimeLayout.addItem(spacerItem3)
        self.timeRemaining = QtWidgets.QLabel(self.sideBar)
        self.timeRemaining.setStyleSheet("font:bold")
        self.timeRemaining.setObjectName("timeRemaining")
        self.audioTimeLayout.addWidget(self.timeRemaining)
        self.verticalLayout.addLayout(self.audioTimeLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.volumeDial = QtWidgets.QDial(self.sideBar)
        self.volumeDial.setMinimumSize(QtCore.QSize(200, 200))
        self.volumeDial.setMaximumSize(QtCore.QSize(200, 200))
        self.volumeDial.setMaximum(100)
        self.volumeDial.setSingleStep(1)
        self.volumeDial.setProperty("value", 100)
        self.volumeDial.setInvertedAppearance(False)
        self.volumeDial.setWrapping(True)
        self.volumeDial.setObjectName("volumeDial")
        self.gridLayout.addWidget(self.volumeDial, 0, 1, 1, 1)
        self.searchLineEdit = QtWidgets.QLineEdit(self.sideBar)
        self.searchLineEdit.setStyleSheet("font:bold")
        self.searchLineEdit.setFrame(True)
        self.searchLineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.searchLineEdit.setClearButtonEnabled(True)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.gridLayout.addWidget(self.searchLineEdit, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.sideBar)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("font:bold")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.activeQueueLabel = QtWidgets.QLabel(self.sideBar)
        self.activeQueueLabel.setStyleSheet("margin-left: 2px;\n"
"font-weight: bold;")
        self.activeQueueLabel.setObjectName("activeQueueLabel")
        self.verticalLayout_2.addWidget(self.activeQueueLabel)
        self.activeQueue = QtWidgets.QListWidget(self.sideBar)
        self.activeQueue.setStyleSheet("background-color: #415466;\n"
"color: white")
        self.activeQueue.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.activeQueue.setObjectName("activeQueue")
        self.verticalLayout_2.addWidget(self.activeQueue)
        self.titleLabel = QtWidgets.QLabel(self.sideBar)
        self.titleLabel.setStyleSheet("font:bold")
        self.titleLabel.setText("")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout_2.addWidget(self.titleLabel)
        self.artistLabel = QtWidgets.QLabel(self.sideBar)
        self.artistLabel.setText("")
        self.artistLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.artistLabel.setWordWrap(True)
        self.artistLabel.setObjectName("artistLabel")
        self.verticalLayout_2.addWidget(self.artistLabel)
        self.albumLabel = QtWidgets.QLabel(self.sideBar)
        self.albumLabel.setText("")
        self.albumLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.albumLabel.setWordWrap(True)
        self.albumLabel.setObjectName("albumLabel")
        self.verticalLayout_2.addWidget(self.albumLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.albumArtLabel = QtWidgets.QLabel(self.sideBar)
        self.albumArtLabel.setMinimumSize(QtCore.QSize(400, 400))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setBold(True)
        font.setWeight(75)
        self.albumArtLabel.setFont(font)
        self.albumArtLabel.setText("")
        self.albumArtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.albumArtLabel.setWordWrap(True)
        self.albumArtLabel.setObjectName("albumArtLabel")
        self.horizontalLayout.addWidget(self.albumArtLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 2165, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.menu_Metadata = QtWidgets.QMenu(self.menuEdit)
        self.menu_Metadata.setObjectName("menu_Metadata")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionScan_Library = QtWidgets.QAction(MainWindow)
        self.actionScan_Library.setCheckable(False)
        self.actionScan_Library.setObjectName("actionScan_Library")
        self.actionRegenerate_Album_Grid = QtWidgets.QAction(MainWindow)
        self.actionRegenerate_Album_Grid.setObjectName("actionRegenerate_Album_Grid")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionCurrent_Song = QtWidgets.QAction(MainWindow)
        self.actionCurrent_Song.setObjectName("actionCurrent_Song")
        self.actionCurrent_Album = QtWidgets.QAction(MainWindow)
        self.actionCurrent_Album.setObjectName("actionCurrent_Album")
        self.actionCurrent_Artist = QtWidgets.QAction(MainWindow)
        self.actionCurrent_Artist.setObjectName("actionCurrent_Artist")
        self.actionAll_Songs_in_Queue = QtWidgets.QAction(MainWindow)
        self.actionAll_Songs_in_Queue.setObjectName("actionAll_Songs_in_Queue")
        self.actionBackground_Color = QtWidgets.QAction(MainWindow)
        self.actionBackground_Color.setObjectName("actionBackground_Color")
        self.actionText_Color = QtWidgets.QAction(MainWindow)
        self.actionText_Color.setObjectName("actionText_Color")
        self.actionMini_Media_Player = QtWidgets.QAction(MainWindow)
        self.actionMini_Media_Player.setObjectName("actionMini_Media_Player")
        self.actionAdd_Media = QtWidgets.QAction(MainWindow)
        self.actionAdd_Media.setObjectName("actionAdd_Media")
        self.menuFile.addAction(self.actionScan_Library)
        self.menuFile.addAction(self.actionReset)
        self.menuFile.addAction(self.actionPreferences)
        self.menuFile.addAction(self.actionExit)
        self.menu_Metadata.addAction(self.actionCurrent_Song)
        self.menu_Metadata.addAction(self.actionCurrent_Album)
        self.menu_Metadata.addAction(self.actionCurrent_Artist)
        self.menu_Metadata.addAction(self.actionAll_Songs_in_Queue)
        self.menuEdit.addAction(self.menu_Metadata.menuAction())
        self.menuView.addAction(self.actionMini_Media_Player)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        self.musicTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Thuillier Audio"))
        self.musicTabs.setTabText(self.musicTabs.indexOf(self.albumTab), _translate("MainWindow", "Albums"))
        self.albumArtistShuffle.setText(_translate("MainWindow", "..."))
        self.musicTabs.setTabText(self.musicTabs.indexOf(self.albumArtistsTab), _translate("MainWindow", "Album Artists"))
        self.genreShuffle.setText(_translate("MainWindow", "..."))
        self.musicTabs.setTabText(self.musicTabs.indexOf(self.genreTab), _translate("MainWindow", "Genres"))
        self.musicTabs.setTabText(self.musicTabs.indexOf(self.ArtistsTab), _translate("MainWindow", "Artists"))
        self.musicTabs.setTabText(self.musicTabs.indexOf(self.playlistTab), _translate("MainWindow", "Playlists"))
        self.musicTabs.setTabText(self.musicTabs.indexOf(self.allSongsTab), _translate("MainWindow", "Songs"))
        self.labelThuillier.setText(_translate("MainWindow", "3yJj¸`B6F"))
        self.labelAudio.setText(_translate("MainWindow", " yD2`B~N"))
        self.timeElapsed.setText(_translate("MainWindow", "00:00"))
        self.timeRemaining.setText(_translate("MainWindow", "00:00"))
        self.searchLineEdit.setPlaceholderText(_translate("MainWindow", "Search..."))
        self.label.setText(_translate("MainWindow", "Volume"))
        self.activeQueueLabel.setText(_translate("MainWindow", "Queue"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menu_Metadata.setTitle(_translate("MainWindow", "&Metadata"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionScan_Library.setText(_translate("MainWindow", "Scan Library"))
        self.actionRegenerate_Album_Grid.setText(_translate("MainWindow", "Regenerate Album Grid"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
        self.actionCurrent_Song.setText(_translate("MainWindow", "Current Song"))
        self.actionCurrent_Album.setText(_translate("MainWindow", "Current Album"))
        self.actionCurrent_Artist.setText(_translate("MainWindow", "Current Artist"))
        self.actionAll_Songs_in_Queue.setText(_translate("MainWindow", "All Songs in Queue"))
        self.actionBackground_Color.setText(_translate("MainWindow", "Background Color"))
        self.actionText_Color.setText(_translate("MainWindow", "Text Color"))
        self.actionMini_Media_Player.setText(_translate("MainWindow", "Mini Media Player"))
        self.actionAdd_Media.setText(_translate("MainWindow", "Add Media for Session"))
import resources_rc
