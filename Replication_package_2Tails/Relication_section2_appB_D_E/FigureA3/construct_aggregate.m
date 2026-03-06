clear
close all

this_dir = fileparts(mfilename('fullpath'));
orig_dir = pwd;
cleanup_obj = onCleanup(@() cd(orig_dir));
cd(this_dir);

addpath(fullfile(this_dir,'..','functions_new'), '-begin');
addpath(genpath(fullfile(this_dir,'..','data','functions')), '-end');

out_dir = fullfile(this_dir,'..','Output');
if ~exist(out_dir,'dir')
    mkdir(out_dir);
end

cepr_dir = fullfile(this_dir,'..','data','Raw_data','CPS','ELABORATED DATA');
raw_dir = fullfile(this_dir,'..','data','Raw_data','raw');
PROB=30;
dperc=[1 99];
DATA=[];
AG=[];
WW=[];

for yy=1979:2019
    yy
fname=fullfile(cepr_dir,sprintf('data_%d.csv',yy));
tmpx=importdata(fname);


%month rw hourslw orgwgt fnlwgt empl unem educ pt ptecon

%Keep employed
dummy=tmpx(:,6)==1;
tmpx=tmpx(dummy,:);

% % Drop PT
% dummy=tmpx(:,9)==1;
% tmpx(dummy,:)=[];

%
wage0=tmpx(:,2);
weight0=tmpx(:,4);
[~,dummy]=cutoff(wage0,dperc,weight0);
tmpx(dummy,:)=[]; %drop all datapoints in upper and lower 1 % of wage 



%month rw hourslw orgwgt fnlwgt empl unem educ pt ptecon
month=tmpx(:,1);
hours=tmpx(:,3); %all


wage=tmpx(:,2);
weight=tmpx(:,4);
weighth=tmpx(:,5);
data1=[];%zeros(rows(tmpx),cols(tmpx));

mth=[];
DATA1=[];
DATA2=[];
AG1=[];
AG1x=[];
AG2x=[];
for j=1:1:12
    
    sel=month==j;
    wage_m=wage(sel,:);
    hours_m=hours(sel,:); 
    weight_m=weight(sel,:);
    weight_hm=weighth(sel,:);

    


    [out,out1,outx,dummy]=...
         getpercw_2(wage_m,PROB,weight_m,...
         [hours_m ],weight_hm,0);
        tmp=[out outx];
        
   agh=wmean1(hours_m,weight_hm);
      agw=wmean1(wage_m,weight_m);

        
    %weights
     [outw,out1w,outxw,dummyw]=...
         getpercw_2_sum(wage_m,PROB,weight_m,...
        [hours_m ],weight_hm,0);
     
    [outz,~,outxz,~]=...
         getpercw_2_sum(wage_m,[1 99],weight_m,...
         hours_m,weight_hm,0);
     
    rat=[outw./outz(2) outxw./outxz(2)];
    
        
 
        DATA1=[DATA1; vecr(tmp)'];
        DATA2=[DATA2;vecr(rat)'];
       AG=[AG;[agh agw]];
    


end


DATA=[DATA;DATA1];
WW=[WW;DATA2];
AG1=[AG1;AG];
end

 

t1 = datetime(1979,1,1,8,0,0);
t2 = datetime(2019,12,1,8,0,0);
t = t1:calmonths(1):t2;
date=datenum(t);
 %outliers
NN=cols(DATA);
DATA_m=getSAMx13(DATA,date);

 

namesx{1}='wages';
namesx{2}='actual_hours_main';


namespp{1}=strcat('<',num2str(PROB(1)));
jj=2;
for j=1:length(PROB)-1
namespp{jj}=strcat('>',num2str(PROB(j)),' and <=',...
    num2str(PROB(j+1)));
jj=jj+1;
end
namespp{jj}=strcat('>',num2str(PROB(end)));

    
jj=1;
for j=1:length(namespp)
    for i=1:length(namesx)
    namesp{jj}=strcat('$',namesx{i},'_{',namespp{j},'}$');
    jj=jj+1;
    end
end

AG=getSAMx13(AG,date);
tmp1=readtable(fullfile(raw_dir,'AWHNONAG.xls'),'range','B12:B503');

AWHNONAG=tmp1.Var1;%(tmp.Var1+tmp1.Var1)/2;





fig = figure(2);
subplot(1,1,1)
plot(t,[movav(filloutliers(log(AG(:,1))-lagmatrix(log(AG(:,1)),12),'linear'),6) ...
    movav(log(AWHNONAG)-lagmatrix(log(AWHNONAG),12),0)])
xlim([t(73) t(end)])
legend('Constructed from CPS','AWHNONAG')
title('Annual Growth of hours worked')


exportgraphics(fig, fullfile(out_dir,'ag_hours.pdf'), 'ContentType','vector');

cleanup_patterns = {'*.mdl','*.d11','*.out','*.err','*.log','*.spc'};
for i = 1:numel(cleanup_patterns)
    ff = dir(fullfile(this_dir,cleanup_patterns{i}));
    for j = 1:numel(ff)
        delete(fullfile(this_dir,ff(j).name));
    end
end
WW=mean(WW);
