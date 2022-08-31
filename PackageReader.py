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
from Pattern import Pattern
import os


class PackageReader:
    class NotPackageFile(Exception):
        pass
    
    def read(path: str) -> Pattern:
        pattern = Pattern()
        
        filename, extension = os.path.splitext(path)
        if extension != '.package':
            raise PackageReader.NotPackageFile
        package = Package.OpenPackage(0, path, False)
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
                # print(xml)
                pattern.xml = xml
                
            # Get patternlist resource
            if resource_type == 0xD4D9FBE5:
                ptrn_resource = WrapperDealer.GetResource(0, package, indexEntry)
                stream = ptrn_resource.Stream
                ptrn = System.Text.UTF8Encoding.UTF8.GetString(ptrn_resource.AsBytes)
                # print(xml)
                pattern.ptrn = ptrn
                
        Package.ClosePackage(0, package)
        
        return pattern