// outline <in.svg> <out.svg>: the same drawing with every text turned into paths, using the system's fonts
fn main() {
    let a: Vec<String> = std::env::args().collect();
    let data = std::fs::read(&a[1]).unwrap();
    let mut opt = usvg::Options::default();
    opt.fontdb_mut().load_system_fonts();
    let tree = usvg::Tree::from_data(&data, &opt).unwrap();
    std::fs::write(&a[2], tree.to_string(&usvg::WriteOptions::default())).unwrap();
}
