# codethis

python based GUI for coding audio files (still in beta stage)

The script assumes files to be coded live in one directory (to be selected by user when script runs).
Outputs a csv file (name and location specified by user when script runs) with two columns (file name, coding)

System dependencies: <a href="http://sox.sourceforge.net/sox.html">sox</a> (for playing audio)

python dependencies: <a href="https://pandas.pydata.org/">pandas</a>

Unfortunately due to a <a href="https://bugs.python.org/issue37833">tkinter bug on macOS</a> the script currently only works on Linux.
