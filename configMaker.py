import tkinter as tk
from tkinter import TclError, ttk

itemID = [
    "PrimalItemConsumable_RawPrimeMeat",
    "PrimalItemConsumable_CookedPrimeMeat",
    "PrimalItemConsumable_RawMutton",
    "PrimalItemConsumable_CookedLambChop",
    "PrimalItemConsumable_Honey",
    "PrimalItemResource_Sap"
]

def ResetStacks(isBaseStack,isInvidStack):
    Output = []
    if isInvidStack:
        with open("ShooterGame/Saved/Config/WindowsNoEditor/Game.ini", "r") as File:
            for line in File.readlines():
                if line.count("ConfigOverrideItemMaxQuantity") > 0 or line == "\n":
                    pass
                else:
                    Output.append(line)
        with open("ShooterGame/Saved/Config/WindowsNoEditor/Game.ini", "w") as File:
            File.write("".join(Output))
    
    Output = []
    if isBaseStack:
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
        ResetStacks(isBaseStack,isInvidStack)
        for item,id in zip(Items,itemID):
            if item.get():
                with open("ShooterGame/Saved/Config/WindowsNoEditor/Game.ini", "a") as File:
                    File.write(f'\nConfigOverrideItemMaxQuantity=(ItemClassString="{id}_C",Quantity=(MaxItemQuantity={invidValue}, bIgnoreMultiplier=true))')
    if isBaseStack:
        with open("ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini", "r") as File:
            for line in File.readlines():
                if line.count("ItemStackSizeMultiplier") > 0:
                    Output.append(f"ItemStackSizeMultiplier={GetEntry(BaseStackValue)}\n")
                else:
                    Output.append(line)
        with open("ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini", "w") as File:
            File.write("".join(Output))
            
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

    buttonGenerate = tk.Button(Frame,text="Generate Stack Configs",width=20,height=2,bg="blue",fg="yellow",command=lambda: (GenerateStackOverride(BaseStackValue.get(),InvidStackValue.get(),entryBaseStack,entryInvidStack)))
    buttonGenerate.grid(column=2,row=0,padx=5, pady=5)
    buttonClean = tk.Button(Frame,text="Reset",width=20,height=2,bg="blue",fg="black",command=lambda: (ResetStacks(BaseStackValue.get(),InvidStackValue.get())))
    buttonClean.grid(column=2,row=1,padx=5, pady=5)

    labelBaseStack= tk.Label(Frame,text="Base Stack Multiplier:",fg="white",bg="black",width=18,height=1)
    labelBaseStack.grid(column=0,row=0,pady=5)
    labelInvidStack= tk.Label(Frame,text="Invidual Stack Size:",fg="white",bg="black",width=18,height=1)
    labelInvidStack.grid(column=0,row=1,pady=5)

    entryBaseStack = tk.Entry(Frame,fg="yellow", bg="blue", width=5,textvariable = tk.StringVar(value="10"))
    entryBaseStack.grid(column=1,row=0,pady=5)
    entryInvidStack = tk.Entry(Frame,fg="yellow", bg="blue", width=5,textvariable = tk.StringVar(value="500"))
    entryInvidStack.grid(column=1,row=1,pady=5)

    checkBaseStack = tk.Checkbutton(Frame,text='Change Base Stack Size',onvalue=True, offvalue=False,variable=BaseStackValue)
    checkBaseStack.grid(column=0,sticky=tk.NW)
    checkInvidStack = tk.Checkbutton(Frame,text='Change Invidual Stack Size',onvalue=True, offvalue=False,variable=InvidStackValue)
    checkInvidStack.grid(column=0,sticky=tk.NW)

    return Frame

def createFrameInvidItems(container):
    global itemID,Items
    Frame = tk.Frame(container)
    Frame.columnconfigure(0, weight=1)

    Items = []
    for i,itemName in enumerate(itemID):
        Items.append(tk.BooleanVar(value=True))
        checkItem = ttk.Checkbutton(Frame,text=itemName,onvalue=True,offvalue=False,variable=Items[i])
    
    for widget in Frame.winfo_children():
        widget.grid(padx=5, pady=5,sticky=tk.NW)

    return Frame

def createWindow():
    root = tk.Tk()
    root.geometry("700x400")
    root.title('Ark Stack Config')
    root.resizable(0, 0)
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)

    try:
        # windows only (remove the minimize/maximize button)
        root.attributes('-toolwindow', True)
    except TclError:
        print('Not supported on your platform')

    MainFrame = createMainFrame(root)
    MainFrame.grid(column=0,row=0)

    FrameInvidItems = createFrameInvidItems(root)
    FrameInvidItems.grid(column=1,row=0)

    root.mainloop()


if __name__ == "__main__":
    createWindow()