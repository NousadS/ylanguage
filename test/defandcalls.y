# Test: defining and calling variables, functions and classes #

def hello(name: str): {}
def hello(name: str) -> None: {}

class Name: {}
class Name(Hello): {}

class Name[T]: {}
class Name[T](Hello): {}

hello("John")

Name("John")

Name[str]("John")

boolean = true
null = none
sum = 1 + 2

name = John("Wow") + "Hello"

name.print("Hello")