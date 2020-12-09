# Work around change in go 1.15 for
# https://github.com/golang/go/issues/42559
CGO_LDFLAGS_remove_class-native = "-Wl,-O1 -Wl,--dynamic-linker=${UNINATIVE_LOADER}"
