#! /usr/bin/python3
import tkinter as tk
import random as r

def genBuzzword():
        adjs = [
                "Blockchain",
                "Secure",
                "Leverage",
                "Carbon-fiber"
        ]

        nouns = [
                "blockchain",
                "synergy",
                "internet of things",
        ]

        return r.choice(adjs) + " " + r.choice(nouns)

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.btn = tk.Button(self)
        self.btn["text"] = "Click"
        self.btn["command"] = self.do_random
        self.btn.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def do_random(self):
         self.btn["text"] = genBuzzword()

def main():
    root = tk.Tk()
    root.title("Buzzword Generator")
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
