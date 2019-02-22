# pylint: disable=C0111,R0903

"""Displays the number of todo items from a text file

Parameters:
    * todo.file: File to read TODOs from (defaults to ~/Documents/todo.txt)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import os.path


class Module(bumblebee.engine.Module):


    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.output)
        )
        self._doc = os.path.expanduser(
            self.parameter("file", "~/Documents/todo.txt")
        )
        self._ignore_chrs = self.parameter("ignore", "#").split()
        self._todos = self.count_items()


    def output(self, widget):
       self._todos = self.count_items()
       return str(self._todos)


    def state(self, widgets):
        if self._todos == 0:
            return "empty"
        return "items"


    def count_items(self):
        try:
            num_todos = 0
            with open(self._doc, 'r') as f:
                for line in f:
                    if line.strip():
                        startswith = line.split()[0]
                        if startswith not in self._ignore_chrs:
                            num_todos += 1
            return num_todos
        except Exception:
            return 0
