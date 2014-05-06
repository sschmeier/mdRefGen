NAME: mdRefGen.py
=================

DESCRIPTION
-----------

Sometimes it is desired to create a bibliography out of markdown references/links and append this to the end of a markdown-file.

###Numerical references

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

The result is a numbered list.

###Alphanumerical references

For a markdown-file with alphanumerical references of the form, e.g.:

    Here are two good articles outlining 10 important rules to follow for a good grant application and oral presentation [[Bourne and Chalupa 2006],[Bourne 2007]].

    [Bourne and Chalupa 2006]: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1378105/  "Bourne PE and Chalupa LM. Ten Simple Rules for Getting Grants. PLoS Comput Biol. Feb 2006; 2(2): e12."
    [Bourne 2007]: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1857815/ "Bourne PE. Ten Simple Rules for Making Good Oral Presentations. PLoS Comput Biol. Apr 2007; 3(4): e77."

Here we simply sort according to the tags, so the result will be:

    Here are two good articles outlining 10 important rules to follow for a good grant application and oral presentation [[Bourne and Chalupa 2006],[Bourne 2007]].

    [Bourne and Chalupa 2006]: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1378105/  "Bourne PE and Chalupa LM. Ten Simple Rules for Getting Grants. PLoS Comput Biol. Feb 2006; 2(2): e12."
    [Bourne 2007]: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1857815/ "Bourne PE. Ten Simple Rules for Making Good Oral Presentations. PLoS Comput Biol. Apr 2007; 3(4): e77."
    ##References
    [Bourne PE. Ten Simple Rules for Making Good Oral Presentations. PLoS Comput Biol. Apr 2007; 3(4): e77.] [Bourne 2007]
    [Bourne PE and Chalupa LM. Ten Simple Rules for Getting Grants. PLoS Comput Biol. Feb 2006; 2(2): e12.] [Bourne and Chalupa 2006]

This is a first try. This certainly needs improvement, but works for my purposes so far.

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

* 0.1.3  2014/05/05    Minor bug fix, when writing into the same document
* 0.1.2  2004/05/05    Added alphanumerical reference parsing.
* 0.1    2014/05/02    Initial version.
