
import customtkinter as ctk
from typing import Literal
import math
from helpers.schemas import InputSize, Checkbox
from typing import Callable, List
import tkinter.filedialog as filedialog
from client.jobget import Client

class Input(ctk.CTkFrame):
    """Input widget with a button and labels, optionally with checkboxes

    Attributes
    ----------
    sizing_dims : InputSize
        Sizes of the input components
    entry : ctk.CTkEntry
        Entry widget
    value : str
        Value of the entry widget

    Methods
    ----------
    add_label : (text: str) -> None
        Add a label to the current figure
    add_checkboxes : (options: List[Checkbox], cols: Literal[1,2] = 2) -> None
        Add checkboxes
    """
    def __init__(self,
                 *args,
                 btn_text: str,
                 btn_callback: Callable[[str], None],
                 placeholder: str | None = None,
                 size: Literal[1,2,3,4,5,6,7] = 3,
                 **kwargs):
        """Initialize the input widget .

        Parameters
        ----------
        btn_text : str
            Button text
        btn_callback : Callable[[str], None]
            Button callback
        placeholder : str | None, optional
            Placeholder text, by default None
        size : Literal[1,2,3,4,5,6,7], optional
            Size of the input, by default 3
        """
        super().__init__(*args, **kwargs)
        self.sizing_dims = self.__get_size(size)
        self.grid(row=0, column=0, sticky="nsew")
        
        self.entry = ctk.CTkEntry(self,
                                  placeholder_text=placeholder,
                                  width=self.sizing_dims.entry_width,
                                  height=self.sizing_dims.entry_height,corner_radius=5)
        self.__has_label = self.__hasAttr("label")
        self.entry.grid(row=0,
                        column=1 if self.__has_label else 0,
                        columnspan= 1 if self.__has_label else 2,
                        pady=(20,0),
                        padx=20)
        self.value = self.entry.get()
        
        self.button = ctk.CTkButton(self,
                                    text=btn_text,
                                    width=self.sizing_dims.button_width,
                                    height=self.sizing_dims.button_height,
                                    command=lambda: btn_callback(self.value))
        self.button.grid(row=1, column=0, pady=20, padx=20, columnspan=2)
        
        
    def __hasAttr(self, attr: str) -> bool:
        """ **Internal** Returns True if the node has an attribute .

        :param attr: Attribute to check
        :type attr: str
        :return: Whether attribute exists
        :rtype: bool
        """
        return hasattr(self, attr)
    
    def __get_size(self, size: Literal[1,2,3,4,5,6,7]) -> InputSize:
        """ **Internal** Returns formatted sizes for components

        :param size: Given size
        :type size: Literal[1,2,3,4,5,6,7]
        :return: Formatted size
        :rtype: InputSize
        """
        base_size = InputSize(
            entry_width=120,
            entry_height=30,
            button_height=30,
            button_width=100,
            label_height=30,
            label_width=100,
        )
        new = {}
        for key, value in base_size.dict().items():
            new[key] = math.ceil(value * (0.4 + len(range(size))*0.2))
        return InputSize(**new)
    
    def add_label(self, text: str) -> None:
        """Add a label to the current figure .

        :param text: Label text
        :type text: str
        """
        self.label = ctk.CTkLabel(self,
                                  text=text,
                                  width=self.sizing_dims.label_width,
                                  height=self.sizing_dims.label_height)
        self.label.grid(row=0, column=0, pady=(20,0), padx=20)
        
    def add_checkboxes(self,
                       options: List[Checkbox],
                       cols: Literal[1,2] = 2) -> None:
        """Add checkboxes .

        :param options: List of options for checkboxes
        :type options: List[Checkbox]
        :param cols: Number of columns, defaults to 2
        :type cols: Literal[1,2], optional
        """
        self.checkboxes: List[ctk.CTkCheckBox] = []
        for i, o in enumerate(options):
            row = i+1 if cols == 1 else (i+1 if i%2==0 else i)
            col = 0 if cols == 1 else i%2
            self.checkboxes.append(
                ctk.CTkCheckBox(self,
                                text=o.text,
                                command=lambda: o.callback(self.checkboxes[i].get() == 1)
                                ))
            self.checkboxes[i].grid(row=row, column=col, pady=10, padx=10)

class FileDialog(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        self.filepath = ctk.CTkEntry(self, width=100)
        self.filepath.grid(row=0, column=0, pady=10, padx=10)
        self.button = ctk.CTkButton(self, text="Browse", command=self.__browse)
        self.button.grid(row=0, column=1, pady=10, padx=10)
        
    def __browse(self):
        self.filepath.delete(0, "end")
        self.filepath.insert(0, filedialog.asksaveasfilename())
