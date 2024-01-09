import time

from tkinter import Event
from tkinter import Text
from typing import Optional

class UndoBlock:
    def __init__(self, content, start_line: int, end_line: int, next=None, prev=None) -> None:
        self.edited_time = time.time()
        self.next = next
        self.prev = prev
        
        self.start_line = start_line
        self.end_line = end_line

        self.content = content

    def update_time(self):
        self.edited_time = time.time()

    def dumb_blocks(self):
        head = self
        while head.next:
            head = head.next
        count = 0
        while head.prev:
            if head is self:
                print(f'[{count}*] -> ', end='')
            else:
                print(f'[{count}] -> ', end='')
            count += 1
            head = head.prev
        print(f'[{count}]')

    def addline(self, widget: Text, line=None):
        line = line if line else self.end_line
        self.content += widget.dump(f'{line}.0', f'{line}.end')

    def apply(self, widget: Text):
        old_data = [line
                    for line in widget.dump(
                        f'{self.start_line}.0', 
                        f'{self.end_line}.end') if line[0]=='text']

        widget.delete(f'{self.start_line}.0', f'{self.end_line}.end')
        for d, line in enumerate(self.content):
            if line[0] != 'text':
                continue
            widget.insert(line[2], line[1])
        self.content = old_data  # replace data with current text in undo area

    def link(self, next_block):
        self.next = next_block
        next_block.prev = self

    def destroy_chain(self):
        last = self
        self.dumb_blocks()
        while last.next:
            last = last.next

        while last is not self and last.prev:
            print('deleted')
            temp = last
            last = last.prev
            last.next = None
            del temp

