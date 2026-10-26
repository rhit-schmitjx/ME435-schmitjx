function initializeDhAxes

% Begin: Setup for this stand alone version that will not go into the GUI.
close all
app.axes_arm = axes;
%app.jointAngles = [0 0 0 0 0]; % Zero angle position.
app.jointAngles = [0 90 0 -90 90]; % Servo home position.
%  End : Setup for this stand alone version that will not go into the GUI.



% Begin: Code that can go into your GUI's opening function.
clc

% Prepare the arm axes
view(app.axes_arm, [-5 -5 5]);
axis(app.axes_arm, [-12 12 -8 8 -6 16]);
set(app.axes_arm, 'Visible', 'off');

% Create vertices for all the patches
makeLink0(app.axes_arm, [.5 .5 .5]);  % Doesn't move. No need to save.
% Save references to the vertices of each patch, make points 4x1 not 3x1.
app.link1Patch = makeLink1(app.axes_arm, [.9 .9 .9]);
app.link1Vertices = get(app.link1Patch, 'Vertices')';
app.link1Vertices(4,:) = ones(1, size(app.link1Vertices,2));

app.link2Patch = makeLink2(app.axes_arm, [.9 .9 .9]);
app.link2Vertices = get(app.link2Patch, 'Vertices')';
app.link2Vertices(4,:) = ones(1, size(app.link2Vertices,2));

app.link3Patch = makeLink3(app.axes_arm, [.9 .9 .9]);
app.link3Vertices = get(app.link3Patch, 'Vertices')';
app.link3Vertices(4,:) = ones(1, size(app.link3Vertices,2));

app.link4Patch = makeLink4(app.axes_arm, [.9 .9 .9]);
app.link4Vertices = get(app.link4Patch, 'Vertices')';
app.link4Vertices(4,:) = ones(1, size(app.link4Vertices,2));

app.link5Patch = makeLink5(app.axes_arm, [.95 .95 0]);
app.link5Vertices = get(app.link5Patch, 'Vertices')';
app.link5Vertices(4,:) = ones(1, size(app.link5Vertices,2));
% End: Code that can go into your GUI's opening function.

updateArm(app);

end

function updateArm(app)

% TODO: Create the five homogeneous transformation matrices.

% TODO: Use the A matricies to form the T0_n matricies.
% T0_1 = 
% T0_2 = 
% T0_3 = 
% T0_4 = 
% T0_5 = 

% TODO: Use the T matricies to transform the patch vertices
% link1verticesWRTground = T0_1 * app.link1Vertices;
% link2verticesWRTground = T0_2 * app.link2Vertices;
% link3verticesWRTground = T0_3 * app.link3Vertices;
% link4verticesWRTground = T0_4 * app.link4Vertices;
% link5verticesWRTground = T0_5 * app.link5Vertices;

% TODO: Update the patches with the new vertices
% set(app.link1Patch,'Vertices', link1verticesWRTground(1:3,:)');
% set(app.link2Patch,'Vertices', link2verticesWRTground(1:3,:)');
% set(app.link3Patch,'Vertices', link3verticesWRTground(1:3,:)');
% set(app.link4Patch,'Vertices', link4verticesWRTground(1:3,:)');
% set(app.link5Patch,'Vertices', link5verticesWRTground(1:3,:)');


% Display the XYZ of the gripper tip.
% Update x, y, and z using the gripper (end effector) origin.
% dhOrigin = [0 0 0 1]';
% gripperWRTground = T0_5 * dhOrigin;
% fprintf("TODO: Put each individual value into it's own GUI label X = %.3f, Y = %.3f, Z = %.3f)\n", gripperWRTground(1), gripperWRTground(2), gripperWRTground(3));

end
