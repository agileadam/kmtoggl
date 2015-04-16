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

# Setup

## Toggl configuration

1. Create `~/.togglrc` file: (use your own token)<pre>[toggl]<br/>token=e0926359d8c73bbe7ab136d042530d9a</pre>

## KMLink URL Handler

You will need to have KMLink working. Please follow just the "Installation" instructions here: http://agileadam.com/2015/03/kmlink/

## Keyboard Maestro Macro

This repository contains a macro that you should be able to import into Keyboard Maestro.

1. Import the "start_ac_toggl_timer.kmmacros" macro file into Keyboard Maestro
1. Update the "Execute Shell Script" to point to your copy of kmtoggl.py

## Bookmarklet

1. Copy this string into a text editor:
    1. `javascript:(function()%7Bfunction callback()%7B(function(%24)%7Bvar jQuery%3D%24%3Bvar pathArray %3D window.location.pathname.split( '%2F' )%3Bproject %3D ""%3Bif (pathArray%5B2%5D) %7Bproject %3D pathArray%5B2%5D%3B%7Dvar time_description %3D "General"%3Bvar task_num %3D ""%3Bif (pathArray%5B3%5D %3D%3D 'tasks' %26%26 pathArray%5B4%5D) %7Bvar time_description %3D %24('%23breadcrumbs li%3Anth-child(4) a').text()%3Btask_num %3D pathArray%5B4%5D%3B%7Dvar final_url %3D "kmlink%3A%2F%2Fcom.apple.Applescript.KMLink%3Fmacro%3D676619D3-CE3A-4DE0-A721-C8FD5025C50D%26project%3D" %2B encodeURIComponent(project) %2B "%26time_description%3D" %2B encodeURIComponent(time_description) %2B "%26task_num%3D" %2B task_num%3Bwindow.location %3D final_url%7D)(jQuery.noConflict(true))%7Dvar s%3Ddocument.createElement("script")%3Bs.src%3D"https%3A%2F%2Fajax.googleapis.com%2Fajax%2Flibs%2Fjquery%2F1.7.1%2Fjquery.min.js"%3Bif(s.addEventListener)%7Bs.addEventListener("load"%2Ccallback%2Cfalse)%7Delse if(s.readyState)%7Bs.onreadystatechange%3Dcallback%7Ddocument.body.appendChild(s)%3B%7D)()`
1. Change "676619D3-CE3A-4DE0-A721-C8FD5025C50D" to the UID of your imported Keyboard Maestro macro.
    1. You get the UID of the macro by highlighting it in Keyboard Maestro, then using the menu item "Edit > Copy As > Copy UID"
1. Create a new bookmark (probably should go in your bookmarks toolbar) with the javascript text you edited above as the path/url.

# Usage

1. Click the bookmark. This will pass variables to Keyboard Maestro, which will fire off the python script to create the project (if needed) and start the timer.
1. Check if the timer started (either in Toggl Desktop or on the toggl website).

If a timer is already running when you start a new one, the running timer will stop and the new one will start.