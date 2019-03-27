# Godot C++ Integration

## Requirements

- Python 3
- Scons

## Usage

### Initializing
    
    python gd-cpp.py --platform=osx --cmd=init
    
### Creating Class

    python gd-cpp.py --platform=osx --cmd=add_class --cpp=MyClass
    
### Renaming Class
    
    python gd-cpp.py --run mv_class OldClass:NewClass