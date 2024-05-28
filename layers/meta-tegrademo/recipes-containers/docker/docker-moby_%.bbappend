def process_uri(uri, d, dsmap):
    import re
    elements = uri.split(';')
    updated_elements = []
    param_re = re.compile(r'([^=]+)=(.*)')
    name = None
    ds_index = None
    for i, elem in enumerate(elements):
        m = param_re.match(elem)
        if m is not None:
            if m.group(1) == 'name':
                name = m.group(2)
            elif m.group(1) == 'destsuffix':
                ds_index = i
    if not name or name not in dsmap:
        return uri
    if ds_index is not None:
        elements[ds_index] = "destsuffix=" + dsmap[name]
    else:
        elements.append("destsuffix=" + dsmap[name])
    return ';'.join(elements)

python() {
    destsuffix_base = os.path.basename(d.getVar('S'))
    src_uris = d.getVar('SRC_URI', True).split()
    destsuffix_map = {
        'moby': '${GO_SRCURI_DESTSUFFIX}',
        'libnetwork': destsuffix_base + '/libnetwork',
        'cli': destsuffix_base + '/cli'
    }
    updated_uris = [process_uri(uri, d, destsuffix_map) for uri in src_uris]
    d.setVar('SRC_URI', ' '.join(updated_uris))
}

RDEPENDS:${PN} += "docker-conf"
