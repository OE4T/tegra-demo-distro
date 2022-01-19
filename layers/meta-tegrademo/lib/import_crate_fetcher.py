# Workaround for https://bugzilla.yoctoproject.org/show_bug.cgi?id=14680
import bb, crate
bb.fetch2.methods.append(crate.Crate())
