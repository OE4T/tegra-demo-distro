python () {
    import shlex
    upvar = 'USERADD_PARAM:{}'.format(d.getVar('PN'))
    useradd_params = d.getVar(upvar)
    # For our test images, we want the weston user to have access
    # to audio devices, so ensure that it is in the necessary group
    if useradd_params:
        new_params = []
        watch = -1
        for i, param in enumerate(shlex.split(useradd_params)):
            if i == watch:
                groups = param.split(',')
                if 'audio' not in groups:
                    groups.append('audio')
                new_params.append(','.join(groups))
            else:
                new_params.append(param)
                if param == "-G":
                    watch = i + 1
        d.setVar(upvar, shlex.join(new_params))
}

