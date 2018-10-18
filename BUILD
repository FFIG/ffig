# Sandbox for Bazel build rules for FFIG.

load("//:ffig.bzl", "ffig_c_library")

filegroup(
    name="ffig_headers",
    srcs=glob(["ffig/include/**/*.h"])
    )

cc_library(
    name = "libffig",
    hdrs = glob(["ffig/include/ffig/*.h"])
    )

py_binary(
    name = "ffig_py",
    srcs = glob(["ffig/**/*.py"]),
    main = "__main__.py",
    data = glob(["ffig/**/*.tmpl", "ffig/**/*.macros", "ffig/**/*.h"])
    )

ffig_c_library(
    name="Shape", 
    srcs=["tests/input/Shape.h"],
    copts=["-Itests/input", "-Iffig/include","-std=c++14"],
    deps=[":libffig"]
    )

