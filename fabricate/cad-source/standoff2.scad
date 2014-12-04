
wall_thick = 2; // wall thickness around hole
screw_dia = 2.5; // screw diameter in mm
tolerance = .5; // hole clearance (diameter)
hole_r = (screw_dia+tolerance)/2;
height = 3;

module standoff(){
	difference()
	{
		cylinder(r=hole_r+wall_thick, h=height,$fn=6);
		translate([0,0,-1])cylinder(r=hole_r, h=height+2,$fn=20);
	}
}

standoff();