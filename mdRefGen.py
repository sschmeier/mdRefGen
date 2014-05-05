#!/usr/bin/env python
"""
NAME: mdRefGen.py
=================

DESCRIPTION
-----------

Sometimes it is desired to create a bibliography out of markdown references/links and append this to the end of a markdown-file. In a first step we are dealing here with numbered references. Later we extend this to alphanumeric references.

For a markdown-file with numbered references of the form, e.g.:

    There are several articles showing how to properly write a grant [[1],[2]].

    [1]: http://www.ncbi.../PMC1378105/ "Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)"
    [2]: http://www.blahblahblah.com "This is it!"


Find all those references and append a bibliography to the document e.g.:

    There are several articles showing how to properly write a grant [[1],[2]].

    [1]: http://www.ncbi.../PMC1378105/ "Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)"
    [2]: http://www.blahblahblah.com "This is it!"
    ##Bibliography
    1. [Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)] [1]
    2. [This is it!] [2]


INSTALLATION
------------

Generally speaking you only need a working Python installation. This script was developed using Python 2.7.3.

Local install:
Put this script in the direction where your markdown-files are located.

Global install:
Make the script executable and copy it to a directory that is in your PATH variable (e.g. ~/bin):

```bash
>chmod u+x mdRefGen.py
>cp mdRefGene.py ~/bin
#test
>mdRefGen.py -h
```

USAGE
-----

python mdRefGen.py [-h] [-v] [-o STRING] [-r] [-b] [--noLinks] [--onlyRef] FILE

Examples:

```bash
# Some simple tests:
>python mdRefGen.py -h 
>python mdRefGen.py -r test_numeric.md
# More involved:
>python mdRefGen.py -r test_numeric.md -o test_numeric2.md
>pandoc -f markdown_github -t docx test_numeric2.md -o test_numeric2.docx
```

VERSION HISTORY
---------------

0.1    2014/05/02    Initial version.
"""
__version__='0.1'
__date__='2014/05/02'
__email__='s.schmeier@gmail.com'
__author__='Sebastian Schmeier'
import sys, argparse, re
import gzip, bz2, zipfile

def parse_cmdline():
    
    # parse cmd-line -----------------------------------------------------------
    sDescription = 'Read a markdown-file and find all references/links in the text and append a Bibliography or Referneces to the document.'
    sVersion='version %s, date %s' %(__version__,__date__)
    sEpilog = '''DESCRIPTION:

For a markdown-file with numbered references of the form, e.g.:

---
There are several articles showing how to properly write a grant [[1],[2]].

[1]: http://www.ncbi.../PMC1378105/  "Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)"
[2]: http://www.blah.com "This is it!"
---

Find all those references and append a Biobliography to the document e.g.:


---
There are several articles showing how to properly write a grant [[1],[2]].

[1]: http://www.ncbi.../PMC1378105/  "Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)"
[2]: http://www.blah.com "This is it!"
##Bibliography
1. [Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)] [1]
2. [This is it!] [2]
---


Copyright %s (%s)''' %(__author__, __email__)

    oParser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                      description=sDescription,
                                      version=sVersion,
                                      epilog=sEpilog)
    oParser.add_argument('sFile',
                         metavar='FILE',
                         help='Delimited file. [if set to "-" or "stdin" reads from standard in]')
    oParser.add_argument('-o', '--out',
                         metavar='STRING',
                         dest='sOut',
                         default=None,
                         help='Out-file. If you wish to replace the input file just use same name. [default: "stdout"]')
    oParser.add_argument('-r', '--reference',
                         dest='bRef',
                         action='store_true',
                         default=False,
                         help='If you which a "References" header')
    oParser.add_argument('-b', '--bibliography',
                         dest='bBib',
                         action='store_true',
                         default=False,
                         help='If you which a "Bibliography" header')
    oParser.add_argument('-l', '--level',
                         metavar='INTEGER',
                         type=int,
                         dest='iLevel',
                         default=2,
                         help='Header level for the references/bibliography header. [default: "2"]')
    oParser.add_argument('--noLinks',
                         dest='bLinks',
                         action='store_false',
                         default=True,
                         help='If you do NOT wish the reference entries to be links themselves.')
    oParser.add_argument('--onlyRef',
                         dest='bOnly',
                         action='store_true',
                         default=False,
                         help='If you do NOT wish to append the reference to the origianl text, but only print the reference.')
    
    oArgs = oParser.parse_args()
    return oArgs, oParser

def load_file(s):
    if s in ['-', 'stdin']:
        oF = sys.stdin
    elif s.split('.')[-1] == 'gz':
        oF = gzip.open(s)
    elif s.split('.')[-1] == 'bz2':
        oF = bz2.BZFile(s)
    elif s.split('.')[-1] == 'zip':
        oF = zipfile.Zipfile(s)
    else:
        oF = open(s)
    return oF

def main():
    ## Parse the command-line
    oArgs, oParser = parse_cmdline()

    ## Load the file
    oF = load_file(oArgs.sFile)

    ## Load input lines into list
    ## Not memory sufficient but if we want to do on the fly printing
    ## No time to change it at the moment.
    aLines = oF.readlines() 
    oF.close()
    
    if oArgs.sFile == oArgs.sOut:
        oFout = open(oArgs.sOut, 'a')
    elif not oArgs.sOut:
        oFout = sys.stdout
    elif oArgs.sOut in ['-', 'stdout']:
        oFout = sys.stdout
    else:
        oFout = open(oArgs.sOut, 'w')

    ## Parse line by line.
    dNum = {}
    dAlpha = {}
    oReg1 = re.compile('^\[(\d+)\]:\s+(.+)\s+"(.+)"') ## regular expression
    oReg2 = re.compile('^\[(.+)\]:\s+(.+)\s+"(.+)"')
    for sLine in aLines:
        if not oArgs.bOnly: oFout.write(sLine) ## write original line
        oRes1 = oReg1.search(sLine) ## search reference
        oRes2 = oReg2.search(sLine) ## search reference
        if oRes1:
            dNum[int(oRes1.group(1))] = (oRes1.group(2), oRes1.group(3))
        elif oRes2:
            dAlpha[oRes2.group(1)] = (oRes2.group(2), oRes2.group(3))
            
    ## Header?
    if oArgs.bRef:
        oFout.write('%sReferences\n' %('#' * oArgs.iLevel))
    elif oArgs.bBib:
        oFout.write('%sBibliography\n'%('#' * oArgs.iLevel))
    ## Links?
    if oArgs.bLinks:
        if dNum:
            aKeys = dNum.keys()
            aKeys.sort()
            for sID in aKeys:
                oFout.write('%s. [%s] [%s]\n' %(sID, dNum[sID][1], sID))
        elif dAlpha:
            aKeys = dAlpha.keys()
            aKeys.sort()
            for sID in aKeys:
                oFout.write('[%s] [%s]\n' %(dAlpha[sID][1], sID))

    else:
        if dNum:
            aKeys = dNum.keys()
            aKeys.sort()
            for sID in aKeys:
                oFout.write('%s. %s\n' %(sID, dNum[sID][1]))
        elif dAlpha:
            aKeys = dAlpha.keys()
            aKeys.sort()
            for sID in aKeys:
                oFout.write('%s\n' %(dAlpha[sID][1]))
    return
        
if __name__ == '__main__':
    sys.exit(main())
