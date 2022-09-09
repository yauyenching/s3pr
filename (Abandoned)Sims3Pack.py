import clr
from PatternRecategorizer import PatternRecategorizer
from Package import PackageRecategorizer
import System.IO
from System.IO import BinaryReader, BinaryWriter, FileStream, FileMode, FileAccess, FileInfo
from bs4 import BeautifulSoup

"""
This code was created by Anja Knackstedt for the Pattern Preset Color Extractor
<https://code.google.com/archive/p/pattern-preset-color-extractor/>
under the GNU General Public License v3.

This code was converted to Python by me (Yau Yen Ching) for this program.
"""
class Sims3PackRecategorizer:
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
        stringLength = Sims3PackRecategorizer.getLengthFromDWord(DWordLength);

        # skip string part and WORD         
        binaryReader.BaseStream.Position += stringLength + self.WORD;

        # read 2. DWORD 
        DWordLength = binaryReader.ReadBytes(self.DWORD);
        xmlLength = Sims3PackRecategorizer.getLengthFromDWord(DWordLength);

        # read XML part and convert it
        XMLBytes = binaryReader.ReadBytes(xmlLength);
        print(XMLBytes.Length)
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
        binaryReader.Close()
        
        packageSims3PackFileInfo = FileInfo(path)
        filename = packageSims3PackFileInfo.FullName
        tmp_path = filename.replace(packageSims3PackFileInfo.Extension, "_tmp.package")
        # print(type(bytes(packageBytes, 'utf-8')))

        writeFile = BinaryWriter(FileStream(tmp_path, FileMode.Create, FileAccess.Write))
        writeFile.Write(packageBytes)
        writeFile.Close()
        
        return (xml, tmp_path)
    
    def recategorize(self, tmp_path: str, xml: BeautifulSoup,
                     filename: str, recategorizer: PatternRecategorizer):
        PackageRecategorizer.recategorize(tmp_path, filename, recategorizer)
        
        Length = FileInfo(tmp_path).Length
        xml.Length.string = str(Length)
        
        # len(bytes(str(xml), 'utf-8'))
        writeFile = BinaryWriter(FileStream(tmp_path, FileMode.Create, FileAccess.Write))
        writeFile.Close()
        
        
        

