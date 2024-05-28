python() {
    destsuffix_base = os.path.basename(d.getVar('S'))
    src_uris = d.getVar('SRC_URI', True).split()
    if 'destsuffix=' not in src_uris[0]:
        src_uris[0] += ";destsuffix=${GO_SRCURI_DESTSUFFIX}"    
        d.setVar('SRC_URI', ' '.join(src_uris))
}
