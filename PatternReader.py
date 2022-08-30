import os
import clr
clr.AddReference("../__libraries/s3pi/s3pi.Interfaces")
clr.AddReference("../__libraries/s3pi/s3pi.WrapperDealer")
clr.AddReference("../__libraries/s3pi/s3pi.Package")
clr.AddReference("../__libraries/s3pi/s3pi.ImageResource")
clr.AddReference("System.Drawing")

import System.IO
import System.Drawing
from s3pi.WrapperDealer import WrapperDealer
from s3pi.Package import Package
from s3pi.Interfaces import IResource
import ImageResource

file = 'Simlicious_pattern_AcidWashDenim_big.package'
filename = os.path.splitext(file)[0]
package = Package.OpenPackage(0, file, False)
resources = package.GetResourceList

for indexEntry in resources:
    resource_type = indexEntry.ResourceType

    # Get Icon Image from ICON Resource (different res types for small medium, large, very large)
    icon_res_types = [0x2E75C764, 0x2E75C765, 0x2E75C766, 0x2E75C767]
    if resource_type in icon_res_types:
        image_resource = IResource(WrapperDealer.GetResource(0, package, indexEntry))
        stream = image_resource.Stream
        image = System.Drawing.Image.FromStream(stream)
        image.Save(filename + ".png")

    # Get pattern xml ressource
    if resource_type == 0x0333406C:
        xmlResource = WrapperDealer.GetResource(0, package, indexEntry)
        stream = xmlResource.Stream
        xml = System.Text.UTF8Encoding.UTF8.GetString(xmlResource.AsBytes)
        # print(xml)
