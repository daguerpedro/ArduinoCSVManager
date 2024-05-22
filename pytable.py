class PyTable:
    def __init__(self) -> None:
        self.border = '|'
        self.divisor = ','
        self.alignmentDigits = 5

        pass

    def printHeader(self, variables: list):
        self.addRow(variables)

    def addRow(self, datalist: list):
        if(len(datalist) == 0): # Wont print an empty table!
            return
    
        last = (len(datalist) - 1) # Get the position of the last element
    
        print(self.border, end = '') # Start the table
    
        position = -1

        for data in datalist:
            position += 1    
    
            tempdivisor = self.divisor               
            rawdata = str(data)[:self.alignmentDigits] # Data as string
            ssize = len(rawdata) # String size of the data
            formatted = rawdata # Temp string, if the size is >= digits to align, just print the data!

            if ssize < self.alignmentDigits: # Need to align the string
                missing = self.alignmentDigits - ssize # How many left to align?

                prefix = sufix = ''
    
                for i in range(0, missing // 2): # Align the string
                    prefix += ' '
                    sufix += ' '

                if not (missing % 2) == 0:
                    prefix += ' '

                formatted = prefix + rawdata + sufix
    
            if position >= last: # Quebrar a linha
                tempdivisor = self.border+ '\n'

            print(formatted, end = tempdivisor)