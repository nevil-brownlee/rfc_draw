class language: 
  def __init__(self): 
    self.language = 'PYTHON'
    self.lg = self.specification()
    print(">>> self %s" % self)
    
  def show(self): 
    print("Language:", self.language) 

  class specification: 
    def __init__(self): 
      self.type = 'HIGH-LEVEL'
      self.founded = '1991'
    def display(self): 
      print("type:", self.type) 
      print("Founded:", self.founded) 
  
  
out = language() 
out.show() 
ppool = out.lg 
ppool.display() 
