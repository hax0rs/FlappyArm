use <../connectors/captive_nut.scad>

module middle_base_plate(tk, num_plates, diameter, hole_length, hole_width, shaft_offset, servo_length, screw_diameter, insert_length, nut_indent, nut_width, outset_width, outset_translation) {
    linear_extrude(3) 
    union() {
        difference() {
            rotate([0,0,360/num_plates/2]) circle(d=diameter, $fn=num_plates);
            translate([shaft_offset, 0, 0]) square([hole_length, hole_width], center=true);
            for (i = [-1:2:1]) {
                for (j = [-1:2:1]) {
                    translate([shaft_offset + i*hole_length/2 + i*(servo_length - hole_length)/4, j*hole_width/4]) circle(d=screw_diameter);
                }
            }
            // inner divet
            for (i = [1:2:num_plates]) {
                rotate([0,0,i*360/num_plates]) translate([-cos(360/num_plates/2)*diameter/2,0,0])  nut_slot_cut(screw_diameter, insert_length, nut_indent, nut_width);
            }
        }
        for (i = [1:2:num_plates]) {
            rotate([0,0,i*360/num_plates]) translate([cos(360/num_plates/2)*diameter/2,0,0]) nut_slot_add(tk, outset_width, outset_translation);
        }
    }
}

middle_base_plate(3, 8, 81, 40, 20, 10, 55, 3, 12, 8, 5, 5, 7);