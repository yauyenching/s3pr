import clr
clr.AddReference("../__libraries/s3pi/s3pi.Interfaces")
clr.AddReference("../__libraries/s3pi/s3pi.WrapperDealer")
clr.AddReference("../__libraries/s3pi/s3pi.Package")
clr.AddReference("../__libraries/s3pi/s3pi.ImageResource")
clr.AddReference("System.Drawing")

from ResourceChanger import ResourceChanger
from s3pi.Interfaces import IResource, IResourceIndexEntry
from s3pi.Package import Package
from s3pi.WrapperDealer import WrapperDealer
import System.Drawing
import System.IO
import os


class PatternRecategorizer:
    class NotPackageFile(Exception):
        pass
    
    index = 2

    def recategorize(self, path: str, new_category: str, extract_icon: bool = True, change_category: bool = True) -> None:
        resource_changer = ResourceChanger(new_category)

        filename, extension = os.path.splitext(path)
        if extension != '.package':
            raise PatternRecategorizer.NotPackageFile
        package = Package.OpenPackage(0, path, True)

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
            
            if extract_icon:
                # Get Icon Image from ICON Resource (different res types for small medium, large, very large)
                icon_res_types = [0x2E75C764, 0x2E75C765, 0x2E75C766, 0x2E75C767]
                if resource_type in icon_res_types:
                    image_resource = WrapperDealer.GetResource(0, package, indexEntry)
                    stream = image_resource.Stream
                    image = System.Drawing.Image.FromStream(stream)
                    image_filename = filename + '.png'
                    if os.path.exists(image_filename):
                        image_filename = filename + f"_{self.index}.png"
                        while(os.path.exists(image_filename)):
                            self.index += 1
                            image_filename = filename + f"_{self.index}.png"
                    image.Save(image_filename)
                        
                        

            if change_category:
                # Get pattern xml ressource
                if resource_type == 0x0333406C:
                    xml_resource = extract_resource(package, indexEntry)
                    # Recategorize pattern in xml
                    xml = resource_changer.change_xml(xml_resource)
                    write_resource(package, indexEntry, xml, resource_type)

                # Get patternlist resource
                if resource_type == 0xD4D9FBE5:
                    ptrn_resource = extract_resource(package, indexEntry)
                    # Recategorize pattern in ptrn
                    xml = resource_changer.change_ptrn(ptrn_resource)
                    write_resource(package, indexEntry, xml, resource_type)

        package.SavePackage()
        Package.ClosePackage(0, package)
