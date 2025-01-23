opts = delimitedTextImportOptions("NumVariables", 2);

% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["Alpha", "Cl"];
opts.VariableTypes = ["double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
LC01 = readtable(".\LC01.csv", opts);
LC02 = readtable(".\LC02.csv", opts);
LC03 = readtable(".\LC03.csv", opts);
LC04 = readtable(".\LC04.csv", opts);
LC05 = readtable(".\LC05.csv", opts);
LC06 = readtable(".\LC06.csv", opts);
LC07 = readtable(".\LC07.csv", opts);
LC08 = readtable(".\LC08.csv", opts);
LC09 = readtable(".\LC09.csv", opts);
LC1 = readtable(".\LC1.csv", opts);

clear opts
opts = delimitedTextImportOptions("NumVariables", 2);

% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["Alpha", "Cd"];
opts.VariableTypes = ["double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
DC01 = readtable(".\DC01.csv", opts);
DC02 = readtable(".\DC02.csv", opts);
DC03 = readtable(".\DC03.csv", opts);
DC04 = readtable(".\DC04.csv", opts);
DC05 = readtable(".\DC05.csv", opts);
DC06 = readtable(".\DC06.csv", opts);
DC07 = readtable(".\DC07.csv", opts);
DC08 = readtable(".\DC08.csv", opts);
DC09 = readtable(".\DC09.csv", opts);
DC1 = readtable(".\DC1.csv", opts);


clear opts

Alpha = LC01.Alpha;
Cl = LC01.Cl;
x = [5 5];
y = [50 -50];
[~,yout] = intersections(x,y,Alpha,Cl)
z(1)=yout

Alpha = LC02.Alpha;
Cl = LC02.Cl;
[~,yout] = intersections(x,y,Alpha,Cl);
z(2)=yout;

Alpha = LC03.Alpha;
Cl = LC03.Cl;
[~,yout] = intersections(x,y,Alpha,Cl);
z(3)=yout;

Alpha = LC04.Alpha;
Cl = LC04.Cl;
[~,yout] = intersections(x,y,Alpha,Cl);
z(4)=yout;

Alpha = LC05.Alpha;
Cl = LC05.Cl;;
[~,yout] = intersections(x,y,Alpha,Cl);
z(5)=yout;

Alpha = LC06.Alpha;
Cl = LC06.Cl;
[~,yout] = intersections(x,y,Alpha,Cl);
z(6)=yout;

Alpha = LC07.Alpha;
Cl = LC07.Cl;
[~,yout] = intersections(x,y,Alpha,Cl);
z(7)=yout;

Alpha = LC08.Alpha;
Cl = LC08.Cl;
[~,yout] = intersections(x,y,Alpha,Cl);
z(8)=yout;

Alpha = LC09.Alpha;
Cl = LC09.Cl;
[~,yout] = intersections(x,y,Alpha,Cl);
z(9)=yout;

Alpha = LC1.Alpha;
Cl = LC1.Cl;
[~,yout] = intersections(x,y,Alpha,Cl);
z(10)=yout;
z;

Alpha = DC01.Alpha;
Cd = DC01.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(1)=yout;

Alpha = DC02.Alpha;
Cd = DC02.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(2)=yout;

Alpha = DC03.Alpha;
Cd = DC03.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(3)=yout;

Alpha = DC04.Alpha;
Cd = DC04.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(4)=yout;

Alpha = DC05.Alpha;
Cd = DC05.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(5)=yout;

Alpha = DC06.Alpha;
Cd = DC06.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(6)=yout;

Alpha = DC07.Alpha;
Cd = DC07.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(7)=yout;

Alpha = DC08.Alpha;
Cd = DC08.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(8)=yout;

Alpha = DC09.Alpha;
Cd = DC09.Cd;
[~,yout] = intersections(x,y,Alpha,Cd);
a(9)=yout;

Alpha = DC1.Alpha;
Cd = DC1.Cd;
[xout,yout] = intersections(x,y,Alpha,Cd);
a(10)=yout;
a

delta = ((pi*5.767.*a)./(z.*z))-1
b=0.1:0.1:1;
figure()
hold on
plot(b,delta,'LineWidth',1.5)
title('Taper Analysis : NUM \delta(\lambda)');
xlabel('Taper ratio \lambda ');
ylabel('Drag factor \delta');
