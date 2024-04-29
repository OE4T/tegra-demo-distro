export DOCKER_BUILDKIT=1
docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) --build-arg UNAME=sam --ssh default -t yocto-build-env .
docker run -it --rm -v $(pwd):/yocto -v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK=$SSH_AUTH_SOCK yocto-build-env jetson-orin-nx-a603 dsensos
