[![GitHub Actions Status: CI](https://github.com/Nikoleta-v3/Thesis/workflows/CI/badge.svg)](https://github.com/Nikoleta-v3/Thesis/actions?query=workflow%3ACI+branch%3Amaster)

# Understanding responses to environments for the Prisoner's Dilemma: A machine learning approach

This thesis contains the source code and the Latex documents for the thesis
titled ``Understanding responses to environments for the Prisoner's Dilemma: A
machine learning approach'' submitted in fulfillment of the requirements for the
degree of Doctor of Philosophy.

# Cloning

To clone the repository locally run the following command:

```
$ git clone  --recurse-submodules https://github.com/Nikoleta-v3/Thesis.git
```

Note that command includes the option `--recurse-submodules`. This is because
there are several submodules to this repository.

# Environment and requirements

All code for this thesis is in Python with all versions specified in `environment.yml`.

To create and activate the environment run:

```
$ conda env create -f environment.yml
$ source activate thesis
```

# Compiling the thesis document

Once the repository and the submodules have been cloned locally, and the conda
environment is activated run the following command to compile the written
document:

```
$ inv compile
```

