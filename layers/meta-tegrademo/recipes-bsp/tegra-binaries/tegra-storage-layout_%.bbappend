FILESEXTRAPATHS:prepend := "${THISDIR}/${BPN}:"

SRC_URI = "file://basic_nvme_layout.xml"

def find_layout(d, which='TEMPLATE'):
    alt_layout_name = d.getVar('ALT_PARTITION_LAYOUT_%s' % which)
    if alt_layout_name:
        return os.path.join(d.getVar('S'), alt_layout_name)
    return os.path.join(d.getVar('STAGING_DATADIR'), 'l4t-storage-layout', d.getVar('PARTITION_LAYOUT_%s' % which))

PARTITION_FILE = "${@find_layout(d)}"
PARTITION_FILE_EXTERNAL = "${@find_layout(d, 'EXTERNAL')}"
PARTITION_FILE_RCMBOOT = "${@find_layout(d, 'RCMBOOT')}"
do_compile[vardeps] += "ALT_PARTITION_LAYOUT_TEMPLATE ALT_PARTITION_LAYOUT_EXTERNAL"
