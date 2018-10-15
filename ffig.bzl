LIBFFIG = "//:libffig"
FFIG_PY = "//:ffig_py"

def _ffig_gen_src(name, srcs, module, templates, copts, genfiles):
    ffig_py_path = "$(location {})".format(FFIG_PY)
    source_files = " ".join(["$(locations {})".format(src) for src in srcs])
    cflags = " ".join(["--cflag={}".format(copt) for copt in copts])

    # Generate source with FFIG.
    # $(@D) is the output directory for the target package.
    native.genrule(
        name = name,
        cmd = "{} -i {} -m {} -o $(@D) -b {} {}".format(
            ffig_py_path,
            source_files,
            module,
            " ".join(templates),
            cflags,
        ),
        srcs = srcs + ["//:ffig_headers"],
        outs = genfiles,
        tools = [FFIG_PY, LIBFFIG],
    )

def ffig_c_library(name, module, srcs = None, deps = None, copts = None):
    if len(srcs) != 1:
        fail("ffig_c_library only supports a single source file.")

    srcs = srcs or []
    deps = deps or []
    copts = copts or []

    # Generate source with FFIG.
    genfiles = [module + "_c.h", module + "_c.cpp"]
    _ffig_gen_src(
        name = "_" + name + "_c_srcs",
        srcs = srcs,
        module = module,
        templates = ["_c.h.tmpl", "_c.cpp.tmpl"],
        copts = copts,
        genfiles = genfiles,
    )

    # Build a C DSO for FFIG's generated C-API.
    native.cc_binary(
        name = name + "_c.so",
        linkshared = 1,
        srcs = genfiles + srcs,
        deps = deps,
        copts = copts,
    )

    # Package the DSO and generated header into a cc_library.
    native.cc_library(
        name = name,
        hdrs = [name + "_c.h"],
        srcs = [":" + name + "_c.so"],
    )

def ffig_csharp_src(name, module, srcs = None, deps = None, copts = None):
    if len(srcs) != 1:
        fail("ffig_csharp_src only supports a single source file.")

    srcs = srcs or []
    deps = deps or []
    copts = copts or []

    # Generate source with FFIG.
    genfiles = [module + ".cs"]
    _ffig_gen_src(
        name = "_" + name + "_c_srcs",
        srcs = srcs,
        module = module,
        templates = ["cs.tmpl"],
        copts = copts,
        genfiles = genfiles,
    )

def ffig_py_src(name, module, srcs = None, deps = None, copts = None):
    if len(srcs) != 1:
        fail("ffig_py_src only supports a single source file.")

    srcs = srcs or []
    deps = deps or []
    copts = copts or []

    # Generate source with FFIG.
    genfiles = [module + "/_py2.py", module + "/_py3.py", module + "/__init__.py"]
    _ffig_gen_src(
        name = "_" + name + "_c_srcs",
        srcs = srcs,
        module = module,
        templates = ["python"],
        copts = copts,
        genfiles = genfiles,
    )

def ffig_swift_src(name, module, srcs = None, deps = None, copts = None):
    if len(srcs) != 1:
        fail("ffig_swift_src only supports a single source file.")

    srcs = srcs or []
    deps = deps or []
    copts = copts or []

    # Generate source with FFIG.
    genfiles = [module + ".swift", module + "-Bridging-Header.h"]
    _ffig_gen_src(
        name = "_" + name + "_c_srcs",
        srcs = srcs,
        module = module,
        templates = ["swift"],
        copts = copts,
        genfiles = genfiles,
    )

def ffig_ruby_src(name, module, srcs = None, deps = None, copts = None):
    if len(srcs) != 1:
        fail("ffig_ruby_src only supports a single source file.")

    srcs = srcs or []
    deps = deps or []
    copts = copts or []

    # Generate source with FFIG.
    genfiles = [module + ".rb"]
    _ffig_gen_src(
        name = "_" + name + "_c_srcs",
        srcs = srcs,
        module = module,
        templates = ["ruby"],
        copts = copts,
        genfiles = genfiles,
    )
