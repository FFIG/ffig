import os

root_dir = os.path.dirname(__file__)

flags = "-x c++ -std=c++14 -stdlib=libc++ -I{0}/build/generated -Iffig/include -isystem /usr/include/c++/v1 -isystem {0}/externals/catch2/single_include".format(
    root_dir).split()


def FlagsForFile(filename, **kwargs):
    return {'flags': flags, 'do_cache': True}
