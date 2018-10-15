LIBFFIG = "//:libffig"
FFIG_PY = "//:ffig_py"

def ffig_c_library(name, hdrs=None, deps=None, copts=None):
  hdrs = hdrs or []
  deps = deps or []
  copts = copts or []

  ffig_py_path = "$(location //:ffig_py)"
  header_files = ' '.join(['$(locations {})'.format(h) for h in hdrs])

  # Generate C source with FFIG.
  # $(@D) is the output directory for the package from which this rule was invoked.
  genfiles = [name+"_c.h", name+"_c.cpp"]
  cflags = ' '.join(['--cflag={}'.format(copt) for copt in copts])
  native.genrule(name = "_"+name+"_c_srcs",
                 cmd="{} -i {} -m {} -o $(@D) -b _c.h.tmpl _c.cpp.tmpl {}".format(ffig_py_path, header_files, name, cflags),
                 srcs = hdrs + ["//:ffig_headers"],
                 outs = genfiles,
                 tools = [FFIG_PY, LIBFFIG])

  # Build a C DSO for FFIG's generated C-API.
  native.cc_binary(name = name+"_c.so",
                   linkshared = 1,
                   srcs = genfiles + hdrs,
                   deps = deps,
                   copts = copts,
                   )

  # Package the DSO and generated header into a cc_library.
  native.cc_library(name = name,
                    hdrs = [name+"_c.h"],
                    srcs = [":"+name+"_c.so"],
                    )
