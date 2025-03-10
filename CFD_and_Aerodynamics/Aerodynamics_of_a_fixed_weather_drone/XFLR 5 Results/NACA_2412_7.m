%% Import data from text file DP2412
% Script for importing data from the following text file:
%
%    filename: C:\Users\selim\Documents\HKUST BA5\Aerodynamics\Project\XFLR 5 Results\DP2412.csv
%
% Auto-generated by MATLAB on 01-Nov-2023 17:43:36

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
DP2412 = readtable(".\DP2412.csv", opts);


%Clear temporary variables
clear opts

%% Import data from text file LC2412
% Script for importing data from the following text file:
%
%    filename: C:\Users\selim\Documents\HKUST BA5\Aerodynamics\Project\XFLR 5 Results\LC2412.csv
%
% Auto-generated by MATLAB on 01-Nov-2023 17:44:40

% Set up the Import Options and import the data
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
LC2412 = readtable(".\LC2412.csv", opts);
LC04 = readtable(".\LC04.csv", opts);
LC4 = readtable(".\LC4.csv", opts);
LC8 = readtable(".\LC8.csv", opts);
LC1 = readtable(".\LC1.csv", opts);
W2412LC = readtable(".\W2412LC.csv", opts);
W2412ULC = readtable(".\W2412ULC.csv", opts);
% Clear temporary variables
clear opts

%% Import data from spreadsheet EXP
% Script for importing data from the following spreadsheet:
%
%    Workbook: C:\Users\selim\Documents\HKUST BA5\Aerodynamics\Project\XFLR 5 Results\Experimental Data.xlsx
%    Worksheet: Sheet1
%
% Auto-generated by MATLAB on 01-Nov-2023 18:47:55

% Set up the Import Options and import the data
opts = spreadsheetImportOptions("NumVariables", 29);

% Specify sheet and range
opts.Sheet = "Sheet1";
opts.DataRange = "A1:AC30";

% Specify column names and types
opts.VariableNames = ["Alpha", "NACA2406", "NACA2406D", "NACA2406tripped", "NACA2406trippedD", "NACA2409", "NACA2409D", "NACA2409tripped", "NACA2409trippedD", "NACA2412", "NACA2412D", "NACA2412tripped", "NACA2412trippedD", "NACA2415", "NACA2415D", "NACA2415tripped", "NACA2415trippedD", "NACA2418", "NACA2418D", "NACA2418tripped", "NACA2418trippedD", "NACA2421", "NACA2421D", "NACA2421tripped", "NACA2421trippedD", "NACA1412", "NACA1412D", "NACA3412", "NACA3412D"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double"];

% Import the data
ExperimentalData = readtable(".\Experimental Data.xlsx", opts, "UseExcel", false);


%Clear temporary variables
clear opts
%% Theoratical Approach
x = -20:0.01:20;
C_l= ((pi^2)/90)*(x + 2.077);
figure()
plot(x, C_l,'LineWidth', 0.5)
hold on;
xL = xlim;
yL = ylim;
xline(0, 'k','LineStyle','--','LineWidth',0.25);  %y-axis
yline(0, 'k','LineStyle','--','LineWidth',0.25);  %y-axis
xticks(xL(1):10:xL(2));
yticks(yL(1):0.5:yL(2));
title('Lift curve : NACA 2412');
xlabel('Angle of attack : \alpha (in deg)');
ylabel('Lift coefficient : C_l ');
%% Expermiental
Alpha = ExperimentalData.Alpha;
Cl_a = (ExperimentalData.NACA2412)./(0.5*0.395*0.1*23*23*1.1606);
plot (Alpha,Cl_a,'LineWidth',0.5)

%% LLT Untwisted
Alpha = W2412ULC.Alpha;
Cl = W2412ULC.Cl;
plot (Alpha,Cl,'LineWidth',0.5)
%% LLT Twisted
Alpha = W2412LC.Alpha+2.04;
Cl = W2412LC.Cl;
plot (Alpha,Cl,'LineWidth',0.5)

%%  LLT OPT TAPERED 
Alpha = LC04.Alpha;
Cl = LC04.Cl;
plot (Alpha,Cl,'LineWidth',0.5)
%% LLT RECTANGULAR
Alpha = LC1.Alpha;
Cl = LC1.Cl;
plot (Alpha,Cl,'LineWidth',0.5)
%% LLT AR4

Alpha = LC4.Alpha;
Cl = LC4.Cl;
plot (Alpha,Cl,'LineWidth',0.5)
%% LLT AR4
Alpha = LC8.Alpha;
Cl = LC8.Cl;
plot (Alpha,Cl,'LineWidth',0.5)
hold off
legend('TAT','','','EXP','LLT Untwisted', 'LLT Twisted', 'LLT Tapered', 'LLT Rectangle', 'LLT AR=4', 'LLT AR=8', 'Location', 'southeast')