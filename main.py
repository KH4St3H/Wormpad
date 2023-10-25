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
        self.file= None

        self._create_entry()
        self._create_menu()

        if filename:
            self.openfile(filename)

    @staticmethod
    def create(event=None):
        return TextEditor()

    def _create_entry(self) -> None:
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget = tk.Text(self.root, yscrollcommand=scrollbar.set)
        self.text_widget.pack(fill='both', expand=True)

        scrollbar.config(command=self.text_widget.yview)

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
        if not isinstance(filename, str):
            return

        path = Path(filename)
        if path.is_dir():
            return

        self.clear()
        self.file = path
        self.root.title(path.name)

        if not path.exists():
            with path.open('w') as f:
                pass
            return

        with path.open('r') as f:
            try:
                for d, line in enumerate(f.readlines(), start=1):
                    self.text_widget.insert(f'{d}.0', line)
            except UnicodeDecodeError as e:
                self.text_widget.insert('end', str(e))


    def askopenfile(self, event=None) -> None:
        filename = fd.askopenfilename()
        self.openfile(filename)

    def save_as(self, event=None):
        filename = fd.asksaveasfilename()
        path = Path(filename)
        
        if path.is_dir():
            return

        with path.open('w') as f:
            f.writelines([i[1] for i in self.dump_all()])

        self.openfile(filename)

    def dump_all(self):
        return self.text_widget.dump('1.0', 'end', text=True)

    def save(self, event=None):
        if not self.file:
            self.save_as()
            return

        with open(self.file, 'w') as f:
            f.writelines([i[1] for i in self.dump_all()])

    def undo(self, event=None):
        pass

    def redo(self, event=None):
        pass

    def _create_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # file menu
        file_menu = tk.Menu(menubar, tearoff=False)

        file_menu.add_command(label='New', command=TextEditor.create, accelerator='Control+n')
        self.root.bind('<Control-n>', TextEditor.create)

        file_menu.add_command(label='Open...', command=self.askopenfile, accelerator='Control+o')
        self.root.bind('<Control-o>', self.askopenfile)

        file_menu.add_command(label='Close', command=self.root.destroy)

        file_menu.add_separator()
        file_menu.add_command(label='Save', command=self.save, accelerator='Control+s')
        self.root.bind('<Control-s>', self.save)
        file_menu.add_command(label='Save as..', command=self.save_as)

        # edit menu
        edit_menu = tk.Menu(menubar, tearoff=False)

        edit_menu.add_command(label='Undo', command=self.undo, accelerator='Control-z')
        self.root.bind('<Control-z>', self.undo)

        edit_menu.add_command(label='Redo', command=self.redo, accelerator='Control-Shift-z')
        self.root.bind('<Control-Shift-z>', self.redo)



        menubar.add_cascade(label='File', menu=file_menu)
        menubar.add_cascade(label='Edit', menu=edit_menu)

    def run(self):
        self.root.mainloop()
        
if __name__=='__main__':
    te = TextEditor()
    te.run()
