use <../connectors/captive_nut.scad>

module middle_base_plate(tk, num_plates, diameter, hole_length, hole_width, shaft_offset, servo_length, screw_diameter) {
    echo(concat(tk, num_plates, diameter, hole_length, hole_width, shaft_offset, servo_length, screw_diameter));
    linear_extrude(3) difference() {
        rotate([0,0,360/num_plates/2]) circle(d=diameter, $fn=num_plates);
        translate([shaft_offset, 0, 0]) square([hole_length, hole_width], center=true);
        for (i = [-1:2:1]) {
            for (j = [-1:2:1]) {
                translate([shaft_offset + i*hole_length/2 + i*(servo_length - hole_length)/4, j*hole_width/4]) circle(d=screw_diameter);
            }
        }
    }
}

middle_base_plate(3, 8, 81, 40, 20, 10, 55, 3);