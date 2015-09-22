# WARNING:

Feel free to use this script, but it's not very polished. I've published it for a few co-workers and myself.

# Requirements:

1. Requests - http://docs.python-requests.org/en/latest/
1. Keyboard Maestro
1. KMLink URL Handler (link/instructions below)
1. A working Toggl account with a working API token

# Intro:

AciveCollab is a time management system. ActiveCollab has projects, and projects have tasks within them.

Toggl is a web-based time tracking application.

Keyboard Maestro is an automation application for the Mac.

Using this python script, a bookmarklet, and Keyboard Maestro, you can one-click start a Toggl timer for a task
or project in ActiveCollab. Some advantages to the bookmarklet are:

1. Automatically creates the ActiveCollab project in Toggl (saving several steps) if it doesn't already exist
1. Time entries it creates are compatible with https://github.com/agileadam/actoggltimeimport
1. Makes it almost effortless to track your time on ActiveCollab projects and tasks
1. Includes inbox.google.com integration to start a timer from Active Collab emails

# Setup

## Toggl configuration

1. Create `~/.togglrc` file: (use your own token)<pre>[toggl]<br/>token=e0926359d8c73bbe7ab136d042530d9a</pre>

## KMLink URL Handler

You will need to have KMLink working. Please follow just the "Installation" instructions here: http://agileadam.com/2015/03/kmlink/

## Keyboard Maestro Macro

This repository contains a macro that you should be able to import into Keyboard Maestro.

1. Import the `start_ac_toggl_timer.kmmacros` macro file into Keyboard Maestro
1. Update the "Execute Shell Script" to point to your copy of `kmtoggl.py`

## Bookmarklet

1. Copy this string into a text editor:
    1. `javascript:(function()%7Bfunction%20callback()%7B(function(%24)%7Bvar%20jQuery%3D%24%3Bvar%20cur_url%20%3D%20window.location.host%3Bvar%20href%3D''%3Bvar%20project%20%3D%20''%3Bvar%20task_num%20%3D%20''%3Bvar%20task_description%20%3D%20'General'%3Bif%20(cur_url%20%3D%3D%20'projects.twsgrp.com')%20%7Bhref%20%3D%20window.location%3Bvar%20pathArray%20%3D%20window.location.pathname.split(%20'%2F'%20)%3Bif%20(pathArray%5B2%5D)%20%7Bproject%20%3D%20pathArray%5B2%5D%3B%7Dif%20(pathArray%5B3%5D%20%3D%3D%20'tasks'%20%26%26%20pathArray%5B4%5D)%20%7Btask_description%20%3D%20%24('%23breadcrumbs%20li%3Anth-child(4)%20a').text()%3Btask_num%20%3D%20pathArray%5B4%5D%3B%7D%7Delse%20if%20(cur_url%20%3D%3D%20'inbox.google.com')%20%7Bvar%20links%20%3D%20%24('a%5Bhref%5E%3D%22https%3A%2F%2Fprojects.twsgrp.com%22%5D')%3Btask_description%20%3D%20links.first().text().replace(%2F(%5Cr%5Cn%7C%5Cn%7C%5Cr)%2Fgm%2C%22%22)%3Bhref%20%3D%20links.first().attr('href')%3Bvar%20pathArray%20%3D%20href.split(%20'%2F'%20)%3Bif%20(pathArray%5B4%5D)%20%7Bproject%20%3D%20pathArray%5B4%5D%3B%7Dif%20(pathArray%5B5%5D%20%3D%3D%20'tasks'%20%26%26%20pathArray%5B6%5D)%20%7Btask_num%20%3D%20pathArray%5B6%5D%3B%7D%7Dvar%20final_url%20%3D%20%22kmlink%3A%2F%2Fcom.apple.Applescript.KMLink%3Fmacro%3D676619D3-CE3A-4DE0-A721-C8FD5025C50D%26project%3D%22%20%2B%20encodeURIComponent(project)%20%2B%20%22%26time_description%3D%22%20%2B%20encodeURIComponent(task_description)%20%2B%20%22%26task_num%3D%22%20%2B%20task_num%3Bwindow.location%20%3D%20final_url%7D)(jQuery.noConflict(true))%7Dvar%20s%3Ddocument.createElement(%22script%22)%3Bs.src%3D%22https%3A%2F%2Fajax.googleapis.com%2Fajax%2Flibs%2Fjquery%2F1.7.1%2Fjquery.min.js%22%3Bif(s.addEventListener)%7Bs.addEventListener(%22load%22%2Ccallback%2Cfalse)%7Delse%20if(s.readyState)%7Bs.onreadystatechange%3Dcallback%7Ddocument.body.appendChild(s)%3B%7D)()`
1. Change `676619D3-CE3A-4DE0-A721-C8FD5025C50D` to the UID of your imported Keyboard Maestro macro.
    1. You get the UID of the macro by highlighting it in Keyboard Maestro, then using the menu item *Edit > Copy As > Copy UID*
1. Create a new bookmark (probably should go in your bookmarks toolbar) with the javascript text you edited above as the path/url.

# Usage

1. Click the bookmark (from any Active Collab page, or while viewing Active Collab emails in inbox.google.com). This will pass variables to Keyboard Maestro, which will fire off the python script to create the project (if needed) and start the timer.
1. Check if the timer started (either in Toggl Desktop or on the toggl website).

If a timer is already running when you start a new one, the running timer will stop and the new one will start.
