

class Animal:
    def __init__(self, color, legs):
        self.color = color
        self.legs = legs

class Cat:
    def pure(self):
        print("Purr..")
class Dog:
    def pure(self):
        print("Waff..")


yossi = Dog()
hatul = Cat()


# print("\nyossi have a " + yossi.color+" color and sounds: "+yossi.bark()+" and he has"+yossi.legs+ " legs!")
# print("\nhatul have a " + hatul.color+" color and sounds: "+hatul.pure()+" and he has"+hatul.legs+ " legs!")

yossi.pure()
hatul.pure()
