// generates sketches for a "captive nut" joint

module nut_slot_cut(bolt_width, insert_length, nut_indent, nut_width) {
    translate([0,-bolt_width/2,0]) square([nut_indent, bolt_width]);
    translate([nut_indent, -(nut_width*1.5)/2, 0]) polygon([
        [0, 0],
        [(insert_length - nut_indent), (nut_width*1.5)/2],
        [0, nut_width*1.5]
    ]);
}

module nut_slot_add(height, width, translation) {
    for (i = [-1:2:1]) {
        translate([height/2, i*translation, 0]) square([height, width], center=true);
    }
}

module bolt_slot(height, width, translation, circle_dia) {
    circle(d=circle_dia);
    for (i = [-1:2:1]) {
        translate([i*translation, 0, 0]) square([width, height], center=true);
    }
}


//nut_slot_cut(3, 12, 8, 5);
//nut_slot_add(3, 10, 8);