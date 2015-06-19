clear;
clc;
close all;

%constants taken from http://psas.pdx.edu/rollcontrol/
Izz = 0.08594;       %m2*kg
Ts = 0.0033;

%State Space equation
%assuming partial-state feedback (angular vel.)
%model equation from http://psas.pdx.edu/rollcontrol/
a = [0 1; 0 -0.001/Izz];
b = [0; 1];
c = [1 0];
d = 0;

sys_state_space = ss(a,b,c,d,'statename',{'Angular Accel','Angular Vel'});

[num den] = ss2tf(a,b,c,d);
%num = [0 1];
%den = [Izz 0.001];
Gp = tf(num, den)
[a, b, c, d] = tf2ss(num, den)
sysd = c2d(Gp,Ts,'zoh');

controller = pidtool(sysd,'pid')
