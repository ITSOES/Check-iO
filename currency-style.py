import re
def checkio(text):
    print re.findall(r'\$[0-9]{1,3}(?:\.[0-9]{3})*(?:,[0-9][0-9])?\b', text)
    "Convert Euro style currency in dollars to US/UK style"
    return ""

if __name__ != '__main__':

    #These "asserts" using only for self-checking and not necessary for auto-testing
    #assert checkio("$1.234.567,89") == "$1,234,567.89" , "1st Example"
    #assert checkio("$0,89") == "$0.89" , "2nd Example"
    assert checkio("Euro Style = $12.345,67, US Style = $12,345.67") == \
                   "Euro Style = $12,345.67, US Style = $12,345.67" , "European and US"
    assert checkio("Us Style = $12,345.67, Euro Style = $12.345,67") == \
                   "Us Style = $12,345.67, Euro Style = $12,345.67" , "US and European"
    assert checkio("$1.234, $5.678 and $9") == \
                   "$1,234, $5,678 and $9", "Dollars without cents"
