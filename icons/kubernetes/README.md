# Kubernetes icons

The labeled resource, control plane and infrastructure icons of the Kubernetes project, from
[kubernetes/community](https://github.com/kubernetes/community/tree/master/icons) at commit `d0476ffb`, under the
Apache License 2.0 (`LICENSE` here).

One change: the short name inside each icon (`pod`, `svc`, `api`) is turned into outlines, set in Liberation Sans, so
it draws in renderers that show no text inside an SVG image (FastDraw's PNG export among them).
`tools/k8s-icons.sh` remakes them; it needs the converter in `tools/outline` (`cargo build --release`, then
`OUTLINE=tools/outline/target/release/outline tools/k8s-icons.sh`).
