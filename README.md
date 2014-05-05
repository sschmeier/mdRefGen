NAME: mdRefGen.py
=================

DESCRIPTION
-----------

Sometimes it is diserable to create a bibliography out of markdown
references/links and append this to the end of a markdown-file. In a first
step we are dealing here with numbered references. Later we extend this to
alphanumeric references.

For a markdown-file with numbered references of the form, e.g.:

    There are several articles showing how to properly write a grant [[1],[2]].

    [1]: http://www.ncbi.../PMC1378105/ "Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)"
    [2]: http://www.blahblahblah.com "This is it!"


Find all those references and append a Biobliography to the document e.g.:

    There are several articles showing how to properly write a grant [[1],[2]].

    [1]: http://www.ncbi.../PMC1378105/ "Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)"
    [2]: http://www.blahblahblah.com "This is it!"
    ##Bibliography
    1. [Ten Simple Rules for Getting Grants. Bourne PE and Chalupa LM. PLoS Comput Biol. 2006; 2(2)] [1]
    2. [This is it!] [2]


INSTALLATION
------------

Generally speaking you only need a working Python intallation.
This script was developed using Python 2.7.3.

Local install:
Put this script in the direction where your markdown-files are located

Global install:
Make the script executeable and copy it to a directory that is in your PATH variable (e.g. ~/bin):

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
