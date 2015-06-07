__author__ = 'Przemek'

from Tkinter import *
#from Tkinter import ttk
import ttk

class mainWindow():

    root = Tk()
    root.title("Simulated annealing")


#----- Frames
    mainframe = ttk.Frame(root, padding="20 20 20 20", width=200, height=100)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    entryframe = ttk.Frame(root, padding="20 20 20 20", width=200, height=100)
    entryframe.grid(column=0, row=1, sticky=(N, W, E, S))
    entryframe.columnconfigure(0, weight=1)
    entryframe.rowconfigure(0, weight=1)

    checkbuttonframe = ttk.Frame(root, padding="20 20 20 20", width=200, height=100)
    checkbuttonframe.grid(column=0, row=2, sticky=(N, W, E, S))
    checkbuttonframe.columnconfigure(0, weight=1)
    checkbuttonframe.rowconfigure(0, weight=1)

    buttonsframe = ttk.Frame(root, padding="20 20 20 20", width=200, height=100)
    buttonsframe.grid(column=0, row=3, sticky=(N, W, E, S))
    buttonsframe.columnconfigure(0, weight=1)
    buttonsframe.rowconfigure(0, weight=1)



#----- Entry
    entry1 = StringVar()
    entry2 = StringVar()
    entry3 = StringVar()

    entry1 = ttk.Entry(entryframe, width=7, textvariable=entry1)
    entry1.grid(column=1, row=0, sticky=(W, E))
    entry1.insert(1, "50")

    entry2 = ttk.Entry(entryframe, width=7, textvariable=entry2)
    entry2.grid(column=1, row=1, sticky=(W, E))
    entry2.insert(1, "50")

    entry3 = ttk.Entry(entryframe, width=7, textvariable=entry3)
    entry3.grid(column=1, row=2, sticky=(W, E))
    entry3.insert(1, "0.7")


#----- Labels
    ttk.Label(mainframe, text="TASK OPTIMIZATION").grid(column=0, row=1, sticky=W, columnspan=2)
    ttk.Label(entryframe, text="Number of cycles").grid(column=0, row=0, sticky=W, padx=20)
    ttk.Label(entryframe, text="Trials per cycle").grid(column=0, row=1, sticky=W, padx=20)
    ttk.Label(entryframe, text="Initial prob. worse solution").grid(column=0, row=2, sticky=W, padx=20)

#----- Radiobuttons
    var = IntVar()
    linearly = Radiobutton(checkbuttonframe, text="linearly", variable=var, value=1)
    linearly.pack( anchor = W )

    logarithmically = Radiobutton(checkbuttonframe, text="logarithmically", variable=var, value=2)
    logarithmically.pack( anchor = W )

    geometrically = Radiobutton(checkbuttonframe, text="geometrically", variable=var, value=3)
    geometrically.pack( anchor = W)

    linearly.grid(column=0, row=3)
    logarithmically.grid(column=1, row=3)
    geometrically.grid(column=2, row=3)

#----- Buttons
    ttk.Button(buttonsframe, text="Start").grid(column=1, row=5, sticky=W)
    ttk.Button(buttonsframe, text="Quit", command=root.quit).grid(column=3, row=5, sticky=W)



    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)




    root.mainloop()
