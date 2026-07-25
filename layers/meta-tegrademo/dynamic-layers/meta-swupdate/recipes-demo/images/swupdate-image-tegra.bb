# By default, use demo-image-base as the base image.
# Redefine in local.conf if you'd like to use a different base image,
# or use one of the demo-image-{base,sato,weston,full}-swupdate
# recipes already present here.
SWUPDATE_CORE_IMAGE_NAME ?= "demo-image-base"
require swupdate-image-tegra-common.inc
