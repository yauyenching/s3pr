import clr

clr.AddReference("../__libraries/s3pi/s3pi.Interfaces")
clr.AddReference("../__libraries/s3pi/s3pi.Package")
clr.AddReference("../__libraries/s3pi/s3pi.WrapperDealer")
from s3pi.Package import Package
from s3pi.WrapperDealer import WrapperDealer
import System.IO

path = 'Simlicious_pattern_AcidWashDenim_big.package'
package = Package.OpenPackage(0, path, False)
resources = package.GetResourceList

for indexEntry in resources:
    # Get pattern xml ressource
    if indexEntry.ResourceType == 0x0333406C:
        xmlResource = WrapperDealer.GetResource(0, package, indexEntry)
        stream      = xmlResource.Stream
        xml         = System.Text.UTF8Encoding.UTF8.GetString(xmlResource.AsBytes);  
        print(xml)