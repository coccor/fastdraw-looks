set -e
K=https://raw.githubusercontent.com/kubernetes/community/d0476ffb364cd9dc6b007221410db3b50989ebc3/icons/svg
# outline: a small usvg program that writes an SVG back out with its text as paths (usvg 0.45, Tree::to_string)
O=${OUTLINE:-outline}
SRC=$(mktemp -d); OUT=$(dirname "$0")/../icons/kubernetes
mkdir -p $SRC $OUT
get() { # dir name
  curl -sfL "$K/$1/labeled/$2.svg" -o $SRC/$2.svg
  sed -i -E 's/font-family:[^;"]*/font-family:Liberation Sans/g; s/font-family="[^"]*"/font-family="Liberation Sans"/g' $SRC/$2.svg
  $O $SRC/$2.svg $OUT/$2.svg
}
for n in c-role cm crb crd cronjob deploy ds ep group hpa ing job limits netpol ns pod psp pv pvc quota rb role rs sa sc secret sts svc user vol; do get resources $n; done
for n in control-plane etcd node; do get infrastructure_components $n; done
for n in api c-c-m c-m k-proxy kubelet sched; do get control_plane_components $n; done
ls $OUT | wc -l; grep -l "<text" $OUT/*.svg | wc -l
