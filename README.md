<!-- PropertyShop active 0 Joplin  18:30 Wednesday 4 March 2025   -->
# Property Shop dynamically creates customized python properties
#### ©2025 David A. Kra dakra137@gmail.com  
#### This work is openly licensed with the [Creative Commons CC BY-SA license](https://creativecommons.org/licenses/by-sa/4.0/)

Revisions: 
- version 0.9 First public version

**Contains:**
- README.md 
- LICENSE
- PropertyShop.py
- PropertyShopTestCases.py

#### Backstory
Python properties are very convenient to use, but inconvenient to create, especially if there will be many of them. This module removes the inconveniences and adds several conveniences.

In the film industry, each studio has its own "property shop" where custom properties are created and stored. The studio's property shop has both a front-side department with which a film team interacts and a back-room with the workshop and storage.

This module does the same for python properties. It provides a factory which produces totally independent property shops.

#### Property Shop
This module lets you create multiple Property Shops. Each is totally independent, so the same property names can be used in each without collisions.

Each property shop you create with this module (e.g. ** `ps=PropertyShopFactory( ) `**) has:
- Its own back room (a unique class) where that shop's properties will be stored. It is where the synthesis of properties happens.
- Its front-side (an instance of the class). Programs interact with the property shop through the front side: 
	-	Requesting adding a property to the shop, usually with customization.
	-	Getting and setting properties, along the way automagically invoking the property's custom getter or setter.
	- Additional miscellaneous capabilities, such as listing the inventory of all the properties, erasing all the properties, recalculating the values of designated properties, and more

Example uses include:
-	Properties whose setter enforces casting the value to a particular type, such as to numpy . longdouble. This makes the property "[type-immutable](#immutable-type)" in that the property's type is immutable.  
-	Properties that act much like [spreadsheet cells](#programming-code-vs-spreadsheets) with formulas, [manual](#create-properties-that-behave-very-much-like-spreadsheet-cells-with-manual-recalculation) recalculation of [one](#the-formulas-calculation-happens-whenever-the-property-is-initialized-or-set) or [all designated](#recalculate) formulas, or [automatic]()  formula recalculation, and even allowance for [circular references]().
-	[Immutable properties](), whose value never changes, silently ignoring efforts to set its value to something else.  
-	[Generator-like properties]() whose value autoincrements every time the property is used, similar to a range generator.

See many examples in the [PropertyShopTestCases.py](https://github.com/dakra137/PropertyShop/blob/main/PropertyShopTestCases.py) file in the repository.

##### How easy is it to use?

Here we create a PropertyShop, **ps**, and then add to it properties named x, y, name, address, state, and postalcode. At the same time, customize them so that x is always a float, y is always an int, and the others are always strings. Set initial values for x and y.

First, create the PropertyShop, and properties x and y.

```python
from PropertyShop import PropertyShopFactory
ps=PropertyShopFactory() # create a PropertyShop
a2ps=ps.AddProperty      # create a convenient alias for ps.AddProperty
	
a2ps("x",3.14,sc=float) #sc is the setter customization, forcing it to always be a float
a2ps("y",3,sc=int) #sc is the setter customization, forcing it to always be an int
```

Then, use them, 

```python
y=72 # a local variable
# Assign a value. Invoke the property's setter.
ps.x=413 # ps.x will be cast to 413.0
# Reference property values. Invoke two properties' getter's
z=(y +  ps.x )**  ps.y
```

Now create the name, address, state, and postalcode properties all at once. All of these will always be strings, even the postal code.

```python
a2ps(["name","address","city","state","postalcode"],sc=str) #sc is the setter customization, forcing them to always be strings
ps.name,ps.address,ps.city,ps.state,ps.postalcode=["David Kra", "14 Main St.", "Springfield", "PR", 12345.6789]
print(f"Name: {ps.name} at {ps.address} in {ps.city}, {ps.state}  {ps.postalcode}")
```
		
Easy, isn't it?

## Module quick summary example using all the functions and methods

```python
from PropertyShop import PropertyShopFactory
ps=PropertyShopFactory() # create a Property Shop
ps.addProperty("z")      # create a minimal property
ps.addProperty(["a","b"],0,sc=float,gc=str) # create properties a and b within ps. They are always set to float, but get reports them out as string.
ps.addProperty("c",0,sc=lambda x:float(ps.a*ps.b),gc=str,recalc=True,doc="ps.c = ps.a*ps.b") # create a property which is the product of ps.a * ps.b and is recalculated by ps.recalculate
ps.addProperty("d",0,gc=str(ps.a*ps.b),doc="ps.c = ps.a*ps.b") # create a property which is the product of ps.a * ps.b and is automatically recalculated when retrieved.
print(ps.a) # use a property
ps.b=3.14159265   # set a property
for item in ps.inventory(): print(item) # print the inventory of properties in this Property Shop
print(ps.a,ps.b,ps.c, ps.d)
ps.recalculate()      # recalculate the properties specified with recalc=True, such as ps.c
print(ps.a,ps.b,ps.c, ps.d)
objidpsc=ps.propobj(ps.c)  # get the object id of the property
ps..makealias("c",ps,"x") # ps.x will be an alias for ps.c (not a copy), with the same recalculation characteristics.
del ps.b    # delete a property
ps.empty()  # delete all properties in ps
```

## Module Details
The module has one function, `PropertyShopFactory()`, which fabricates an independent  PropertyShop. It is the synthesized PropertyShop object which has methods to add properties plus more.

### function PropertyShopFactory() -> PropertyShop:
**Purpose:**  Create a PropertyShop into which properties can be added dynamically, and then to be set, get, deleted, recalculated, aliased, and listed.

Each call to PropertyShopFactory() creates:
- A unique container class, so that each PropertyShop has its own namespace and contents. 	
- An instance of that class, through which to insert, set, delete properties and more.	
- A method to add one or more properties. The setter and getter can be customized.	
- A few convenience methods.
    
**Args:**
- none

**Returns:**

- A unique instance of a unique PropertyShop class.
	- Each instance refers to a different PropertyShop class with a different object id.
	- Each provides a separate namespace for that class's properties.

**Example:**
```python
        ps=PropertyShopFactory()  # returns a PropertyShop instance
```

## class PropertyShop():

This is a dynamically created container class for a Property Shop. An instance of it will be the interface to the container for properties. An instance is returned by calling PropertyShopFactory(). Your code uses the instance, not the class.

**Arguments:**

   None.  The user application does not create any instances of the class. The Factory creates the class and one instance. The Factory returns the instance.

**Attributes:**
- 	Initially a set and a dictionary used in conjunction with recalculating formulas. Your application does not use them.
  
  <pre>
    For each property that later gets inserted, there will be two attributes.  
            For ps=PropertyShopFactory(),  
                after properties "x" and "y" are added by using
			         ps.addProperty(["x","y"])
                there will be attributes:
                       ps.x used from the instance for its setter and getter.
                       ps.y used from the instance for its setter and getter.
                       ps._x (actually in the class, not the instance) holding the property's actual value
                       ps._y (actually in the class, not the instance) holding the property's actual value
  </pre> 
	  
**Usage:**

Your application does not knowingly use the PropertyShop class itself. Your application uses the PropertyShop instance returned, for example, by `ps=PropertyShopFactory()`.

Instantiation: Indirectly only. Instances of the class are not instantiated by applications, but only by the factory.
- Each call to PropertyShopFactory() creates and returns one unique instance.
- Each call to instance.addProperty creates one or more property objects within the class.


## **PropertyShop Methods:**
All these methods are invoked only through an instance of PropertyShop, not the class. for example:
```python
ps=PropertyShopFactory()
inv=ps.inventory()
```

### class method addProperty  (   
  ```cls,  # Note: cls is the class, not the instance.  
  name:str="YouForgotToAssignAPropertyName",  
  value=None,   # by default, addProperty will set it to the property name
  sc:callable=None,  
  gc:callable=None,   
  doc:str=None,   
  recalc:boolean=False,  
  recalcnewvalue:callable=lambda:0,  
  ) -> None:
  ```

**Purpose**: Adds one or more properties to the class.

**Args:**

#### **cls**:class   : NOT SPECIFIED BY THE USER!  Automatically added by python. Not specified by the caller.

#### **name**:str    : REQUIRED (Unless you like the silly default):

- Either:
	- -   The name, as a string, of one property to be added. It will be referenced without the quotes.  
               Example: name="myproperty"  # It will be be referred to as:   something.myproperty
	   
          or
	   
             A list, tuple, or set of one or more strings, each of which will be the name of a property.
	                All will have the same initial value, sc, gc, and recalc parameters
                Example: name=("i", "j", "k") will produce properties something.i, something.j, and something.k

#### **value**       : OPTIONAL: Initial value to be used to set the property.

  - DEFAULT: The property's name as a string

#### **sc:callable**: OPTIONAL: A callable **s**etter **c**ustomization function which is applied to the new value whenever the property is set or is initialized
  - DEFAULT: None
  - Regarding the sc callable:
  -- The callable will be called with one parameter, an incoming newvalue.
  -- The callable must return the value to actually be assigned to the parameter.
  -- Callable's Args: (Later, when it is called, not here in the call to addProperty.)
	- The newvalue as specified by an application's assigning a value to the property, for example, `aPropertyShop.aproperty=42`  
	- The callable Returns:
		 - The value to be actually set into the property
		 - Example:  `sc=float` # This will force the property to always be a float.


#### **gc:callable**: OPTIONAL: A callable **g**etter **c**ustomization function which is applied to the property's value when it is retrieved.
  - DEFAULT: None
  - Regarding the gc callable:
        The callable will be called with one parameter, the value stored in the property. 
        The callable must return a value. It will be returned as the property's externally visible value.
        Args: (Later, when it is called, not here in the call to addProperty.)
          The value of the property as retrieved by the getter.
       Returns:
          The value to be actually returned by the getter to the user of something=class.property
     - Example:  gc=str # This will force the getter to return a string representation of the property.

#### **doc:str**:       OPTIONAL: Docstring for the property. 
-  DEFAULT:  Will be set to the property's name.
            
    To retrieve the docstring: For a property added with:
```python
		ps=PropertyShopFactory()
		ps.addProperty("aproperty",doc="This property is my property.")
```

- Use either:
	 
```python
        xdoc=ps.propdoc("aproperty") # propdoc is a method of PropertyShop
        xdoc=ps.__class__.aproperty.__doc__
```

#### **recalc:boolean**:    OPTIONAL: Register that the property behaves like a spreadsheet cell that will be recalculated whenever set  or whenever the `recalculate()` method is invoked.
   - DEFAULT: False

#### **recalcnewvalue:callable**: A function used to set the newvalue when a property is recalculated.
- DEFAULT: `lambda : 0`
	- For each property to be recalculated, the recalculate method will invoke the setter with this callable, which takes no parameters. The invocation will be equivalent to:
	- `somePropertyshop.someproperty=recalcnewvalue()` 
	- The `addProperty` method saves this callable in a dictionary for `recalculate` to use.
	- The del method removes this from the dictionary as part of deleting the property, if it is there.
     
**Returns**: None

**Side effects:**

- Creates one or more properties by name with its setter, getter, deleter, and initial internal value.
 For each:
	- Sets an initial value, getter, setter, deleter, and doc.
   - Sets setter customization, if any.
   - Sets getter customization, if any.
   - Discards the property from or adds it to `recalculate()`'s recalculation set.
   - Discards a callable from a dictionary if present, or, for properties that can be recalculated by `recalculate()`, adds a callable to a dictionary.

**Examples: **
 See [Usage Examples](#usage-examples) below

### Method inventory (self)->list[lists]

List all the properties in the container.
             
**Args:**

#### **self**: NOT SPECIFIED BY THE USER!  Automatically added by python. Not specified by the caller.
             
**Returns:**
A list containing one element per property, with each element being a list containing:
- The property name
- The value as stored in the property
- The type of what is stored in the property
- The value as returned by the property's getter
- The type of the value returned by the property's getter
- The property's docstring.
- Whether or not the property is to be recalculated when recalculate is called: YesInRecalcset or NotInRecalcset
               
**Usage:** 

```python
	p=mypropertyshop.inventory()
```
           
### Method propdoc(self,name:str)->str

Report a property's docstring
             
**Args**: 
#### **Self**: NOT SPECIFIED BY THE USER!  Automatically added by python. Not specified by the caller.
                
#### **name**: The name of the property, as a string 
                
**Returns**:  The property's docstring
             
**Example**:
```python
	d=mypropertyshop.propdoc("b1")  # returns the __doc__ value within mypropertyshop.b1
```
            
- Alternative:
To get the docstring without using the property name in quotes as a string, use the following to get it directly.
```python 
    mypropertyshop.__class__.b1.__doc_
```


### Method propobj(self,name:str)->property
Return a property's object as it is in the Property Shop class. This method is present for debugging purposes, not for normal use.

**Warning**: Using this object does not invoke its setter or getter.
             
**Args**: 
#### *Self**: NOT SPECIFIED BY THE USER!  Automatically added by python. Not specified by the caller.
                
#### **name**: The name of the property, as a string 
                
**Returns**:  The property's property object
             
**Example**:
```python
	d=mypropertyshop.propobj("b1")  # returns the property object 
```

			
### Method  empty(self)
Remove all the properties from the PropertyShop 

**Args**: 
                
#### **Self**: NOT SPECIFIED BY THE USER!  Automatically added by python. Not specified by the caller.
                
**Returns**:  None
             
**Example**:
```python
        mypropertyshop.empty()   
```

###### Recalculate
### Method recalculate(self,ntimes)
Recalculate all the properties added with parameter `recalc=True`.The recalculations are done in sorting order by property name.  B2 is recalculated after B1z and before B20

**Args**: 
                
#### **Self**: NOT SPECIFIED BY THE USER!  Automatically added by python. Not specified by the caller.

#### **ntimes**: How many times to do the recalculation.
- DEFAULT: 1
  Why recalculate more than once? When the formula for A1 depends on B1, and the formula for B1 depends on C1, then it takes two recalculations for A1 to get the correct value.
                
**Returns**:  None
             
**Example**:
```python
    mypropertyshop.recalculate(2)   
```
     
## Persistence:
 
A  PropertyShop with any properties already added to it **cannot** be dumped by either pickle or dill. 
    
An empty PropertyShop, with no properties yet added can be dumped by dill. But why bother?
    
The PropertyShopFactory can be dumped with pickle and dill.  But why bother?

There has not been and there will not be any testing of using a PropertyShopFactory or an empty PropertyShop that has been loaded from a pickle or a dill.
          

## Usage examples:
### Beginning

```python
# import
from PropertyShop import PropertyShopFactory

# Create instances of two independent containers, named a and b
a= PropertyShopFactory()   # create an instance of a unique container class
b= PropertyShopFactory()   # create an instance of a different unique container class

# Create convenient aliases for each class's AddProperty method
a2a=a.addProperty
a2b=b.addProperty

# Create simple properties
a2b("somepropertyname")
a2a("i",123)  # a.i is initialized to value 123
a2b("i","246")  # b.i is initialized to value "246"
print(b.somepropertyname, a.i, b.i)

#Create multiple similar properties at once
#   The name=parameter of addProperty can take a list, set, or tuple.
#      In that case, it will add multiple similar properties in one call,
# all with the same initial value and other parameters.
a2b(['k','l',"m","n"],100,doc="added as one of several all at once")

# List the inventory of what is in the PropertyShops a dn b
for l in a.inventory() : print(l)
for l in b.inventory() : print(l)

# Get property values two ways:
# classinstanc.property   or  getattr(classinstance,"propertyname")
print( a.i, getattr(a,"i") )

# Set property values two ways:
#classinstance.property=newvalue   or    setattr(classinstance,"propertyname",newvalue)
b.somepropertyname="This is the forest primeval"
a.i = 3.14159265+len(b.somepropertyname)
a.i = setattr(a,"i", 3.14159265+len(b.somepropertyname) )

# Delete a property
del(b.i)

# Remove all the properties in PropertyShop b.
b.empty()
```

## Fancier usage:
### Customize setters and getters.

A major value of properties is that setting and getting them invokes a function that can do something, yet does not require parentheses.

It would be very useful if dynamic property creation software allowed the user to easily inject their own customizations into the getters and setters when the property is created.

This library enables doing those things as part of adding a property.

For setter and getter customizations, the examples mostly use lambda's, but a few use a separate function, sometimes in conjunction with a lambda. 

### Customize the property's setter

Customize the setter with the **optional** parameter sc (setter customization),
- sc must be a callable with signature  sc(setvalue:object) -> object  as in 
-- The parameter to the sc will be the newvalue in the assignment statement
       `apropertyshop.aproperty=newvalue`
-- `sc=lambda newvalue:newvalue` # is equivalent to, but slower than the default  `sc=None` . The default skips the customization.
-- The sc function or lambda can use variables, functions, methods, and other objects that will be in scope when executed.  Alternatively functools.partial can be used to create a function that has with preset parameters.

```python
# sc(value:object) -> object
alambda = lambda x: x+22
# or a lambda x:
def alambda(x):
  t= x+22 # or other expression, usually using x 
	      # but not necessarily, as we will see later.
  return t
b=PropertyShopFactory()
a2b=b.addProperty
a2b(name="propertyname",value=somevalue,sc=alambda) # where lambday is the lambda above
a2b(name="propertyname",value=somevalue,sc=lambda x: x+22)
```


**See examples below for:**

- An immutable-type setter producing a type-immutable property where the value can change, but not its type. The new value is cast to the property's defined type. 
- An immutable-value setter producing an immutable property whose value does not change even when set. 
- A property being replaced by with the same name, but a new definition.
- Properties with setter customizations so as to behave like spreadsheet cells with manual recalculation.
- Properties with setter customizations so as to behave like spreadsheet cells with manual recalculation, but which will be recalculated when the recalc function is called.
- Properties with getter customizations so as to behave like spreadsheet cells with automatic recalculation whenever retrieved.
- A property with getter customization so as to behave similar to an incrementing generator, It returns the next sequential value every time it is retrieved, without using `next( )`. The current value can be reinitialized to a new starting point. One example uses a `lambda`, while the other uses a `functools.partial`.
	
##### Immutable type
Immutable Type properties : The value can be set, but the type never changes.

Create Immutable-type properties by using setter customizations.

This is different from using the pydantic, typing, and typeguard libraries. 
- Those libraries **reject** assignment of a non-matching type by failing precompilation or by throwing an exception at runtime. The example here does not, as long as the new value can be cast to the property's type.

	- For example, create an immutably-int and an immutably-np.longdouble property.

```python
# assume that PropertyShops a,b, and functions a2a, and a2b have been created as above
        #  The setter customization invokes any available type casting function. All python-supplied types do casting.
   
        import numpy as np
        a2a('i',75.6,sc=np.int)     # add a property a.i with type int and value stored in a._i set to 75
        a2a('x',144,sc=np.longdouble) # add a property a.x with type np.longdouble and value stored in a._x set to 144.0
        print(a.i )                   # get i's value
        a.x = 44                      # set x's value to np.longdouble(44)
        a2b('x',"288",sc=int)         # add a property x to b with value stored in b._x set to int(288)
        b.x="144"                     # b.x=int("144") , which is 144
        z=a.x+a.i+b.x                 # use the properties
```

##### Immutable value
Create an immutable property by using setter customization.
The setter customization returns the immutable value no matter what any assignment statement sets it to.

 ```
         a2a("im1",sc=lambda x:"Initial immutable value")
         a.im1="I've changed!" # accomplishes nothing
         print(a.im1)
```

#### Replace a property
A property can be replaced, even if it has an immutable type or an immutable value, 
```
        # Completely replace a property with a new definition. 
        a2a("im1",sc=lambda x:"I've been replaced!")    
```

## Concepts: Programming code vs. Spreadsheets
Spreadsheets operate very differently from most programming code. 

In most programming languages, the sequence
```python
  x1=10
  y1=x1
  x1=20
```
results in y1 having the value 10. The statements were processed in sequence. y1 got its value while x1 was 10. The fact that x1 later changed has no effect on y1.

In a spreadsheet, the same sequence results in y1 having the value 20. 

Why? The spreadsheet recalculates the formulas, usually automatically. When x1 changes, so does y1.

Can we achieve similar things by exploiting properties? YES.

## Fancier usage examples - continued

### Create properties that behave very much like spreadsheet cells with manual recalculation.
The cell's formula goes into the **setter customization** in the call to add the property. It may be a lambda.

#### The formula's calculation happens whenever the property is initialized or assigned a value.

The cell's formula may access other cells, non-cell variables, functions, and even the setter's input newvalue. 

```python
# Spreadsheet cell examples:
# ss is short for spreadsheet. The property names mimic spreadsheet cell notation.
ss=PropertyShopFactory() 
a2ss=ss.addProperty # shorthand convenience
a2ss(["c1","c2","c3"]) # These will be simple values without formulas.
ss.c1,ss.c2,ss.c3=[1,2,3] # set them to numeric values
print(ss.c1,ss.c2,ss.c3)

lv=314.7 # a local variable
            
a2ss("s1",sc=lambda ignorednewvalue :20*ss.c1) # does not use the newvalue at all.
a2ss("s2",sc=lambda newvalue:2*ss.c1+newvalue) # uses the newvalue

ss.c1,ss.c2,ss.c3=[10,20,30] # set them to differrent numeric values
ss.s1=42 # causes ss.s1's formula to be recalculated. The formula ignores the newvalue.
ss.s2=700 # causes ss.s1's formula to be recalculated. The formula uses the newvalue.

```

#### Mass recalculation

The PropertyShop internally maintains a set containing the names of its properties which are to be recalculated when the PropertyShop's `recalculate` method is called. 

When a property is added with `addProperty`,  if the `recalc` optional parameter is set with `recalc=True`, then the property will be added to the PropertyShop's recalculation set.

When `recalculate` is invoked, it invokes the setter for each property in its recalculation set. When it invokes the setter, it must pass a newvalue to the setter. By default, `recalculate` passes to the setter `0` as the newvalue.

Recalculation Sequence: Properties are recalculated in sort order, by name, for example, A02, A195, A2, A20, A201, A21 


```python
# Examples: # continued from above        
a2ss("r1",sc=lambda newvalue:20*ss.c1,recalc=True) # The setter refers only to other cells. It does not use either the newvalue the cell's own current value at all.
a2ss("r2",sc=lambda newvalue:2*ss.c1+newvalue,recalc=True) # uses the newvalue and another cell. 
ss.r1=42 # causes ss.s1's formula to be recalculated. The formula ignores the newvalue.
ss.recalculate() #recalculate ss.r1 and ss.r2
```

##### Controlling what `recalculate()` uses as the newvalue for each assignment
Recalculate must perform the equivalent of `aproperty=newvalue` for each property it processes. What that newvalue will be can be customized for each property when the property is added.  

When a property is added with `recalc=True`, the `addProperty` saves the function specified or defaulting in the `recalcnewvalue` parameter.  Its defaults to`recalcnewvalue=lambda : 0`

##### Circular references
In spreadsheet terminology, a circular reference happens when a cell's formula refers to itself, whether directly (e.g. A1 refers to A1) or indirectly (e.g. A1refers to B1 which refers to C1 which refers to A1). As with some popular spreadsheet products, here too circular references are allowed. One iteration of the calculation happens per setting of the property. To avoid an exception, every property involved in a circular reference must be created first **without** any circular reference and only then can be redefined **with** the circular reference. An example below shows this.

```python
	# Example of circular references. Continued from above.
	a2ss(["s3","s4"],100) # must be already set with a value before any formula with a circular reference refers to them.
	a2ss("s3",1000,sc=lambda newvalue: ss.s3 + ss.s4 +12+2*ss.c1, recalc=True) # uses itself, a constant, and another cell in both a direct and an indirect circular reference, but does not use the newvalue.   
	a2ss("s4",0,sc=lambda newvalue:ss.s3 + ss.s4 + newvalue +3+2*ss.c1+lv, recalc=True) # uses a constant, the newvalue, a local variable, itself and other cells in both a direct and an indirect circular reference 
	ss.s3=22 # The newvalue, 22, is ignored by the setter's formula.
	ss.s4=22 # The newvalue, 22, is used by the setter's formula.
	ss.recalculate() #recalculates ss.s3 and ss.s4
```

**Note:** Circular references are permitted with setter customizations, as above., but not with getter customizations, below.


### Customize the property's getter

Customize the getter with the optional parameter **`gc`**(getter customization),
- If specified, the gc must be a callable with signature  gc(value:object) -> object
- The parameter to the gc will be the internal value of the property
- The following is the equivalent to not specifying **`gc`**.
	-  "piv" is short for "property internal value." 
	- `b.addProperty(name="propertyname",value=14,gc=lambda piv: piv)`
	-  This gc just passes out the property's internal value.
 
#### Create an alias or transformation
Customize the getter to create an alias or transformation of something else.
Examples:
 ```python
# assume that PropertyShops a,b, and functions a2a, and a2b have been created as above
a2b("x",3.14159265e20)  

# The following getter does does not refer to its own value at all!
# It returns the int of another property in another property shop.
a2a("bxasint",gc=lambda piv:int(b.x))
print(a.bxasint)

# The following adds itself + something else
a2a("pppbx",gc=lambda piv:piv+int(b.x)) 
a.pppx=2.718282e20
print (b.x,a.bxasint,a.pppx)
````
 
 #### Customize the getter using a regular function with and without a lambda. 
 
The getter customization can, but does not have to use a lambda. It can invoke a named function directly. 

##### Examples:

###### Simple: A simple getter customization function:
```python
def demogetter(piv):
      return f"{piv} has been customized by demogetter."

a2a("gf",75,gc=demogetter)
print(a.gf)
```

###### Generator-like: A function that enables a property to be incremented with each retrieval, like a generator object for sequential numbers, but without requiring using `next` syntax.

A property incrementor  function:
```python 
def pincrementor(piv,ps, pname:str):
   """
Property incrementor
A property getter customization function for a property to act like a generator which issues sequential numbers. 
The property's value is incremented every time the property's getter is called. 
Arguments:
    piv           The property's internal value being passed to the function.
    ps            The property shop instance such as ps 
    pname         The property name as a string such as "g2"
Example with a lambda: 
    ps.addProperty(pn:="g2",-1,gc=lambda x: pincrementor( x, ps , pn ) ) 
Example with a partial:
    from functools import partial
    pincrementorpsg3=partial(pincrementor,ps=ps ,pname=(pn:="g3"))
    aps(pn,-1,gc=pincrementorpsg3  )                             
   """
   newvalue=piv+1 # do not use 1+getattr(propertyshop,propertyname) which invokes the getter, causing a recursion exception! 
   setattr(ps,pname,newvalue)
   return newvalue  
```


When using this, either a lambda or a functools partial is required. Why? This function uses parameters in addition to the property's internal value (piv), but it will be invoked as a property getter which is passed only the piv.  The lambda or the partial provide ways to pass the other parameters. 

What is the difference between using a  lambda vs. functools.partial? **Parameter evaluation time**.
- The lambda evaluates all its parameters every time it is invoked. They have to be in scope and accessible.
- The partial evaluates the specified partial parameters when the partial is created. They only have to be visible and in scope at that time.

With the lambda:
```python
# With the lambda:
a2a(pn:="wl",-1,gc=lambda piv: pincrementor(piv, a ,pn) )  
print("generator analog",a.wl,a.wl,a.wl) # expect 0 1 2
```

Without the lambda, by using functools.partial:
```python
# Without the lambda, by using functools.partial:
from functools import partial
# create from pincrementor a partial function that prespecifies all the parameters other than the value. 
pincrementor4awp=partial(pincrementor,ps=a ,pname="wp")
a2a("wp",99,gc=pincrementor4awp) 
print("generator analog without lambda",a.wp,a.wp,a.wp ) # expect 100 101 102
```

By defining `pincrementor` this way, the same function can be used to create many independent incrementor properties.

######  Create properties that behave very much like spreadsheet cells with automatic recalculation.
The automatic recalculation cell's formula goes into **gc**, which is the get customization parameter of the call to add the property. It may be a lambda.

The cell will be recalculated every time the cell is accessed by the getter. If the getter refers to other "get customization" cells, they will in turn be recalculated themselves. Circular references will cause a recursion exception.

The formula may, but is not required to use the property's value.
```python
ss=PropertyShopFactory()
a2ss=ss.addProperty
a2ss(["v1","v2"])
a2ss("g1", 0, gc=lambda piv: ss.v1+ss.v2) # This getter does does not refer to its own value at all!
a2ss("g2", 1000, gc=lambda piv: piv + ss.v1 ) # this adds self + something else
ss.v1=120.1
ss.v2=240.2
print(ss.v1,ss.v2,ss.g1,ss.g2)
ss.v1=10
ss.v2=20
ss.g1=3.14159
ss.g2=100000
print(ss.v1,ss.v2,ss.g1,ss.g2)
```

**Warning**: **Circular references** are not allowed and do **not** work with getter customizations. They fail with: `RecursionError: maximum recursion depth exceeded.`

**NOTE**: Do not set `recalc=True` in the call to `add.Property` when using get recalculation, unless there is also a setter that needs to be recalculated. It is both unnecessary and not helpful.

#### It is, of course possible to exploit both setter customization and getter customization.
```python
a2ss("b1",12.34,sc=float,gc=str) # Always a float, but reports itself as a string.

a2ss("b2",12.34,sc=float,gc=lambda piv: [piv,t:=str(piv),len(t)]) # Always a float, but it reports itself as a list.

a2ss("b3",1234,sc=float,gc=lambda piv: f"ss.b3 is a type {type(piv)} with value {piv}")
print(ss.b1, ss.b2, ss.b3)
```

### Aliasing and copying a property 
#### Aliasing a property
A program can create an alias to a property in the same or other Property Shop.  
- That means that a program can set and get property alias a.b, but really be getting and setting property x.y.
- The alias can be created in one part of the program, and then used elsewhere.
- The `makealias` method must be invoked from the instance that has the existing property that is to be aliased. 'makealias` makes the alias in the same or in a different Property Shop 

Example:
```python
x=PropertyShopFactory()
a2x=x.addProperty
#Create property y in Property Shop x.
a2x("y",0,sc=lambda newvalue: newvalue+1) # the property gets 1 more than what you set it to.

a=PropertyShopFactory()
#Create an alias, a.b, of property x.y. Create it in class a. Set and get from an instance of a.
# x.makealias(propertyname:str,recipientPropertyShop,aliasname:str)
x.makealias("y",a,"b") # a.b will be an alias for x.y

x.y=10
a.b

a.b=20
x.y

```

If the original was on the recalculate list, the alias will also be, with the same newvalue processing as the original.

**Warning:** Deleting an alias and deleting a property having an alias are both not safe. Doing so can cause problems immediately or later, such as the program throwing an exception. This may change in version 1.0

#### [Deep]Copying a property to clone it: not feasible

A program cannot simply create an independent copy of a property in the same or other Property Shop.  The reason is that a property internally refers to, but does not contain a private variable in the original class. An independent copy would need to use an independent private variable. Even deepcopy cannot create and switch to using that.
This may change in version 1.0

### References, Citations and Acknowledgements

Thank you to the stackoverflow responders who quickly answered questions, even coding and providing examples.

https://stackoverflow.com/posts/1355444/revisions  
https://stackoverflow.com/questions/79481870/how-do-you-unwrap-a-python-property-to-get-attributes-from-the-getter/79482480#79482480
	 https://www.dropbox.com/scl/fi/vahot6oi1ddt3epasyyie/dynamic_properties_simple.py?rlkey=q8rqcpufdf4lva2y0ahmih798&e=1&dl=0
https://www.programiz.com/python-programming/property
https://docs.python.org/2/howto/descriptor.html#properties

https://realpython.com/python-property/
https://stackoverflow.com/questions/75050310/python-dynamically-add-properties-to-class-instance-properties-return-function
https://stackoverflow.com/questions/2954331/dynamically-adding-property-in-python
https://github.com/Infinidat/munch
https://docs.python.org/3/tutorial/classes.html
https://discuss.python.org/t/dynamic-generation-of-methods-for-a-class-from-a-list-of-names/14566/2
https://www.geeksforgeeks.org/classmethod-in-python/
https://www.programiz.com/python-programming/methods/built-in/classmethod
https://mgarod.medium.com/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
https://tush.ar/post/descriptors/
https://stackoverflow.com/questions/51866342/setter-ignored-when-property-is-assigned-to-variable-python-3-4
https://stackoverflow.com/questions/53323001/property-setter-not-called-in-python-3
https://stackoverflow.com/questions/19693993/python-property-being-ignored-acting-like-an-attribute
https://stackoverflow.com/questions/57811102/creating-class-properties-dynamically
https://stackoverflow.com/questions/33984487/pythonic-way-to-declare-multiple-class-instance-properties-as-numbers
https://stackoverflow.com/questions/27713264/dynamic-python-properties
https://stackoverflow.com/questions/77669846/is-there-a-way-to-type-hint-a-class-property-created-without-the-property-decora
https://www.freecodecamp.org/news/python-attributes-class-and-instance-attribute-examples/
https://stackoverflow.com/questions/7117892/how-do-i-assign-a-property-to-an-instance-in-python
https://stackoverflow.com/a/7118013/1496279

