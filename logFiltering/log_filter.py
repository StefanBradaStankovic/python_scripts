import sys

args = sys.argv[1:]

if len(args) <= 2:
    print("Script must contain input file name, decode and isolate parameters!\n")
    print("Decode:  wheter to decode all byte hex values into chars or not")
    print("Isolate: wheter to isolate or delete found files")
    print("To filter a sentence, put it in double quotations:  \"example sentence\"")
    print("Script syntax:")
    print("python log_filter.py <file_name> <decode: y/n> <isolate: y/n> <arg> <arg> <arg> ...")
    quit()

fileName = args[0]

def _parseName(string):
    values = string.split('.')
    values.pop()
    return ".".join(values)

fileName = _parseName(fileName)

def _parseArgs():
    argsList = []
    for arg in args[3:]:
        argsList.append(arg)
    return argsList

def DecodeBytes():
    tempString = "bytes"
    unwantedBytes = ["0A", '0D', '8F', 'F7']
    print("Decoding all bytes from file " + fileName + ".log")
    print("Writing into file " + fileName + "_decoded.log\n")
    inputFile = open(fileName + '.log', 'r')
    outputFile = open(fileName + '_decoded.log', 'w')
    for line in inputFile:
        if "SerialDevice" in line and tempString.casefold() in line.casefold():
            listOfStrings = line.split('\"')
            listOfHex = listOfStrings[1].split('-')
            for item in unwantedBytes:
                listOfHex = list(map(lambda x: x.replace(item, ''), listOfHex))
            e = bytes.fromhex("".join(listOfHex)).decode('utf-8')
            listOfStrings[1] = e
            outputFile.write("".join(listOfStrings))
        else:
            outputFile.write(line)
    outputFile.close()
    
def FilterKeywords(listOfStrings, isolate):
    print("Filtering substrings from file " + fileName + ".log")
    print("Targeted substrings:", end = " ")
    outputFileName = fileName + "_keywords"
    for item in listOfStrings:
        print(item.casefold(), end = " ")
    if isolate:
        print("\nIsolating all lines with substrings found...")
        outputFileName += "-isolated"
    else:
        print("\nRemoving all lines with substrings found...")
        outputFileName += "-removed"
    print("Writing into file " + outputFileName + ".log\n")
    inputFile = open(fileName + '.log', 'r')
    outputFile = open(outputFileName + '.log', 'w')
    for line in inputFile:
        if not line:
            break
        foundSubstring = any(substring.casefold() in line.casefold() for substring in listOfStrings)
        if not(foundSubstring ^ isolate):
            outputFile.write(line)
    outputFile.close()

if args[1] == 'y':
    DecodeBytes()
    fileName += '_decoded'
    
if len(args) >= 4:
    parsedArgs = _parseArgs()
    if args[2] == 'y':
        FilterKeywords(parsedArgs, True)
    else:
        FilterKeywords(parsedArgs, False)