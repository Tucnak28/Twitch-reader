import tkinter as tk

class TwitchChatUI:
    def __init__(self, master):
        self.master = master
        master.title("Twitch Chat")

        self.chat_frame = tk.Frame(master)
        self.chat_frame.pack(expand=True, fill=tk.BOTH)

        self.chat_text = tk.Text(self.chat_frame, wrap=tk.WORD)
        self.chat_text.pack(expand=True, fill=tk.BOTH)

        self.input_frame = tk.Frame(master, bd=1, relief=tk.SUNKEN)
        self.input_frame.pack(expand=True, fill=tk.X)

        self.input_field = tk.Entry(self.input_frame)
        self.input_field.pack(expand=True, fill=tk.BOTH)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def send_message(self):
        message = self.input_field.get()
        if message:
            self.chat_text.insert(tk.END, f"You: {message}\n")
            self.input_field.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    twitch_chat_ui = TwitchChatUI(root)
    root.mainloop()
