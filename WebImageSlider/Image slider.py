from itertools import cycle
from PIL import Image,ImageTk
import time
import tkinter as tk

root=tk.Tk()
root.title("Image Slideshow reviewer")

image_path=[
    r"E:\future is now\Screenshot (270).png",
    r"E:\future is now\Screenshot (271).png",
    r"E:\future is now\Screenshot (272).png",
    r"E:\future is now\Screenshot (273).png",
    r"E:\future is now\Screenshot (274).png",
    r"E:\future is now\WhatsApp Image 2025-07-04 at 14.01.04_6c08df4f.jpg",
    r"E:\future is now\WhatsApp Image 2025-07-24 at 17.12.05_bf846b7c.jpg",
    r"E:\future is now\WhatsApp Image 2025-08-03 at 15.49.56_5bb179ae.jpg",
]


image_size=(1080,1080)
images=[Image.open(path).resize(image_size) for path in image_path]
photo_images=[ImageTk.PhotoImage(image) for image in images]

label=tk.Label(root)
label.pack()

def update_image():
    for photo_image in photo_images:
        label.config(image=photo_image)
        label.update()
        time.sleep(3)


slideshow=cycle(photo_images)


def start_slideshow():
    for _ in range(len(image_path)):
        update_image()


play_button=tk.Button(root,text="play",command=start_slideshow)
play_button.pack()

root.mainloop()
