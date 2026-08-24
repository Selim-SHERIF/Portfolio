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
LC2 = readtable(".\LC2.csv", opts);
LC8 = readtable(".\LC8.csv", opts);
LC6 = readtable(".\LC6.csv", opts);
LC4 = readtable(".\LC4.csv", opts);
LC2VLM = readtable(".\LC2VLM.csv", opts)
clear opts
% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 2);

% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["Cl", "Cd"];
opts.VariableTypes = ["double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
DP2 = readtable(".\DP2.csv", opts);
DP4 = readtable(".\DP4.csv", opts);
DP6 = readtable(".\DP6.csv", opts);
DP8 = readtable(".\DP8.csv", opts);

%Clear temporary variables
clear opts

% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 2);

% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["Cl", "Cd_i"];
opts.VariableTypes = ["double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
DPI2 = readtable(".\DPI2.csv", opts);
DPI4 = readtable(".\DPI4.csv", opts);
DPI6 = readtable(".\DPI6.csv", opts);
DPI8 = readtable(".\DPI8.csv", opts);

%Clear temporary variables
clear opts

Alpha = LC2.Alpha;
Cl = LC2.Cl;
figure()
plot (Alpha,Cl,'LineWidth',1.5)
hold on;
xL = xlim;
yL = ylim;
xticks(xL(1):10:xL(2));
yticks(yL(1):0.5:yL(2));
title('Lift curve : NUM AR Analysis');
xlabel('Angle of attack : \alpha (in deg)');
ylabel('Lift coefficient : C_l ');
Alpha = LC4.Alpha;
Cl = LC4.Cl;
plot (Alpha,Cl,'LineWidth',1.5)

Alpha = LC6.Alpha;
Cl = LC6.Cl;
plot (Alpha,Cl,'LineWidth',1.5)

Alpha = LC8.Alpha;
Cl = LC8.Cl;
plot (Alpha,Cl,'LineWidth',1.5)


yline(0, 'k','LineStyle','--','LineWidth',0.25);   %x-axis
xline(0, 'k','LineStyle','--','LineWidth',0.25);  %y-axis
legend('2','4','6', '8', 'Location', 'southeast')
hold off

%Drag polar 
Cl=DP2.Cl;
Cd=DP2.Cd;
figure()
plot (Cl,Cd,'LineWidth',1.5)
hold on;
xL = xlim;
yL = ylim;
yticks(yL(1):0.25:yL(2));
xticks(xL(1):0.02:xL(2));
Cl=DP4.Cl;
Cd=DP4.Cd;
plot (Cl,Cd,'LineWidth',1.5)
Cl=DP6.Cl;
Cd=DP6.Cd;
plot (Cl,Cd,'LineWidth',1.5)
Cl=DP8.Cl;
Cd=DP8.Cd;
plot (Cl,Cd,'LineWidth',1.5)
title('Drag polar : NUM AR Analysis');
ylabel('Lift coefficient : C_l');
xlabel('Drag coefficient : C_d');
yline(0, 'k','LineStyle','--','LineWidth',0.25);   %x-axis  %y-axis
legend('2','4','6', '8', 'Location', 'southeast')
hold off;
% I Drag polar 
Cl=DPI2.Cl;
Cd=DPI2.Cd_i;
figure()
plot (Cl,Cd,'LineWidth',1.5)
hold on;
xL = xlim;
yL = ylim;
yticks(yL(1):0.25:yL(2));
xticks(xL(1):0.02:xL(2));
xlim([0 xL(2)])
Cl=DPI4.Cl;
Cd=DPI4.Cd_i;
plot (Cl,Cd,'LineWidth',1.5)
Cl=DPI6.Cl;
Cd=DPI6.Cd_i;
plot (Cl,Cd,'LineWidth',1.5)
Cl=DPI8.Cl;
Cd=DPI8.Cd_i;
plot (Cl,Cd,'LineWidth',1.5)
title('Induced drag polar : NUM AR Analysis');
ylabel('Lift coefficient : C_l');
xlabel('Induced drag coefficient : C_{d_i}');
yline(0, 'k','LineStyle','--','LineWidth',0.25);   
legend('2','4','6', '8', 'Location', 'southeast')
hold off;

%Combine
Cl=DPI2.Cl;
Cd=DPI2.Cd_i;
figure()
plot (Cl,Cd,'b','LineWidth',0.5)
hold on;
xL = xlim;
yL = ylim;
yticks(yL(1):0.25:yL(2));
xticks(xL(1):0.02:xL(2));
xlim([0 xL(2)])
Cl=DPI4.Cl;
Cd=DPI4.Cd_i;
plot (Cl,Cd,'b','LineWidth',0.5)
Cl=DPI6.Cl;
Cd=DPI6.Cd_i;
plot (Cl,Cd,'b','LineWidth',0.5)
Cl=DPI8.Cl;
Cd=DPI8.Cd_i;
plot (Cl,Cd,'b','LineWidth',0.5)


Cl=DP2.Cl;
Cd=DP2.Cd;
plot (Cl,Cd,'color','[0.8500 0.3250 0.0980]','LineWidth',0.5)
hold on;
xL = xlim;
yL = ylim;
yticks(yL(1):0.25:yL(2));
xticks(xL(1):0.02:xL(2));
Cl=DP4.Cl;
Cd=DP4.Cd;
plot (Cl,Cd,'color','[0.8500 0.3250 0.0980]','LineWidth',0.5)
Cl=DP6.Cl;
Cd=DP6.Cd;
plot (Cl,Cd,'color','[0.8500 0.3250 0.0980]','LineWidth',0.5)
Cl=DP8.Cl;
Cd=DP8.Cd;
plot (Cl,Cd,'color','[0.8500 0.3250 0.0980]','LineWidth',0.5)
title('Drag polar/Induced drag polar : NUM AR Analysis');
ylabel('Lift coefficient : C_l');
xlabel('Drag coefficient/ Induced drag coefficient: C_d/C_{d_i}');
yline(0, 'k','LineStyle','--','LineWidth',0.25); 
legend('Induced drag','','', '','Full drag', 'Location', 'southeast')
%% vlm vs llt
clear opts

Alpha = LC2.Alpha;
Cl = LC2.Cl;
figure()
plot (Alpha,Cl,'LineWidth',1.5)
hold on;

title('Lift curve : NUM LLT VS VLM');
xlabel('Angle of attack : \alpha (in deg)');
ylabel('Lift coefficient : C_l ');

Alpha = LC2VLM.Alpha;
Cl = LC2VLM.Cl;
xL = xlim;
yL = ylim;
xticks(xL(1):10:xL(2));
yticks(yL(1):0.5:yL(2));
plot (Alpha,Cl,'LineWidth',1.5);
yline(0, 'k','LineStyle','--','LineWidth',0.25);   %x-axis
xline(0, 'k','LineStyle','--','LineWidth',0.25);  %y-axis
legend('LLT','VLM', 'Location', 'southeast')
hold off