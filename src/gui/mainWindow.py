__author__ = 'Przemek'

from Tkinter import *
#from Tkinter import ttk
import ttk

class mainWindow():

    root = Tk()
    root.title("Simulated annealing")

    mainframe = ttk.Frame(root, padding="20 20 20 20", width=200, height=100)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    entryframe = ttk.Frame(root, padding="20 20 20 20", width=200, height=100)
    entryframe.grid(column=0, row=3, sticky=(N, W, E, S))
    entryframe.columnconfigure(0, weight=1)
    entryframe.rowconfigure(0, weight=1)

    buttonsframe = ttk.Frame(root, padding="20 20 20 20", width=200, height=100)
    buttonsframe.grid(column=0, row=6, sticky=(N, W, E, S))
    buttonsframe.columnconfigure(0, weight=1)
    buttonsframe.rowconfigure(0, weight=1)


    entry1 = StringVar()
    entry2 = StringVar()
    entry3 = StringVar()

    entry1 = ttk.Entry(entryframe, width=7, textvariable=entry1)
    entry1.grid(column=1, row=0, sticky=(W, E))

    entry2 = ttk.Entry(entryframe, width=7, textvariable=entry2)
    entry2.grid(column=1, row=1, sticky=(W, E))

    entry3 = ttk.Entry(entryframe, width=7, textvariable=entry3)
    entry3.grid(column=1, row=2, sticky=(W, E))

    ttk.Label(mainframe, text="TASK OPTIMIZATION").grid(column=1, row=1, sticky=N, columnspan=3)
    ttk.Label(entryframe, text="parameter 1").grid(column=0, row=0, sticky=E)
    ttk.Label(entryframe, text="parameter 2").grid(column=0, row=1, sticky=E)
    ttk.Label(entryframe, text="parameter 3").grid(column=0, row=2, sticky=E)

    ttk.Button(buttonsframe, text="Start").grid(column=1, row=5, sticky=W)
    ttk.Button(buttonsframe, text="Quit", command=root.quit).grid(column=3, row=5, sticky=W)



    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)




    root.mainloop()
