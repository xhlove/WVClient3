from distutils.core import setup, Extension

setup(
    name="cdmapi",
    version="1.0",
    ext_modules=[Extension(
        "cdmapi",
        ["bind.cpp", "codelift.cpp"],
        include_dirs=['cryptopp850', 'wasm_src'],
        extra_objects=['cryptlib_MD.lib']
    )]
)