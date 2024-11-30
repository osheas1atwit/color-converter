# import sys
import argparse

# Order of types must match order of arguments defined
# (or else arg validation will no longer work properly)
TYPES = ['hex', 'rgb', 'cmyk']
# look into CMY, HSL, HSV

HEX_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']

def main():

    # Set up arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-hex', action='store_true', help='convert from hex (accepts hexadecimal input [ffffff] or string ["#ffffff"] (both are case insensitive)')
    parser.add_argument('-rgb', action='store_true', help='convert from RGB (accepts integer input [R G B], or string [\"rgb(R, G, B)\"] (case/whitespace insensitive)')
    parser.add_argument('-cmyk', action='store_true', help='convert from CMYK (accepts integer input [C M Y K], or string [\"cmyk(C, M, Y, K)\"] (case/whitespace insensitive)')
    
    parser.add_argument('color', nargs='*', help='accepts a color in Hex, RGB, CMYK, or HSL and performs format conversions (does not support CMYK profiles, conversions are uncalibrated)')
    args = parser.parse_args()


    # debug print
    print('args type: ', type(vars(args)))
    print(args, '\n')


    # INPUT SYNTAX VALIDATION
    if not validateArguments(args) :
        return;

    color = args.color
    
    # HANDLE HEX INPUT
    if args.hex :
        color = color[0].lower().replace(' ', '').strip('#')
        if not validateHex(color) :
            return

        convertFromHex(color)

    # HANDLE RGB INPUT
    if args.rgb :
        # cleanse any non-numerical stuff
        if len(color) == 1 :
            color = color[0].lower().strip('rgb(').strip(')').replace(' ', '').split(',')
        if not validateRGB(color) :
            return
        
        for i in range(len(color)) :
            color[i] = int(color[i])

        convertFromRGB(color)

    # HANDLE CMYK INPUT
    if args.cmyk :
        # cleanse any non-numerical stuff
        if len(color) == 1 :
            color = color[0].lower().strip('cmyk(').strip(')').replace('%', '').replace(' ', '').split(',')
        if not validateCMYK(color) :
            return

        print('convert cmyk: ', color)
##
# HEX CONVERSION SECTION
##

# Takes in valid RGB code and converts it to the other formats
def convertFromHex(hexCode) :
    print('convert hex: ', hexCode)
    convertToRGB('hex', hexCode)
    # convertToCMYK('hex', code)
    # convertToHSL('hex', code)

def convertToHex(codeFormat, code) :
    hexValue = '#'
    
    if codeFormat == 'rgb' :
        for rgbValue in code :
            hexValue += hex(int(rgbValue / 16)) 
            hexValue += hex(int(rgbValue % 16))
    
    print('HEX: ', hexValue)


##
# RGB CONVERSION SECTION
##

# Takes in valid RGB code and converts it to the other formats
def convertFromRGB(code) :
    print('convert RGB: ', code)
    convertToHex('rgb', code)
    # convertToCMYK('rgb', code)
    # convertToHSL('rgb', code)

def convertToRGB(codeFormat, code) :
    rgbValue = '' 

    if codeFormat == 'hex' :
        
        tempSum = 0
        i = 0
        while i < 6 :
            tempSum += int(code[i], 16) * 16
            tempSum += int(code[i+1], 16)
            rgbValue += str(tempSum) + ' '
            i = i + 2
            tempSum = 0
    
    print('RGB: ', rgbValue)



##
# INPUT VALIDATION SECTION
##

# Takes in a string. Returns True if valid Hex color code.
def validateHex(value) :
    if len(value) != 6 :
        print('ERROR: Improper number of values for hex (should be 6 digits)')
        return False

    for i in range(len(value)):
        if value[i-1].isnumeric() :
            continue
        elif HEX_LETTERS.count(value[i-1]) != 0 :
            continue
        else :
            print('ERROR: Invalid character in hex code')
            return False

    return True


# Takes in a list of numerical strings. Returns True if valid RGB values. 
def validateRGB(values) :
    if len(values) != 3 :
        print('ERROR: Improper number of values for RGB (should be 3)')
        return False

    for value in values :
        if not value.strip().isnumeric() :
            print('ERROR: Improper format for RGB value(s)')
            return False
        value = int(value)
        if (value < 0) or (value > 255) :
            print('ERROR: Each RBG value must be between 0-255')
            return False
    return True

# Takes in a string. Returns True if valid CMYK values.
def validateCMYK(values) :
    if len(values) != 4 :
        print('ERROR: Improper number of values for CMYK (should be 4)')
        return False
    
    for value in values :
        if not value.isnumeric() :
            print('ERROR: Improper format for CMYK value(s). All values must be numeric and between 0-100(%)!')
            return False
        value = int(value)
        if (value < 0) or (value > 100) :
            print('ERROR: Each CMYK value must be between 0-100(%)')
            return False
    
    return True

   

##
# GENERAL UTILITIES
##

# Takes in the program's arguments generated by argparse. Returns True if valid arguments
def validateArguments(args) :
    # First, check that only one input flag is being used
    flagsActive = 0
    for flag in range(len(vars(args))-1) :
        # this uses our TYPES list to key into the args dictionary and determine how many flags are True
        if vars(args)[TYPES[flag]] :
            flagsActive += 1
        if flagsActive > 1 :
            print('ERROR: Currently this tool only supports one input type at a time. Too many flags!')
            return False

    # Second, check that there is a color code to convert
    if len(args.color) == 0 :
        print('ERROR: Must enter both an input flag and color code (did you forget to wrap color code in quotes?)\nFor more info, use the \'-h\' or \'--help\' flag.')
        return False
    
    return True
 

# Takes in a decimal number and converts it to hexadecimal
def hex(number) :
    number = int(number)
    if number > 16 :
        print("ERROR: Decimal to Hexidecimal conversion failed")
        return "ERROR: Decimal to Hexidecimal conversion failed" 
    if number < 10 :
        return str(number)
    return HEX_LETTERS[number % 10]



if __name__ == '__main__' :
    main()
