#!/usr/bin/env python3
import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSIONFILE="plot_phylo/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
     name='plot_phylo',
     version=verstr,
     author="Katy Brown, Duncan Cross",
     author_email="kab84@cam.ac.uk",
     description="Module to draw a phylogenetic tree using matplotlib",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/KatyBrown/plot_phylo",
     packages=setuptools.find_packages(),
     package_dir={'plot_phylo':'plot_phylo'},
     install_requires=['matplotlib', 'ete3'],
     scripts=['plot_phylo/plot_phylo.py'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"]
 )
