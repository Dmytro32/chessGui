from tkinter import Canvas
from abc import ABC, abstractmethod

class Pieces(ABC):
    def __init__(self,name:str,obj:Canvas):
            self.name=name
            self.obj=obj
    def read_dict(dic:dict,search:any):
        for key,value in dic.items():
            if value==search:
                return key
    def tran_cor(x:int):
        l= [60,120,180,240,300,360,420,480]
        for i in l:
            if x<i:
                x=i-60
                return x
    def color(self):
        if self.name[0]=="w":
            return True
        return False


