# Sandbox for Bazel build rules for FFIG.

load("//:ffig.bzl", 
     "ffig_c_library", 
     "ffig_csharp_src", 
     "ffig_py_src", 
     "ffig_swift_src")

filegroup(
    name = "ffig_headers",
    srcs = glob(["ffig/include/**/*.h"]),
)

cc_library(
    name = "libffig",
    hdrs = glob(["ffig/include/ffig/*.h"]),
)

py_binary(
    name = "ffig_py",
    srcs = glob(["ffig/**/*.py"]),
    data = glob([
        "ffig/**/*.tmpl",
        "ffig/**/*.macros",
        "ffig/**/*.h",
    ]),
    main = "__main__.py",
)

ffig_c_library(
    name = "Shape",
    module = "Shape",
    srcs = ["tests/input/Shape.h"],
    copts = [
        "-Itests/input",
        "-Iffig/include",
        "-std=c++14",
        "-DShape_c_EXPORTS"
    ],
    deps = [":libffig"],
)

ffig_csharp_src(
    name = "Shape.net.src",
    module = "Shape",
    srcs = ["tests/input/Shape.h"],
    copts = [
        "-Itests/input",
        "-Iffig/include",
        "-std=c++14",
    ],
    deps = [":libffig"],
)

ffig_py_src(
    name = "Shape.py.src",
    module = "Shape",
    srcs = ["tests/input/Shape.h"],
    copts = [
        "-Itests/input",
        "-Iffig/include",
        "-std=c++14",
    ],
    deps = [":libffig"],
)

ffig_swift_src(
    name = "Shape.swift.src",
    module = "Shape",
    srcs = ["tests/input/Shape.h"],
    copts = [
        "-Itests/input",
        "-Iffig/include",
        "-std=c++14",
    ],
    deps = [":libffig"],
)
