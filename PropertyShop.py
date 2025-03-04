#!/bin/python3.12
"""
Property Shop for dynamically creating customized python properties - Enhanced for spreadsheet-like capability
©2025 David A. Kra dakra137@gmail.com  This work is openly licensed with Creative Commons CC BY-SA 4.0 license
                                       https://creativecommons.org/licenses/by-sa/4.0/
v.0.9 original publicly posted on github https://github.com/dakra137/PropertyShop/blob/main/PropertyShop.py 

See the documentation in the README at https://github.com/dakra137/PropertyShop 
See a more extensive set of test case eamples in https://github.com/dakra137/PropertyShop/PropertyShopTestCases.py
"""

def PropertyShopFactory():

    class PropertyShop(object):

       recalcset = set( )
       recalcnewvalues = { } # dictionary
       pass 

       @classmethod
       def addProperty(cls,
                       name:str="YouForgoTtoAssignAPropertyName",
                       value=None,
                       sc=None,
                       gc=None,
                       doc=None,
                       recalc=False,
                       recalcnewvalue=lambda : 0) : #cls is the class, not an instance.

           if isinstance(name,(list,set,tuple)):
              for aname in name:
                  cls.addProperty(aname,value,sc,gc,doc,recalc)
              return
   
           # print(f"\n Adding property named: {name} to class: {cls} at {id(cls)} with parm values: value={value} , sc={sc}, gc={gc}, doc={doc}, recalc={recalc}, recalcnewvalue={recalcnewvalue} " )        
             
           if recalc: 
               cls.recalcset.add(name)
           else:
               cls.recalcset.discard(name) # It might be there due to a previous addProperty with recalc=True
               
           if doc is None: doc=name
           
           if value is None: value=name

           #print(f"adding property named: {name} to class: {cls} at {id(cls)} with parm values: value={value} , sc={sc}, gc={gc}, doc={doc}, recalc={recalc}, recalcnewvalue={recalcnewvalue} " )

           if callable(gc):  # getter customization
               #MUST NOT BE @classmethod.  Causes TypeError: 'classmethod' object is not callable
               def pgetter(self):   #*args,**kwargs): # arguments are unused
                   #t=gc(getattr(pgetter.cls,pgetter.fromwhattoget))# these  attributes are set externally just after this function definition
                   t=gc(pgetter._pvalue)
                   # self.__class__.get_age.pvalue = a # set the attribute in the getter
                   #print("invoked the getter for name= ",name, pgetter.fromwhattoget, "; value= ",t, ". clsparm=",clsparm)
                   return t
           else:
               #MUST NOT BE @classmethod.  Causes TypeError: 'classmethod' object is not callable
               def pgetter(self):   #*args,**kwargs): # arguments are unused
                   #t=getattr(pgetter.cls,pgetter.fromwhattoget) # these  attributes are set externally just after this function definition
                   t=pgetter._pvalue
                   #print("invoked the getter for name= ",name, pgetter.fromwhattoget, "; value= ",t, ". clsparm=",clsparm)
                   return t

           pgetter.fromwhattoget="_"+name
           pgetter.propname=name
           pgetter.cls=cls         

           if callable(sc): # setter customization
               #MUST NOT BE @classmethod. Causes TypeError: 'classmethod' object is not callable
               def psetter(clsparm, newvalue=3.14159):
                   #print("invoked a setter for name ",name, psetter.intowhattoset, " = ",newvalue)
                   t=sc(newvalue)
                   setattr(psetter.cls,psetter.intowhattoset,t) # these attributes are set externally just after this function definition
                   pgetter._pvalue=t
                   #ap.__class__.aprop.__get__.__self__.fget._usecount
                   return
               setattr(cls, "_"+name, value ) # in case of a self reference in the sc
               setattr(cls, "_"+name, sc(value) )
               pgetter._pvalue=value               
               pgetter._pvalue=sc(value)
               cls.recalcnewvalues[name]=recalcnewvalue
           else:
               #MUST NOT BE @classmethod. Causes TypeError: 'classmethod' object is not callable
               def psetter(clsparm, newvalue=3.14159): # no setter customization
                   #print("invoked a setter for name ",name, psetter.intowhattoset, " = ",newvalue)
                   setattr(psetter.cls,psetter.intowhattoset,newvalue) # these attributes are set externally just after this function definition
                   pgetter._pvalue=newvalue
                   return
               setattr(cls, "_"+name, value )
               pgetter._pvalue=value   

           psetter.intowhattoset="_"+name
           psetter.propname=name
           psetter.cls=cls

           def pdeleter(clsparm):
               delattr(psetter.cls,"_"+pdeleter.whattodelete)
               delattr(psetter.cls,pdeleter.whattodelete)
               pdeleter.cls.recalcset.discard(pdeleter.whattodelete)
               try:
                  del pdeleter.cls.recalcnewvalues[pdeleter.whattodelete]
               except:
                  pass
               return           
           pdeleter.whattodelete=name
           pdeleter.cls=cls

           #print("fromwhat to get and into what toset = ",pgetter.fromwhattoget, psetter.intowhattoset)

           # Make the property !!! Point an attribute in the class to it.
           setattr(cls,name, property( fget=pgetter, fset=psetter, fdel=pdeleter, doc=doc) )
           return # from addProperty
       
       def inventory(self):
           cls=type(self)
           property_names=[p for p in dir(cls) if isinstance(getattr(cls,p),property)]
           p=[[d, # (for d in property_names )
               v:=getattr(cls,"_"+d) if hasattr(cls,"_"+d) else " must be an alias " , 
               getattr(cls,d).__get__.__self__.fget._pvalue,
               type(v), 
               g:=getattr(self,d), type(g), getattr(getattr(cls,d),"__doc__"),f" {'IsIn' if d in cls.recalcset else 'NotIn'}Recalcset",
               
               ]
              for d in property_names]
           return p
       
       def propdoc(self,name:str): #  ss.propdoc("b1")
           return getattr(getattr(type(self),name),"__doc__") 
 
       def empty(self):
           cls=type(self) 
           cls.recalcset = set()
           cls.recalcnewvalues = { }
           property_names=[p for p in dir(cls) if isinstance(getattr(cls,p),property)]  
           for pn in  property_names:
              delattr(cls,"_"+pn)
              delattr(cls,pn)
       
       def recalculate(self,ntimes=1):
           cls=type(self)
           recalist=list(cls.recalcset)
           recalist.sort()
           for n in range(ntimes):
               for p in recalist:
                   # setattr(self,p,None) # invoke the setter for the cell, passing parameter None
                   # setattr(self,p,getattr(cls,"_"+p) ) # invoke the setter for the cell, passing the cell's current internal value
                   # invoke the setter with the result of invoking the recalcnewvalue function for that property.
                   setattr(self,p,cls.recalcnewvalues[p]() ) #getattr(cls,"_"+p) )                  
                   
       def propobj(self,prop=str):
           o=None
           try:
              o= getattr(self.__class__,prop)
           except:
              pass
           return o
        
       @classmethod
       def makealias(cls,propertyname,recipient,aliasname): 
          ### Usage:  aPropertyShop.makealias("propertyname",inPropertyShop,"aliasname")  
          #  a.__class__.b=x.__class__.y   # or x.alias("y",a,"b") 
          # the alias points to the same objectid as the original
          setattr(recipient.__class__,aliasname,getattr(cls,propertyname) )
          if propertyname in cls.recalcset: 
             recipient.__class__.recalcset.add(aliasname)
             recipient.__class__.recalcnewvalues[aliasname]=cls.recalcnewvalues[propertyname]
          return 
       # end of the class definition
             
    return PropertyShop() # return from PropertyShopFactory. Return an instance of the class
# end of PropertyShop.py

