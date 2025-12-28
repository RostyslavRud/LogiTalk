from customtkinter import *
from PIL import Image
from socket import*
import threading

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.main_font = ('Helvetica', 20, 'bold')

        self.left_frame = CTkFrame(self)
        self.left_frame.pack(side='left', fill='both')

        self.right_frame = CTkFrame(self, fg_color='white')
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side='right', fill='both', expand='True')

        self.left_frame = CTkFrame(self)
        self.left_frame.pack(side='left', fill='both')

        img_ctk = CTkImage(light_image=Image.open('bg.png'), size=(450, 400))
        self.img_label = CTkLabel(self.left_frame, text='Welcome', image=img_ctk, font=('Helvetica', 60, 'bold'))
        self.img_label.pack()

        self.right_frame = CTkFrame(self, fg_color='white')
        self.right_frame.pack(side='right', fill='both', expand='True')
        CTkLabel(self.right_frame, text='LogiTalk', font=self.main_font, text_color='#6753cc').pack(pady=60)

        self.name_entry = CTkEntry(self.right_frame, placeholder_text='@ ім\'я', height=45, font=self.main_font, corner_radius=25, fg_color='#eae6ff', border_color='#eae6ff', text_color='#6753cc',placeholder_text_color='#6753cc')
        self.name_entry.pack(fill='x', padx=10)

        self.register = CTkButton(self.right_frame, text='Зареєструватися', height=45, width=200, font=self.main_font, corner_radius=25, fg_color='#eae6ff', border_color='#eae6ff', text_color='#6753cc',command=self.registration)
        self.register.pack(padx = 20)

    def registration(self):
        name = self.name_entry.get()
        if not name:
            return
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect(('localhost', 8080))
            sock.send(name.encode())
        except:
            pass
        chat = ChatWindow(name, sock)
        self.destroy()
        chat.mainloop()

class ChatWindow(CTk):
    def __init__(self, name, sock,):
        super().__init__()
        self.name = name
        self.sock = sock
        self.geometry("500x500")
        self.title("chat")
        self.message_field = CTkTextbox(self, height=400, width=400, state= 'disable')
        self.message_field.pack()
        self.text_entry = CTkEntry(self, height = 30,width = 400)
        self.text_entry.pack(side = "bottom")
        self.send_button = CTkButton(self, height=30, width= 40, command=self.send_message, text=">")
        self.send_button.place(x=430, y=470)
        threading.Thread(target=self.recv_message).start()

    def add_message(self, message):
        self.message_field.configure(state='normal')
        self.message_field.insert(END, self.name + ': ' +  message + "\n")
        self.message_field.configure(state='disable')
    def send_message(self):
        global sock
        message = self.text_entry.get()
        self.text_entry.delete(0, END)
        if not message:
            return
        try:
            self.sock.send(message.encode())
        except:
            pass

    def recv_message(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                self.add_message(data)
            except:
                print('No message received!')






window = MainWindow()
window.mainloop()