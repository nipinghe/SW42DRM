#! /usr/bin/env python
import h5py
import scipy as sp
import time
import math
import pickle
from station_generator import *

# #################################################### Usr input variables #######################################

# #############################define base point information ###########################################
# base_point_index=23;
base_point_x=input('Specify the x coordinate of the base point in ESSI model: ');
base_point_y=input('Specify the y coordinate of the base point in ESSI model: ');
base_point_z=input('Specify the z coordinate of the base point in ESSI model: ');
######################################################################################################

#############################################define location information ##########################

# translation_base_station_index_x=input('Specify the x coordinate of translation reference point in SW4 model: ');
# translation_base_station_index_y=input('Specify the y coordinate of translation reference point in SW4 model: ');
# translation_base_station_index_z=input('Specify the z coordinate of translation reference point in SW4 model: ');
# rotation_base_station_index_x=input('Specify the x coordinate of rotation reference point in SW4 model: ');
# rotation_base_station_index_y=input('Specify the x coordinate of rotation reference point in SW4 model: ');
# rotation_base_station_index_z=input('Specify the x coordinate of rotation reference point in SW4 model: ');

translation_base_station_x=input('Specify the x coordinate of translation reference point in SW4 model: ');
translation_base_station_y=input('Specify the y coordinate of translation reference point in SW4 model: ');
translation_base_station_z=input('Specify the z coordinate of translation reference point in SW4 model: ');

rotation_base_station_x=input('Specify the x coordinate of rotation reference point in SW4 model: ');
rotation_base_station_y=input('Specify the y coordinate of rotation reference point in SW4 model: ');
rotation_base_station_z=input('Specify the z coordinate of rotation reference point in SW4 model: ');
# ####################################################################################################

############################################ define degree of rotation along three axies ###########################################
x_rotation=input('Specify the degree of rotation along x axis: '); #the degree of rotating along x axis based on base station, right hand rule for positive direction of x
y_rotation=input('Specify the degree of rotation along y axis: '); #the degree of rotating along y axis based on base station, right hand rule for positive direction of y
z_rotation=input('Specify the degree of rotation along z axis: '); #the degree of rotating along z axis based on base station, right hand rule for positive direction of z
#####################################################################################################################################

# #################################################### Ending input ##############################################

boundary_node=sp.loadtxt("boundary_node.txt")
exterior_node=sp.loadtxt("exterior_node.txt")
# station=sp.loadtxt("station.txt")

node=sp.concatenate((boundary_node,exterior_node))

# print boundary_node.shape
# print node.shape
# print exterior_node.shape
# print node[0,5]
NO_node=node.shape
NO_node=NO_node[0]
No_station=station.shape[0]

# print NO_node

############################################coordinate transformation ###############################
# node transformation relationship: x_sw4=x_essi;  y_sw4=-y_essi ; z_sw4=-z_essi
for i in xrange(0,NO_node):
	node[i,2]=-node[i,2];
	node[i,3]=-node[i,3];
base_point_y=-base_point_y;
base_point_z=-base_point_z;


# print node[0,2], node[0,3],node[530,2],node[530,3], base_point_y, base_point_z;
###################################################################################################



# for i1 in xrange(0,No_station):
# 	if station[i1,0]==translation_base_station_index_x and station[i1,1]==translation_base_station_index_y and station[i1,2]==translation_base_station_index_z:
# 		translation_base_station_x=station[i1,3]
# 		translation_base_station_y=station[i1,4]
# 		translation_base_station_z=station[i1,5]
# 	if station[i1,0]==rotation_base_station_index_x and station[i1,1]==rotation_base_station_index_y and station[i1,2]==rotation_base_station_index_z:
# 		rotation_base_station_x=station[i1,3]
# 		rotation_base_station_y=station[i1,4]
# 		rotation_base_station_z=station[i1,5]


translation_x= translation_base_station_x-base_point_x;
translation_y= translation_base_station_y-base_point_y;
translation_z= translation_base_station_z-base_point_z;


new_node=sp.zeros((NO_node,6))

	#####ATTENTION: ROTATION ARE PATH DEPENDENT, please take care the order of calling 3 rotation functions ##########################################
for i3 in xrange(0,NO_node):

	new_node[i3,0]=node[i3,0]
	new_node[i3,1]=node[i3,1]+translation_x
	new_node[i3,2]=node[i3,2]+translation_y
	new_node[i3,3]=node[i3,3]+translation_z
	new_node[i3,4]=node[i3,4]
	new_node[i3,5]=node[i3,5]
	
	# ######################################rotation along z axis###########################################################
def rotation_z(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,z_rotation):

	No_new_node=new_node.shape[0];
	for i4 in xrange(0,No_new_node):
		dx=new_node[i4,1]-rotation_base_station_x
		dy=new_node[i4,2]-rotation_base_station_y
		dz=new_node[i4,3]-rotation_base_station_z
	
		r_xy=math.sqrt(dx*dx+dy*dy)

		if dx==0 and dy>=0:
			theta=90;
		if dx==0 and dy<0:
			theta=270;
		if dx>0 and dy>=0:
			theta=sp.arctan(1.0*dy/dx);
			theta=(180.0*theta)/sp.pi;
		if dx>0 and dy<0:
			theta=2*sp.pi+sp.arctan(1.0*dy/dx);
			theta=(180.0*theta)/sp.pi;
		if dx<0 and dy>=0:
			theta=sp.pi+sp.arctan(1.0*dy/dx);
			theta=(180.0*theta)/sp.pi;
		if dx<0 and dy<0:
			theta=sp.pi+sp.arctan(1.0*dy/dx);
			theta=(180.0*theta)/sp.pi;
		new_theta=theta+z_rotation;
		new_dx=r_xy*math.cos(new_theta*sp.pi/180.0);
		new_dy=r_xy*math.sin(new_theta*sp.pi/180.0);
		new_dz=dz;

		new_node[i4,1]=rotation_base_station_x+new_dx
		new_node[i4,2]=rotation_base_station_y+new_dy
		new_node[i4,3]=rotation_base_station_z+new_dz
	return new_node

	#####################################rotation along x axis###########################################################
def rotation_x(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,x_rotation):

	No_new_node=new_node.shape[0];
	for i5 in xrange(0,No_new_node):
		dx=new_node[i5,1]-rotation_base_station_x
		dy=new_node[i5,2]-rotation_base_station_y
		dz=new_node[i5,3]-rotation_base_station_z
		r_yz=math.sqrt(dy*dy+dz*dz)

		if dy==0 and dz>=0:
			theta=90;
		if dy==0 and dz<0:
			theta=270;
		if dy>0 and dz>=0:
			theta=sp.arctan(1.0*dz/dy);
			theta=(180.0*theta)/sp.pi;
		if dy>0 and dz<0:
			theta=2*sp.pi+sp.arctan(1.0*dz/dy);
			theta=(180.0*theta)/sp.pi;
		if dy<0 and dz>=0:
			theta=sp.pi+sp.arctan(1.0*dz/dy);
			theta=(180.0*theta)/sp.pi;
		if dy<0 and dz<0:
			theta=sp.pi+sp.arctan(1.0*dz/dy);
			theta=(180.0*theta)/sp.pi;
		new_theta=theta+x_rotation;
		new_dy=r_yz*math.cos(new_theta*sp.pi/180.0);
		new_dz=r_yz*math.sin(new_theta*sp.pi/180.0);
		new_dx=dx;
		new_node[i5,1]=rotation_base_station_x+new_dx
		new_node[i5,2]=rotation_base_station_y+new_dy
		new_node[i5,3]=rotation_base_station_z+new_dz
	return new_node


	######################################rotation along y axis#########################################################
def rotation_y(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,y_rotation):
		
	No_new_node=new_node.shape[0];
	for i6 in xrange(0,No_new_node):
		dx=new_node[i6,1]-rotation_base_station_x
		dy=new_node[i6,2]-rotation_base_station_y
		dz=new_node[i6,3]-rotation_base_station_z
		r_xz=math.sqrt(dx*dx+dz*dz)
		if dz==0 and dx>=0:
			theta=90;
		if dz==0 and dx<0:
			theta=270;
		if dz>0 and dx>=0:
			theta=sp.arctan(1.0*dx/dz);
			theta=(180.0*theta)/sp.pi;
		if dz>0 and dx<0:
			theta=2*sp.pi+sp.arctan(1.0*dx/dz);
			theta=(180.0*theta)/sp.pi;
		if dz<0 and dx>=0:
			theta=sp.pi+sp.arctan(1.0*dx/dz);
			theta=(180.0*theta)/sp.pi;
		if dz<0 and dx<0:
			theta=sp.pi+sp.arctan(1.0*dx/dz);
			theta=(180.0*theta)/sp.pi;
		new_theta=theta+y_rotation;
		new_dy=dy
		new_dz=r_xz*math.cos(new_theta*sp.pi/180.0);
		new_dx=r_xz*math.sin(new_theta*sp.pi/180.0);
		new_node[i6,1]=rotation_base_station_x+new_dx
		new_node[i6,2]=rotation_base_station_y+new_dy
		new_node[i6,3]=rotation_base_station_z+new_dz
	return new_node

###################conduct rotation operation, here our rotate oeder is z ,x ,y########################################
new_node=rotation_z(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,z_rotation)
new_node=rotation_x(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,x_rotation)
new_node=rotation_y(new_node,rotation_base_station_x,rotation_base_station_y,rotation_base_station_z,y_rotation)

# print new_node

################################################################################################################################

##########################################output new DRM nodes information################################################### 
# f=open('new_DRM_nodes.p','w')
# pickle.dump(new_node,f)
# f.close()
##############################################################################################################################

# print translation_x, translation_y, translation_z
# print new_node[1,1], new_node[1,2], new_node[1,3]