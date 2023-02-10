% Trajectory
% Plot the trajectory of a particle

[x0, y0, z0, t] = textread(...
    'feb9202310F4.out', ...
    '%f %f %f %f', 'headerlines', 28 );
plot3(x0, y0, z0, 'blue', 'LineWidth', 1);

xlabel('x', 'Interpreter', 'LaTex');
ylabel('y', 'Interpreter', 'LaTex');
zlabel('z', 'Interpreter', 'LaTex');

title('Trajectory of a $^{11}$Li Isotope effusing through a 10 foil target', 'Interpreter', 'LaTex');

grid on
hold on
