#!/usr/bin/env python3
"""
ThemOmatic: Them(e) + (Aut)omatic
Simple script to automatically change GTK+3 themes (tested on Ubuntu Budgie 20.04) & wallpapers to either dark or light (or you may use your own themes)
changes occur twice a day (default : 7am & 8pm)
Author: mBilG
Date: 15 Jun 2020
"""
import schedule
import time
import threading
import sys, os
import gi
from gi.repository import Gio
gi.require_version('Notify', '0.7')
from gi.repository import Notify

#################################################################
#      Change these to your own themes, wallpapers & times      #
#################################################################
dark_theme = 'Mcata-dark'
light_theme = 'Mcata-light'
dark_wallpaper = 'file://' + os.path.abspath('') + '/dark.png'
light_wallpaper = 'file://' + os.path.abspath('') + '/light.png'        
day_start = "07:00"    # Use the same time format! 08:00 & 14:00
night_start = "20:00"  # Use the same time format! 08:00 & 14:00
##################################################################

def main():

    # Multithread to run 2 schedules (1-@7AM; 2-@8PM)
    # Copied from:
    # https://schedule.readthedocs.io/en/stable/faq.html#how-to-execute-jobs-in-parallel
    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()
    
    # Fn to create notification when Theme changes
    def notif(th):
        # One time initialization of libnotify
        Notify.init("Theme Changer")
        # Create the notification object
        summary = 'Theme Changed'
        body = "Theme changed to " + th
        notification = Notify.Notification.new(summary,body)
        notification.show()

    # Get the current theme in use
    def get_current_theme():
        gsettings = Gio.Settings.new('org.gnome.desktop.interface')
        return gsettings['gtk-theme']
    
    
    def job_dark():   # Fn to change to night theme & dark wallpaper
        gsettings = Gio.Settings.new('org.gnome.desktop.interface')
        gsetbackg = Gio.Settings.new('org.gnome.desktop.background')
        gsettings['gtk-theme'] = dark_theme 
        gsetbackg['picture-uri'] = dark_wallpaper
        gsetbackg['picture-options'] = 'spanned'
        gsetbackg.apply()
        notif("Dark") # Show notification on screen

    def job_light():   # Fn to change to day theme & light wallpaper
        gsettings = Gio.Settings.new('org.gnome.desktop.interface')
        gsetbackg = Gio.Settings.new('org.gnome.desktop.background')
        gsettings['gtk-theme'] = light_theme
        gsetbackg['picture-uri'] = light_wallpaper
        gsetbackg['picture-options'] = 'spanned'
        gsetbackg.apply() # Apply wallpaper
        notif("Light") # Show notification on screen


    def main_job():
        thistime = time.localtime() # check local time
        t = thistime[3] # 3 for hour, 4 for min, 5 for sec > print "thistime" for more details
        day_int = int(day_start[0:2]) # get hour value for day time start
        night_int = int(night_start[0:2]) # get hour value for night time start
        if t >= day_int and t < night_int: # check daytime
            theme = get_current_theme()
            if theme != light_theme: # check that theme is not set 
                job_light() # apply light theme & wall papaer
        
        else: # night time
            theme = get_current_theme()
            if theme != dark_theme:
                job_dark() # apply dark theme & wallpapaer
    
    main_job() # run job once to update theme & wallpaper @ login
    schedule.every().day.at(day_start).do(run_threaded, main_job) # schedule change for 7AM
    schedule.every().day.at(night_start).do(run_threaded, main_job) # schedule change for 8PM
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
