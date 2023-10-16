import tkinter as tk
from tkinter import filedialog as fd


class TextEditor:
    def __init__(self, root=None, filename=None):
        if not root:
            root = tk.Tk()

        self.root = root

        self.create_entry()
        self.create_menu()

    def create_entry(self) -> None:
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack(fill='both', expand=True)

    def create_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='New', command=TextEditor)
        file_menu.add_command(label='Open...', command=fd.askopenfile)

        file_menu.add_command(label='Close', command=self.root.destroy)

        menubar.add_cascade(label='File', menu=file_menu)

    def run(self):
        self.root.mainloop()
        
if __name__=='__main__':
    te = TextEditor()
    te.run()
