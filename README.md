# Middy

[![PyPI](https://img.shields.io/badge/Discord.PY-v1.0.0a-orange.svg)](https://pypi.python.org/pypi/discord.py/)
[![PyPI](https://img.shields.io/pypi/pyversions/discord.py.svg)](https://pypi.python.org/pypi/discord.py/)

Middy is an Bot written for Discord for the Mega Shogun discord channel

The LFM does a bit of offloading to an external server via HTTP, this was to make life a little easier
with MySQL plus the server Middy runs on is a development server that doesn't have MySQL or some of the needed
packages to make this work efficiently

## Installation

if you want to contribute to Middy or just like running things, the following is how you can install and run your own instance of middy.

Before installing and running your own instance of middy, you will first need to install the following:

* Python 3.6
* Pip
* Dependencies: `python3.6 -m pip install -r requirements.txt`
* The rewrite version of [discord.py](https://github.com/Rapptz/discord.py) with voice support: `python3.6 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]`
