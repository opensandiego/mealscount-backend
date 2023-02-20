from tkinter import ttk,Tk,PhotoImage,filedialog,StringVar,BooleanVar,BOTH,messagebox,IntVar
import os.path
from statewide import optimize,load_from_csv
from strategies import STRATEGIES
from us.states import STATES
import threading

class MealsCountDesktop(object):
  def __init__(self):
    self.filename = None
    self.districts = None
    self.root = None
    self.frame = None
    self.progress = None
    self.fileFrame = None
    self.configFrame = None
    self.runFrame = None
    self.strategyVars = []

  def initialize(self):
    # root window
    root = Tk()
    root.title("MealsCount Desktop")
    root.geometry("800x600")

    # Create logo frame
    frm = ttk.Frame(root,padding=10)
    #ttk.Label(frm,text="Hello World").grid(column=0,row=0)
    logo = PhotoImage("logo",file=os.path.join("src","assets","MC_Logo@2x.png"))
    ttk.Label(frm,image=logo)
    self.root = root
    self.frame = frm
    frm.pack()

  def handle_choose_file(self):
    self.filename = filedialog.askopenfilename(
      title="Select csv file",
      filetypes=(("CSV Files","*.csv"),("XLS Files","*.xls"),("XLSX Files","*.xlsx"))
    )
    districts,schools,lastyear_groupings = load_from_csv(self.filename,csv_encoding="utf-8",state=self.stateCombobox.get())
    self.file_selected.config(text="Selected %s\nFound %i Districts, %i Schools" % (
      os.path.basename(self.filename),
      len(districts),
      len(schools)
    ))
    self.districts = districts

  def handle_progress(self,n):
    self.progressVar.set(round(n*100))

  def handle_run(self):
    if not self.districts:
      messagebox.showerror("No Districts Loaded","Please select your CSV and make sure it shows your districts have been loaded")
      return
    goal = self.optimizeForVar.get()
    strategies = [v[0] for v in self.strategyVars if v[2].get()]
    #districts = {c:d for c,d in self.districts.items() if len(d.schools) <= 5}
    districts = self.districts 
    t = threading.Thread(target=lambda: self.run(districts,strategies,goal))
    t.start()

  def run(self,districts,strategies,goal):
    results = optimize(districts,strategies,goal=goal,progress_callback=lambda n: self.handle_progress(n))
    print("Result Len",len(results))
    messagebox.showinfo("Complete","Optimization complete")

  def handle_cancel(self):
    pass


  def addFileFrame(self):
    fileFrame = ttk.LabelFrame(self.frame,text="Select File",padding=10)
    ttk.Button(fileFrame, text="Select CSV", command=self.handle_choose_file).pack()
    self.file_selected = ttk.Label(fileFrame,text="")
    self.file_selected.pack()
    self.fileFrame = fileFrame
    fileFrame.pack(fill=BOTH,expand=True)

  def addConfigureFrame(self):
    configFrame = ttk.LabelFrame(self.frame,text="Configure Run",padding=10)
    ttk.Label(configFrame,text="State").pack()
    self.stateCombobox = ttk.Combobox(configFrame,values=[s.abbr for s in STATES],state="readonly")
    self.stateCombobox.set("CA")
    self.stateCombobox.pack()

    optimizeForFrame = ttk.LabelFrame(configFrame,text="Optimize For",padding=5)
    self.optimizeForVar = StringVar(value="reimbursement")
    ttk.Radiobutton(optimizeForFrame,text="Max Reimbursement",value="reimbursement",var=self.optimizeForVar).pack()
    ttk.Radiobutton(optimizeForFrame,text="Max Coverage",value="coverage",var=self.optimizeForVar).pack()
    optimizeForFrame.pack(fill=BOTH,expand=True)

    strategyFrame = ttk.LabelFrame(configFrame,text="Strategies",padding=5)
    for i,strategy in enumerate(STRATEGIES.items()):
      sVar = BooleanVar(value=True)
      self.strategyVars.append((strategy[0],strategy[1],sVar))
      sFrame = ttk.Frame(strategyFrame)
      sFrame.pack()
      ttk.Checkbutton(sFrame,text=strategy[0],variable=sVar).pack()
    strategyFrame.pack(fill=BOTH,expand=True)

    configFrame.pack()
    self.configFrame = configFrame

  def addRunFrame(self):
    runFrame = ttk.LabelFrame(self.frame,text="Run Optimization",padding=10) 
    ttk.Button(runFrame, text="Run",command=self.handle_run).grid(column=0, row=0)
    #cancel = ttk.Button(runFrame, text="Cancel", command=self.handle_cancel)
    #cancel.grid(column=1, row=0)
    self.progressVar = IntVar()
    ttk.Progressbar(runFrame,maximum=100,variable=self.progressVar).grid(column=0,row=1,columnspan=2)
    self.runFrame = runFrame
    runFrame.pack(fill=BOTH,expand=True)

  def loop(self):
    self.root.mainloop()

def init():
  win = MealsCountDesktop()
  win.initialize()
  win.addFileFrame()
  win.addConfigureFrame()
  win.addRunFrame()
  print("looping")
  win.loop() 

if __name__=="__main__":
  init()