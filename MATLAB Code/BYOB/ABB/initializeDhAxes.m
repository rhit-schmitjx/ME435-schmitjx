function initializeDhAxes

% Begin: Setup for this stand alone version that will NOT go into the GUI.
close all
app.axes_arm = axes;  % Create a new axes and save a handle to it.
app.jointAngles = [0 -90 0 0 0 0]; % Start at the zero angle position.

clc

% Prepare the axes_arm properties
app.axes_arm.View = [90 -50];
app.axes_arm.Visible = 'off';

% Once you are in Matlab App Designer you can try these axes_arm properties too.
% These properties keep the Axes from automatically resizing (optional)
% app.axes_arm.XLim = [-160 250];
% app.axes_arm.YLim = [-250 250];
% app.axes_arm.ZLim = [-22 22];

% Create vertices for all the patches
makeStlLink("link_0.stl", app.axes_arm, [.2 .2 .2]);  % Doesn't move. No need to save a handle to it.
% Save references to the vertices of each patch, make points 4x1 not 3x1.
app.link1Patch = makeStlLink("link_1.stl", app.axes_arm, [211/255 211/255 211/255]);
app.link1Vertices = get(app.link1Patch, 'Vertices')';
app.link1Vertices(4,:) = ones(1, size(app.link1Vertices,2));

app.link2Patch = makeStlLink("link_2.stl", app.axes_arm, [255/255 165/255 0/255]);
app.link2Vertices = get(app.link2Patch, 'Vertices')';
app.link2Vertices(4,:) = ones(1, size(app.link2Vertices,2));

app.link3Patch = makeStlLink("link_3.stl", app.axes_arm, [255/255 255/255 0/255]);
app.link3Vertices = get(app.link3Patch, 'Vertices')';
app.link3Vertices(4,:) = ones(1, size(app.link3Vertices,2));

app.link4Patch = makeStlLink("link_4.stl", app.axes_arm, [135/255 206/255 235/255]);
app.link4Vertices = get(app.link4Patch, 'Vertices')';
app.link4Vertices(4,:) = ones(1, size(app.link4Vertices,2));

app.link5Patch = makeStlLink("link_5.stl", app.axes_arm, [0/255 0/255 128/255]);
app.link5Vertices = get(app.link5Patch, 'Vertices')';
app.link5Vertices(4,:) = ones(1, size(app.link5Vertices,2));

app.link6Patch = makeStlLink("link_6.stl", app.axes_arm, [255/255 105/255 180/255]);
app.link6Vertices = get(app.link6Patch, 'Vertices')';
app.link6Vertices(4,:) = ones(1, size(app.link6Vertices,2));


% End: Code that can go into your GUI's opening function.

updateArm(app);

end

function updateArm(app)

% Create the A homogeneous transformation matrices for the given jointAngles.

A1 = create_A_matrix(0,290,-90, app.jointAngles(1));
A2 = create_A_matrix(270,0,0, app.jointAngles(2));
A3 = create_A_matrix(70,0,-90, app.jointAngles(3));
A4 = create_A_matrix(0,302,90, app.jointAngles(4));
A5 = create_A_matrix(0,0,-90, app.jointAngles(5));
A6 = create_A_matrix(0,72,0, app.jointAngles(6));


% Use the current A matricies to form the T0_n matricies.
T0_1 = A1;
T0_2 = T0_1 * A2;
T0_3 = T0_2 * A3;
T0_4 = T0_3 * A4;
T0_5 = T0_4 * A5;
T0_6 = T0_5 * A6;
% Use the current T matricies to transform the original patch vertices
link1VerticesWRTground = T0_1 * app.link1Vertices;
link2VerticesWRTground = T0_2 * app.link2Vertices;
link3VerticesWRTground = T0_3 * app.link3Vertices;
link4VerticesWRTground = T0_4 * app.link4Vertices;
link5VerticesWRTground = T0_5 * app.link5Vertices;
link6VerticesWRTground = T0_6 * app.link6Vertices;

% Update the patches with the newly transformed vertices
set(app.link1Patch, 'Vertices', link1VerticesWRTground(1:3,:)');
set(app.link2Patch, 'Vertices', link2VerticesWRTground(1:3,:)');
set(app.link3Patch, 'Vertices', link3VerticesWRTground(1:3,:)');
set(app.link4Patch, 'Vertices', link4VerticesWRTground(1:3,:)');
set(app.link5Patch, 'Vertices', link5VerticesWRTground(1:3,:)');
set(app.link6Patch, 'Vertices', link6VerticesWRTground(1:3,:)');

end
