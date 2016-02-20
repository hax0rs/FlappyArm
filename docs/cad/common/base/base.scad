use <bottom_base_plate.scad>
use <top_base_plate.scad>
use <side_plate.scad>

height_offset = 10;
side_plate_diameter_offset = 0.9; // percentage offset of interior plates

module base(plate, tk, diameter, servo, num_plates, air_holes_num) {
    if (plate) {
        projection() {
            bottom_base_plate(tk, diameter);
            translate([100, 0, 0]) top_base_plate(tk, diameter);
        }
    } else {
        plate_height = servo[0] + height_offset;
        side_plate_width = sin(180/num_plates) * diameter * side_plate_diameter_offset;
        side_plate_offset = cos(180/num_plates) * diameter * side_plate_diameter_offset /2 + tk;
        
        bottom_base_plate(tk, diameter); // place bottom plate
        
        for (i = [1:num_plates]) {
            rotate([0,0,360/num_plates*i])
            translate([-side_plate_width/2,side_plate_offset,tk])
            rotate([90,0,0])
            if (floor(i/2) == i/2) {
                // if even
                side_plate(tk, side_plate_width, plate_height, num_plates, 0, servo[5]);
            } else {
                // if odd
                side_plate(tk, side_plate_width, plate_height, num_plates, air_holes_num, servo[5]);
            }
        }
        
        translate([0, 0, plate_height]) {
            top_base_plate(tk, diameter);
        }
    }
}

base(false, 3, 90, [41, 40, 37, 20, 55, 26, 10], 8, 3);