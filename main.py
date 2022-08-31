from PackageReader import PatternRecategorizer
from ResourceChanger import ResourceChanger

test_file = 'Simlicious_pattern_AcidWashDenim_big.package'

categories = ['Fabric',
              'Weave_Wicker',
              'Plastic_Rubber',
              'Tile_Mosaic',
              'Abstract',
              'Metal',
              'Miscellaneous',
              'Carpet_Rug',
              'Paint',
              'Theme',
              'Wood',
              'Leather_Fur',
              'Geometric',
              'Masonry',
              'Rock_Stone']

pattern = PatternRecategorizer.recategorize(test_file, categories[1])
# pattern.change_category(categories[1])
# print(pattern.xml)
# print('\n')
# print(pattern.ptrn)
print('Program Done.')
