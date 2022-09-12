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

    def change_manifest(self, manifest) -> str:
        pattern_manifest = BeautifulSoup(manifest, "xml")
        mat_category = pattern_manifest.matcategory
        if mat_category != None:
            pattern_manifest.matcategory.string = self.new_category
        else:
            pattern_manifest.matCategory.string = self.new_category
            # print(pattern_manifest.metatags.matCategory)
        return str(pattern_manifest)
