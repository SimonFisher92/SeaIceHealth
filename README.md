### Sea Ice Health

- 1 Introduction
- 2 Installation
- 3 Usage
- 4 License
- 5 Acknowledgements
- 6 Contact

### Introduction

This codebase should allow users to generate heuristics on ice health other than the traditional ones of area, 
and volume. The codebase is written in Python. This is very much a work in progress and focuses on the class HealthIndex
upon which uses should iteratively build components to generate their own heuristics.

I have started here with fragmentation.

### Installation

To install the codebase, clone the repository and install the requirements as listed in requirements.txt. As a user,
you should first create a virtual environment and then install the requirements by the following command in terminal.
I like to do that in the following way:

```bash
git clone https://github.com/SimonFisher92/SeaIceHealth.git
cd SeaIceHealth
conda create -n seaicehealth python=3.10
conda activate seaicehealth
pip install -r requirements.txt
```

### Usage

First begin with the download_data.py script. This will download all requested data at 3.125 km resolution in .nc format.
You can tweak requested data by changing the arguments to the generate_links function (see top of download_data.py). The data
is downloaded to the path set in paths.py. 

Having done this, you can then run health_index.py. This will generate fragmentation data for the requested region and 
date space. You can see I am cropping data to the CAB (roughly), because the problem becomes inverted at seas with 
predominant open water.

Again, this is a work in progress. Probably the most useful function currently is the data
downloader.

### License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Acknowledgements

Users on the Arctic Sea Ice Forum, namely Kassy, John_the_Younger, Bruce Steele and uniquorn.

### Contact

Github messages preferred.