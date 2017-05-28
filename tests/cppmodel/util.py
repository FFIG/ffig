# This file provides common utility functions for the test suite.

from ffig.clang.cindex import Cursor, TranslationUnit, Config

import os.path
import sys

Config.set_compatibility_check(False)


def find_clang_library_path():
    paths = [
        '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib',
        '/Library/Developer/CommandLineTools/usr/lib',
    ]
    for path in paths:
        if os.path.isfile(os.path.join(path, 'libclang.dylib')):
            return path
    raise Exception('Unable to find libclang.dylib')

if sys.platform == 'darwin':
    # OS X doesn't use DYLD_LIBRARY_PATH if System Integrity Protection is
    # enabled. Set the library path for libclang manually.
    Config.set_library_path(find_clang_library_path())


def get_tu(source, lang='c', all_warnings=False, flags=[]):
    """Obtain a translation unit from source and language.

    By default, the translation unit is created from source file "t.<ext>"
    where <ext> is the default file extension for the specified language. By
    default it is C, so "t.c" is the default file name.

    Supported languages are {c, cpp, objc}.

    all_warnings is a convenience argument to enable all compiler warnings.
    """
    args = list(flags)
    name = 't.c'
    if lang == 'cpp':
        name = 't.cpp'
        args.extend('-std=c++11 -stdlib=libc++'.split())
    elif lang == 'objc':
        name = 't.m'
    elif lang != 'c':
        raise Exception('Unknown language: %s' % lang)

    if all_warnings:
        args += ['-Wall', '-Wextra']

    return TranslationUnit.from_source(
        name, args, unsaved_files=[(name, source)])


def get_named_tu(source, name, all_warnings=False, flags=[]):
    """Obtain a translation unit from source and filename.

    Language is deduced from the filename.

    The filename does not need to correspond to a real file but will be the
    name of an unsaved translation unit.
    """

    args = list(flags)
    if name.endswith('cpp') or name.endswith('.cxx'):
        args.extend('-x c++ -std=c++11 -stdlib=libc++'.split())
    if all_warnings:
        args += ['-Wall', '-Wextra']

    return TranslationUnit.from_source(
        name, args, unsaved_files=[(name, source)])


def get_cursor(source, spelling):
    """Obtain a cursor from a source object.

    This provides a convenient search mechanism to find a cursor with specific
    spelling within a source. The first argument can be either a
    TranslationUnit or Cursor instance.

    If the cursor is not found, None is returned.
    """
    # Convenience for calling on a TU.
    root_cursor = source if isinstance(source, Cursor) else source.cursor

    for cursor in root_cursor.walk_preorder():
        if cursor.spelling == spelling:
            return cursor

    return None


def get_cursors(source, spelling):
    """Obtain all cursors from a source object with a specific spelling.

    This provides a convenient search mechanism to find all cursors with
    specific spelling within a source. The first argument can be either a
    TranslationUnit or Cursor instance.

    If no cursors are found, an empty list is returned.
    """
    # Convenience for calling on a TU.
    root_cursor = source if isinstance(source, Cursor) else source.cursor

    cursors = []
    for cursor in root_cursor.walk_preorder():
        if cursor.spelling == spelling:
            cursors.append(cursor)

    return cursors


__all__ = [
    'get_cursor',
    'get_cursors',
    'get_tu',
]
