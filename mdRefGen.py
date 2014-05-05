#!/usr/bin/env python
"""
NAME: mdRefGen.py
=================

DESCRIPTION
-----------

Sometimes it is diserable to create a bibliography out of markdown
references/links and append this to the end of a markdown-file. In a first
step we are dealing here with numbered references. Later we extend this to
alphanumeric references.

For a markdown-file with numbered references of the form, e.g.:

```
There are several articles showing how to properly write a grant [[1],[2]].

[1]: http://www.ncbi.../PMC1378105/ "Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)"
[2]: http://www.blahblahblah.com "This is it!"
```

Find all those references and append a Biobliography to the document e.g.:


```
There are several articles showing how to properly write a grant [[1],[2]].

[1]: http://www.ncbi.../PMC1378105/ "Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)"
[2]: http://www.blahblahblah.com "This is it!"
##Bibliography
1. [Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)] [1]
2. [This is it!] [2]
```

INSTALLATION
------------

Generally speaking you only need a working Python intallation.
This script was developed using Python 2.7.3.

Local install:
Put this script in the direction where your markdown-files are located

Global install:
Make the script executeable and copy it to a directory that is in your PATH variable (e.g. ~/bin):

```
>chmod u+x mdRefGen.py
>cp mdRefGene.py ~/bin
#test
>mdRefGen.py -h
```

USAGE
-----

python mdRefGen.py [-h] [-v] [-o STRING] [-r] [-b] [--noLinks] [--onlyRef] FILE

Examples:

```
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
import sys, argparse, collections, re
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
    oParser.add_argument('-b', '--biobliography',
                         dest='bBib',
                         action='store_true',
                         default=False,
                         help='If you which a "Bibliography" header')
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
    oArgs, oParser = parse_cmdline()

    ## Load the file
    oF = load_file(oArgs.sFile)

    d = collections.OrderedDict()
    oReg = re.compile('^\[(\d+)\]:\s+(.+)\s+"(.+)"') ## regular expression
    aLines = oF.readlines() ## load input lines
    oF.close()
    
    if oArgs.sFile == oArgs.sOut:
        oFout = open(oArgs.sOut, 'a')
    elif not oArgs.sOut:
        oFout = sys.stdout
    elif oArgs.sOut in ['-', 'stdout']:
        oFout = sys.stdout
    else:
        oFout = open(oArgs.sOut, 'w')

    for sLine in aLines:
        if not oArgs.bOnly and oArgs.sFile != oArgs.sOut:
            oFout.write(sLine)
        oRes = oReg.search(sLine)
        if oRes:
            d[oRes.group(1)] = (oRes.group(2), oRes.group(3))
            
    if oArgs.bRef:
        oFout.write('##References\n')
    elif oArgs.bBib:
        oFout.write('##Bibliography\n')
    if oArgs.bLinks:
        for sID in d:
            oFout.write('%s. [%s] [%s]\n' %(sID, d[sID][1], sID))
    else:
        for sID in d:
            oFout.write('%s. %s\n' %(sID, d[sID][1]))
    return
        
if __name__ == '__main__':
    sys.exit(main())
