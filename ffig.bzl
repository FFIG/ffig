LIBFFIG = "//:libffig"
FFIG_PY = "//:ffig_py"

def ffig_c_library(name, srcs = None, deps = None, copts = None):
    if len(srcs) != 1:
        fail("ffig_c_library only supports a single source file.")

    srcs = srcs or []
    deps = deps or []
    copts = copts or []

    ffig_py_path = "$(location {})".format(FFIG_PY)
    source_files = " ".join(["$(locations {})".format(src) for src in srcs])

    # Generate C source with FFIG.
    # $(@D) is the output directory for the target package.
    genfiles = [name + "_c.h", name + "_c.cpp"]
    cflags = " ".join(["--cflag={}".format(copt) for copt in copts])
    native.genrule(
        name = "_" + name + "_c_srcs",
        cmd = "{} -i {} -m {} -o $(@D) -b _c.h.tmpl _c.cpp.tmpl {}".format(
            ffig_py_path,
            source_files,
            name,
            cflags,
        ),
        srcs = srcs + ["//:ffig_headers"],
        outs = genfiles,
        tools = [FFIG_PY, LIBFFIG],
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

def ffig_csharp_src(name, srcs = None, deps = None, copts = None):
  if len(srcs) != 1:
    fail("ffig_csharp_src only supports a single source file.")

  srcs = srcs or []
  deps = deps or []
  copts = copts or []

  ffig_py_path = "$(location {})".format(FFIG_PY)
  source_files = " ".join(["$(locations {})".format(src) for src in srcs])

  # Generate C# source with FFIG.
  # $(@D) is the output directory for the target package.
  genfiles = [name + ".cs"]
  cflags = " ".join(["--cflag={}".format(copt) for copt in copts])
  native.genrule(
      name = name,
      cmd = "{} -i {} -m {} -o $(@D) -b cs.tmpl {}".format(
          ffig_py_path,
          source_files,
          name,
          cflags,
          ),
      srcs = srcs + ["//:ffig_headers"],
      outs = genfiles,
      tools = [FFIG_PY, LIBFFIG],
      )

def ffig_py_src(name, srcs = None, deps = None, copts = None):
  if len(srcs) != 1:
    fail("ffig_py_src only supports a single source file.")

  srcs = srcs or []
  deps = deps or []
  copts = copts or []

  ffig_py_path = "$(location {})".format(FFIG_PY)
  source_files = " ".join(["$(locations {})".format(src) for src in srcs])

  # Generate C# source with FFIG.
  # $(@D) is the output directory for the target package.
  genfiles = [name+"/_py2.py", name+"/_py3.py", name+"/__init__.py"]
  cflags = " ".join(["--cflag={}".format(copt) for copt in copts])
  native.genrule(
      name = name,
      cmd = "{} -i {} -m {} -o $(@D) -b python {}".format(
          ffig_py_path,
          source_files,
          name,
          cflags,
          ),
      srcs = srcs + ["//:ffig_headers"],
      outs = genfiles,
      tools = [FFIG_PY, LIBFFIG],
      )
