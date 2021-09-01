# Adélie
## Overview
Adélie is a desktop music player written in Python with a UI designed using Qt. This goal of this project is to produce a music player and library management system with a simple UI for individuals with large libraries. The most notable feature of Adélie is the introduction of tabs as an intermediate step between queueing and playlist creation. Playlists in Adélie are permanent objects saved as .m3u files in the users's playlist directory. Tabs are temporary objects: lists of songs that are created and editable during a single session but are not saved when the application is closed. They allow for the user to 
* build and rearrange lists of songs for a future queue or playlist
* save an existing subset of the library in an easy to access location when switching views
* group many objects from a library for mass metadata editing
These features all target users with large music libraries who want flexibility in playing their music. 

The interface is straightforward and most functionality is provided through the use of context menus. Right-click on any music object or title on the screen to see a list of available actions. There are also a number of keyboard shortcuts:
* *Space* Toggle play
* *Ctrl+M* Toggle mute
* *Ctrl+N* Play next song
* *Ctrl+P* Play previous song
* *Ctrl+S* Toggle shuffle
* *Ctrl+L* Toggle looping (off/queue/single)
* *Ctrl+U* Scan for new songs and rebuild library database
* *Ctrl+Q* Exit
As new features are added, a manual will be provided in future releases for reference. 
## Installation
If you are running 64-bit Windows, the executable for the most recent release can be found under [Dist]. Alternatively, for Mac or Linux users, the application can be assembled as an executable using PyInstaller. Instructions pending.
<img src="UI/resources/images/penguin_cartoon.png" width="100">
