# Godot C++ Integration

## Requirements

- Python 3
- Scons

## Install

 1. Create a Godot project (let's say under ```/home/user/cpp_test```)
 2. ```cd /home/user/cpp_test```
 3. ```git clone --recursive https://github.com/mudlee/godot-cpp.git```
 4. ```cd godot-cpp```
 5. ```pip install -r requirements.txt```
 6. Initialize C++ integration (see below) 

## Usage

### Initializing

This commands compiles the c++ bindings for your platforms.
    
    python gd-cpp.py --platform=osx --cmd=init
    
### Build

Recompiles your c++ code.
    
    python gd-cpp.py --platform=osx --cmd=build

### Creating Class

    python gd-cpp.py --platform=osx --cmd=add_class --cpp=MyClass

### Removing Class

    python gd-cpp.py --platform=osx --cmd=rm_class --cpp=MyClass
    
### Renaming Class
    
    python gd-cpp.py --platform=osx --cmd=mv_class --cpp=OldClass:NewClass
    
### License

Source code is released under MIT (see LICENSE).