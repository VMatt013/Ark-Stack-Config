import tkinter as tk
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
    ("PrimalItemResource_Sap","Sap")
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
    global itemID,Items
    Frame = tk.Frame(container)
    Frame['borderwidth'] = 5
    Frame['relief'] = 'sunken'
    Frame.columnconfigure(0, weight=1)

    Items = []
    for i,itemName in enumerate(itemID):
        Items.append(tk.BooleanVar(value=True))
        checkItem = ttk.Checkbutton(Frame,text=itemName[1],onvalue=True,offvalue=False,variable=Items[i])
    
    for widget in Frame.winfo_children():
        widget.grid(padx=5, pady=5,sticky=tk.W)

    return Frame

def createWindow():
    root = tk.Tk()
    root.geometry("600x300")
    root.title('Ark Stack Config')
    root.resizable(0, 0)
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)

   

    MainFrame = createMainFrame(root)
    MainFrame.grid(column=0,row=0,sticky=tk.NS)

    FrameInvidItems = createFrameInvidItems(root)
    FrameInvidItems.grid(column=1,row=0,sticky=tk.NS,pady=20)

    root.mainloop()


if __name__ == "__main__":
    createWindow()