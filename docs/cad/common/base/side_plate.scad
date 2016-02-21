use <../connectors/captive_nut.scad>

// Side plates for the base

air_holes_length = 0.6; // percentage of total length for holes
air_holes_width = 0.6; // percentage of plate width for holes
air_holes_thickness = 3; // width of holes

module side_plate(tk, width, height, num_plates, air_holes_num, servo_height, slot_width, slot_translation, bolt_diameter) {
    height = height - tk;
    air_holes_num = air_holes_num - 1;
    linear_extrude(tk) difference() {
        square([width, height], center = false);

        if (air_holes_num > 0) {
            start = width * (1 - air_holes_width) / 2;
            end = start + width * air_holes_width;
            vertical_offset = height / 2;
    
            for (i = [start:(end-start)/air_holes_num:end + 1]) {
                translate([i, vertical_offset])
                square([air_holes_thickness, height*air_holes_length], center = true);
            }
        } else {
            translate([width/2, servo_height, 0]) bolt_slot(tk, slot_width, slot_translation, bolt_diameter);
        }
    }
}

side_plate(3, 30.9974, 51, 8, 0, 27.5, 7.74934, 7.74934, 2.5);