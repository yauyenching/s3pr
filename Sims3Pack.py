import clr
import System.IO
from System.IO import BinaryReader, BinaryWriter, FileStream, FileMode, FileAccess, FileInfo
from PatternRecategorizer import PatternRecategorizer

from bs4 import BeautifulSoup

"""
This code was created by Anja Knackstedt for the Pattern Preset Color Extractor
<https://code.google.com/archive/p/pattern-preset-color-extractor/>
under the GNU General Public License v3.

This code was converted to Python by me (Yau Yen Ching) for this program.
"""
class Sims3Pack:
    def getLengthFromDWord(dword) -> int:
        byte0 = dword[0]
        byte1 = dword[1] * 0x100
        byte2 = dword[2] * 0x10000
        byte3 = dword[3] * 0x1000000
        
        return byte0 + byte1 + byte2 + byte3
    
    DWORD = 4
    WORD = 2
    
    def read(self, path: str):
        """ 
        Sims3Pack:
            DWORD length of the following string
            String
            WORD
            DWORD length of the following xml part 
        """

        binaryReader = BinaryReader(FileStream(path, FileMode.Open, FileAccess.Read))

        # read 1. DWORD 
        DWordLength = binaryReader.ReadBytes(self.DWORD);
        stringLength = Sims3Pack.getLengthFromDWord(DWordLength);

        # skip string part and WORD         
        binaryReader.BaseStream.Position += stringLength + self.WORD;

        # read 2. DWORD 
        DWordLength = binaryReader.ReadBytes(self.DWORD);
        xmlLength = Sims3Pack.getLengthFromDWord(DWordLength);

        # read XML part and convert it
        XMLBytes = binaryReader.ReadBytes(xmlLength);
        XMLPart = System.Text.UTF8Encoding.UTF8.GetString(XMLBytes);    
        # print(XMLPart)
        
        BinaryStartPosition = self.DWORD + stringLength + self.WORD + self.DWORD + xmlLength
        
        xml = BeautifulSoup(XMLPart, "xml")
        Length = int(xml.Length.string)
        print(Length)
        Offset = int(xml.Offset.string)
        print(Offset)
        
        binaryReader.BaseStream.Position = BinaryStartPosition + Offset     
        
        packageBytes = binaryReader.ReadBytes(Length)
        binaryReader.Close();
        
        packageSims3PackFileInfo = FileInfo(path)
        filename = packageSims3PackFileInfo.FullName
        tmp_filepath = filename.replace(packageSims3PackFileInfo.Extension, "_tmp.package")
        # print(type(bytes(packageBytes, 'utf-8')))

        destFile = FileStream(tmp_filepath, FileMode.Create, FileAccess.Write)
        writeFile = BinaryWriter(destFile)
        writeFile.Write(packageBytes)
        
        return tmp_filepath
    
    def recategorize(path: str, filename: str, recategorizer: PatternRecategorizer):
        package = Package.OpenPackage(0, path, True)
        
        

