use <./common/base/base.scad>;

servo_heavy = [43, 42,   39, 20,   54,   27, 10.5]; // HX12K, 10kg, 55g
servo_med =   [40, 33,   34, 19,   44,   24, 7.5 ]; // Corona DS339HV, 5.1kg, 32g
servo_light = [41, 40,   37, 20,   55,   26, 10  ]; // HK15138, 4.3kg, 38g
servo_micro = [31, 23.2, 27, 12.3, 32.3, 16, 6   ]; // TGY-50090M, 1.6kg, 9g

plans = false; // trigger to generate plans

tk = 3; // main wood thickness

base_diameter = 90;

$fn = 100;

base(plans, tk, base_diameter, servo_light, 8, 3);