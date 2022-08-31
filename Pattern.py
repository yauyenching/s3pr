from bs4 import BeautifulSoup
from ResourceChanger import ResourceChanger

class Pattern:
    def __init__(self):
        self.xml: str = None
        self.ptrn: str = None
        
    def change_category(self, new_category: str) -> None:
        rc = ResourceChanger(new_category)
        self.xml = rc.change_xml(self.xml)
        self.ptrn = rc.change_ptrn(self.ptrn)
        
    