import clr
clr.AddReference("s3pi/s3pi.Package")
from s3pi.Package import Package
from PatternRecategorizer import PatternRecategorizer

class PackageRecategorizer:
    def recategorize(path: str, filename: str, recategorizer: PatternRecategorizer):
        package = Package.OpenPackage(0, path, True)
        
        try:
            recategorizer.recategorize_package(package, filename)
            package.SavePackage()
        except Exception as e:
            raise e
        finally:
            Package.ClosePackage(0, package)