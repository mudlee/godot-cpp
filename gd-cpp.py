import click
import subprocess
import os
from os import listdir
from os.path import isfile, join


def init(platform):
    print('Compile Godot C++ bindings...')
    result = subprocess.run([
        'scons',
        'platform={platform}'.format(platform=platform),
        'generate_bindings=yes',
        'bits=64'
    ], cwd='godot-cpp')
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError('Could not compile Godot C++ bindings, see error above')


def build(platform):
    if not os.path.exists('../src'):
        os.mkdir('../src')

    result = subprocess.run([
        'scons',
        'platform={platform}'.format(platform=platform),
        'use_llvm=yes'
    ], cwd='./')
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError('Could not compile bindings, see error above')


def check_cpp(cmd, cpp):
    if cpp is None:
        raise click.BadArgumentUsage('{} needs --cpp flag'.format(cmd))


def generate_library():
    cpp_files = [f for f in listdir('../src') if isfile(join('../src', f)) and f.endswith('.hpp')]

    with open('templates/library.cpp.template', 'r') as file:
        library_content = file.read().format(
            INCLUDE_CLASSES='\n'.join('#include "{f}"'.format(f=f) for f in cpp_files),
            REGISTER_CLASSES='\n'.join(
                'godot::register_class<godot::{f}>();'.format(f=f.replace('.hpp', '')) for f in cpp_files)
        )

    with open('../src/library.cpp', 'w') as file:
        file.write(library_content)


def add_class(class_name):
    with open('templates/hpp.template', 'r') as file:
        hpp_content = file.read().format(CLASS_NAME=class_name)

    with open('templates/cpp.template', 'r') as file:
        cpp_content = file.read().format(CLASS_NAME=class_name)

    with open('templates/gdns.template', 'r') as file:
        gdns_content = file.read().format(CLASS_NAME=class_name)

    with open('templates/gdnlib.template', 'r') as file:
        gdnlib_content = file.read().format(CLASS_NAME=class_name)

    with open('../src/'+class_name+'.hpp', 'w') as file:
        file.write(hpp_content)

    with open('../src/'+class_name+'.cpp', 'w') as file:
        file.write(cpp_content)

    with open('../bin/'+class_name+'.gdns', 'w') as file:
        file.write(gdns_content)

    with open('../bin/'+class_name+'.gdnlib', 'w') as file:
        file.write(gdnlib_content)

    print(class_name+' created')


def remove_file(file):
    try:
        os.remove(file)
    except OSError:
        pass


def rm_class(class_name):
    remove_file('../src/' + class_name + '.hpp')
    remove_file('../src/' + class_name + '.cpp')
    remove_file('../src/' + class_name + '.os')
    remove_file('../bin/' + class_name + '.gdnlib')
    remove_file('../bin/' + class_name + '.gdns')

    print(class_name + ' deleted')


@click.command()
@click.option('--platform', type=click.Choice(['osx', 'windows']), help="Type of your platform. osx or windows")
@click.option("--cmd", help="Runs a command", type=click.Choice(['init', 'build', 'add_class', 'rm_class', 'mv_class']))
@click.option("--cpp", help="Parameters for class commands")
def main(platform, cmd, cpp):
    if platform is None:
        raise ValueError('--platform is a required parameter')

    if cmd == 'init':
        init(platform)
        build(platform)
    elif cmd == 'build':
        build(platform)
    elif cmd == 'add_class':
        check_cpp(cmd, cpp)
        add_class(cpp)
        generate_library()
        build(platform)
    elif cmd == 'rm_class':
        check_cpp(cmd, cpp)
        rm_class(cpp)
        generate_library()
        build(platform)
    elif cmd == 'mv_class':
        check_cpp(cmd, cpp)
        classes = str(cpp).split(':')
        rm_class(classes[0])
        add_class(classes[1])
        generate_library()
        build(platform)


if __name__ == '__main__':
    main()
