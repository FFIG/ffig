# Sandbox for Bazel build rules for FFIG.

load("//:ffig.bzl", "ffig_c_library")

filegroup(
    name="ffig_headers",
    srcs=glob(["ffig/include/**/*.h"])
    )

ffig_c_library(
    name="Shape", 
    hdrs=["tests/input/Shape.h"],
    copts=["-Itests/input", "-Iffig/include","-std=c++14"],
    deps=[":libffig"]
    )

cc_library(
    name = "libffig",
    hdrs = glob(["ffig/include/ffig/*.h"])
    )

cc_binary(
    name = "shape_c.dll",
    linkshared = 1,
    srcs = ["build_out/generated/Shape_c.cpp", "build_out/generated/Shape_c.h",  "build_out/generated/Shape.h"],
    copts = [
        "-Iffig/include/",
        "-DShape_c_EXPORTS"
        ],
    deps = [":libffig"]
    )

py_binary(
    name = "ffig_py",
    srcs = glob(["ffig/**/*.py"]),
    main = "__main__.py",
    data = glob(["ffig/**/*.tmpl", "ffig/**/*.macros", "ffig/**/*.h"])
    )
