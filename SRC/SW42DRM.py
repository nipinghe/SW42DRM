#! /usr/bin/env python
SOURCE_DIR='/home/hexiang/git/SW42DRM/SRC'
import matlab.engine

import h5py
import scipy as sp
import time
import pickle


from ESSI_location import * 
from interpolation_function_array import *
from numpy.linalg import inv



############################################## Radius interpolation method###########################################################################################
#####################################################################################################################################################################
	###########search all interpolation nodes#####################################################
# def interpolation_Nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio):
# 	No_station=station.shape[0];
# 	interpolation_nodes=[];
# 	interpolation_nodes_index=0
# 	for i4 in xrange(0,No_station):
# 		selected_points=sp.zeros((7));
# 		if (station[i4,3]-new_node_x)*(station[i4,3]-new_node_x)+(station[i4,4]-new_node_y)*(station[i4,4]-new_node_y)+(station[i4,5]-new_node_z)*(station[i4,5]-new_node_z)<=Interpolation_Radius*Interpolation_Radius:
# 			selected_points[0:6]=station[i4,0:6]
# 			selected_points[6]=i4;
# 			interpolation_nodes.append(selected_points);
# 			interpolation_nodes_index=interpolation_nodes_index+1

# 	# print interpolation_nodes,interpolation_nodes_index,"I am here"

# 	if interpolation_nodes_index<4:
# 		print "serach radius R is too small for node ", new_node_index, ", search again using",scale_ratio, "*R..."
# 		Interpolation_Radius=Interpolation_Radius*scale_ratio
# 		return interpolation_Nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio)
# 	if interpolation_nodes_index>15:
# 		print "serach radius R is too big for node ", new_node_index, ", search again using R/",scale_ratio,"..."
# 		Interpolation_Radius=Interpolation_Radius/scale_ratio
# 		return interpolation_Nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio)
# 	print "Done interpolation nodes searching"

# 	print interpolation_nodes,interpolation_nodes_index,"I am here"
	
# 	return interpolation_nodes

# ########################################################################################################################################################################

# def getField (new_node_x,new_node_y,new_node_z,new_node_index,sample_time_step_interval):
# 	interpolation_nodes=interpolation_Nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio);

# 	print "I am hre ar ger field", new_node_x, new_node_y, new_node_z, new_node_index; 

# 	No_interpolation_nodes=len(interpolation_nodes);
# 	original_velocity=sp.zeros((3,No_time_step));
# 	original_displacement=sp.zeros((3,No_time_step));
# 	original_acceleration=sp.zeros((3,No_time_step));
# 	sampled_displacement=sp.zeros((3,sampled_No_time_step));
# 	sampled_acceleration=sp.zeros((3,sampled_No_time_step));


# 	for i7 in xrange(0,No_time_step):  
# 		for i6 in xrange(0,3):  # 0 1 2 for ux uy uz
# 			RHS=sp.zeros((No_interpolation_nodes,1))
# 			LHS=[]
# 			for i5 in xrange(0,No_interpolation_nodes):
# 				LHS_component=sp.zeros((No_interpolation_nodes))
# 				for i12 in xrange(0,No_interpolation_nodes):
# 					LHS_component[i12]=fun_list[i12](interpolation_nodes[i5][3],interpolation_nodes[i5][4],interpolation_nodes[i5][5])
# 				# print LHS_component, "\n"
# 				LHS.append(LHS_component)

# 				station_id_x=int(interpolation_nodes[i5][0]);
# 				station_id_y=int(interpolation_nodes[i5][1]);
# 				station_id_z=int(interpolation_nodes[i6][2]);

# 				u=eng.read_station(sw4_motion_path,station_id_x,station_id_y,station_id_z);
# 				u=sp.array(u);

# 				# print "down raeading sac"

# 				RHS[i5,0]=u[i7][i6]

# 			LHS=sp.array(LHS)
# 	 		print RHS,"\n", "i AM rhs"
# 	 		print LHS,"\n", "I am lhs"
# 			inv_LHS=inv(LHS)
# 			interpolation_parameter=np.dot(inv_LHS, RHS)
# 			# print interpolation_parameter, "\n"
# 			node_velocity=0;
# 			for i8 in xrange(0,No_interpolation_nodes):
# 				node_velocity=node_velocity+interpolation_parameter[i8,0]*fun_list[i8](new_node_x,new_node_y,new_node_z)
# 			original_velocity[i6,i7]=node_velocity;
# 	for x10 in xrange(1,No_time_step):
# 		original_displacement[:,x10]=original_displacement[:,x10-1]+original_velocity[:,x10]*original_time_step;
# 		original_acceleration[:,x10]=(original_velocity[:,x10]-original_velocity[:,x10-1])/original_time_step;
# 	for x11 in xrange(0,sampled_No_time_step):
# 		sampled_displacement[:,x11]=original_displacement[:,x11*sample_time_step_interval];
# 		sampled_acceleration[:,x11]=original_acceleration[:,x11*sample_time_step_interval];
# 	print sampled_displacement, sampled_acceleration
# 	return sampled_displacement,sampled_acceleration;

############################################################################################################################################################
############################################################################################################################################################

############################################################## 8 node brick shape function interpolation ###################################################
###############################################################################################################################################################
def getField (new_node_x,new_node_y,new_node_z,new_node_index,sample_time_step_interval):

	original_velocity=sp.zeros((No_time_step,3));
	original_acceleration=sp.zeros((3,No_time_step));
	original_displacement=sp.zeros((3,No_time_step));
	sampled_displacement_component=sp.zeros((3,sampled_No_time_step));
	sampled_acceleration_component=sp.zeros((3,sampled_No_time_step));

	x_pos_id=int(sp.floor(abs(new_node_x-Reference_station_x)/ESSI_nodes_x_spacing))+1;
	x_neg_id=int(sp.floor(abs(new_node_x-Reference_station_x)/ESSI_nodes_x_spacing));
	y_pos_id=int(sp.floor(abs(new_node_y-Reference_station_y)/ESSI_nodes_y_spacing))+1;
	y_neg_id=int(sp.floor(abs(new_node_y-Reference_station_y)/ESSI_nodes_y_spacing));
	z_pos_id=int(sp.floor(abs(new_node_z-Reference_station_z)/ESSI_nodes_z_spacing))+1;
	z_neg_id=int(sp.floor(abs(new_node_z-Reference_station_z)/ESSI_nodes_z_spacing));

	u1=eng.read_station(sw4_motion_path,x_pos_id,y_pos_id,z_pos_id);
	u2=eng.read_station(sw4_motion_path,x_neg_id,y_pos_id,z_pos_id);
	u3=eng.read_station(sw4_motion_path,x_pos_id,y_neg_id,z_pos_id);
	u4=eng.read_station(sw4_motion_path,x_neg_id,y_neg_id,z_pos_id);
	u5=eng.read_station(sw4_motion_path,x_pos_id,y_pos_id,z_neg_id);
	u6=eng.read_station(sw4_motion_path,x_neg_id,y_pos_id,z_neg_id);
	u7=eng.read_station(sw4_motion_path,x_pos_id,y_neg_id,z_neg_id);
	u8=eng.read_station(sw4_motion_path,x_neg_id,y_neg_id,z_neg_id);



	u1=sp.array(u1);
	u2=sp.array(u2);
	u3=sp.array(u3);
	u4=sp.array(u4);
	u5=sp.array(u5);
	u6=sp.array(u6);	
	u7=sp.array(u7);
	u8=sp.array(u8);

	###### for 8 node brick, some notation is listed here: node 1 (+1, +1, +1); node 2 (-1,+1,+1); node 3 (+1, -1, +1); node 4 (-1, -1, +1); node 5 (+1, +1, -1); node 6 (-1, +1, -1); node 7(+1, -1, -1); node 8 (-1,-1,-1)
	x1=x_pos_id*ESSI_nodes_x_spacing+Reference_station_x;
	y1=y_pos_id*ESSI_nodes_y_spacing+Reference_station_y;
	z1=z_pos_id*ESSI_nodes_z_spacing+Reference_station_z;

	x2=x_neg_id*ESSI_nodes_x_spacing+Reference_station_x;
	# y2=y_pos_id*ESSI_nodes_y_spacing+Reference_station_y;
	# z2=z_pos_id*ESSI_nodes_z_spacing+Reference_station_z;

	# x3=x_pos_id*ESSI_nodes_x_spacing+Reference_station_x;
	# y3=y_neg_id*ESSI_nodes_y_spacing+Reference_station_y;
	# z3=z_pos_id*ESSI_nodes_z_spacing+Reference_station_z;

	# x4=x_neg_id*ESSI_nodes_x_spacing+Reference_station_x;
	y4=y_neg_id*ESSI_nodes_y_spacing+Reference_station_y;
	# z4=z_pos_id*ESSI_nodes_z_spacing+Reference_station_z;

	# x5=x_pos_id*ESSI_nodes_x_spacing+Reference_station_x;
	# y5=y_pos_id*ESSI_nodes_y_spacing+Reference_station_y;
	z5=z_neg_id*ESSI_nodes_z_spacing+Reference_station_z;

	# x6=x_neg_id*ESSI_nodes_x_spacing+Reference_station_x;5

	# y6=y_pos_id*ESSI_nodes_y_spacing+Reference_station_y;
	# z6=z_neg_id*ESSI_nodes_z_spacing+Reference_station_z;

	# x7=x_pos_id*ESSI_nodes_x_spacing+Reference_station_x;
	# y7=y_neg_id*ESSI_nodes_y_spacing+Reference_station_y;
	# z7=z_neg_id*ESSI_nodes_z_spacing+Reference_station_z;

	# x8=x_neg_id*ESSI_nodes_x_spacing+Reference_station_x;
	# y8=y_neg_id*ESSI_nodes_y_spacing+Reference_station_y;
	# z8=z_neg_id*ESSI_nodes_z_spacing+Reference_station_z;

	# print "node coordinates",x1,x2,y1,y4,z1,z5;
	# print "current node", new_node_x,new_node_y,new_node_z;

	# print "node value", u1[4500,0], u2[4500,0], u3[4500,0], u4[4500,0], u5[4500,0], u6[4500,0],  u7[4500,0], u8[4500,0];    



	kexi=(2*new_node_x-(x1+x2))/(x1-x2);   ### local coordinate in x direction
	yita=(2*new_node_y-(y1+y4))/(y1-y4);   ### local coordinate in y direction
	zeta=(2*new_node_z-(z1+z5))/(z1-z5);   ### local coordinate in z direction

	# print "kexi",kexi, yita,zeta;


	N1=1.0/8.0*(1+kexi)*(1+yita)*(1+zeta);  ### be careful that by 1/8 will be evaulated as 0 not 0.125
	N2=1.0/8.0*(1-kexi)*(1+yita)*(1+zeta);
	N3=1.0/8.0*(1+kexi)*(1-yita)*(1+zeta);
	N4=1.0/8.0*(1-kexi)*(1-yita)*(1+zeta);
	N5=1.0/8.0*(1+kexi)*(1+yita)*(1-zeta);
	N6=1.0/8.0*(1-kexi)*(1+yita)*(1-zeta);
	N7=1.0/8.0*(1+kexi)*(1-yita)*(1-zeta);
	N8=1.0/8.0*(1-kexi)*(1-yita)*(1-zeta);

	# print "Immediate result",N1, N2, N3, N4, N5, N6, N7, N8;


	original_velocity=N1*u1+N2*u2+N3*u3+N4*u4+N5*u5+N6*u6+N7*u7+N8*u8;



	# print "original_velocity", original_velocity;

	original_velocity=sp.array(original_velocity);

	original_velocity=original_velocity.transpose();

	# print original_velocity[0,4500]

	# print "shape is: ", original_velocity.shape

	for x10 in xrange(1,No_time_step):
		original_displacement[:,x10]=original_displacement[:,x10-1]+original_velocity[:,x10]*original_time_step;
		original_acceleration[:,x10]=(original_velocity[:,x10]-original_velocity[:,x10-1])/original_time_step;

	# print "original_dis", original_displacement;
	# print "original_acc", original_acceleration;

	for x11 in xrange(0,sampled_No_time_step):
		sampled_displacement_component[:,x11]=original_displacement[:,x11*sample_time_step_interval];
		sampled_acceleration_component[:,x11]=original_acceleration[:,x11*sample_time_step_interval];



	print "Down with ground motion interpolation for node # ", new_node_index, "!!";

	# print "sampled_dis","sampled_acc",sampled_displacement_component, sampled_acceleration_component

	return sampled_displacement_component,sampled_acceleration_component;


###############################################################################################################################################################
###############################################################################################################################################################

######################### usr input variable ###################################################################
model_name=raw_input('Specify the model name: ');

sw4_motion_path=raw_input('Specify the sw4 motion directory: ');    #'/home/hexiang/SMR_work/smr/sw4_motion/M5.5_ESSI_srf.sw4output';
sample_time_step_interval=input('Specify the interval of time steps for sampling: ');


# Interpolation_Radius=input('Specify initial search radius: ');
# scale_ratio=input('Specify radius scale ratio: ');

########################## Ending usr input ####################################################################

DRM_hdf5_filename=model_name+".h5.drminput"

matlab_path=SOURCE_DIR+'/sw4_tools';

No_new_node=new_node.shape[0]

boundary_node=sp.loadtxt("boundary_node.txt",dtype=sp.int32)

exterior_node=sp.loadtxt("exterior_node.txt",dtype=sp.int32)

element=sp.loadtxt("DRM_element.txt",dtype=sp.int32)

############################################ Generate time data #####################################
eng = matlab.engine.start_matlab()

eng.cd(matlab_path, nargout=0)

No_time_step=eng.read_station_time_step(sw4_motion_path,0,0,0);

No_time_step=int(No_time_step);

t=eng.read_station_time(sw4_motion_path,0,0,0);

original_time_step= t 

sampled_time_step=original_time_step*sample_time_step_interval;

sampled_No_time_step=(No_time_step-1)/sample_time_step_interval+1;

Time=[i*sampled_time_step for i in xrange(0,sampled_No_time_step)];

# print Time;


####################################################################################################

######################################### generate DRM node and element data########################

Ne=exterior_node.shape[0]
Nb=boundary_node.shape[0]
Nt=Ne+Nb

Exterior_node=sp.zeros((Ne))
Boundary_node=sp.zeros((Nb))

for i1 in xrange(0,Ne):
	Exterior_node[i1]=exterior_node[i1,0]
for i2 in xrange(0,Nb):
	Boundary_node[i2]=boundary_node[i2,0]

all_nodes=sp.hstack((Boundary_node,Exterior_node))
is_boundary_node=sp.zeros(Nt, dtype=sp.int32)
is_boundary_node[0:Nb]=1

######################################################################################################

#################################### generate displacement and acceleration data ###################
# station_grid_space=10;
# search_scale=1.1;
# Interpolation_Radius=station_grid_space*search_scale;
# scale_ratio=1.2;


# def interpolated_motion(interpolation_nodes,new_node_x,new_node_y,new_node_z,u_total):
# 	# No_station=(u_total.shape[1]-1)/3;
# 	No_interpolation_nodes=len(interpolation_nodes)
# 	No_time_step=u_total.shape[0]
# 	node_motion_component=sp.zeros((3,No_time_step))

# 	for i7 in xrange(0,No_time_step):  
# 	# for i7 in xrange(0,1): 
# 		for i6 in xrange(0,3):  # 0 1 2 for ux uy uz
# 			RHS=sp.zeros((No_interpolation_nodes,1))
# 			LHS=[]
# 			for i5 in xrange(0,No_interpolation_nodes):
# 				LHS_component=sp.zeros((No_interpolation_nodes))
# 				for i12 in xrange(0,No_interpolation_nodes):
# 					LHS_component[i12]=fun_list[i12](interpolation_nodes[i5][3],interpolation_nodes[i5][4],interpolation_nodes[i5][5])
# 				# print LHS_component, "\n"
# 				LHS.append(LHS_component)
# 				RHS_column=int(interpolation_nodes[i5][6]*3+i6+1)
# 				RHS[i5,0]=u_total[i7][RHS_column]
# 			LHS=sp.array(LHS)
# 	 		# print RHS,"\n"
# 	 		# print LHS,"\n"
# 			inv_LHS=inv(LHS)
# 			interpolation_parameter=np.dot(inv_LHS, RHS)
# 			# print interpolation_parameter, "\n"
# 			motion=0;
# 			for i8 in xrange(0,No_interpolation_nodes):
# 				motion=motion+interpolation_parameter[i8,0]*fun_list[i8](new_node_x,new_node_y,new_node_z)
# 			node_motion_component[i6,i7]=motion
# 	return node_motion_component

	#####################finally generate motion for every DRM node##############################################



sampled_acceleration=sp.zeros((1,sampled_No_time_step));
# sampled_acceleration.shape[1]=sampled_No_time_step;
sampled_displacement=sp.zeros((1,sampled_No_time_step));
# sampled_displacement.shape[1]=sampled_No_time_step;

h5file=h5py.File(DRM_hdf5_filename,"a")
h5file.create_dataset("Elements", data=element)
h5file.create_dataset("DRM Nodes", data=all_nodes)
h5file.create_dataset("Is Boundary Node", data=is_boundary_node)
h5file.create_dataset("Number of Exterior Nodes", data=Ne)
h5file.create_dataset("Number of Boundary Nodes", data=Nb)
h5file.create_dataset("Time", data=Time)

DRMInput_Accelerations = h5file.create_dataset("Accelerations", (3*No_new_node,sampled_No_time_step), 'f')
DRMInput_Displacements = h5file.create_dataset("Displacements", (3*No_new_node,sampled_No_time_step), 'f')
h5file.close()

for i9 in xrange(0,No_new_node):
	# No_new_node
# for i9 in xrange(0,1):
	h5file    = h5py.File(DRM_hdf5_filename, 'a')   # 'r' means that hdf5 file is open in read-only mode
	DRMInput_Accelerations = h5file["Accelerations"];
	DRMInput_Displacements = h5file["Displacements"];
	sampled_displacement_component,sampled_acceleration_component=getField(new_node[i9,1],new_node[i9,2],new_node[i9,3],new_node[i9,0],sample_time_step_interval);
	DRMInput_Accelerations[i9*3:i9*3+3,:]=sampled_acceleration_component;
	DRMInput_Displacements[i9*3:i9*3+3,:]=sampled_displacement_component;
	h5file.close()

	print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
	print "DRMInputGenerator::[", i9+1, " of ",  No_new_node,"] completed \n"; 	
	print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
		


##################################################################################################



















