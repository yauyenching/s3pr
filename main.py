from PatternRecategorizer import PatternRecategorizer
import os

# test_path = r'D:\Users\yenching\Desktop\sims\[s3pr]\test'
test_file = 'Simlicious_pattern_AcidWashDenim_big.package'

def recategorize_dir(path: str, new_category: str):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        PatternRecategorizer.recategorize(f, new_category)

# recategorize_dir(test_path, categories[1])
PatternRecategorizer.recategorize(test_file, 'Weave_Wicker')

print('Program Done.')
