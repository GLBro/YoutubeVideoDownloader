import io
import time
from tkinter import *
from pytube import *
from PIL import Image, ImageTk
import urllib.request, urllib
root = Tk()
root.geometry("300x450")

def updateToURL():
    global textBoxText, typeLabel,listBox,textBox,tellLabel
    textBoxText = "Enter URL: "
    typeLabel.config(text=textBoxText)
    listBox.delete(0, END)
    textBox.delete(0, END)
    tellLabel.config(text="")

def updateToSearch():
    global textBoxText, typeLabel, listBox, textBox,tellLabel
    textBoxText = "Search: "
    typeLabel.config(text=textBoxText)
    listBox.delete(0, END)
    textBox.delete(0, END)
    tellLabel.config(text="")

def downloadVideo():
    global videoStore,listBox, tellLabel
    for i in listBox.curselection():
        v = videoStore[i]
        stream = v.streams.first()
        stream.download("Videos")
        tellLabel.config(text="Download Complete")


def update(event):
    global videoStore
    tellLabel.config(text="")
    if (selected.get()==2):
        listBox.delete(0, END)
        s = Search(textBox.get())
        counter = 0
        videoStore.clear()
        for i in s.results:
            counter += 1
            element = i.title+" ("+i.author+")"
            listBox.insert(counter, element)
            videoStore.append(i)
    elif (selected.get()==1):
        listBox.delete(0, END)
        try:
            v = YouTube(textBox.get())
            element = v.title + " (" + v.author + ")"
            listBox.insert(1, element)
            imageUpdate(v.thumbnail_url)
            videoStore.append(v)
        except:
            element = "Could not find Video"
            listBox.insert(1, element)

def imageUpdate(url):
    global imageLabel,downButton
    urllib.request.urlretrieve(url, "image.jpg")
    with Image.open("image.jpg") as image:
        newImage = image.resize((100, 100))
        photo = ImageTk.PhotoImage(newImage)
        imageLabel.pack_forget()
        downButton.pack_forget()
        imageLabel = Label(root, image=photo)
        imageLabel.image = photo
        imageLabel.pack()
        downButton.pack()

def selectVideo(event):
    global videoStore
    for i in listBox.curselection():
        v = videoStore[i]
        imageUpdate(v.thumbnail_url)


videoStore = []
textBoxText = "Enter URL: "
typeLabel = Label(root, text=textBoxText)
textBox = Entry(root)
selected = IntVar()
urlMode = Radiobutton(root, text="URL Mode", variable=selected, value=1, command=updateToURL)
searchMode = Radiobutton(root, text="Search Mode", variable=selected, value=2, command=updateToSearch)
urlMode.pack()
searchMode.pack()
urlMode.invoke()
typeLabel.pack()
textBox.pack()
listBox = Listbox(root, width=20, height=10, bg="white", highlightcolor="red")
listBox.pack()
url = "https://lh3.googleusercontent.com/3zkP2SYe7yYoKKe47bsNe44yTgb4Ukh__rBbwXwgkjNRe4PykGG409ozBxzxkrubV7zHKjfxq6y9ShogWtMBMPyB3jiNps91LoNH8A=s500"
with urllib.request.urlopen(url) as u:
    data = u.read()
image = Image.open(io.BytesIO(data))
newImage = image.resize((100, 100))
photo = ImageTk.PhotoImage(newImage)
imageLabel = Label(root, image=photo)
imageLabel.pack()
downButton = Button(root, text="Download", command=downloadVideo)
downButton.pack()
tellLabel = Label(root, text="")
tellLabel.pack()
root.bind("<KeyPress>", update)
listBox.bind("<<ListboxSelect>>", selectVideo)
root.mainloop()
