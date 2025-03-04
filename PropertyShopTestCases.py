#!/bin/python3.12
"""
©2025 David A. Kra dakra137@gmail.com  This work is openly licensed with Creative Commons CC BY-SA 4.0 license
                                       https://creativecommons.org/licenses/by-sa/4.0/
Test Cases for PropertyShop 
https://github.com/dakra137/PropertyShopPrivate/blob/main/PropertyShopTestCases.py
uses https://github.com/dakra137/PropertyShopPrivate/blob/main/PropertyShop.py 
"""
if __name__ == "__main__":
    from PropertyShop import PropertyShopFactory
    ps=PropertyShopFactory()
    aps=ps.addProperty
   
    def pincrementor(x,ps, pname:str):
        """
        Property incrementor
        A property getter customization function for property ps.g2 to act like a generator which issues sequential numbers. 
        The property's value is incremented every time the property's getter is called. 
        Arguments:
            x             The property's internal value being passed to the function.
            ps            The property shop instance such as ps 
            pname         The property name as a string such as "g2"
        Example with a lambda: 
                          ps.addProperty(p:="g2",-1,gc=lambda x: pincrementor( x, ps , p ) ) 
        Example with a partial:
                          from functools import partial
                          pincrementorpsg3=partial(pincrementor,ps=ps ,pname=(pn:="g3"))
                          aps(pn,-1,gc=pincrementorpsg3  )                             
        """
        newvalue=x+1 # do not use 1+getattr(propertyshop,propertyname) which invokes the getter, causing a recursion exception! 
        setattr(ps,pname,newvalue)
        return newvalue  

  
    aps(p:="g",-1,gc=lambda x: pincrementor( x, ps ,p) ) 
    ps.g=-1
    print("generator analog using pincrementor with a lambda",ps.g, ps.g,ps.g) # expect 0 1 2

    from functools import partial
    pincrementorpsgp=partial(pincrementor,ps=ps ,pname=(pn:="gp"))
    aps(pn,99,gc=pincrementorpsgp  ) # for a different property shop, change the ps parameter
    print("generator analog ps.gp with a partial ",ps.gp, ps.gp,ps.gp) # expect 100 101 102

    print(f" propobj's g {ps.propobj('g')} ,  gp {ps.propobj('gp')} ")

    #aps("g3",399 )    
    incrementorpsg3 = partial(pincrementor, ps=ps, pname="g3") #aproperty as it is at this moment
    aps("g3",399,gc=incrementorpsg3 )  
    print("generator analog using pincrementor with a partial ",ps.g3, ps.g3,ps.g3) # expect 400,401,402
    
    aps("r1","r1 was recalculated",recalc=False)
    aps("r2",10)
    aps("r2",10,sc=lambda x: ps.r2+1,recalc=True)

    a=PropertyShopFactory()
    x=PropertyShopFactory()
    a2a=a.addProperty
    a2x=x.addProperty
    a2a(["a","b"],10)
    a2x(["y","z"],"a string")
    
    print("ps = ",ps.inventory() )
    print("a = ",a.inventory() )
    print("x = ", x.inventory() )
    print ("Use Property Shops: ps, a, and x." )

    for i in range(3):
        print(f"{i} : {ps.r1} {ps.r2}" )
        ps.recalculate()

    print(f"recalcset: {ps.__class__.recalcset}")       
    del(ps.r1)
    print(f"recalcset: {ps.__class__.recalcset}") 
    
    lv=314.7
    ss=PropertyShopFactory()
    a2ss=ss.addProperty
    a2ss(["v1","v2","v3"]) # simple values with defaults
    ss.v1,ss.v2,ss.v3=[1,2,3]
    print(ss.v1,ss.v2,ss.v3)
    a2ss("s1",sc=lambda newvalue:2*ss.v1) # does not use the newvalue at all.
    a2ss("s2",0,sc=lambda newvalue:2*ss.v1+newvalue) # uses the newvalue
    a2ss("s3",100) # must be already set if there will be a self reference.
    a2ss("s3",1000,sc=lambda newvalue:2*ss.v1+newvalue+ss.s3) # uses both the newvalue and itself in a circular reference.
    a2ss("s4",0,sc=lambda newvalue:2*ss.v1+newvalue+lv) # use local variable in the formula
    ss.s1=22
    ss.s2=23
    ss.s3=24
    print(ss.s1,ss.s2,ss.s3,ss.s4)
    lv=3314.7
    ss.s4=0
    ss.s3=10000
    print(ss.s1,ss.s2,ss.s3,ss.s4)
    ss.v1=12
    ss.s1=0 # set it to anything to recalculate. this formula does not use the setting input value
    ss.s2=23 # recalculate with the same new value
    ss.s3=10000 # uses old and new value
    print(ss.s1,ss.s2,ss.s3,ss.s4)


    #a2ss=ss.addProperty
    a2ss("g1", 0, gc=lambda pv: ss.v1+ss.v2) # This getter does does not refer to its own value at all!
    a2ss("g2", 1000, gc=lambda pv: pv + ss.v1 ) # this adds self + something else
    ss.v1=120.1
    ss.v2=240.2
    print(ss.v1,ss.v2,ss.g1,ss.g2)
    ss.v1=10
    ss.v2=20
    ss.g1=3.14159
    ss.g2=100000
    print(ss.v1,ss.v2,ss.g1,ss.g2)
    a2ss("b1",12.34,sc=float,gc=str, doc="b1 custom doc\n")
    a2ss("b2",12.34,sc=float,gc=lambda pv: [pv,t:=str(pv),len(t)])
    a2ss("b3",1234,sc=float,gc=lambda pv: f"ss.b3 is a type {type(pv)} with value {pv}")
    ss.b3="2468.3"
    print(ss.b1, ss.b2, ss.b3)
    print(type(ss).b2.__doc__)
    print(ss.b1, type(ss.b1), type(ss).b1.__doc__, type(type(ss).b1),  type(ss), type(type(ss)))
    for item in ss.inventory(): print(item)
    print("ss.propdoc('b1')" , ss.propdoc('b1') )
    print("type(ss).b1.__doc__", type(ss).b1.__doc__)
    print("ss.__class__.b1.__doc__", ss.__class__.b1.__doc__)
    
    a2ss("im1",sc=lambda x:"immutable value")
    print(ss.im1)
    ss.i1="I changed"
    print(ss.im1) # no it did not
    a2ss("im1",sc=lambda x:"I've been replaced!") 
    print(ss.im1)
    for item in ss.inventory(): print(item)
    ss.empty()
    print(" after emptying :")
    for item in ss.inventory(): print(item)
       
    import numpy as np
    v=PropertyShopFactory() # v is an instance of a unique class.
    print("created v, ",v, " with type=",type(v)," and id=",id(v))
    v.addProperty('i',1024.1024,sc=np.int64)
    print(v.i)

    w=PropertyShopFactory() # w is an instance of a different unique class.
    print("created w with type=",type(w)," and id=",id(w))

    w.addProperty(['k','l',"m","n"],100,sc=np.longdouble) #np.int64) #np.longdouble)
    w.k=30100
    w.l=np.longdouble(1)/np.longdouble(3)
    print(w.k,w.l,w.m,w.n, w.k+w.l+w.m+w.n)
    print([type(x) for x in (w.k,w.l,w.m,w.n)])

    w.k=3.14e20
    w.addProperty("intk",gc=lambda x:int(w.k))
    print (w.k,w.intk)

    # Create two independent containers a and b
    a= PropertyShopFactory()   # create an instance of a unique container class
    b= PropertyShopFactory()         # create an instance of a different unique container class

    # Create convenient aliases for each class's AddProperty method
    a2a=a.addProperty
    a2b=b.addProperty

    # Create customized getters
    a2b("x",3.14159265e20,sc=float)
    a2a("x",gc=lambda pv:int(b.x)) # This getter does does not refer to its own value at all!
    a2a("pvpx",gc=lambda pv:pv+int(b.x)) # this adds self + something else
    a.pvpx=2.718282e20
    print (b.x,a.x,a.pvpx)

    print("\n")
    c=PropertyShopFactory()
    a2c=c.addProperty
    a2c("p1")
    a2c("p2","1.6")
    a2c("p3",12.6,int)
    a2c("p4",123.6,int,float)
    print(c.p1,c.p2,c.p3,c.p4)
    c.p3=16
    print(c.p1,c.p2,c.p3,c.p4)

    w.addProperty('x',144,sc=np.longdouble)
    print("\n dir(w.x) = ", dir(w.x), "\n" )#, w.x.getter)         #, w.x.fget.__code__  w.x.fget, )
    print("w.x ",w._x, type(w._x), w._x , w.x, type(w.x))# , w.x.fget() )
    w.x=176.6
    print("w.x ",w._x, type(w._x), w._x , w.x, type(w.x)) #, w.x.fget() )
    w.x=277.7
    w.i=77
    w.addProperty('i',144,sc=np.longdouble)
    print("w.x ",w._x, type(w._x), w._x , w.x, type(w.x)) #, w.x.fget() )
    print("w.i ",w._i, type(w._i), w._i         , w.i, type(w.i)) #, w.x.fget() )

    """
    import dill 
    
    with open('PropertyShopFactory.dill', 'wb') as f:  
      dill.dump(PropertyShopFactory, f) 
       
    p=PropertyShopFactory()
    
    with open('PropertyShop.p0.dill', 'wb') as f:  
      dill.dump(p, f) 
 
    a2p=p.addProperty
      
    a2p("trivial","trivial")
    print (p.inventory())

    print(p.__class__.trivial)
    quit()
    
    with open('PropertyShop.p.trivial.dill', 'wb') as f:  # open a text file
      dill.dump(p.__class__.trivial, f)   
    """
 



