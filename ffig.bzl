LIBFFIG = "//:libffig"
FFIG_PY = "//:ffig_py"

def _ffig_gen_src(name, srcs = None, deps = None, module = None, templates = None, copts = None, genfiles = None):
    srcs = srcs or []
    deps = deps or []
    copts = copts or []

    if len(srcs) != 1:
        fail("ffig code generation only supports a single source file.")

    if not module:
        fail("module must be supplied")
    if not templates:
        fail("templates must be supplied")
    if not genfiles:
        fail("genfiles must be supplied")

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
    srcs = srcs or []
    deps = deps or []
    copts = copts or []

    c_srcs = [module + "_c.h", module + "_c.cpp"]

    # Generate source with FFIG.
    _ffig_gen_src(
        name = "_" + name + "_c_srcs",
        srcs = srcs,
        module = module,
        templates = ["c"],
        copts = copts,
        genfiles = c_srcs,
    )

    # Build a C DSO for FFIG's generated C-API.
    native.cc_binary(
        name = name + "_c.so",
        linkshared = 1,
        srcs = c_srcs + srcs,
        deps = deps + ["//:libffig"],
        copts = copts,
    )

    # Package the DSO and generated header into a cc_library.
    native.cc_library(
        name = name,
        hdrs = [name + "_c.h"],
        srcs = [":" + name + "_c.so"],
    )

def ffig_csharp_src(name, module, srcs = None, deps = None, copts = None):
    _ffig_gen_src(
        name = name,
        srcs = srcs,
        module = module,
        templates = ["cs.tmpl"],
        copts = copts,
        genfiles = [module + ".cs"],
    )

def ffig_py_src(name, module, srcs = None, deps = None, copts = None):
    if not module.islower():
        fail("Module name for FFIG Python source must be lower case")
    _ffig_gen_src(
        name = name,
        srcs = srcs,
        module = module,
        templates = ["python"],
        copts = copts,
        genfiles = [module + "/_py2.py", module + "/_py3.py", module + "/__init__.py"],
    )

def ffig_swift_src(name, module, srcs = None, deps = None, copts = None):
    _ffig_gen_src(
        name = name,
        srcs = srcs,
        module = module,
        templates = ["swift"],
        copts = copts,
        genfiles = [module + ".swift", module + "-Bridging-Header.h"],
    )

def ffig_ruby_src(name, module, srcs = None, deps = None, copts = None):
    _ffig_gen_src(
        name = name,
        srcs = srcs,
        module = module,
        templates = ["ruby"],
        copts = copts,
        genfiles = [module + ".rb"],
    )
