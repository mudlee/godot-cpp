import click
import subprocess


def init():
    print('Compile Godot C++ bindings...')
    result = subprocess.run(['scons', 'platform=osx', 'use_llvm=yes', 'bits=64'], cwd='bindings/godot-cpp')
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError('Could not compile Godot C++ bindings, see error above')

    #print('Compile bindings...')
    #result = subprocess.run(['scons','-f', 'bindings/SConstruct', 'platform=osx', 'use_llvm=yes'])
    #if result.returncode != 0:
        #print(result.stderr)
        #raise RuntimeError('Could not compile bindings, see error above')


@click.command()
@click.option("--run", help="Run's a command", type=str)
# @click.option("--init", help="Initializes C++ support for Godot")
# @click.option("--create_class", help="Create's a C++ class, usage: --create_class=classname")
# @click.option("--rename_class", help="Rename's a C++ class, usage: --rename_class=oldname:newname")
def main(run):
    if run == 'init':
        init()


if __name__ == '__main__':
    main()
