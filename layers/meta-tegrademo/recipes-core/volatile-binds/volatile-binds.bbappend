# For Mender builds, remove /var/lib from the list
VOLATILE_BINDS:tegrademo-mender = "\
    /var/volatile/cache /var/cache\n\
    /var/volatile/spool /var/spool\n\
    /var/volatile/srv /srv\n\
"
