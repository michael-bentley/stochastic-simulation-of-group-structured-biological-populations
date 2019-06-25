# stochastic-simulation-of-biological-populations

A model from from [Allen & Dytham (2009)](#references) written in Python. The model is used to demonstrate the use of an individual-based, stochastic simulation of biological populations in continuous time.

## Introduction

Two algorithms are coded up from the paper: 1) a novel algorithm from [Allen & Dytham (2009)](#references), here called the A&D Method; and 2) the Gillespie Alorithm developed in [Gillespie (1976, 1979)](#references), and otherwise known as the Direct Method. Whilst the A&D Method performs much faster than the Direct Method and converges on the same solution, it appears to generate much noisier outputs around that solution (general observation, not formally tested).

## References

Allen, George Edward, and Calvin Dytham. "[An efficient method for stochastic simulation of biological populations in continuous time.](https://www.sciencedirect.com/science/article/pii/S0303264709001130)" Biosystems 98.1 (2009): 37-42.

Gillespie, Daniel T. "[A general method for numerically simulating the stochastic time evolution of coupled chemical reactions.](https://www.sciencedirect.com/science/article/pii/0021999176900413)" Journal of computational physics 22.4 (1976): 403-434.

Gillespie, Daniel T. "[Exact stochastic simulation of coupled chemical reactions.](https://pubs.acs.org/doi/pdf/10.1021/j100540a008)" The journal of physical chemistry 81.25 (1977): 2340-2361.

