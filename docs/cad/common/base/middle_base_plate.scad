use <../connectors/captive_nut.scad>

module middle_base_plate(tk, num_plates, diameter, hole_length, hole_width) {

    linear_extrude(3) difference() {
        circle(d=diameter, $fn=num_plates);
        translate() square();
    }
}

middle_base_plate(3, 8, 20, 45, 40, 20);