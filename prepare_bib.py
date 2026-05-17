import bibtexparser

import os
import glob
import jinja2
import numpy as np
import re
from datetime import datetime as dt
from pylatexenc.latex2text import LatexNodes2Text


files = glob.glob('_publications/*')
for f in files:
    os.remove(f)

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader="bibliography/",
    autoescape=select_autoescape()
)

templateLoader = jinja2.FileSystemLoader( searchpath="bibliography" )
templateEnv = jinja2.Environment( loader=templateLoader )

template = templateEnv.get_template( "bib_template.md" )

#parser = BibTexParser(common_strings=True)
with open('bibliography/callaghan-publications.bib') as file:
    bib_db = bibtexparser.load(file)

#bib_db = bibtexparser.parse_file('bibliography/callaghan-publications.bib')

#os.remove("_cv/nocite.tex")

entries = [x for x in bib_db.entries if re.match("\w",x["title"])]



#dates = np.array([dt.strptime(f'{e["year"]}-{e["month"]}',"%Y-%b") for e in entries])
dates = np.array([dt.strptime(f'{e["year"]}',"%Y") for e in entries])

print(dates)

n = 0

author_set = set([])

with open("_cv/nocite.tex", "w") as ncf:
    for i in np.argsort(dates)[::-1]:
        
        n+=1

        e = {}
        #print(entries[i])
        #print(dir(entries[i]))
        for k,v in entries[i].items():
            e[k] = v#.value

        e["title"] = e["title"].replace("{","").replace("}","")
        fname = f"_publications/{n:03d}.md"
        authors = e["author"].split(" and ")
        for a in authors:
            author_set.add(a.split(',')[0].replace('{','').replace('}',''))
        authors = ["<b>"+x+"</b>" if "Callaghan" in x else x for x in authors]
        e["author"] = ", ".join(authors)
        if "journal" in e:
            e["journal"] = e["journal"].replace("\\","")
        e["author"] = LatexNodes2Text().latex_to_text(e["author"])
        ncf.write(r"\nocite{" + entries[i]['ID'] + "}")
        ncf.write("\n")
        with open(fname, "w") as f:
            f.write(template.render({"e":e, "i": n}))

print(author_set)
print(len(author_set))