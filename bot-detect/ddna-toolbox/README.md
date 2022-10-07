# [Digital DNA Toolbox](https://ocean.sagepub.com/blog/2018/6/22/digital-dna-how-to-map-our-online-behavior?rq=DDNA)

<!--
[![Travis Status](https://travis-ci.org/scikit-learn-contrib/project-template.svg?branch=master)](https://travis-ci.org/scikit-learn-contrib/project-template)
[![Coveralls Status](https://coveralls.io/repos/scikit-learn-contrib/project-template/badge.svg?branch=master&service=github)](https://coveralls.io/r/scikit-learn-contrib/project-template)
[![CircleCI Status](https://circleci.com/gh/scikit-learn-contrib/project-template.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/scikit-learn-contrib/project-template/tree/master)
-->

[![SAGE Publishing logo](https://uk.sagepub.com/sites/all/themes/sage_corp/logo.svg)](https://uk.sagepub.com/en-gb/eur/home)

This project has been possible thanks to [SAGE Ocean Concept Grants 2018](https://ocean.sagepub.com/concept-grants).

This project was build upon the [scikit-learn template](http://contrib.scikit-learn.org/project-template/) in order to be compatible with the scikit-learn pipelines and (hyper)parameter search, while facilitating testing (including some API compliance), documentation, open source development, packaging, and continuous integration.

## Installation

This module in order to work needs:
- Python v3.6.x or greater
- `numpy` package
- `glcr` python module - available [here](https://github.com/WAFI-CNR/glcr)


You can download and install `digitaldna` as follow:

```shell
git clone https://github.com/WAFI-CNR/ddna-toolbox
cd ddna-toolbox
git clone https://github.com/WAFI-CNR/glcr

pip install numpy 
pip install glcr/.
pip install .
```

## Getting started

If the installation is successful, and `digitaldna` is correctly installed,
you should be able to execute the following in Python:

```python
from digitaldna.lcs import LongestCommonSubsequence
X = ['banana', 'ananan', 'anana', 'hanoi', 'banas']
estimator = LongestCommonSubsequence()
estimator.fit_predict(X)
```

Some usage examples can be found in the documentation [website](https://wafi-cnr.github.io/ddna/stable/quick_start.html).

You can find other examples in this [page](examples/notebook/DigitalDNA_python_package.md)

## Credits and Aknowledgement

This library has been made possible thanks to the collaboration and contribution of:
- [SAGE Publishing](https://uk.sagepub.com/en-gb/eur/home)
- [Bellomo Salvatore](https://www.iit.cnr.it/en/salvatore.bellomo)
- [Cresci Stefano](https://www.iit.cnr.it/en/stefano.cresci)
- [Gagliano Giuseppe](https://github.com/giuseppegagliano)
- [Martella Antonio](https://www.iit.cnr.it/en/antonio.martella)
- [Spognardi Angelo](https://angelospognardi.site.uniroma1.it)
- [Tesconi Maurizio](https://www.iit.cnr.it/en/maurizio.tesconi)
- ... and all the contributors of this opensource library

## Want to contribute?

If you want to contribute you can refer to the scikit-learn template documentation:

- [scikit-learn template homepage](http://contrib.scikit-learn.org/project-template/)
- [scikit-learn template source code](https://github.com/scikit-learn-contrib/project-template)
- [scikit-learn Contributing section](http://scikit-learn.org/stable/developers/contributing.html)

### Useful links

- [Social Fingerprinting: Detection of Spambot Groups Through DNA-Inspired Behavioral Modeling](https://ieeexplore.ieee.org/document/7876716)
- [Exploiting Digital DNA for the Analysis of Similarities in Twitter Behaviours](https://ieeexplore.ieee.org/document/8259831)
- [Linear Time Algorithms for Generalizations of the Longest Common Substring Problem](https://link.springer.com/article/10.1007/s00453-009-9369-1)
- [Scikit-learn Template Documentation](http://contrib.scikit-learn.org/project-template/)
