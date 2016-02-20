use <bottom_base_plate.scad>
use <top_base_plate.scad>

module base(plate, tk, diameter, servo) {
    if (plate) {
        projection() {
            bottom_base_plate(tk, diameter);
            translate([100, 0, 0]) top_base_plate(tk, diameter);
        }
    } else {
        bottom_base_plate(tk);
        translate([0,0,10]) top_base_plate(tk, diameter);
    }
}

base(false, 3, 90, [41, 40, 37, 20, 55, 26, 10]);