include <lada.scad>

left_span = 20 * mm; // distance from center of left mount hole to edge of display
right_span = 20 * mm; // "                      right "
bottom_span = 20 * mm; // "                     bottom "
top_span = 20 * mm;    // "                      top     "
screen_thickness = 4.75*mm;
overhang = 5*mm;

//rotate([90,0,0])screen_clip(left_span, screen_thickness, overhang);

//translate([0, 20*mm, 0])rotate([90,0,0])screen_clip(right_span, screen_thickness, overhang);
for(y=[-1:0]){
	translate([0,y*20,0])rotate([90,0,0])screen_clip(top_span, screen_thickness, overhang);
}
//translate([0, 80*mm, 0])screen_clip(top_span, screen_thickness, overhang);
//translate([0, 60*mm, 0])screen_clip(bottom_span, screen_thickness, overhang);
//rotate([90,0,0]){screen_clip(bottom_span, screen_thickness, overhang);}

