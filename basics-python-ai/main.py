# printing
print("I am ready for office")
print("I am going to office", end=" ")
print("I am at office")
print("I am at the office at", 3, 14, " time")

"""
datatypes

"""

x = str(123)

print(type(x))

"""
custom variables
camelCase
"""

myName = "waqar"
myname = "a"

print(myName, myname)

"""
PascalCase
"""

MyName = "Waqar"

print(MyName)

"""
snake_case
"""
my_name = "Waqar"

print(my_name)

"""
kebab-obj key
"""

myObject = {"my-name": "A"}

print(myObject)

"""
unpacking
"""

myarr = [1, 2, 3, 4]
one, two, three, four = myarr


print("myarr", myarr, "vals:", one, two, three, four)


"""
multi assign
"""

okay = good = "okay or good"

print(okay, "g:", good)


"""
str and int donot work combining
"""

x = 5
y = "John"
print(y + str(x))


"""
global keyword
"""


def myfucn():
    global someval
    someval = "global val"


# lets assign global value
myfucn()
print(someval)


"""
global vs act. global
"""

actGlobal = "I am actual global"


def updater():
    global actGlobal
    actGlobal = "I am updated global"


print("actual global:", actGlobal)
updater()

print("updated global:", actGlobal)

"""

Text Type:	str
Numeric Types:	int, float, complex
Sequence Types:	list, tuple, range
Mapping Type:	dict
Set Types:	set, frozenset
Boolean Type:	bool
Binary Types:	bytes, bytearray, memoryview
None Type:	NoneType

"""


print("__name__")
print(__name__)
if __name__ == "__main__":
    print("I am running directly")
