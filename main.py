import tkinter as tk
from tkinter import filedialog as fd

from pathlib import Path


class TextEditor:
    def __init__(self, root=None, filename: str=''):
        """
        Initializes text editor

        Args:
            root (tk.Tk): if text editor needs to be built on existing tk window
            filename (str): opens file if specified
        """
        if not root:
            root = tk.Tk()

        root.title('Wormpad')

        self.root = root

        self.__create_entry()
        self.__create_menu()

        if filename:
            self.openfile(filename)

    def __create_entry(self) -> None:
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack(fill='both', expand=True)

    def clear(self) -> None:
        """
        clears text_widget
        """
        self.text_widget.delete('1.0', 'end')

    def openfile(self, filename: str) -> None:
        """ 
        Reads a file into text_widget

        Args:
            filename (str): file name to be read
        """
        self.clear()

        path = Path(filename)
        if not path.exists():
            raise FileNotFoundError(f'{filename} does not exist')

        self.file = path
        with open(path, 'r') as f:
            try:
                for d, line in enumerate(f.readlines(), start=1):
                    self.text_widget.insert(f'{d}.0', line)
            except UnicodeDecodeError as e:
                self.text_widget.insert('end', str(e))

        self.root.title(path.name)

    def askopenfile(self) -> None:
        filename = fd.askopenfilename()
        self.openfile(filename)

    def __create_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='New', command=TextEditor)
        file_menu.add_command(label='Open...', command=self.askopenfile)
        file_menu.add_command(label='Close', command=self.root.destroy)

        menubar.add_cascade(label='File', menu=file_menu)

    def run(self):
        self.root.mainloop()
        
if __name__=='__main__':
    te = TextEditor()
    te.run()
