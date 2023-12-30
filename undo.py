from tkinter import Event
from typing import Optional


class Memento:
    '''
    Doubly linked list including changes
    '''
    def __init__(self, prev=None) -> None:
        self.prev = None
        self.next: Memento

class UndoBlock:
    def __init__(self, content, start_line: int, end_line: int, next=None, prev=None) -> None:
        self.next: Optional[UndoBlock] = next
        self.prev: Optional[UndoBlock] = prev
        
        self.start_line = start_line
        self.end_line = end_line

        self.content = content
        self.original_content = []
        
    def apply(self, widget):
        widget.delete(f'{self.start_line}.0', f'{self.end_line}.0')
        print(self.start_line, self.end_line)
        for d, line in enumerate(self.content):
            if line[0] != 'text':
                continue
            widget.insert(f'{self.start_line + d}.0', line[1])

    def link(self, next_block):
        self.next = next_block
        next_block.prev = self

    def destroy_chain(self):
        last = self
        while last.next:
            last = last.next

        while last is not self and last.prev:
            print('deleted')
            temp = last
            last = last.prev
            last.next = None
            del temp

class UndoList:
    def __init__(self) -> None:
        self.current_memento = Memento()


    def save_state(self, state):
        new_memento = Memento(prev=self.current_memento)
        self.current_memento.next = new_memento
