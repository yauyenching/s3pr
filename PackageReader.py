from importlib.abc import ResourceReader
from ResourceChanger import ResourceChanger
import clr
clr.AddReference("../__libraries/s3pi/s3pi.Interfaces")
clr.AddReference("../__libraries/s3pi/s3pi.WrapperDealer")
clr.AddReference("../__libraries/s3pi/s3pi.Package")
clr.AddReference("../__libraries/s3pi/s3pi.ImageResource")
clr.AddReference("System.Drawing")

from s3pi.Interfaces import IResource
from s3pi.Package import Package
from s3pi.WrapperDealer import WrapperDealer
import System.Drawing
import System.IO
import os


class PatternRecategorizer:
    class NotPackageFile(Exception):
        pass
    
    def recategorize(path: str, new_category: str) -> None:
        resource_changer = ResourceChanger(new_category)
        
        filename, extension = os.path.splitext(path)
        if extension != '.package':
            raise PatternRecategorizer.NotPackageFile
        package = Package.OpenPackage(0, path, True)
        resources = package.GetResourceList
        
        for indexEntry in resources:
            resource_type = indexEntry.ResourceType

            # Get Icon Image from ICON Resource (different res types for small medium, large, very large)
            icon_res_types = [0x2E75C764, 0x2E75C765, 0x2E75C766, 0x2E75C767]
            if resource_type in icon_res_types:
                image_resource = IResource(
                    WrapperDealer.GetResource(0, package, indexEntry))
                stream = image_resource.Stream
                image = System.Drawing.Image.FromStream(stream)
                image.Save(filename + ".png")

            # Get pattern xml ressource
            if resource_type == 0x0333406C:
                xml_resource = WrapperDealer.GetResource(0, package, indexEntry)
                stream = xml_resource.Stream
                xml = System.Text.UTF8Encoding.UTF8.GetString(xml_resource.AsBytes)
                # Recategorize pattern in xml
                xml = resource_changer.change_xml(xml)
                # Create tmp resource file and write the new xml
                tmp = WrapperDealer.CreateNewResource(0, str(resource_type))
                tmp.Stream.Position = 0
                System.IO.BinaryWriter(tmp.Stream).Write(bytes(xml, 'utf-8'));
                # Replace the resource
                package.ReplaceResource(indexEntry, tmp)
                
                
            # Get patternlist resource
            if resource_type == 0xD4D9FBE5:
                ptrn_resource = WrapperDealer.GetResource(0, package, indexEntry)
                stream = ptrn_resource.Stream
                ptrn = System.Text.UTF8Encoding.UTF8.GetString(ptrn_resource.AsBytes)
                # print(xml)
                
        package.SavePackage()
        Package.ClosePackage(0, package)
        