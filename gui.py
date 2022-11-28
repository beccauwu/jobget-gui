import customtkinter as ctk
from widgets.custom import Input
from app import get_query
from helpers import schemas
from typing import List
from jobget import JobGetClient as Client
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("JobGet")
        self.geometry("500x500")
        # self.progressbar = ctk.CTkProgressBar(self)
        # self.progressbar.pack()
        # self.progressbar.configure(fg_color="purple", bg_color="black")
        self.input_frame = Input(self,
                                 placeholder="Enter search query",
                                 btn_text="Search",
                                 size=5,
                                 btn_callback=self.search)
        self.input_frame.pack(padx=20, pady=20)
        self.ads: List[schemas.Ad] = []
        self.client = Client()
    def search(self, q: str) -> None:
        params = schemas.QueryParams(q=q)
        self.ads = get_query(params)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
