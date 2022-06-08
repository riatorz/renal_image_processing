import pydicom

import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tkinter import *
import glob

file_paths=[]
os.chdir("./")
ct =0

#file_path = "CT0048.dcm"
print(file_paths)
file_path = "CT0040.dcm"

output_path = "/"

medical_image = pydicom.read_file(file_path)

print(medical_image)

image = medical_image.pixel_array

print(image.shape)

print(image.min())

print(image.max())

def transform_to_hu(medical_image, image):

    intercept = medical_image.RescaleIntercept
    
    slope = medical_image.RescaleSlope

    hu_image = image * slope + intercept



    return hu_image

def window_image(image, window_center, window_width):

    img_min = window_center - window_width // 2

    img_max = window_center + window_width // 2

    window_image = image.copy()

    window_image[window_image < img_min] = img_min

    window_image[window_image > img_max] = img_max



    return window_image

def thresholding(image,th_min,th_max):
    w_image = image.copy()
    w_image[w_image<th_min] = 255
    w_image[w_image>=th_max] = 1
    
    return w_image

def load_and_plot_image(file_path,x,y ,save=False):
    medical_image = pydicom.read_file(file_path)
    image = medical_image.pixel_array
    
    print(image.shape)
    
    hu_image = transform_to_hu(medical_image, image)
    kidney_image = window_image(hu_image, x, y) #92-93.5
    bone_image = window_image(hu_image, 400, 1000)
    th_image = thresholding(hu_image,x,y)

    print(th_image)

    plt.figure(figsize=(15, 5))
    plt.style.use('grayscale')

    plt.subplot(151)
    plt.imshow(image)
    plt.title('Original')
    plt.axis('off')

    plt.subplot(152)
    plt.imshow(hu_image)
    plt.title('Hu image')
    plt.axis('off')

    plt.subplot(153)
    plt.imshow(kidney_image)
    plt.title('Renal image')
    plt.axis('off')

    plt.subplot(154)
    plt.imshow(th_image)
    plt.title('Thresholded renal image')
    plt.axis('off')
    
    if save:
        mpimg.imsave(os.path.join(output_path, f'{file_path[:-4]}-original.png'), image)
        mpimg.imsave(os.path.join(output_path, f'{file_path[:-4]}-hu_image.png'), hu_image)
        mpimg.imsave(os.path.join(output_path, f'{file_path[:-4]}-brain_image.png'), kidney_image)
        mpimg.imsave(os.path.join(output_path, f'{file_path[:-4]}-bone_image.png'), bone_image)
def plot_images_all():
    # plt.figure(figsize=(15, 5))
    cx = 150
    for file in glob.glob(f"./dcm_exports/{dirLabel.cget('text')}/*.dcm"):
        print(file)
        medical_image = pydicom.read_file(file)
        image = medical_image.pixel_array
        print(image)
        # plt.style.use('grayscale')
        # plt.subplot(cx+1)
        # plt.imshow(image)
        # plt.title('Original')
        # plt.axis('on')

    # plt.show()

#Functions
def show_values():
    
    for i in listbox2.curselection():
        x = listbox2.get(i)
        print(listbox2.get(i))
        x1 = f"./dcm_exports/{dirLabel.cget('text')}/{x}"
        load_and_plot_image(x1,w1.get(),w2.get())
        plt.show()

# def show_values():
#     ct = 1
#     for i in listbox1.curselection():
#         print(listbox1.get(i))
def on_select():
    ct = 1
    print(listbox1.get(listbox1.curselection()[0]))
    for file in glob.glob(f".\\dcm_exports\\{listbox1.get(listbox1.curselection()[0])}/*.dcm"):
        fp = file.split("\\")
        listbox2.insert(ct,fp[3])
        ct+=1
        dirLabel.config(text=fp[2])
        print(file)

def list_all():
    #f(x,y,i)
    plot_images_all()


#Objects

master = Tk()
master.geometry('500x300')
##Trackbar
w1 = Scale(master, from_=0, to=1000, orient=HORIZONTAL)
w2 = Scale(master, from_=0, to=1000 , orient=HORIZONTAL)
##Buttons
bt = Button(master, text='Show', command=show_values,width=10)
bt_list_c = Button(master, text='Dosya değiştir', command=on_select,width=10)
bt_list_all = Button(master, text='list => f(x,y,i)', command=list_all,width=10)
##Labels
namelbl = Label(master, text="Names")
dirLabel = Label(master, text="Directory Name")
##ListBoxes
listbox1 = Listbox(
    master,
    listvariable=file_paths,
    height=8,
    selectmode='single')
ct = 1
for dir in os.listdir("./dcm_exports/./"):
    listbox1.insert(ct,dir)
    ct+=1
listbox2 = Listbox(
    master,
    listvariable=file_paths,
    height=8,
    selectmode='single')

# Grid

w1.set(118)
w1.grid(column=0,row=0,padx=10,pady=5,sticky=W)
w2.set(162)
w2.grid(column=0,row=1,padx=10,pady=2,sticky=W)

listbox1.grid(column=3,row=1,padx=30,pady=5,columnspan=2)
listbox2.grid(column=5,row=1,pady=5)

bt.grid(column=5,row=5,padx=10,pady=5)
bt_list_c.grid(column=3,row=5,padx=10,pady=5)
bt_list_all.grid(column=3,row=6,padx=10,pady=5)
namelbl.grid(column=3,row=0,padx=5,pady=5)
dirLabel.grid(column=5,row=0,pady=5)
master.mainloop()


#load_and_plot_image("CT0040.dcm")
plt.show()