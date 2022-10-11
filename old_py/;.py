
from tkinter import *
from old_py import numpy as np
import matplotlib.pyplot as plt


root = Tk()
root.title('Snir\'s Panel')
root.iconbitmap('C:/Users/sodedx/Downloads/images.ico')


def graph():
    house_prices = np.random.normal(200000, 25000, 5000)
    # plt.hist(house_prices, 1000)
    plt.polar(house_prices)
    #plt.pie(house_prices)
    plt.show()


my_button = Button(root, text="graph it", command=graph)
my_button.pack()
root.mainloop()