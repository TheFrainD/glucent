# glucent
glucent is a simple closs-platform OpenGL core profile loader and wrapper

## Build
#### Prerequisites
- CMake (at least 3.16)
- Python (3.x)

#### Generating loader
A python script `gengl.py` generates an OpenGL loader files that a necessary to build the library. You can specify extension families you want to load by using `-ext (or -e)`. Available extension families:

- ext  (generic extensions)
- arb
- khr
- ovr
- nv
- amd
- intel
- mesa

To generate loader with no extensions:
```
python gengl.py
```

To generate loader with specified extensions:
```
python gengl.py -ext ext arb khr
```

#### CMake
Building with CMake is pretty straitforward. Currently library doesn't support building shared libraries.