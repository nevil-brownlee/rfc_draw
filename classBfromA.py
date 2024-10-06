# https://stackoverflow.com/questions/3856413/call-class-method-from-another-class

class Test1(object): # always inherit from object in 2.x. it's called new-style classes. look it up
    s = "cats&dogs"

    def method1(self, a, b):  # self is the caller's environment
        print("self =%s, s = %s" % (self, self.s))
        self.xxx = "xxx"
        return a + b

    @staticmethod
    def method2(a, b):  # No cls argument
        return a + b

    @classmethod
    def method3(cls, a, b):
        print("classmethod, cls = %s (%s)" % (cls, type(cls)))
        return cls.method2(a, b)

t = Test1()  # same as doing it in another class

print(Test1.method1(t, 1, 2)) #form one of calling a method on an instance
print(t.method1(1, 2))        # form two (the common one) essentially reduces to form one
print(" @@@ t.xxx = %s" % t.xxx)

"""
print(Test1.method2(1, 2))  #the static method can be called with just arguments
print(t.method2(1, 2))      # on an instance or the class
print()

print(Test1.method3(1, 2))  # ditto for the class method. It will have access to the class
print(t.method3(1, 2))      # that it's called on (the subclass if called on a subclass) 
"""




"""
class ClassA:
    #  @staticmethod

    def __init__(self, p1, p2):
        self.xyz = "xyz"
        self.p1 = p1;  self.p2 = p2
        
        def method_in_class_a(self, p1):
            print("Method in ClassA, p1 %s" % p1)
            print("  > class_a  > self.xyz %s" % self.xyz)
            print("  > class_a  > self %s" % self)
 
class ClassB:
    def __init__(self, p1, p2):
        self.xyz = "xyz"
        self.p1 = p1;  self.p2 = p2

    def call_method_from_class_a(self, a, b):
        #ClassA.method_in_class_a(self, "abc")
        ClassA.method_in_class_a(self, a, b)
        print("Method in ClassB")
 
# Create an instance of ClassB
obj_b = ClassB("Bp1", "Bp2")
print(" - * - ") 
# Call the method in ClassB, which in turn calls the method in ClassA
obj_b.call_method_from_class_a("xa", "xb")
"""
