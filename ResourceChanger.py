from bs4 import BeautifulSoup

class ResourceChanger:
    def __init__(self, new_category: str):
        self.new_category = new_category

    def change_xml(self, xml) -> str:
        pattern_data = BeautifulSoup(xml, "xml").complate
        pattern_data['category'] = self.new_category
        return pattern_data.prettify()

    def change_ptrn(self, ptrn) -> str:
        pattern_list = BeautifulSoup(ptrn, "lxml").patternlist
        pattern_list.category['name'] = self.new_category
        return pattern_list.prettify()
