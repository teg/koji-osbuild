FROM quay.io/osbuild/koji:v1

RUN dnf -y upgrade \
    && dnf -y \
            --setopt=fastestmirror=True \
            --setopt=install_weak_deps=False \
            install \
	koji-web \
	&& dnf clean all

COPY container/hub/hub.conf /etc/koji-hub/hub.conf
COPY container/hub/ssl.conf /etc/httpd/conf.d/ssl.conf
COPY plugins/hub/osbuild.py /usr/lib/koji-hub-plugins/
COPY container/hub/run-hub.sh /app/run-hub.sh

COPY container/hub/web.conf /etc/kojiweb/web.conf
COPY container/hub/kojiweb.conf /etc/httpd/conf.d/kojiweb.conf

ENTRYPOINT /app/run-hub.sh
