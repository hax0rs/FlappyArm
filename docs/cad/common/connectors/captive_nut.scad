module nut_slot() {
    
}

module bolt_slot(height, width, translation, circle_dia) {
    circle(d=circle_dia);
    for (i = [-1:2:1]) {
        translate([i*translation, 0, 0]) square([width, height], center=true);
    }
}

bolt_slot(3, 5, 10, 2.5);