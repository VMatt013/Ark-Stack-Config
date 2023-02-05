import tkinter as tk
import os
from tkinter import TclError, ttk
from tkinter.messagebox import showerror, showwarning, showinfo


itemID = [
    ("PrimalItemConsumable_RawPrimeMeat","Raw Prime Meat"),
    ("PrimalItemConsumable_CookedPrimeMeat","Cooked Prime Meat"),
    ("PrimalItemConsumable_RawPrimeMeat_Fish","Raw Prime Fish Meat"),
    ("PrimalItemConsumable_CookedPrimeMeat_Fish","Cooked Prime Fish Meat"),
    ("PrimalItemConsumable_RawMutton","Raw Mutton"),
    ("PrimalItemConsumable_CookedLambChop","Cooked Lamb Chop"),
    ("PrimalItemConsumable_Honey","Giant Bee Honey"),
    ("PrimalItemResource_Sap","Sap"),
]

def ResetStacks(isBaseStack,isInvidStack):
    if isInvidStack:
        Output = []
        with open("ShooterGame/Saved/Config/WindowsNoEditor/Game.ini", "r") as File:
            for line in File.readlines():
                if line.count("ConfigOverrideItemMaxQuantity") > 0 or line == "\n":
                    pass
                else:
                    Output.append(line)
        with open("ShooterGame/Saved/Config/WindowsNoEditor/Game.ini", "w") as File:
            File.write("".join(Output))
    
    if isBaseStack:
        Output = []
        with open("ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini", "r") as File:
            for line in File.readlines():
                if line.count("ItemStackSizeMultiplier") > 0:
                    Output.append(f"ItemStackSizeMultiplier=1\n")
                else:
                    Output.append(line)
        with open("ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini", "w") as File:
            File.write("".join(Output))

def GenerateStackOverride(isBaseStack,isInvidStack,BaseStackValue,InvidStackValue):
    global itemID,Items
    invidValue = GetEntry(InvidStackValue)
    Output = []

    if isInvidStack:
        ResetStacks(False,True)
        for item,id in zip(Items,itemID):
            if item.get():
                with open("ShooterGame/Saved/Config/WindowsNoEditor/Game.ini", "a") as File:
                    File.write(f'\nConfigOverrideItemMaxQuantity=(ItemClassString="{id[0]}_C",Quantity=(MaxItemQuantity={invidValue}, bIgnoreMultiplier=true))')
    if isBaseStack:
        ResetStacks(True,False)
        with open("ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini", "r") as File:
            for line in File.readlines():
                if line.count("ItemStackSizeMultiplier") > 0:
                    Output.append(f"ItemStackSizeMultiplier={GetEntry(BaseStackValue)}\n")
                else:
                    Output.append(line)
        with open("ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini", "w") as File:
            File.write("".join(Output))
    showinfo("Info", "Config has been generated.")
            
def GetEntry(Entry,default=1):
    Multiplier = Entry.get()
    if Multiplier == "":
        return default
    else:
        return Multiplier

def createMainFrame(container):
    Frame = ttk.Frame(container)
    Frame.columnconfigure(0, weight=1)
    Frame.columnconfigure(1, weight=1)
    Frame.columnconfigure(2, weight=2)

    BaseStackValue = tk.BooleanVar(value=True)
    InvidStackValue = tk.BooleanVar(value=True)

    buttonGenerate = tk.Button(Frame,text="Generate Stack Configs",width=20,height=2,bd=3,bg="grey85",fg="black",command=lambda: (GenerateStackOverride(BaseStackValue.get(),InvidStackValue.get(),entryBaseStack,entryInvidStack)))
    buttonGenerate.grid(column=2,row=0,padx=5, pady=5)
    buttonClean = tk.Button(Frame,text="Reset",width=20,height=2,bd=3,bg="grey85",fg="black",command=lambda: (showinfo("Reset", "Config has been reset."),ResetStacks(BaseStackValue.get(),InvidStackValue.get())))
    buttonClean.grid(column=2,row=1,padx=5, pady=5)

    labelBaseStack= tk.Label(Frame,text="Base Stack Multiplier:",fg="black",width=18,height=1)
    labelBaseStack.grid(column=0,row=0,pady=5)
    labelInvidStack= tk.Label(Frame,text="Invidual Stack Size:",fg="black",width=18,height=1)
    labelInvidStack.grid(column=0,row=1,pady=5)

    entryBaseStack = tk.Entry(Frame,fg="black", bg="grey80", width=5,textvariable = tk.StringVar(value="10"))
    entryBaseStack.grid(column=1,row=0,pady=5,sticky=tk.E)
    entryInvidStack = tk.Entry(Frame,fg="black", bg="grey80", width=5,textvariable = tk.StringVar(value="500"))
    entryInvidStack.grid(column=1,row=1,pady=5,sticky=tk.E)

    checkBaseStack = tk.Checkbutton(Frame,text='Change Base Stack Size',onvalue=True, offvalue=False,variable=BaseStackValue)
    checkBaseStack.grid(column=0,sticky=tk.NW)
    checkInvidStack = tk.Checkbutton(Frame,text='Change Invidual Stack Size',onvalue=True, offvalue=False,variable=InvidStackValue)
    checkInvidStack.grid(column=0,sticky=tk.NW)

    return Frame

def createFrameInvidItems(container):
    global itemID,Items,scrollable_frame
    Frame = ttk.Frame(container)
    Frame['borderwidth'] = 5
    Frame['relief'] = 'sunken'
    Frame.columnconfigure(0, weight=99)
    Frame.columnconfigure(1, weight=1)

    canvas = tk.Canvas(Frame)
    scrollbar = tk.Scrollbar(Frame, orient="vertical", command=canvas.yview,)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    Items = refreshInvidItems()

    canvas.grid(columnspan=2)
    scrollbar.grid(column=1,row=0,sticky=tk.NS,padx=0,pady=0)

    newEntryFrame = tk.Frame(Frame)
    newEntryFrame.grid(column=0)

    buttonCreate = tk.Button(newEntryFrame,text="Create",width=10,height=1,bd=3,bg="grey85",fg="black",command=lambda: (addNewEntry(entryID.get(),entryName.get()),refreshInvidItems(),newEntryFrame.grid_remove(),buttonNewEntry.grid(),Frame.focus_set()))
    buttonCreate.grid(column=2,row=0,padx=5, pady=5)

    buttonCancel = tk.Button(newEntryFrame,bg="red",text="X",bd=3,height=1,command=lambda:(print("Canceled"), newEntryFrame.grid_remove(),buttonNewEntry.grid(),Frame.focus_set(),  ))
    buttonCancel.grid(column=3,row=0,padx=0, pady=0)
    
    entryID = tk.Entry(newEntryFrame,fg="black", bg="grey80", width=20,textvariable = tk.StringVar(value="Item ID"))
    entryID.grid(column=0,row=0,pady=5,sticky=tk.E)
    

    entryName = tk.Entry(newEntryFrame,fg="black", bg="grey80", width=20,textvariable = tk.StringVar(value="Item Name"))
    entryName.grid(column=1,row=0,pady=5,sticky=tk.E)

    newEntryFrame.grid_remove()

    buttonNewEntry = tk.Button(Frame,text="New Entry",width=10,height=1,bd=3,bg="grey85",fg="black",command= lambda: (buttonNewEntry.grid_remove(),  newEntryFrame.grid(), setEntryValue(entryID,"Item ID"),setEntryValue(entryName,"Item Name"),entryID.focus_set() ))
    buttonNewEntry.grid(columnspan=2,padx=5, pady=5)
    
    return Frame

def refreshInvidItems():
    global Items,scrollable_frame
    Items = []

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    with open("configMakerFile","w") as File:
        for i,item in enumerate(itemID):
            File.write(f"{item[0]} --- {item[1]}\n")
            Items.append(tk.BooleanVar(value=True))
            Frame = ttk.Frame(scrollable_frame,height=1)
            checkItem = ttk.Checkbutton(Frame,text=item[1],width=48,onvalue=True,offvalue=False,variable=Items[i])
            checkItem.grid(column=0,row=0,padx=5, pady=5,sticky=tk.E)
            buttonDelete = tk.Button(Frame,bg="red",text="X",bd=3,height=1,command= lambda item=item: deleteEntry(item))
            buttonDelete.grid(column=1,row=0,padx=5, pady=5,sticky=tk.E)

    
     
    for widget in scrollable_frame.winfo_children():
        widget.grid(padx=5, pady=5,sticky=tk.W)


    return Items


def createWindow():
    root = tk.Tk()
    root.title('Ark Stack Config')
    root.resizable(0, 0)
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)  

    MainFrame = createMainFrame(root)
    MainFrame.grid(column=0,row=0,sticky=tk.NS)

    FrameInvidItems = createFrameInvidItems(root)
    FrameInvidItems.grid(column=1,row=0,sticky=tk.NS,pady=20)

    root.mainloop()

def addNewEntry(ID,Name):
    global itemID
    itemID.append((ID,Name))

def setEntryValue(entry,text):
    entry.delete(0,tk.END)
    entry.insert(0,text)

def deleteEntry(entry):
    global itemID
    itemID.remove(entry)
    refreshInvidItems()

def checkForFile():
    global itemID
    if os.path.isfile("configMakerFile"):
        with open("configMakerFile",'r') as File:
            itemID = []
            for line in File:
                a,b = line.split(' --- ')
                itemID.append((a.strip(),b.strip()))
    print(f"Items: {itemID}")

if __name__ == "__main__":
    checkForFile()
    createWindow()