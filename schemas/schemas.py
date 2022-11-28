from pydantic import BaseModel
from typing import Callable

class InputSize(BaseModel):
    label_width: int
    label_height: int
    button_width: int
    button_height: int
    entry_width: int
    entry_height: int

class Checkbox(BaseModel):
    text: str
    value: bool
    callback: Callable[[bool], None]