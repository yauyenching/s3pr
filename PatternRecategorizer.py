import os
import System.IO
import System.Drawing
from s3pi.WrapperDealer import WrapperDealer
from s3pi.Package import Package
from s3pi.Interfaces import IResource, IResourceIndexEntry
from ResourceChanger import ResourceChanger
import clr
clr.AddReference("s3pi/s3pi.Interfaces")
clr.AddReference("s3pi/s3pi.WrapperDealer")
clr.AddReference("s3pi/s3pi.Package")
clr.AddReference("s3pi/s3pi.DefaultResource")
clr.AddReference("System.Drawing")


"""
I referenced how to extract pattern resources from Anja Knackstedt 
who wrote code for the Pattern Preset Color Extractor
<https://code.google.com/archive/p/pattern-preset-color-extractor/>
under the GNU General Public License v3.
"""


class PatternRecategorizer:
    # class NotPackageFile(Exception):
    # pass

    def __init__(self, new_category: str, extract_icon: bool = True,
                 overwrite: bool = False, change_category: bool = True):
        self.resource_changer = ResourceChanger(new_category)
        self.extract_icon = extract_icon
        self.overwrite = overwrite
        self.change_category = change_category

    index = 2

    def recategorize(self, path: str):
        filename, extension = os.path.splitext(path)
        if extension != '.package':
            raise PatternRecategorizer.NotPackageFile
        package = Package.OpenPackage(0, path, True)

        try:
            self.recategorize_package(package, filename)
        except Exception as e:
            raise e
        finally:
            Package.ClosePackage(0, package)

    def recategorize_package(self, package: Package, filename: str) -> None:
        def extract_resource(package: Package, indexEntry: IResourceIndexEntry) -> str:
            resource = WrapperDealer.GetResource(0, package, indexEntry)
            return System.Text.UTF8Encoding.UTF8.GetString(resource.AsBytes)

        def write_resource(package: Package, indexEntry: IResourceIndexEntry,
                           resource: IResource, resource_type: int) -> None:
            # Create tmp resource file and write the new xml
            tmp = WrapperDealer.CreateNewResource(0, str(resource_type))
            tmp.Stream.Position = 0
            System.IO.BinaryWriter(tmp.Stream).Write(bytes(resource, 'utf-8'))
            # Replace the resource
            package.ReplaceResource(indexEntry, tmp)

        resources = package.GetResourceList
        for indexEntry in resources:
            resource_type = indexEntry.ResourceType

            if self.extract_icon:
                # Get Icon Image from ICON Resource (different res types for small medium, large, very large)
                icon_res_types = [0x2E75C764,
                                  0x2E75C765, 0x2E75C766, 0x2E75C767]
                if resource_type in icon_res_types:
                    image_resource = WrapperDealer.GetResource(
                        0, package, indexEntry)
                    stream = image_resource.Stream
                    image = System.Drawing.Image.FromStream(stream)
                    image_filename = filename + '.png'
                    if os.path.exists(image_filename) and not self.overwrite:
                        image_filename = filename + f"_{self.index}.png"
                        while (os.path.exists(image_filename)):
                            self.index += 1
                            image_filename = filename + f"_{self.index}.png"
                    image.Save(image_filename)

            if self.change_category:
                # Get pattern xml resource
                if resource_type == 0x0333406C:
                    xml_resource = extract_resource(package, indexEntry)
                    # Recategorize pattern in xml
                    xml = self.resource_changer.change_xml(xml_resource)
                    write_resource(package, indexEntry, xml, resource_type)

                # Get patternlist resource
                if resource_type == 0xD4D9FBE5:
                    ptrn_resource = extract_resource(package, indexEntry)
                    # Recategorize pattern in ptrn
                    ptrn = self.resource_changer.change_ptrn(ptrn_resource)
                    write_resource(package, indexEntry, ptrn, resource_type)

                # Get pattern xml manifest
                if resource_type == 0x73E93EEB:
                    xml_manifest = extract_resource(package, indexEntry)
                    # Recategorize pattern in manifest
                    manifest = self.resource_changer.change_manifest(
                        xml_manifest)
                    write_resource(package, indexEntry,
                                   manifest, resource_type)
