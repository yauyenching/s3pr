from bs4 import BeautifulSoup

class Pattern:
    def __init__(self):
        self.xml: str = None
        self.ptrn: str = None
        
    class ResourceChanger:
        def __init__(self, pattern: Pattern, new_category: str):
            self.pattern = pattern
            self.new_category = new_category
        
        def change_xml(self) -> str:
            pattern_data = BeautifulSoup(self.pattern.xml, "xml").complate
            pattern_data['category'] = self.new_category
            return pattern_data.prettify()
        
        def change_ptrn(self) -> str:
            pattern_list = BeautifulSoup(self.pattern.ptrn, "lxml").patternlist
            pattern_list.category['name'] = self.new_category
            return pattern_list.prettify()