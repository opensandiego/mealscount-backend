from tkinter import ttk,Tk,PhotoImage,filedialog,StringVar,BooleanVar,BOTH,messagebox,IntVar
import tksheet
import os,os.path,configparser
from bulktools import optimize,load_from_csv,output_rows,write_to_csv
from strategies import STRATEGIES
from us.states import STATES
import threading
import multiprocessing
import sys


class MealsCountDesktop(object):
  def __init__(self,app_path):
    self.filename = None
    self.districts = None
    self.root = None
    self.frame = None
    self.progress = None
    self.fileFrame = None
    self.configFrame = None
    self.runFrame = None
    self.strategyVars = []
    self.processPool = {}

    # Save prefs for each load
    self.config = configparser.ConfigParser() 
    self.config['DEFAULT'] = {
      'csv_file': '',
      'state': 'CA',
      'starts': '50',
      'iterations': '1000',
      'optimizeFor': 'reimbursement',
      'nGroups': '10',
      'debug': '5',
    }
    self.config['current'] = {}
    self.cfg = self.config['current']
    self.configLocation = os.path.join(app_path,"mealscount.cfg")
    if os.path.exists(self.configLocation):
      self.config.read(self.configLocation)
    else:
      self.write_cfg()

  def write_cfg(self):
    with open(self.configLocation,'w') as configFile:
      self.config.write(configFile)

  def initialize(self):
    # root window
    root = Tk()
    root.title("MealsCount Bulk Optimizer")
    #root.geometry("800x600")
    root.grid_columnconfigure(0,weight=1)

    # Create logo frame
    # why did this stop working?
    #logo = PhotoImage("logo",file=os.path.join("src","assets","MC_Logo@2x.png"))
    #ttk.Label(root,image=logo).grid(row=0,column=0)
    ttk.Label(root,text="Meals Count Bulk Optimizer").grid(row=0,column=0)

    # Create frame for the rest of our components
    frm = ttk.Frame(root,padding=10)
    frm.grid(row=1,column=0)

    self.root = root
    self.frame = frm

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
    #strategies = [v[0] for v in self.strategyVars if v[2].get()]
    strategies = [s for s in STRATEGIES if "NYCMODA" not in s]
    starts = int(self.startsVar.get())
    iterations = int(self.iterationsVar.get())
    ngroups = int(self.nGroupsVar.get()) 
    strategies.append("NYCMODA?fresh_starts=%i&iterations=%i&ngroups=%i" % (starts,iterations,ngroups))
    districts = self.districts 
    if self.testRunVar.get():
      districts = {c:d for c,d in self.districts.items() if len(d.schools) <= 5}
    t = threading.Thread(target=lambda: self.run(districts,strategies,goal))
    t.start()

  def handle_save_as(self):
    save_file = filedialog.asksaveasfile()
    if(save_file):
      write_to_csv(self.resultRows,save_file)
      messagebox.showinfo("Saved %i district optimizations to %s" %(len(self.districts),save_file.name))

  def handle_cancel(self):
    if 'pool' in self.processPool:
      self.processPool['pool'].terminate()
      del self.processPool['pool']
      self.progressVar.set(0)

  def run(self,districts,strategies,goal):
    if 'pool' in self.processPool:
      messagebox.showerror("Please cancel current job before starting a new one")
      return
    self.write_cfg()
    self.results = optimize(
      districts,
      strategies,
      goal=goal,
      poolTrack=self.processPool,
      progress_callback=lambda n: self.handle_progress(n),
    )
    del self.processPool['pool']
    messagebox.showinfo("Complete","Optimization complete\n%i results" % len(self.results))
    self.resultRows = output_rows(
      self.districts,
      self.results,
      [], #TODO add in coverage comparison?
      [], #TODO add in lastyear comparison
    )
    self.show_results()

  def show_results(self):
    self.resultSheet.set_sheet_data(self.resultRows)

  def addFileFrame(self):
    fileFrame = ttk.LabelFrame(self.frame,text="Select File",padding=10)
    ttk.Button(fileFrame, text="Select CSV", command=self.handle_choose_file).grid(row=0,column=0,sticky="nw")
    self.file_selected = ttk.Label(fileFrame,text="")
    self.file_selected.grid(row=0,column=1,stick="ne")
    fileFrame.grid(row=1,column=0)

  def addConfigureFrame(self):
    configFrame = ttk.LabelFrame(self.frame,text="Configure Run",padding=10)

    stateFrame = ttk.LabelFrame(configFrame,text="State")
    stateFrame.grid(row=0,column=0,stick='nw')
    ttk.Label(stateFrame,text="Select State").grid(row=0,column=0)
    self.stateCombobox = ttk.Combobox(configFrame,values=[s.abbr for s in STATES],state="readonly")
    self.stateCombobox.set(self.cfg.get('state'))
    self.stateCombobox.grid(row=1,column=0)

    optimizeForFrame = ttk.LabelFrame(configFrame,text="Optimize For",padding=5)
    self.optimizeForVar = StringVar(value="reimbursement")
    ttk.Radiobutton(optimizeForFrame,text="Max Reimbursement",value="reimbursement",var=self.optimizeForVar).grid(row=0,column=0)
    ttk.Radiobutton(optimizeForFrame,text="Max Coverage",value="coverage",var=self.optimizeForVar).grid(row=1,column=0)
    ttk.Label(optimizeForFrame,text="Max Number of Groups").grid(row=2,column=0)
    self.nGroupsVar = StringVar(value='10')
    ttk.Spinbox(optimizeForFrame,from_=5,to=1000,textvariable=self.nGroupsVar).grid(row=3,column=0)
    optimizeForFrame.grid(row=0,column=1)

    iterationsFrame = ttk.LabelFrame(configFrame,text="Iterations",padding=5)
    ttk.Label(iterationsFrame,text="Starts").grid(row=0,column=0)
    self.startsVar = StringVar(value='50')
    ttk.Spinbox(iterationsFrame,from_=50,to=1000,textvariable=self.startsVar).grid(row=0,column=1)
    ttk.Label(iterationsFrame,text="Iterations").grid(row=1,column=0)
    self.iterationsVar = StringVar(value='1000')
    ttk.Spinbox(iterationsFrame,from_=1000,to=1000000,textvariable=self.iterationsVar).grid(row=1,column=1)
    iterationsFrame.grid(row=0,column=2)

#    strategyFrame = ttk.LabelFrame(configFrame,text="Strategies",padding=5)
#    for i,strategy in enumerate(STRATEGIES.items()):
#      sVar = BooleanVar(value=True)
#      self.strategyVars.append((strategy[0],strategy[1],sVar))
#      sFrame = ttk.Frame(strategyFrame)
#      sFrame.pack()
#      ttk.Checkbutton(sFrame,text=strategy[0],variable=sVar).pack()
#    strategyFrame.pack(fill=BOTH,expand=True)

    configFrame.grid(row=1,column=1,stick='nesw')
    self.configFrame = configFrame

  def addRunFrame(self):
    runFrame = ttk.LabelFrame(self.frame,text="Run Optimization",padding=10) 
    ttk.Button(runFrame, text="Run",command=self.handle_run).grid(column=0, row=0)
    cancel = ttk.Button(runFrame, text="Cancel", command=self.handle_cancel)
    cancel.grid(column=1, row=0)
    self.testRunVar = BooleanVar(value=True)
    ttk.Checkbutton(runFrame,text="Test Run of 5 districts only",variable=self.testRunVar).grid(column=2,row=0)

    self.progressVar = IntVar()
    ttk.Progressbar(runFrame,maximum=100,variable=self.progressVar).grid(column=0,row=1,columnspan=2,sticky='nesw')
    self.runFrame = runFrame
    runFrame.grid(row=3,column=0,columnspan=2,sticky='nesw')

  def addResultFrame(self):
    resultFrame = ttk.LabelFrame(self.frame,text="Results",padding=10)
    ttk.Button(resultFrame, text="Save As",command=self.handle_save_as).grid(row=0,column=0)
    sheet=tksheet.Sheet(resultFrame)  
    #sheet.set_sheet_data([['a','b','c'],[1,2,3],[4,5,6]])
    sheet.grid(row=1,column=0,sticky='nesw')
    self.resultSheet = sheet
    resultFrame.grid(row=4,column=0,columnspan=2,sticky='nesw')

  def loop(self):
    self.root.mainloop()

def init(app_path):
  win = MealsCountDesktop(app_path)
  win.initialize()
  win.addFileFrame()
  win.addConfigureFrame()
  win.addRunFrame()
  win.addResultFrame()
  win.loop() 

if __name__=="__main__":
  app_path = ""
  if sys.platform.startswith('win'):
    app_path = os.getenv("APPDATA")
    multiprocessing.freeze_support()
  init(app_path)