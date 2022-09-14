from bs4 import BeautifulSoup


class ResourceChanger:
    def __init__(self, new_category: str):
        self.new_category = new_category

    def change_xml(self, xml) -> str | None:
        pattern_data = BeautifulSoup(xml, "xml").complate
        if pattern_data == None:
            return None
        else:
            pattern_data['category'] = self.new_category
            return pattern_data.prettify()

    def change_ptrn(self, ptrn) -> str:
        pattern_list = BeautifulSoup(ptrn, "lxml").patternlist
        pattern_list.category['name'] = self.new_category
        return pattern_list.prettify()

    def change_manifest(self, manifest) -> str:
        pattern_manifest = BeautifulSoup(manifest, "xml")
        matcategory = pattern_manifest.matcategory
        matCategory = pattern_manifest.matCategory
        if matcategory == None and matCategory == None:
            return None
        elif matcategory != None:
            pattern_manifest.matcategory.string = self.new_category
        else:
            pattern_manifest.matCategory.string = self.new_category
            # print(pattern_manifest.metatags.matCategory)
        return str(pattern_manifest)
