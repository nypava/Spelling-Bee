import customtkinter
from config import *
from threading import Thread
from PIL import Image 
from utilities.helpers import *
import telebot 
from config import *
import tkinter

# Global variables
MESSAGE = None
START = True
BOT = None
INDEXNUMBER = 0
FINAL = False
RESET = True

# Main Game page
class MainFrame(customtkinter.CTkFrame):
    '''
    Main frame which contain the main Game lable.
    '''
    def __init__(self, parent):
        global BOT

        # Import init function from CTKFRAME
        super().__init__(parent)

        # Change colors and pack it to the main window
        self.configure(bg_color="#1D1F1E", fg_color="#1D1F1E")
        self.pack(side="top", ipady=1000, ipadx=1000)

        # Letter variable
        self.letters_font = customtkinter.CTkFont(size=55, weight='bold')

        self.content()

    def content(self):
        # Make and place hexagonal image
        self.hexa_image = customtkinter.CTkImage(dark_image=Image.open("images/Base.png"), size=(352.8,354.9))
        self.hexa_lable = customtkinter.CTkLabel(self, image=self.hexa_image, fg_color="transparent", text=None)
        self.hexa_lable.place(relx=0.38, rely=0.05)

        # Call letters function
        self.letters()

        # Make Button
        self.next_image = customtkinter.CTkImage(dark_image=Image.open("images/Next-button.png"), size=(100.1,100.1))
        self.next_lable = customtkinter.CTkButton(self, image=self.next_image, fg_color="transparent", text=None,hover=True,hover_color="#1D1F1E",command=self.spellingChanged)
        self.next_lable.place(relx=0.63, rely=0.2)

    def letters(self):
        global INDEXNUMBER

        # Assign each letters that appears to hexagonal image
        middle,letter_1,letter_2,letter_3,letter_4,letter_5,letter_6 = jsonManager().getSpelling(INDEXNUMBER)
    
        # Make letters and place them.
        self.letter1 = customtkinter.CTkLabel(self.hexa_lable, text=letter_1, font=self.letters_font, width=60, text_color="#F5F5F5", fg_color="#2C2E2D", bg_color="#2C2E2D")
        self.letter1.place(relx=0.414, rely=0.06)

        self.letter2 = customtkinter.CTkLabel(self.hexa_lable, text=letter_2, font=self.letters_font, text_color="#F5F5F5", bg_color="#2C2E2D", fg_color="#2C2E2D", width=60)
        self.letter2.place(relx=0.72, rely=0.24)

        self.letter3 = customtkinter.CTkLabel(self.hexa_lable, text=letter_3, font=self.letters_font, bg_color="#2C2E2D", text_color="#F5F5F5", fg_color="#2C2E2D", width=60)
        self.letter3.place(relx=0.725, rely=0.58)

        self.letter4 = customtkinter.CTkLabel(self.hexa_lable, text=letter_4, font=self.letters_font, bg_color="#2C2E2D", text_color="#F5F5F5", fg_color="#2C2E2D", width=60)
        self.letter4.place(relx=0.414, rely=0.75)

        self.letter5 = customtkinter.CTkLabel(self.hexa_lable, text=letter_5, font=self.letters_font, bg_color="#2C2E2D", text_color="#F5F5F5", fg_color="#2C2E2D", width=60)
        self.letter5.place(relx=0.11, rely=0.58)

        self.letter6 = customtkinter.CTkLabel(self.hexa_lable, text=letter_6, font=self.letters_font, bg_color="#2C2E2D", text_color="#F5F5F5", fg_color="#2C2E2D", width=60)
        self.letter6.place(relx=0.11, rely=0.24)
        
        self.middle = customtkinter.CTkLabel(self.hexa_lable, text=middle, font=self.letters_font, bg_color="yellow", text_color="black", fg_color="yellow", width=60)
        self.middle.place(relx=0.414, rely=0.41)
        
        # Call rankFrame function
        self.pointFrame()
    
    def pointFrame(self):
        # Make Point Frame
        lable_font = customtkinter.CTkFont(size=20, weight='bold')
        self.scrollable_label = ScrollableLabel(master=self, width=1200, corner_radius=5,height=300,label_text="Score-Board",label_font=lable_font)
        self.scrollable_label.place(rely=0.53, relx=0.1)

        # for each groups make 1 row
        for i,j in jsonManager().initialPoint(): 
            self.scrollable_label.add_item(i,j)
        
        # Initial pointUpdate thread and start
        point_thread = Thread(target=self.pointUpdate)
        point_thread.start()

    def letterModify(self):
        global INDEXNUMBER
        INDEXNUMBER += 1

        # Modify spellings when next button is clicked
        middle,letter_1, letter_2, letter_3, letter_4 ,letter_5, letter_6 = jsonManager().getSpelling(INDEXNUMBER)
        self.letter1.configure(text=letter_1)
        self.letter2.configure(text=letter_2)
        self.letter3.configure(text=letter_3)
        self.letter4.configure(text=letter_4)
        self.letter5.configure(text=letter_5)
        self.letter6.configure(text=letter_6)        
        self.middle.configure(text=middle)
    
    def spellingChangeNotify(self):
        # Send notification message for all IDS
        for i in jsonManager().getIds():
            BOT.send_message(i,makeResponse().roundChanged(), parse_mode="MARKDOWN")

    def spellingChanged(self):
        global FINAL
        # Call lettersModify function
        if INDEXNUMBER + 1  ==  jsonManager().spellingLen():
            FINAL = True
            self.hexa_lable.destroy()
            self.next_lable.destroy()
            self.scrollable_label.place(rely=0.2)
            self.scrollable_label.configure(height=500)
            tkinter.messagebox.showwarning("Error","The game is finished")
            notify_thread = Thread(target=self.finalGameNotify)
            notify_thread.start()
            return
        # Initialize and start spellingChangeNotify thread
        self.change_thread = Thread(target=self.spellingChangeNotify)
        self.change_thread.start()
        final_page = True if INDEXNUMBER + 2 == jsonManager().spellingLen() else False
        jsonManager().removeSpellings(final_page)

        self.letterModify()
    def finalGameNotify(self):
        # Send notification message for all IDS
        for i in jsonManager().getIds():
            BOT.send_message(i,makeResponse().final(), parse_mode="MARKDOWN")
    
    def pointUpdate(self):
        global RESET

        while True:
            try:
                if RESET == True:
                    points = jsonManager().getPoint()
                    self.scrollable_label.modity_item(points)
            except Exception as e:
                pass

class ScrollableLabel(customtkinter.CTkScrollableFrame):
    '''
    Scrollabable frame for Point table.
    '''
    def __init__(self, master, command=None, **kwargs):
        # Import init funtion from CTkScrollableFrame
        super().__init__(master, **kwargs)

        # Make a gird for gropup name and point
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.group_list = []
        self.point_list = []
        self.rank_font = customtkinter.CTkFont(size=25, weight='bold')

    def add_item(self, group_name:str, point_num:int) -> None:
        # Add Group name and Point to table.
        text_color = "white"
        group = customtkinter.CTkLabel(self, text=group_name, text_color=text_color, compound="left", padx=5, anchor="w", font=self.rank_font)
        point = customtkinter.CTkLabel(self, text=f"{point_num} Pts", font=self.rank_font, text_color=text_color,compound="left")
        group.grid(row=len(self.group_list), column=0, pady=(0, 10),padx=(200,0), sticky="w")
        point.grid(row=len(self.point_list), column=2, pady=(0, 10), padx=(0,200))
        self.group_list.append(group)
        self.point_list.append(point)
    
    def modity_item(self,points:list) -> None:
        num = 0

        for group, point in zip(self.group_list, self.point_list):
           group.configure(text=points[num][0])
           point.configure(text=f"{points[num][1]} Pts")
           num += 1



# Start Game Page
class StartFrame():
    def __init__(self, master) -> None:
        
        self.master = master
        self.master.configure(bg_color="#1D1F1E",fg_color="#1D1F1E")
        self.GROUP_NUMBER = jsonManager().groupLen()
        
        # Main Frame    
        self.main_frame = customtkinter.CTkFrame(master, corner_radius=15, fg_color="#242424")
        self.main_frame.pack(side="top", pady=100, ipady=100, ipadx=200)
    
        # Logo
        logo_image = customtkinter.CTkImage(dark_image=Image.open("images/Logo-Big.png"), size=(235, 88))
        logo_lable = customtkinter.CTkLabel(self.main_frame, image=logo_image, fg_color="transparent", text=None)
        logo_lable.place(relx=0.3, rely=0.1)

    
        # Bot start Button 
        self.start_button = customtkinter.CTkButton(self.main_frame, text="Start Bot", width=150, height=40, text_color="black", font=customtkinter.CTkFont(size=16, weight='bold'), fg_color="white", hover_color="#B5B5B5", hover=True, corner_radius=20)
        self.start_button.configure(command=self.botStart)
        self.start_button.place(relx=0.34, rely=0.47)
    
    # Changing Frame
    def botStart(self):
        # Initialize multi thread and start it
        self.polling_thread = Thread(target=self.tLongPoll)
        self.polling_thread.start()
        self.start_button.configure(text="Start Game")
        self.start_button.configure(command=self.gameStart)

        # Link icon
        link_image = customtkinter.CTkImage(dark_image=Image.open("images/link.png"), size=(20.4 ,19.8))
        link_lable = customtkinter.CTkLabel(self.main_frame, image=link_image, fg_color="transparent", text=None)
        link_lable.place(relx=0.06, rely=0.9)

        # Number of Group
        self.group_lable = customtkinter.CTkLabel(self.main_frame, text=f"{self.GROUP_NUMBER} Playes joined the Game", font=customtkinter.CTkFont(size=14, weight='bold'))
        self.group_lable.place(relx=0.12, rely=0.9)

    def gameStartedMsg(self):
        # Send Game start notification for all users
        for i in jsonManager().getIds():
            BOT.send_message(i,makeResponse().gameStarted(),parse_mode="MARKDOWN")

    def gameStart(self):
        global START
        START = False
        self.main_frame.destroy()
        frame = MainFrame(self.master)
        frame.tkraise()
        jsonManager().createScore()
        jsonManager().createTotalScore()
        self.startMsgThread = Thread(target=self.gameStartedMsg)
        self.startMsgThread.start()


    # Long poll telegram requests
    def tLongPoll(self):
        global BOT

        BOT = telebot.TeleBot(bot_token) 

        @BOT.message_handler(commands=["start"]) 
        def start(message):  
            global START
            global FINAL

            if START == True:
                # Send start message to user
                response = makeResponse().startHandler(message)
                BOT.send_message(message.chat.id, response, parse_mode="MARKDOWN")
                self.group_lable.configure(text=f"{jsonManager().groupLen()} Groups joined the Game")
            else:
                # Send error message to user
                response = makeResponse().alreadyStarted(message.chat.id)
                BOT.send_message(message.chat.id, response, parse_mode="MARKDOWN")
                
        @BOT.message_handler(commands=["reset"])
        def reset(message):
            global RESET
            if message.chat.id in admin_ids:
                RESET = False
                jsonManager().reset()
                RESET = True
                BOT.send_message(message.chat.id,text="Done.")
        
        @BOT.message_handler(func=lambda message: True) 
        def message(message): 
            global START
            global FINAL

            if START == True and FINAL == False:
                # Send Error message to user
                response = makeResponse().startMessageHandler()

            elif START == False and FINAL == False:
                response = makeResponse().messageHandler(message.chat.id,INDEXNUMBER,message.text)

            else:
                response = makeResponse().final()
            BOT.send_message(message.chat.id,text=response,parse_mode="MARKDOWN")
        BOT.infinity_polling()

# Runner
if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Spelling Bee")
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    root._set_appearance_mode("dark")
    window = StartFrame(root)
    root.mainloop()

