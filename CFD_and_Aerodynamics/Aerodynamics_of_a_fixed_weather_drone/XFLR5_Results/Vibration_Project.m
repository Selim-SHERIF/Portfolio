%% Passive model
% Step 1: Assignment of values to parametres
mc = 400;    % kg
mw = 20;     % kg
bp = 700;   % N/m/s
ks = 16000 ; % N/m
kt = 190000; % N/m
% Step 2: State space matrices 
A = [ 0 1 0 0; [-ks -bp ks bp]/mc ; ...
      0 0 0 1; [ks bp -ks-kt -bp]/mw]
B = [ 0 ; 0 ; 0; [kt]/mw]
C = [1 0 0 0; 1 0 -1 0; A(2,:)]
D = [0 ; 0 ; 0]
A(2,:);
% Step 3 : State space system
car = ss(A,B,C,D)
car.StateName = {'body displacement (m)';'body vel (m/s)';...
          'wheel displacement (m)';'wheel vel (m/s)'};
car.InputName = {'r'};
car.OutputName = {'xb';'sd';'ac'}
% Step 4 : Road disturbance
t = 0:0.0025:1;
roaddist = zeros(size(t));
roaddist(1:101) = 0.025*(1-cos(8*pi*t(1:101)));
% Step 5 : Simulate
Passive = lsim(car,roaddist,t);
figure()
subplot(211)
plot(t,Passive(:,1),'b',t,roaddist,'g')
title('Body travel'), ylabel('x_b (m)')
subplot(212)
plot(t,Passive(:,3),t,roaddist,'g')
title('Body acceleration'), ylabel('a_b (m/s^2)')

%% Active model
% State space matrices 
A = [ 0 1 0 0; [-ks -bp ks bp]/mc ; ...
      0 0 0 1; [ks bp -ks-kt -bp]/mw];
B = [ 0 0; 0 1e3/mc ; 0 0 ; [kt -1e3]/mw];
C = [1 0 0 0; 1 0 -1 0; A(2,:)];
D = [0 0; 0 0; B(2,:)];
% State space system
car = ss(A,B,C,D);
car.StateName = {'body displacement (m)';'body vel (m/s)';...
          'wheel displacement (m)';'wheel vel (m/s)'};
car.InputName = {'r';'fa'};
car.OutputName = {'xb';'sd';'ac'};
% Step 6 : Actuator model 
ActNom = tf(1,[1/60 1]);
Wunc = makeweight(0.40,15,3);
unc = ultidyn('unc',[1 1],'SampleStateDim',5);
Act = ActNom*(1 + Wunc*unc);
Act.InputName = 'u';
Act.OutputName = 'fa';
% Step 7: Weights 
Wroad = ss(0.07);  Wroad.u = 'd1';   Wroad.y = 'r'; % Weight of road
Wact = 0.8*tf([1 50],[1 500]);  Wact.u = 'u';  Wact.y = 'e1';%Actuator weight
Wd2 = ss(0.01);  Wd2.u = 'd2';   Wd2.y = 'Wd2';%Noise weight
Wd3 = ss(0.5);   Wd3.u = 'd3';   Wd3.y = 'Wd3';
HandlingTarget = 0.04 * tf([1/8 1],[1/80 1]);% frequency filter for Handling 
ComfortTarget = 0.4 * tf([1/0.45 1],[1/150 1]);% frequency filter for Comfort 
beta = 0.5;% Balance coeffincient
Wsd = beta / HandlingTarget;% Weight of suspension deflection output
Wsd.u = 'sd';  Wsd.y = 'e3';
Wab = (1-beta) / ComfortTarget;% Weight of accelaration of car output
Wab.u = 'ac';  Wab.y = 'e2';
sdmeas  = sumblk('y1 = sd+Wd2');
abmeas = sumblk('y2 = ac+Wd3');
% Step 8: Define closed loop

ICinputs = {'d1';'d2';'d3';'u'};
ICoutputs = {'e1';'e2';'e3';'y1';'y2'};
caric = connect(car(2:3,:),Act,Wroad,Wact,Wd2,Wd3,Wab,Wsd,...
                 sdmeas,abmeas,ICinputs,ICoutputs) 
% Step 9 : Define Controller
ncont = 1; % one control signal, u
nmeas = 2; % two measurement signals, sd and ab
K = ss(zeros(ncont,nmeas,3));
gamma = zeros(3,1);

   [K(:,:,1),~,gamma(1)] = hinfsyn(caric(:,:,1),nmeas,ncont);

K.u = {'sd','ac'};  K.y = 'u';

% Step 10 : Closed-loop model
SIMK = connect(car,Act.Nominal,K,'r',{'xb';'sd';'ac';'fa'});

% Step 11 : Simulate the conditions imposed
y1 = lsim(SIMK(1:4,1,1),roaddist,t);

% Step 12 : Plot results and compare 
figure()
subplot(211)
plot(t,Passive(:,1),'b',t,y1(:,1),'r',t,roaddist,'g')
title('Body travel'), ylabel('x_b (m)')
subplot(212)
plot(t,Passive(:,3),'b',t,y1(:,3),'r',t,roaddist,'g')
title('Body acceleration'), ylabel('a_c (m/s^2)')
legend('Passive','Active','Road','location','SouthEast')
figure()
plot(t,zeros(size(t)),'b',t,y1(:,4),'k')
title('Control force'), xlabel('Time (s)'), ylabel('f_s (kN)')
legend('Passive','Active','location','SouthEast')



