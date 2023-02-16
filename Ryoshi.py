import customtkinter
import os
from os.path import basename
import smtplib
import ssl
from datetime import datetime
from PIL import Image
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tkinter import filedialog
import subprocess



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ryōshi.py")
        self.geometry(f"{1200}x{780}")
        self.resizable(False, False)
        customtkinter.set_appearance_mode("dark")  

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo_ryoshi.png")), size=(50, 50))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "mail_send_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "mail_send_white.png")), size=(30, 22))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "craft_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "craft_white.png")), size=(30, 22))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "verify_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "verify_white.png")), size=(30, 28))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Ryōshi", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Send Mail",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Craft Mail",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Verify Mail",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_label = customtkinter.CTkLabel(self.navigation_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(0, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)                                                            
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(80, 10))

        self.scaling_label = customtkinter.CTkLabel(self.navigation_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 35))
        self.scaling_optionemenu.set("100%")


        # -------------------------------------------- #

        # create send mail frame
        self.send_mail_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.send_mail_frame.grid(row=0, column=0, sticky="nsew")


        # -------------------------------------------- #

        # first line frame
        self.first_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.first_line_frame.grid_columnconfigure(4, weight=1)

        # label + entry mail smtp server
        self.label_mail_smtp_server = customtkinter.CTkLabel(master=self.first_line_frame, text="SMTP E-Mail:", justify=customtkinter.LEFT)
        self.label_mail_smtp_server.grid(row=0, column=0, pady=(20,0), padx=(20, 5))
        self.entry_mail_smtp_server = customtkinter.CTkEntry(master=self.first_line_frame, width=300)
        self.entry_mail_smtp_server.grid(row=0, column=1, pady=(20,0), padx=0)

        # label + entry password smtp server
        self.label_passsword_smtp_server = customtkinter.CTkLabel(master=self.first_line_frame, text="Password:", justify=customtkinter.LEFT)
        self.label_passsword_smtp_server.grid(row=0, column=2, pady=(20,0), padx=(20, 5))
        self.entry_passsword_smtp_server = customtkinter.CTkEntry(master=self.first_line_frame, show="\u25CF", width=300)
        self.entry_passsword_smtp_server.grid(row=0, column=3, pady=(20,0), padx=0)


        # -------------------------------------------- #

        # second line frame
        self.second_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.second_line_frame.grid_columnconfigure(5, weight=1)

        # label + entry smtp server
        self.label_smtp_server = customtkinter.CTkLabel(master=self.second_line_frame, text="SMTP Server:", justify=customtkinter.LEFT)
        self.label_smtp_server.grid(row=0, column=0, pady=0, padx=(20, 5))
        self.entry_smtp_server = customtkinter.CTkEntry(master=self.second_line_frame, width=300)
        self.entry_smtp_server.grid(row=0, column=1, pady=0, padx=0)

        # label + entry port smtp server
        self.label_port_smtp_server = customtkinter.CTkLabel(master=self.second_line_frame, text="Port:", justify=customtkinter.LEFT)
        self.label_port_smtp_server.grid(row=0, column=2, pady=0, padx=(20,5))
        self.entry_port_smtp_server = customtkinter.CTkEntry(master=self.second_line_frame, width=80)
        self.entry_port_smtp_server.grid(row=0, column=3, pady=0, padx=0)

        # button login smtp server
        def success_login():
            self.label_mail_smtp_server.configure(state="disabled")
            self.entry_mail_smtp_server.configure(state="disabled")
            self.label_passsword_smtp_server.configure(state="disabled")
            self.entry_passsword_smtp_server.configure(state="disabled")
            self.label_smtp_server.configure(state="disabled")
            self.entry_smtp_server.configure(state="disabled")
            self.label_port_smtp_server.configure(state="disabled")
            self.entry_port_smtp_server.configure(state="disabled")
            self.login_smtp_server.configure(state="disabled")
            self.from_name_label.configure(state="normal")
            self.from_name_entry.configure(state="normal")
            self.from_mail_label.configure(state="normal")
            self.from_mail_entry.configure(state="normal")
            self.subject_label.configure(state="normal")
            self.subject_entry.configure(state="normal")
            self.to_mail_label.configure(state="normal")
            self.to_mail_entry.configure(state="normal")
            self.cc_label.configure(state="normal")
            self.cc_entry.configure(state="normal")
            self.bcc_label.configure(state="normal")
            self.bcc_entry.configure(state="normal")
            self.HTML_checkbox.configure(state="normal")
            self.add_images.configure(state="normal")
            self.images_label.configure(state="normal")
            self.images_entry.configure(state="normal")
            self.add_attachments.configure(state="normal")
            self.attachments_label.configure(state="normal")
            self.attachments_entry.configure(state="normal")
            self.body_mail.configure(state="normal")
            self.body_mail.delete("0.0", "end")
            self.body_mail.insert("0.0", "Mail text here\n\n")
            self.send_mail_button.configure(state="normal")


        def login_smtp_server():
            smtp_server = self.entry_smtp_server.get()
            port = self.entry_port_smtp_server.get()
            login = self.entry_mail_smtp_server.get()
            password = self.entry_passsword_smtp_server.get()
            ssl_context = ssl.create_default_context()
            try:  
                s = smtplib.SMTP(smtp_server, port)
                s.starttls(context=ssl_context)
                s.login(login, password)
                success_login()      
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S')  + " - Login Successfully !\n")    
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")


        self.login_smtp_server = customtkinter.CTkButton(master=self.second_line_frame, text="Login", command=login_smtp_server, width=220)
        self.login_smtp_server.grid(row=0, column=4, pady=20, padx=(30,0))


        # -------------------------------------------- #

        # third line frame
        self.third_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.second_line_frame.grid_columnconfigure(6, weight=1)

        # label + entry "From name"
        self.from_name_label = customtkinter.CTkLabel(master=self.third_line_frame, text="From Name:", state="disabled")
        self.from_name_label.grid(row=0, column=0, pady=(20,0), padx=(20,5))
        self.from_name_entry = customtkinter.CTkEntry(master=self.third_line_frame, width=220, state="disabled")
        self.from_name_entry.grid(row=0, column=1, pady=(20,0), padx=0)

        # label + entry "From mail"
        self.from_mail_label = customtkinter.CTkLabel(master=self.third_line_frame, text="From Mail:", state="disabled")
        self.from_mail_label.grid(row=0, column=2, pady=(20,0), padx=(20,5))
        self.from_mail_entry = customtkinter.CTkEntry(master=self.third_line_frame, width=220, state="disabled")
        self.from_mail_entry.grid(row=0, column=3, pady=(20,0), padx=0)

        # label + entry "Subject"
        self.subject_label = customtkinter.CTkLabel(master=self.third_line_frame, text="Subject:", state="disabled")
        self.subject_label.grid(row=0, column=4, pady=(20,0), padx=(20,5))
        self.subject_entry = customtkinter.CTkEntry(master=self.third_line_frame, width=310, state="disabled")
        self.subject_entry.grid(row=0, column=5, pady=(20,0), padx=0)


        # -------------------------------------------- #

        # fourth line frame
        self.fourth_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.fourth_line_frame.grid_columnconfigure(7, weight=1)

        # label + entry "To mail"
        self.to_mail_label = customtkinter.CTkLabel(master=self.fourth_line_frame, text="To Mail:", state="disabled")
        self.to_mail_label.grid(row=0, column=0, pady=(20,0), padx=(20,5))
        self.to_mail_entry = customtkinter.CTkEntry(master=self.fourth_line_frame, width=220, state="disabled")
        self.to_mail_entry.grid(row=0, column=1, pady=(20,0), padx=0)

        # label + entry "CC"
        self.cc_label = customtkinter.CTkLabel(master=self.fourth_line_frame, text="CC:", state="disabled")
        self.cc_label.grid(row=0, column=2, pady=(20,0), padx=(20,5))
        self.cc_entry = customtkinter.CTkEntry(master=self.fourth_line_frame, width=220, state="disabled")
        self.cc_entry.grid(row=0, column=3, pady=(20,0), padx=0)

        # label + entry "BCC"
        self.bcc_label = customtkinter.CTkLabel(master=self.fourth_line_frame, text="BCC:", state="disabled")
        self.bcc_label.grid(row=0, column=4, pady=(20,0), padx=(20,5))
        self.bcc_entry = customtkinter.CTkEntry(master=self.fourth_line_frame, width=220, state="disabled")
        self.bcc_entry.grid(row=0, column=5, pady=(20,0), padx=0)

        # checkbox HTML
        self.HTML_checkbox = customtkinter.CTkCheckBox(master=self.fourth_line_frame, text="HTML", state="disabled")
        self.HTML_checkbox.grid(row=0, column=6, pady=(20, 0), padx=30)
        

        # -------------------------------------------- #

        # fivth line frame
        self.fivth_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.fivth_line_frame.grid_columnconfigure(8, weight=1)   

        # button "Add Images"
        def add_image():
            print("Images")

        self.add_images = customtkinter.CTkButton(master=self.fivth_line_frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="Add Image", command=add_image, state="disabled")
        self.add_images.grid(row=0, column=0, pady=(20,0), padx=(20,0))

        # label + entry disabled "Images"
        self.images_label = customtkinter.CTkLabel(master=self.fivth_line_frame, text="Images:", state="disabled")
        self.images_label.grid(row=0, column=1, pady=(20,0), padx=(10,5))
        self.images_entry = customtkinter.CTkEntry(master=self.fivth_line_frame, width=255, state="disabled")
        self.images_entry.grid(row=0, column=2, pady=(20,0), padx=0)

        # button "Add Attachment"
        attachments = []
        def add_attachment():
            file = filedialog.askopenfilename(title = "Select a File", filetypes = (("all files", "*.*"), ("all files", "*.*")))
            attachment = MIMEApplication(open(file, 'rb').read())
            filename = basename(file)
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            self.attachments_label.configure(state="normal")
            self.attachments_entry.configure(state="normal")
            self.attachments_entry.insert(0, filename + ", ")
            attachments.append(attachment)
            self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S')  + " - Add Attachment : " + filename + "\n")   
            

        self.add_attachments = customtkinter.CTkButton(master=self.fivth_line_frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="Add Attachment", command=add_attachment, state="disabled")
        self.add_attachments.grid(row=0, column=3, pady=(20,0), padx=(35,0))

        # label + entry disabled "Attachments"
        self.attachments_label = customtkinter.CTkLabel(master=self.fivth_line_frame, text="Attachments:", state="disabled")
        self.attachments_label.grid(row=0, column=4, pady=(20,0), padx=(10,5))
        self.attachments_entry = customtkinter.CTkEntry(master=self.fivth_line_frame, width=255, state="disabled")
        self.attachments_entry.grid(row=0, column=5, pady=(20,0), padx=0)

        
        # -------------------------------------------- #

        # sixth line frame
        self.sixth_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.sixth_line_frame.grid_columnconfigure(2, weight=1)  

        # body of the mail
        self.body_mail = customtkinter.CTkTextbox(master=self.sixth_line_frame, width=975, height=400, state="disabled")
        self.body_mail.grid(row=0, column=0, padx=20, pady=20)


        # -------------------------------------------- #

        # seventh line frame
        self.seventh_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.seventh_line_frame.grid_columnconfigure(3, weight=1)  

        # function "Send Mail"
        def send_mail():
            try: 
                msg = MIMEMultipart('mixed')
                sender = self.from_name_entry.get() + "<" + self.from_mail_entry.get() + ">"
                mailTo = self.to_mail_entry.get()
                mailCC = self.cc_entry.get()
                mailBCC = self.bcc_entry.get()
                subject = self.subject_entry.get()  
                recipients = mailTo.split(",") + mailCC.split(",") + mailBCC.split(",")
                formatMail = ''
                if self.HTML_checkbox.get() == 0:
                    formatMail = 'plain'
                else:
                    formatMail = 'html'
                msg['From'] = sender
                msg['To'] = mailTo
                msg['CC'] = mailCC
                msg['Subject'] = subject
                text = MIMEText(self.body_mail.get('0.0', 'end'), formatMail)
                msg.attach(text)
                for a in attachments:
                    msg.attach(a)
                print(msg)
                ssl_context = ssl.create_default_context()
                s = smtplib.SMTP(self.entry_smtp_server.get(), self.entry_port_smtp_server.get())
                s.starttls(context=ssl_context)
                s.login(self.entry_mail_smtp_server.get(), self.entry_passsword_smtp_server.get())
                s.sendmail(sender, recipients, msg.as_string())  
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Mail sent !\n")    
            except Exception as e:
                self.logs_textbox.insert("0.0", datetime.now().strftime('%H:%M:%S') + " - Error: "+str(e)+"\n")


        # Send mail button
        self.send_mail_button = customtkinter.CTkButton(master=self.seventh_line_frame, border_width=1, text="Send Mail", command=send_mail, width=270, height=55, state="disabled")
        self.send_mail_button.grid(row=0, column=0, pady=0, padx=20)

        # label + entry disabled "Results"
        self.logs_label = customtkinter.CTkLabel(master=self.seventh_line_frame, text="Logs:")
        self.logs_label.grid(row=0, column=1, pady=0, padx=(10,5))
        self.logs_textbox = customtkinter.CTkTextbox(master=self.seventh_line_frame, width=632, height=50)
        self.logs_textbox.grid(row=0, column=2, pady=0, padx=0)



        # https://www.youtube.com/watch?v=xB6u9zeRMpY
        # https://github.com/TomSchimansky/CustomTkinter/wiki/

        # https://support.google.com/mail/answer/1311182?hl=fr#null
        # https://support.google.com/mail/answer/81126
        # https://support.google.com/mail/answer/81126#auth-reqs

        # https://www.alibabacloud.com/help/en/directmail/latest/how-can-i-send-emails-with-attachments-using-smtp






        # -------------------------------------------- #

        # create craft frame
        self.craft_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.craft_frame.grid(row=0, column=0, sticky="nsew")






        # -------------------------------------------- #

        # create verify frame
        self.verify_mail_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.verify_mail_frame.grid(row=0, column=0, sticky="nsew")


        # -------------------------------------------- #

        # first line verify frame
        self.first_line_verify_frame = customtkinter.CTkFrame(self.verify_mail_frame, corner_radius=0, fg_color="transparent")
        self.first_line_verify_frame.grid_columnconfigure(3, weight=1)

        # label + entry verify mail
        self.label_verify_mail = customtkinter.CTkLabel(master=self.first_line_verify_frame, text="Mail to verify:", justify=customtkinter.LEFT)
        self.label_verify_mail.grid(row=0, column=0, pady=(20,0), padx=(20, 5))
        self.entry_verify_mail = customtkinter.CTkEntry(master=self.first_line_verify_frame, width=300)
        self.entry_verify_mail.grid(row=0, column=1, pady=(20,0), padx=0)

        # function verify mail
        def verify_mail():
            mail = self.entry_verify_mail.get()
            holehe_results = subprocess.getoutput("holehe " + mail + " --only-used").split('\n')
            results = '****************************************\n' + mail + '\n****************************************\n\n'
            found = 0
            for line in holehe_results:
                if line.startswith("[+]") and not line.startswith("[+] Email used"):
                    if found == 0:
                        results += "----- Mail found on: -----\n\n" + line + "\n"
                    else:
                        results += line + "\n"
                    found += 1
            if found == 0:
                results += "This mail seems to be wrong"
            self.results_holehe.delete("0.0", "end")
            self.results_holehe.insert("0.0", results) 

        # Verify button
        self.verify_button = customtkinter.CTkButton(master=self.first_line_verify_frame, border_width=1, text="Verify Mail", command=verify_mail)
        self.verify_button.grid(row=0, column=2, pady=(20,0), padx=20)


        # -------------------------------------------- #

        # second line verify frame
        self.second_line_verify_frame = customtkinter.CTkFrame(self.verify_mail_frame, corner_radius=0, fg_color="transparent")
        self.second_line_verify_frame.grid_columnconfigure(1, weight=1)  

        # image powered by Holehe
        self.holehe_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "holehe.png")), size=(600, 200))
        self.holehe_image_label = customtkinter.CTkLabel(self.second_line_verify_frame, text="", image=self.holehe_image)
        self.holehe_image_label.grid(row=0, column=1, padx=20, pady=(30,10))


        # -------------------------------------------- #

        # second line verify frame
        self.third_line_verify_frame = customtkinter.CTkFrame(self.verify_mail_frame, corner_radius=0, fg_color="transparent")
        self.third_line_verify_frame.grid_columnconfigure(1, weight=1) 

        # results of holehe
        self.results_holehe = customtkinter.CTkTextbox(master=self.third_line_verify_frame, width=975, height=400)
        self.results_holehe.grid(row=0, column=0, padx=20, pady=20)


        # -------------------------------------------- #





        # select default frame
        self.select_frame_by_name("send_mail")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "send_mail" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "craft_mail" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "verify_mail" else "transparent")

        # show selected frame
        if name == "send_mail":
            self.send_mail_frame.grid(row=0, column=1, sticky="nsew")
            self.first_line_frame.grid(row=1, column=1, sticky="nsew")
            self.second_line_frame.grid(row=2, column=1, sticky="nsew")
            self.third_line_frame.grid(row=3, column=1, sticky="nsew")
            self.fourth_line_frame.grid(row=4, column=1, sticky="nsew")
            self.fivth_line_frame.grid(row=5, column=1, sticky="nsew")
            self.sixth_line_frame.grid(row=6, column=1, sticky="nsew")
            self.seventh_line_frame.grid(row=7, column=1, sticky="nsew")
        else:
            self.send_mail_frame.grid_forget()
        if name == "craft_mail":
            self.craft_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.craft_frame.grid_forget()
        if name == "verify_mail":
            self.verify_mail_frame.grid(row=0, column=1, sticky="nsew")
            self.first_line_verify_frame.grid(row=1, column=1, sticky="nsew")
            self.second_line_verify_frame.grid(row=2, column=1, sticky="nsew")
            self.third_line_verify_frame.grid(row=3, column=1, sticky="nsew")
        else:
            self.verify_mail_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("send_mail")

    def frame_2_button_event(self):
        self.select_frame_by_name("craft_mail")

    def frame_3_button_event(self):
        self.select_frame_by_name("verify_mail")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scale = new_scaling.replace("%", "")
        new_scaling_float = int(new_scale) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        if new_scale == "80":
            self.geometry(f"{960}x{620}")
        elif new_scale == "90":
            self.geometry(f"{1100}x{700}")
        elif new_scale == "100":
            self.geometry(f"{1200}x{780}")
        elif new_scale == "110":
            self.geometry(f"{1320}x{850}")
        elif new_scale == "120":
            self.geometry(f"{1450}x{930}")
        


if __name__ == "__main__":
    app = App()
    app.mainloop()

