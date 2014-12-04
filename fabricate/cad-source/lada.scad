$fn=100;

mm = 1;
inch = 25.4 * mm;

LENGTH = .75 * inch;
EDGE_WIDTH = .5 * inch;
THICKNESS = .2 * inch;

MATERIAL_THICKNESS = 3 * mm;
OFFSET = .4 * inch;

HEX_R = 6.2 * mm / 2;
HEX_r = 5.6 * mm / 2;
HEX_THICKNESS = 2.3 * mm; 

PCB_L = 5 * inch;
PCB_W = 5 * inch;
PCB_H = 2 * mm;

//HEX_THICKNESS = 1.5 * mm; // for thin version
//THICKNESS = 3 * mm; // for thin version

SCREW_R = 1.6 * mm;
module hex(){
  linear_extrude(height=HEX_THICKNESS * 2, center=false) circle(r=HEX_R, $fn=6);
}
module hex_old(){
  difference(){
    cylinder(r=HEX_R, h=HEX_THICKNESS);
    for(i=[0, 1, 2, 3, 4, 5]){
      rotate(a=60 * i, v=[0, 0, 1])
	translate([HEX_r, -5, 5])rotate(a=90, v=[0, 1, 0])cube([10, 10, HEX_THICKNESS]);
    }
  }
}

TAB_HEIGHT = .5*mm;
TAB_R = 5*mm;
// tab to prevent rollup
module tab(x, y){
  translate([x, y])cylinder(r=TAB_R, h=TAB_HEIGHT);
}

module edge(length, thickness, offset){
  LENGTH = length;
  THICKNESS = thickness;
  OFFSET = offset;
  difference(){
    union(){
      difference(){
	cube([OFFSET, EDGE_WIDTH, OFFSET]);
	translate([THICKNESS, -.01 * EDGE_WIDTH/2, THICKNESS])scale([1, 1.01, 1])cube([LENGTH, EDGE_WIDTH, LENGTH]);
      }
      union(){
	translate([OFFSET, EDGE_WIDTH/2, 0])cylinder(r=EDGE_WIDTH / 2, h=THICKNESS);
	translate([0, EDGE_WIDTH/2, OFFSET])rotate(v=[0, 1, 0], a=90)cylinder(r=EDGE_WIDTH / 2, h=THICKNESS);
		//square top
		//translate([0, 0, OFFSET*1.5])rotate(v=[0, 1, 0], a=90)cube([EDGE_WIDTH,EDGE_WIDTH,THICKNESS]);
      }
    }
    translate([OFFSET, EDGE_WIDTH/2, 0])cylinder(r=SCREW_R, h=THICKNESS * 1.1);
    translate([-.01, EDGE_WIDTH/2, OFFSET])rotate(v=[0, 1, 0], a=90)cylinder(r=SCREW_R, h=THICKNESS * 10);
  }
}

module pcb(){
  cube([PCB_L, PCB_W, PCB_H]);
}

module inside_edge(length, thickness, offset){
  LENGTH = length;
  THICKNESS = thickness;
  OFFSET = offset;
  difference(){
    edge(length, thickness, offset);
    //translate([.2 * inch - 1*mm, EDGE_WIDTH/2 + PCB_H/2, .2 * inch - 1*mm])rotate(v=[-1, 0, 0], a=-90)translate([THICKNESS * 3/4, -1, THICKNESS])pcb();
    translate([OFFSET, EDGE_WIDTH/2, THICKNESS - HEX_THICKNESS])scale([1, 1, 1.01])hex();
    translate([THICKNESS - HEX_THICKNESS, EDGE_WIDTH/2, OFFSET])rotate(v=[0, 1, 0], a=90)scale([1, 1, 1.01])hex();
  }
}
module outside_edge(length, thickness, offset){
  difference(){
    edge(length, thickness, offset);
    translate([OFFSET, EDGE_WIDTH/2, 0])scale([1, 1, 1.01])cylinder(r=HEX_R * 1.1, h=HEX_THICKNESS);
    translate([0, EDGE_WIDTH/2, OFFSET])scale([1, 1, 1.01])rotate(v=[0, 1, 0], a=90)cylinder(r=HEX_R * 1.1, h=HEX_THICKNESS);
  }
}

module corner(length, thickness, offset){
  echo("offset", offset);
  LENGTH = length;
  THICKNESS = thickness;
  OFFSET = offset;
  union(){
    //tab(0, 0);
    //tab(LENGTH, 0);
    //tab(0, LENGTH);

    intersection(){
      difference(){
	cube(LENGTH);
	translate([THICKNESS, THICKNESS, THICKNESS])
	  cube(LENGTH);
	translate([OFFSET, OFFSET, 0])
	  translate([0, 0, -1])
	  cylinder(r=SCREW_R, h=2 * THICKNESS);
	translate([OFFSET, 0, OFFSET])
	  rotate(v=[-1, 0, 0], a=90) 
	  translate([0, 0, -1])
	  cylinder(r=SCREW_R, h=2 * THICKNESS);
	translate([0, OFFSET, OFFSET])
	  rotate(v=[0, 1, 0], a=90)
	  translate([0, 0, -1])
	  cylinder(r=SCREW_R, h=2 * THICKNESS);
      }
      
      union(){
	rotate(v=[0, 0, -1], a=0)cylinder(r=LENGTH*1.04, h=THICKNESS);
	rotate(v=[-1,0, 0], a=90)cylinder(r=LENGTH*1.04, h=THICKNESS);
	rotate(v=[0, 1, 0], a=90)cylinder(r=LENGTH*1.04 , h=THICKNESS);
      }
      // sphere(r=LENGTH);
    }
  }
}
module inside_corner(length, thickness, offset, standoff_h=10*mm){
  LENGTH = length;
  THICKNESS = thickness;
  OFFSET = offset;

  // translate([THICKNESS, THICKNESS, THICKNESS])cube(standoff_h*mm);
  difference(){
    corner(LENGTH, THICKNESS, OFFSET);
    translate([OFFSET, OFFSET, THICKNESS - HEX_THICKNESS])scale([1, 1, 100])hex();
    translate([OFFSET, THICKNESS - HEX_THICKNESS,  OFFSET])
      rotate(v=[-1, 0, 0], a=90)
      scale([1, 1, 100])
      hex();
    translate([THICKNESS - HEX_THICKNESS, OFFSET,  OFFSET])
      rotate(v=[1, 0, 0], a=30) // correct one!
      rotate(v=[0, 1, 0], a=90) // correct one!
      scale([1, 1, 100]) hex();
    //translate([THICKNESS * 2/4, THICKNESS * 2/4, THICKNESS + standoff_h])pcb();
  }
}
module outside_corner(length, thickness, offset, material_thickness){
  LENGTH = length + (material_thickness + thickness) * sqrt(2);
  THICKNESS = thickness;
  OFFSET = offset + material_thickness + thickness;
  echo("OFFSET", OFFSET);
  difference(){
    union(){
      corner(LENGTH, THICKNESS, OFFSET);
    }

    // counter bore
    translate([OFFSET,  HEX_THICKNESS, OFFSET])
      rotate(v=[1, 0, 0], a=90)
      rotate(v=[0, 0, 1], a=180)
      scale([1, 1, 100])
      cylinder(r=HEX_R * 1.1);
    translate([HEX_THICKNESS, OFFSET, OFFSET])
      rotate(v=[0, -1, 0], a=90)
      scale([1, 1, 100])
      cylinder(r=HEX_R * 1.1);
    translate([OFFSET,  OFFSET, HEX_THICKNESS, ])
      rotate(v=[0, 1, 0], a=180)
      scale([1, 1, 100])
      cylinder(r=HEX_R * 1.1);
  }
}
/* used for a specialized screen holder for photo booth */
module screen_clip(span, screen_h, overhang){
  difference(){
    union(){
      edge(LENGTH, THICKNESS, OFFSET);
      translate([OFFSET, 0, 0])cube([span, EDGE_WIDTH, THICKNESS]);
      translate([OFFSET + span - THICKNESS, 0, 0])cube([THICKNESS, EDGE_WIDTH, screen_h + THICKNESS]);
      translate([OFFSET + span - THICKNESS, 0, screen_h])cube([overhang + THICKNESS, EDGE_WIDTH, THICKNESS]);
    }
    union(){
      translate([OFFSET, EDGE_WIDTH/2, THICKNESS - HEX_THICKNESS])scale([1, 1, 1.01])hex();
      translate([THICKNESS - HEX_THICKNESS, EDGE_WIDTH/2, OFFSET])rotate(v=[0, 1, 0], a=90)scale([1, 1, 1.01])hex();
      translate([OFFSET, EDGE_WIDTH/2, 0])cylinder(r=SCREW_R, h=THICKNESS * 1.1);
    }
  }
}

// translate([0, MATERIAL_THICKNESS + THICKNESS, MATERIAL_THICKNESS + THICKNESS])inside_corner(LENGTH, THICKNESS, OFFSET); // corner
// translate([-MATERIAL_THICKNESS - THICKNESS, 0, 0])
// outside_corner(LENGTH, THICKNESS, OFFSET, MATERIAL_THICKNESS);

// translate([0, -1*inch, 0])inside_corner(LENGTH, THICKNESS, OFFSET);
// translate([0, 1*inch + 13, 0])rotate(v=[0, 0, 1], a=-90)inside_corner(LENGTH, THICKNESS, OFFSET);
inside_edge(LENGTH, THICKNESS, OFFSET);

