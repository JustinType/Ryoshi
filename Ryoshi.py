import customtkinter
import os
from PIL import Image



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ryōshi.py")
        self.geometry(f"{1100}x{680}")
        self.resizable(False, False)
        customtkinter.set_appearance_mode("dark")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo_ryoshi.png")), size=(50, 50))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Ryōshi", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
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


        # create send mail frame
        self.send_mail_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.send_mail_frame.grid(row=0, column=0, sticky="nsew")

        # first line frame
        self.first_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.first_line_frame.grid_columnconfigure(4, weight=1)

        # label + entry mail smtp server
        self.label_mail_smtp_server = customtkinter.CTkLabel(master=self.first_line_frame, text="SMTP E-Mail:", justify=customtkinter.LEFT)
        self.label_mail_smtp_server.grid(row=0, column=0, pady=(20,0), padx=(20, 5))
        self.entry_mail_smtp_server = customtkinter.CTkEntry(master=self.first_line_frame, width=200)
        self.entry_mail_smtp_server.grid(row=0, column=1, pady=(20,0), padx=0)

        # label + entry password smtp server
        self.label_passsword_smtp_server = customtkinter.CTkLabel(master=self.first_line_frame, text="Password:", justify=customtkinter.LEFT)
        self.label_passsword_smtp_server.grid(row=0, column=2, pady=(20,0), padx=(20, 5))
        self.entry_passsword_smtp_server = customtkinter.CTkEntry(master=self.first_line_frame, show="\u25CF", width=200)
        self.entry_passsword_smtp_server.grid(row=0, column=3, pady=(20,0), padx=0)

        # second line frame
        self.second_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.second_line_frame.grid_columnconfigure(5, weight=1)

        # label + entry smtp server
        self.label_smtp_server = customtkinter.CTkLabel(master=self.second_line_frame, text="SMTP Server:", justify=customtkinter.LEFT)
        self.label_smtp_server.grid(row=0, column=0, pady=0, padx=(20, 5))
        self.entry_smtp_server = customtkinter.CTkEntry(master=self.second_line_frame, width=200)
        self.entry_smtp_server.grid(row=0, column=1, pady=0, padx=0)

        # label + entry port smtp server
        self.label_port_smtp_server = customtkinter.CTkLabel(master=self.second_line_frame, text="Port:", justify=customtkinter.LEFT)
        self.label_port_smtp_server.grid(row=0, column=2, pady=0, padx=(20,5))
        self.entry_port_smtp_server = customtkinter.CTkEntry(master=self.second_line_frame, width=60)
        self.entry_port_smtp_server.grid(row=0, column=3, pady=0, padx=0)

        # button login smtp server
        def button_callback():
            print("Button click")

        self.login_smtp_server = customtkinter.CTkButton(master=self.second_line_frame, text="Login", command=button_callback)
        self.login_smtp_server.grid(row=0, column=4, pady=20, padx=(30,0))

        # third line frame
        self.third_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.second_line_frame.grid_columnconfigure(8, weight=1)

        # label + entry "From mail"
        self.from_mail_label = customtkinter.CTkLabel(master=self.third_line_frame, text="From Mail:", justify=customtkinter.LEFT)
        self.from_mail_label.grid(row=0, column=0, pady=(20,0), padx=(20,5))
        self.from_mail_entry = customtkinter.CTkEntry(master=self.third_line_frame, width=150)
        self.from_mail_entry.grid(row=0, column=1, pady=(20,0), padx=0)

        # label + entry "To mail"
        self.to_mail_label = customtkinter.CTkLabel(master=self.third_line_frame, text="To Mail:", justify=customtkinter.LEFT)
        self.to_mail_label.grid(row=0, column=2, pady=(20,0), padx=(20,5))
        self.to_mail_entry = customtkinter.CTkEntry(master=self.third_line_frame, width=150)
        self.to_mail_entry.grid(row=0, column=3, pady=(20,0), padx=0)

        # label + entry "CC"
        self.cc_label = customtkinter.CTkLabel(master=self.third_line_frame, text="CC:", justify=customtkinter.LEFT)
        self.cc_label.grid(row=0, column=4, pady=(20,0), padx=(20,5))
        self.cc_entry = customtkinter.CTkEntry(master=self.third_line_frame, width=150)
        self.cc_entry.grid(row=0, column=5, pady=(20,0), padx=0)

        # label + entry "BCC"
        self.bcc_label = customtkinter.CTkLabel(master=self.third_line_frame, text="BCC:", justify=customtkinter.LEFT)
        self.bcc_label.grid(row=0, column=6, pady=(20,0), padx=(20,5))
        self.bcc_entry = customtkinter.CTkEntry(master=self.third_line_frame, width=150)
        self.bcc_entry.grid(row=0, column=7, pady=(20,0), padx=0)

        # fourth line frame
        self.fourth_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.fourth_line_frame.grid_columnconfigure(5, weight=1)

        # label + entry "Subject"
        self.subject_label = customtkinter.CTkLabel(master=self.fourth_line_frame, text="Subject:", justify=customtkinter.LEFT)
        self.subject_label.grid(row=0, column=0, pady=(20,0), padx=(20,5))
        self.subject_entry = customtkinter.CTkEntry(master=self.fourth_line_frame, width=300)
        self.subject_entry.grid(row=0, column=1, pady=(20,0), padx=0)

        # button "Add Attachment"
        def button_callback2():
            print("Button2 click")

        self.add_attachments = customtkinter.CTkButton(master=self.fourth_line_frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="Add Attachment", command=button_callback2)
        self.add_attachments.grid(row=0, column=2, pady=(20,0), padx=(20,0))

        # label + entry disbled "Attachments"
        self.attachments_label = customtkinter.CTkLabel(master=self.fourth_line_frame, text="Attachments:", justify=customtkinter.LEFT)
        self.attachments_label.grid(row=0, column=3, pady=(20,0), padx=(20,5))
        self.attachments_entry = customtkinter.CTkEntry(master=self.fourth_line_frame, width=200, state="readonly")
        self.attachments_entry.grid(row=0, column=4, pady=(20,0), padx=0)

        # fivth line frame
        self.fivth_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.fivth_line_frame.grid_columnconfigure(1, weight=1)   

        # body of the mail
        self.body_mail = customtkinter.CTkTextbox(master=self.fivth_line_frame, width=880, height=350)
        self.body_mail.grid(row=0, column=0, padx=20, pady=20)
        self.body_mail.insert("0.0", "Mail text here\n\n")

        # sixth line frame
        self.sixth_line_frame = customtkinter.CTkFrame(self.send_mail_frame, corner_radius=0, fg_color="transparent")
        self.sixth_line_frame.grid_columnconfigure(2, weight=1)  

        # button "Send Mail"
        def send_mail():
            print("Mail sent")
            
        self.add_attachments = customtkinter.CTkButton(master=self.sixth_line_frame, border_width=1, text="Send Mail", command=send_mail, width=880, height=40)
        self.add_attachments.grid(row=0, column=0, pady=0, padx=20)




        # https://www.youtube.com/watch?v=xB6u9zeRMpY
        # https://github.com/TomSchimansky/CustomTkinter/wiki/





        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("send_mail")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "send_mail" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "send_mail":
            self.send_mail_frame.grid(row=0, column=1, sticky="nsew")
            self.first_line_frame.grid(row=1, column=1, sticky="nsew")
            self.second_line_frame.grid(row=2, column=1, sticky="nsew")
            self.third_line_frame.grid(row=3, column=1, sticky="nsew")
            self.fourth_line_frame.grid(row=4, column=1, sticky="nsew")
            self.fivth_line_frame.grid(row=5, column=1, sticky="nsew")
            self.sixth_line_frame.grid(row=6, column=1, sticky="nsew")
        else:
            self.send_mail_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("send_mail")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        


if __name__ == "__main__":
    app = App()
    app.mainloop()

