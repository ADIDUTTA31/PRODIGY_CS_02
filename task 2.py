import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

# Initialize main window
window = tk.Tk()
window.geometry("1000x700")
window.title("Image Encryption Decryption")

# Global variables
x = None
panelA = None
panelB = None
eimg = None
image_encrypted = None
key = None

# Utility functions
def getfilename(path):
    return os.path.splitext(os.path.basename(path))[0]

def openfilename():
    return filedialog.askopenfilename(title='Open', filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

def open_img():
    global x, panelA, panelB, eimg
    x = openfilename()
    if x:
        img = Image.open(x)
        eimg = img.copy()
        img_tk = ImageTk.PhotoImage(img)

        if panelA is None:
            panelA = tk.Label(image=img_tk)
            panelA.image = img_tk
            panelA.pack(side="left", padx=10, pady=10)

            panelB = tk.Label(image=img_tk)
            panelB.image = img_tk
            panelB.pack(side="right", padx=10, pady=10)
        else:
            panelA.configure(image=img_tk)
            panelB.configure(image=img_tk)
            panelA.image = img_tk
            panelB.image = img_tk
    else:
        messagebox.showwarning("Warning", "No image selected.")

def en_fun(path):
    global image_encrypted, key
    if not path:
        messagebox.showwarning("Warning", "No image selected.")
        return
    image_input = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image_input is not None:
        image_input = image_input.astype(float) / 255.0
        mu, sigma = 0, 0.1
        key = np.random.normal(mu, sigma, image_input.shape) + np.finfo(float).eps
        image_encrypted = image_input / key
        encrypted_img = (image_encrypted * 255).astype(np.uint8)
        cv2.imwrite('image_encrypted.jpg', encrypted_img)
        imge = Image.open('image_encrypted.jpg')
        imge_tk = ImageTk.PhotoImage(imge)
        panelB.configure(image=imge_tk)
        panelB.image = imge_tk
        messagebox.showinfo("Encrypt Status", "Image Encrypted successfully.")

def de_fun():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        image_output = (image_output * 255.0).clip(0, 255).astype(np.uint8)
        cv2.imwrite('image_output.jpg', image_output)
        imgd = Image.open('image_output.jpg')
        imgd_tk = ImageTk.PhotoImage(imgd)
        panelB.configure(image=imgd_tk)
        panelB.image = imgd_tk
        messagebox.showinfo("Decrypt Status", "Image decrypted successfully.")
    else:
        messagebox.showwarning("Warning", "Image not encrypted yet.")

def reset():
    global x, eimg
    if x:
        img = Image.open(x)
        eimg = img.copy()
        img_tk = ImageTk.PhotoImage(img)
        panelB.configure(image=img_tk)
        panelB.image = img_tk
        messagebox.showinfo("Success", "Image reset to original format!")
    else:
        messagebox.showwarning("Warning", "No image selected.")

def save_img():
    global eimg
    if eimg:
        file = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file:
            eimg.save(file.name)
            messagebox.showinfo("Success", "Image Saved Successfully!")
    else:
        messagebox.showwarning("Warning", "No image to save.")

def download_encrypted():
    global image_encrypted
    if image_encrypted is not None:
        file = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file:
            encrypted_img = (image_encrypted * 255).clip(0, 255).astype(np.uint8)
            cv2.imwrite(file.name, encrypted_img)
            messagebox.showinfo("Success", "Encrypted Image Downloaded Successfully!")
    else:
        messagebox.showwarning("Warning", "No encrypted image to download.")

def download_decrypted():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        image_output = (image_output * 255.0).clip(0, 255).astype(np.uint8)
        file = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file:
            cv2.imwrite(file.name, image_output)
            messagebox.showinfo("Success", "Decrypted Image Downloaded Successfully!")
    else:
        messagebox.showwarning("Warning", "No decrypted image to download.")

def exit_win():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# UI Layout
tk.Label(text="Image Encryption\nDecryption", font=("Arial", 40), fg="magenta").place(x=350, y=10)
tk.Label(text="Original\nImage", font=("Arial", 40), fg="magenta").place(x=100, y=270)
tk.Label(text="Encrypted\nDecrypted\nImage", font=("Arial", 40), fg="magenta").place(x=700, y=230)

tk.Button(window, text="Choose", command=open_img, font=("Arial", 20), bg="orange", fg="blue").place(x=30, y=20)
tk.Button(window, text="Save", command=save_img, font=("Arial", 20), bg="orange", fg="blue").place(x=170, y=20)
tk.Button(window, text="Encrypt", command=lambda: en_fun(x), font=("Arial", 20), bg="light green", fg="blue").place(x=150, y=620)
tk.Button(window, text="Decrypt", command=de_fun, font=("Arial", 20), bg="orange", fg="blue").place(x=450, y=620)
tk.Button(window, text="Reset", command=reset, font=("Arial", 20), bg="yellow", fg="blue").place(x=800, y=620)

tk.Button(window, text="Download Encrypted", command=download_encrypted, font=("Arial", 15), bg="light blue", fg="blue").place(x=30, y=670)
tk.Button(window, text="Download Decrypted", command=download_decrypted, font=("Arial", 15), bg="light blue", fg="blue").place(x=220, y=670)

tk.Button(window, text="EXIT", command=exit_win, font=("Arial", 20), bg="red", fg="blue").place(x=880, y=20)

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()
