clear
close all
beep off

this_dir = fileparts(mfilename('fullpath'));
addpath(fullfile(this_dir,'..','functions_new'), '-begin');
addpath(genpath(fullfile(this_dir,'..','data','functions')), '-end');

out_dir = fullfile(this_dir,'..','Output');
if ~exist(out_dir,'dir')
    mkdir(out_dir);
end

cepr_dir = fullfile(this_dir,'..','data','Raw_data','CPS','ELABORATED DATA');
dperc=[1 99];
PROB=20:20:80;
    
    

jj=1;
for yy=1985:2019
    yy
fname=fullfile(cepr_dir,sprintf('dataun_%d.csv',yy));
tmpx=importdata(fname);
%month rw hourslw orgwgt fnlwgt empl unem educ pt ptecon experience sex wbho




wage0=tmpx(:,2);
weight0=tmpx(:,4);
[~,dummy]=cutoff(wage0,dperc,weight0);
tmpx(dummy,:)=[]; %drop all datapoints in upper and lower 1 % of wage 

%
employ=tmpx(:,6)==1;
unemploy=tmpx(:,7)==1;

%month rw hourslw orgwgt fnlwgt empl unem educ pt ptecon ...
% experience sex wbho occ ind married state metro age

wage=tmpx(:,2);

educ=tmpx(:,8);

%recode

educ1=zeros(rows(educ),1);
educ1(educ==1|educ==2)=1;
educ1(educ==3|educ==4|educ==5)=2;



%%month hours wage weight year 
month=tmpx(:,1);
hours=tmpx(:,3); %all
weight=tmpx(:,4);
weighth=tmpx(:,5);
race=tmpx(:,13);
occ=tmpx(:,14);
married=tmpx(:,16);
state=tmpx(:,17);
metro=tmpx(:,18);
age=tmpx(:,19);
sex=tmpx(:,12);

if yy<2003
ind=tmpx(:,15);
%recode
ind1=zeros(rows(ind),1);
ind1(find_equal(ind,[1 2 46]))=1; % Agriculture, forestry, fishing, and hunting
ind1(find_equal(ind,[3]))=2; %mining
ind1(find_equal(ind,[4]))=3; %construction
ind1(find_equal(ind,5:26))=4;%manufacturing
ind1(find_equal(ind,[32 33]))=5; %wholesale and retail trade
ind1(find_equal(ind,[29 30 31]))=6;%transportation/utilities
ind1(find_equal(ind,[24 30]))=7; %information
ind1(find_equal(ind,[34 35]))=8; %finance
ind1(find_equal(ind,[37 38]))=9; %professional and business
ind1(find_equal(ind,[41 42 43 44]))=10; %education and health
ind1(find_equal(ind,[40]))=11; %leasure
ind1(find_equal(ind,[36 39 45]))=12; %other services
ind1(find_equal(ind,[52]))=13; %public admin
ind1(find_equal(ind,[51]))=14; %armed forces

else
ind1=tmpx(:,20);
end






for j=1:1:12
    sel=month==j;
    wage_m=wage(sel,:);
    weight_m=weight(sel,:);
    weight_hm=weighth(sel,:);
    hours_m=hours(sel,:); 
    educ_m=educ1(sel,:);
    sex_m=sex(sel,:);
    race_m=race(sel,:);
    age_m=age(sel,:);
    ind_m=ind1(sel,:);

    try
      %hours
        [xout,xout1,xoutx1,xdummy]=...
         getpercw_2(wage_m,PROB,weight_m,...
         hours_m ,weight_hm,0);
        %educ
           [xout,xout1,xoutx2,xdummy]=...
         getpercw_2(wage_m,PROB,weight_m,...
         educ_m==2 ,weight_hm,0);
        %sex
           [xout,xout1,xoutx3,xdummy]=...
         getpercw_2(wage_m,PROB,weight_m,...
         sex_m==1 ,weight_hm,0);

           %race
           [xout,xout1,xoutx4,xdummy]=...
         getpercw_2(wage_m,PROB,weight_m,...
         race_m==1 ,weight_hm,0);

           %age
              [xout,xout1,xoutx5,xdummy]=...
         getpercw_2(wage_m,PROB,weight_m,...
         age_m ,weight_hm,0);

    
     outp=[];
for jjj=1:13
[zout,zout1,zoutx,zdummy]=...
         getpercw_2(wage_m,PROB,weight_m,...
         ind_m==jjj ,weight_m,0);
outp=[outp zoutx];

end
     

     
     
        DATA(:,:,jj)=[xoutx1 xoutx2 xoutx3 xoutx4 xoutx5]
        DATA1(:,:,jj)=outp;
    catch
    end
jj=jj+1;
end



end
namesxx{1}=strcat('<',num2str(PROB(1)));
jj=2;
for j=1:length(PROB)-1
namesxx{jj}=strcat('>',num2str(PROB(j)),' and <=',...
    num2str(PROB(j+1)));
jj=jj+1;
end
namesxx{jj}=strcat('>',num2str(PROB(end)));
namesxx=categorical(namesxx,namesxx);

datam=mean(DATA,3);
fig_char = figure(1);
set(fig_char, 'Units', 'pixels', 'Position', [100 100 900 1200]);
subplot(3,2,1)
bar(namesxx,datam(:,1));
title('Hours')
xlabel('wage distribution')

subplot(3,2,2)
bar(namesxx,datam(:,2));axis tight
title('College')
xlabel('wage distribution')


subplot(3,2,3)
bar(namesxx,datam(:,3));axis tight
title('Male')
xlabel('wage distribution')



subplot(3,2,4)
bar(namesxx,datam(:,4));axis tight
title('White')
xlabel('wage distribution')


subplot(3,2,5)
bar(namesxx,datam(:,5));axis tight
title('Age')
xlabel('wage distribution')


%%%%%%%%%%%
nam{1}='agr';
nam{2}='min';
nam{3}='con';
nam{4}='man';
nam{5}='trade';
nam{6}='trans';
nam{7}='info';
nam{8}='fin';
nam{9}='prof';
nam{10}='health';
nam{11}='fun';
nam{12}='other';
nam{13}='public';
datam2=mean(DATA1,3);
fig_industry = figure(2);
bar(namesxx,datam2,'stacked');
legend(nam)
title('Industry by wage')
xlabel('wage distribution')


exportgraphics(fig_char, fullfile(out_dir,'char.pdf'), 'ContentType','vector');
exportgraphics(fig_industry, fullfile(out_dir,'industry_by_wage_quintile_cepr_av_app.pdf'), 'ContentType','vector');

