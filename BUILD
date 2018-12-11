# Uses of Bazel build rules for FFIG.

load(
    "//:ffig.bzl",
    "ffig_c_library",
    "ffig_csharp_src",
    "ffig_py_src",
    "ffig_ruby_src",
    "ffig_swift_src",
)

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

FFIG_C_OPTS = [
    "-Itests/input",
    "-Iffig/include",
    "-std=c++14",
    "-DShape_c_EXPORTS",
]

ffig_c_library(
    name = "Shape",
    srcs = ["tests/input/Shape.h"],
    copts = FFIG_C_OPTS,
    module = "Shape",
)

ffig_csharp_src(
    name = "Shape.net.src",
    srcs = ["tests/input/Shape.h"],
    copts = FFIG_C_OPTS,
    module = "Shape",
)

ffig_py_src(
    name = "Shape.py.src",
    srcs = ["tests/input/Shape.h"],
    copts = FFIG_C_OPTS,
    module = "shape",
)

ffig_swift_src(
    name = "Shape.swift.src",
    srcs = ["tests/input/Shape.h"],
    copts = FFIG_C_OPTS,
    module = "Shape",
)

ffig_ruby_src(
    name = "Shape.rb.src",
    srcs = ["tests/input/Shape.h"],
    copts = FFIG_C_OPTS,
    module = "Shape",
)
