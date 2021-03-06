#!/usr/bin/python3
import argparse
import koji
import os

from pprint import pprint


def main():
    parser = argparse.ArgumentParser(description="osbuild koji client")
    parser.add_argument("--url", metavar="URL", type=str,
                        default="https://localhost/kojihub",
                        help="The URL koji hub API endpoint")
    parser.add_argument("--repo", metavar="REPO", help='The repository to use',
                        type=str, action="append", default=[])
    parser.add_argument("--release", metavar="RELEASE", help='The distribution release')
    parser.add_argument("--user", metavar="USER", default="kojiadmin")
    parser.add_argument("--password", metavar="PASSWORD", default="kojipass")
    parser.add_argument("--principal", metavar="USER", default="osbuild-krb@LOCAL")
    parser.add_argument("--keytab", metavar="FILE", help="kerberos keytab",
                        default="/tmp/osbuild-composer-koji-test/client.keytab")
    parser.add_argument("--serverca", metavar="FILE", help="Server CA",
                        default="/tmp/osbuild-composer-koji-test/ca-crt.pem")
    parser.add_argument("--plain", help="use plain text login",
                        default=False, action="store_true")
    parser.add_argument("name", metavar="NAME", help='The distribution name')
    parser.add_argument("version", metavar="VERSION", help='The distribution version')
    parser.add_argument("distro", metavar="DISTRO", help='The distribution')
    parser.add_argument("target", metavar="TARGET", help='The build target')
    parser.add_argument("arch", metavar="ARCHITECTURE", help='Request the architecture',
                        type=str, nargs="+")
    parser.add_argument("--image-type", metavar="TYPE",
                        help='Request an image-type [default: qcow2]',
                        type=str, action="append", default=[])
    args = parser.parse_args()

    opts = {"user": args.user, "password": args.password, "serverca": args.serverca}
    session = koji.ClientSession(args.url, opts)
    if args.plain:
        session.login()
    else:
        session.gssapi_login(principal=args.principal, keytab=args.keytab)

    name, version, arch, target = args.name, args.version, args.arch, args.target
    distro, image_types = args.distro, args.image_type

    if not image_types:
        image_types = ["qcow2"]

    opts = {}

    if args.release:
        opts["release"] = args.release

    if args.repo:
        opts["repo"] = ",".join(args.repo)

    print("name:", name)
    print("version:", version)
    print("distro:", distro)
    print("arches:", ", ".join(arch))
    print("target:", target)
    print("image types ", str(image_types))
    if opts:
        pprint(opts)

    session.osbuildImage(name, version, distro, image_types, target, arch, opts=opts)


if __name__ == "__main__":
    main()
