import time
import tkinter as tk
from tkinter import Frame, ttk, simpledialog
import ds_messenger as dsm

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._messages = []
        self._users = []
        self._msg_dict = dict()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()

    """
    Update the entry_editor with the full message entry when the corresponding node in the message_tree is selected.
    """
    def node_select(self, event):
        self.entry_editor.delete(0.0, 'end')
        index = int(self.message_tree.selection()[0])-1 #selections are not 0-based, so subtract one.
        try:
            key = self._users[index]
            currt_user = self._msg_dict[key]
            for i in reversed(range(len(currt_user))):
                sent_day= self.convert_time(currt_user[i])[0]
                sent_time = self.convert_time(currt_user[i])[1]
                entry = currt_user[i]['message']
                self.set_text_entry(entry, sent_day, sent_time, True)
        except IndexError:
            raise IndexError("list index out of range") 
    
    """
    Check if the node is selected, return the current selection.
    """
    def check_selection(self):
        return self.message_tree.selection() != ()

    """
    Get current username when selected. 
    """
    def get_current_username(self):
        index = int(self.message_tree.selection()[0])-1 #selections are not 0-based, so subtract one.
        return self._users[index]

    """
    Convert timestamp to readable ones.
    """
    def convert_time(self, message) -> str:
        time_readable = time.localtime(float(message['timestamp']))
        day_str = f"{time_readable.tm_year}/{time_readable.tm_mon}/{time_readable.tm_mday}"
        time_str = f"{time_readable.tm_hour}:{time_readable.tm_min}:{time_readable.tm_sec}"
        return day_str, time_str

    """
    Combine all the messages sent by one user under the same username, 
    instead of listing them separately.
    """
    def combine_user(self):
        user_name = []
        for message in self._messages:
            user_name.append(message['from'])
        
        user_dict = dict.fromkeys(user_name)
        for user in user_name:
            user_dict[user] = []
            for msg in self._messages:
                curr_user = msg['from']
                if curr_user == user:
                    new = msg.copy()
                    del new['from']
                    user_dict[user].append(new)
        return list(set(user_name)), user_dict
    
    """
    Return the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    """
    Return the message that is currently displayed in the entry_editor widget.
    """
    def get_message_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    """
    Set the message to be displayed in the entry_editor widget.
    """
    def set_message_entry(self, text: str):
        self.message_editor.delete(0.0, 'end')
        self.message_editor.insert(0.0, text)

    """
    Set the text to be displayed in the entry_editor widget, together with the timestamp in readable style.
    """
    def set_text_entry(self, text:str, day:str=None, time:str=None, add:bool=None):
        if add:
            if time != None and day!= None:
                self.entry_editor.insert(0.0, day + ' ' + time + '\n' + text + '\n\n')
            else:
                self.entry_editor.insert(0.0, text + '\n')
        else:
            self.entry_editor.delete(tk.END, 'end')
            if time != None and day!= None:
                self.entry_editor.insert(tk.END, day + ' ' + time + '\n' + text + '\n\n')
            else:
                self.entry_editor.insert(tk.END, text + '\n')
    
    """
    Get all the users who have sent us messages and list them only once under the treeview widget.
    """
    def set_users(self, message_all: list):
        self._messages = message_all
        res = self.combine_user()
        self._users = res[0]
        self._msg_dict = res[1]

        for idx, user in enumerate(self._users):
            self._insert_msg_tree(idx+1, user, True)
    
    """
    Insert a single new username into the message_tree.
    """
    def insert_msg(self, new_username):
        self._insert_msg_tree(len(self._users), new_username, True)
    
    """
    Insert a username into the message_tree widget, distinguished between old and new usernames.
    """
    def _insert_msg_tree(self, id, msg, new:bool=None):
        if not new:
            username = msg['from']
        else:
            username = msg
        if len(username) > 25:
            username = username[:24] + '...'
        self.message_tree.insert('', id, id, text=username)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.message_tree = ttk.Treeview(posts_frame)
        self.message_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.message_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)
        
        self.message_editor = tk.Text(message_frame, width=0, height=5, bg='#efefef')
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)
        
        self.entry_editor = tk.Text(editor_frame, width=0, height=5, bg='#efefef')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, add_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        self._draw()

    """
    Call the callback function specified in the send_callback class attribute, if
    available, when the send_button widget has been clicked.
    """
    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()
    
    """
    Call the callback function specified in the add_callback class attribute, if
    available, when the add_user_button has been clicked.
    """
    def add_click(self):
        if self._add_callback is not None:
            self._add_callback()

    
    """
    Update the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)

    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        send_button = tk.Button(master=self, text="Send", width=20)
        send_button.configure(command=self.send_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        add_user_button = tk.Button(master=self, text="Add User", width=20)
        add_user_button.configure(command=self.add_click)
        add_user_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the DirectMessenger class.
"""
class MainApp(tk.Frame):
    def __init__(self, root, username, password, connection):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = username
        self.password = password
        self.connect = connection
        self._is_select = False
        self.all_msg = self.connect.retrieve_all()
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.body.set_users(self.all_msg)

    """
    Send direct messages to another user, asking for username if necessay.
    """
    def send_msg(self):
        msg = self.body.get_message_entry()
        if msg == '':
            self.footer.set_status('Error: Empty Message!')
            return
        self._is_select = self.body.check_selection()

        if not self._is_select:
            recipient = simpledialog.askstring('Ask recipient', "Recipient:")   
        else:
            recipient = self.body.get_current_username()
        
        try:
                user = dsm.DirectMessenger("168.235.86.101", self.username, self.password)
                user.send(msg, recipient)
                self.footer.set_status('Message successfully sent!')
        except Exception as e:
            self.footer.set_status(e)
        self.body.set_message_entry("")
    
    """
    Add a new user to send direct messages to.
    """
    def add_user(self):
        new_user = simpledialog.askstring('Ask new username', "Username:")
        self.body._users.append(new_user)
        self.body.insert_msg(new_user)
        self.footer.set_status('New user successfully added!')
        self.body._msg_dict[new_user] = ""

    """
    Close the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):

        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.footer = Footer(self.root, send_callback=self.send_msg, add_callback=self.add_user)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


"""
A subclass of tk.Frame that is responsible for drawing the widget
of the login page when the program initializes.
Inspired by a website named "jb51.net":
https://www.jb51.net/article/133978.htm
"""
class LoginPage(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.username = tk.StringVar() 
        self.password = tk.StringVar()
        self._draw()

    """
    Retrieve user input including username and password.
    """
    def login_check(self):
        username = self.username.get()
        password = self.password.get()
        
        try:
            dsm_object = dsm.DirectMessenger("168.235.86.101", username, password)
        except Exception as e:
            self.error_label.configure(text=e, fg='red')
            
        else:
            self.loginpage.destroy()
            self.root.geometry("720x480")
            
            MainApp(self.root, username, password, dsm_object)
    
    """
    Close the program when the 'Exit' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self): 
        self.loginpage = tk.Frame(self.root)
        self.loginpage.pack() 
        
        mainpage = tk.Label(self.loginpage)
        mainpage.pack()
        tk.Label(self.loginpage, text = 'Username: ').pack(fill=tk.BOTH)
        tk.Entry(self.loginpage, textvariable=self.username).pack(fill=tk.BOTH) 
        tk.Label(self.loginpage, text = 'Password: ').pack(fill=tk.BOTH)
        tk.Entry(self.loginpage, textvariable=self.password, show='*').pack(fill=tk.BOTH)
        tk.Label(self.loginpage, text = '').pack(fill=tk.BOTH)
        tk.Button(self.loginpage, text='Login', command=self.login_check).pack(fill=tk.BOTH)
        tk.Button(self.loginpage, text='Exit', command=self.close, width=42).pack(fill=tk.BOTH)
        self.error_label = tk.Label(self.loginpage, width=42, )
        self.error_label.pack()

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Messenger")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("480x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the LoginPage class, which is the starting point for the widgets used in the program.
    LoginPage(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
