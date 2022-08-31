from PackageReader import PackageReader
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

pattern = PackageReader.read(test_file)
# test = ResourceChanger(pattern, categories[1])
# test.change_ptrn()
print('Program Done.')
