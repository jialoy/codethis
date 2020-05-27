#!/usr/bin/env python
 
################################################
## GUI script for coding/annotating sound files
## the script assumes files to be coded live in
## one directory (to be selected by user when
## script runs)
##---------------------------------------------
## sound file extension can be modified in
## line 162 of the script
##---------------------------------------------
## output is a csv file (name and location
## specified by user when script runs)
## with two columns (file name, coding)
##---------------------------------------------
## dependencies: sox (for audio playing)
## python dependencies: pandas (for csv stuff)
################################################
 
import glob
import os
import subprocess
import threading
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import pandas as pd

class GlobalVars:
    def __init__(self):
        self.home_path = os.path.expanduser("~")
    
    def get_dir_path(self, title_text):
        # GUI to get directory path
        root = tk.Tk()
        root.withdraw()
        self.dir_path = askdirectory(initialdir=self.home_path,
                                     title=title_text)
        root.destroy()
        return self.dir_path
    
    def create_csv(self, output_dir):
        # output_dir: full path to dir where csv should be saved
        root = tk.Tk()
        
        scrW, scrH = root.winfo_screenwidth(), root.winfo_screenheight()
        winW, winH = 300, 150    # tk window width and height
        winX, winY = int(scrW/2-winW/2), int(scrH/2-winH/2)    # tk window position on screen
        buttonW, buttonH = 100, 30    # ok button width and height
        buttonX, buttonY = int(winW/2-buttonW/2), int(winH/2+buttonH/2)    # ok button position in window
        promptW, promptH = 180, 20    # user input textarea width and height
        promptX, promptY = int(winW/2-promptW/2), int(winH/2-promptH)    # user input textarea position in window
        
        root.geometry("{}x{}+{}+{}".format(winW, winH, winX, winY))    # window width & height and window pos (x and y) on screen
        label = tk.Label(root, text="Enter output csv file name")
        prompt = tk.Entry(root, bd=1)
        prompt.focus_set()    # set focus to prompt (blinking cursor appears by default)
        
        def get_file_name():
            self.file_name = prompt.get() + ".csv"
            root.destroy()
        
        ok_button = tk.Button(root, text="OK", command=get_file_name)
        ok_button.place(x=buttonX, y=buttonY, width=buttonW, height=buttonH)
        root.bind("<Return>", lambda event=None: ok_button.invoke())    # bind return key to ok button
        prompt.place(x=promptX, y=promptY, width=promptW, height=promptH)
        label.pack()
        root.mainloop()
        
        df = pd.DataFrame(columns=["file_name", "coding"])
        
        if self.file_name:
            self.output_file_path = "{}/{}".format(output_dir, self.file_name)
            with open(self.output_file_path, "w") as f:
                df.to_csv(f, index=False)
                
            return self.output_file_path
        
        else:
            print ("file name does not exist")
    
    def get_all_sound_files(self, recs_dir_path, file_ext):
        # get all sound files in directory as list
        sound_file_list = sorted(glob.glob("{}/*{}".format(recs_dir_path, file_ext)))
        return sound_file_list
    
    def open_output_df(self):
        # open output csv as pandas df
        return pd.read_csv(self.output_file_path)
    
    def completed_dialog(self, recs_dir_path):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Information", "Finished coding all audio files in {}".format(recs_dir_path))
        root.destroy()

class SoundFile:
    """Functions associated with instance of a wav file
    """
    def __init__(self, file_name):
        self.file_name = file_name
    
    def play(self):
        # subprocess call to play sound file in background
        subprocess.Popen("play {} tempo 1.0".format(self.file_name), shell=True)

    def coding_box(self):
        # widget for coding sound file
        root = tk.Tk()
        
        scrW, scrH = root.winfo_screenwidth(), root.winfo_screenheight()
        winW, winH = 300, 150
        winX, winY = int(scrW/2-winW/2), int(scrH/2-winH/2)
        promptW, promptH = 180, 20
        promptX, promptY = int(winW/2-promptW/2), int(winH/2-promptH)
        buttonW, buttonH = 80, 30
        ok_buttonX, replay_buttonX, buttonY = int(0.35*winW-buttonW/2), int(0.65*winW-buttonW/2), int(winH/2+buttonH/2)
        
        def get_coding():
            self.coding = prompt.get()
            if self.coding:
                self.coded = True
                root.destroy()
            else:
                leave_blank = messagebox.askyesno("Question", "Are you sure you don't want to enter a value?")
                if leave_blank==True:
                    self.coding = ""
                    root.destroy()
            print("coding: {}".format(self.coding))
        
        root.geometry("{}x{}+{}+{}".format(winW, winH, winX, winY))
        label = tk.Label(root, text="Enter coding or replay audio")
        prompt = tk.Entry(root, bd=1)
        prompt.focus_set()
        ok_button = tk.Button(root, text="OK", command=get_coding)
        replay_button = tk.Button(root, text="Replay", command=self.play)
        
        prompt.place(x=promptX, y=promptY, width=promptW, height=promptH)
        label.pack()
        ok_button.place(x=ok_buttonX, y=buttonY, width=buttonW, height=buttonH)
        replay_button.place(x=replay_buttonX, y=buttonY, width=buttonW, height=buttonH)
        root.bind("<Return>", lambda event=None: ok_button.invoke())
        
        playing = threading.Thread(target=self.play)
        playing.start()
        root.mainloop()
    
    def append_to_df(self, output_file_path):
        # append file name and coding for each trial to output csv
        df = pd.read_csv(output_file_path)
        stripped_file_name = os.path.basename(self.file_name)
        data_to_append = [[stripped_file_name, self.coding]]
        col_names = list(df.columns)
        df = df.append(pd.DataFrame(data_to_append, columns=col_names), ignore_index=True)
        df.to_csv(output_file_path, index=False)
    

def main():
    global_vars = GlobalVars()
    recs_dir = global_vars.get_dir_path("Select directory of sound files to code")
    output_dir = global_vars.get_dir_path("Select directory where output csv is saved")
    all_sound_files = global_vars.get_all_sound_files(recs_dir, ".mp3")
    output_file_path = global_vars.create_csv(output_dir)
    df = global_vars.open_output_df()
    
    for i in range(len(all_sound_files)):
        curr_sound_file = SoundFile(all_sound_files[i])
        curr_sound_file.coding_box()
        curr_sound_file.append_to_df(output_file_path)
        if i==len(all_sound_files)-1:
            global_vars.completed_dialog(recs_dir)

if __name__ == '__main__':
    main()
