clear
close all

this_dir = fileparts(mfilename('fullpath'));
orig_dir = pwd;
cleanup_obj = onCleanup(@() cd(orig_dir));
cd(this_dir);

addpath(fullfile(this_dir,'..','functions_new'), '-begin');
addpath(genpath(fullfile(this_dir,'..','data','functions')), '-end');

rng(1,'twister');

%estimation sample
begdate='01-Jan-1985';
enddate='01-Dec-2019';
TR=timerange(begdate,enddate);
fname=fullfile(this_dir,'..','data','Raw_data','DataEstimation','data_QUANT1.mat');
load(fname);
data_table=data_table(TR,:);
Z_table=Z_table(TR,:);
M_table=M_table(TR,:);
out.data1=data_table.Variables;
out.Z=Z_table.Variables;
out.m_t=M_table.Variables;
out.names=names_big;



%%%%%%%%%%%%%



spec.Nfact=9;
spec.REPS=21000;  %replications
spec.BURN=1000; %burn-in
spec.SKIP=2;  %iterations skipped
spec.Horz=60;
spec.max_L=12;
spec.fix_L=1;
spec.LAMDAP=0.1;
spec.max_fact=20;
spec.CHECK=0;
spec.detrend_all=0;
spec.detrend_Z=10;
spec.over_write=[129 130 150:186];
spec.over_write_val=0;

%sign restrictions
NN=cols(out.data1)+cols(out.Z);
N=cols(out.Z)+spec.Nfact;
CPI_=130;
GS1_=1;
IP_=129;
ebp_=131;
un_=24;
ffr_=77;

pattern=zeros(N,NN);
pattern(1,CPI_)=-1; %CPI
pattern(1,GS1_)=1;%GS1
pattern(1,IP_)=-1;%
pattern(1,ebp_)=1;%ebp
pattern(1,un_)=1;%un
pattern(1,ffr_)=1;%un



tmat=zeros(N,NN);
tmat(1,CPI_)=5; %CPI %5
tmat(1,GS1_)=5;%GS1
tmat(1,IP_)=5;%M2
tmat(1,ebp_)=5;%PCE def
tmat(1,un_)=5;%PCE def
tmat(1,ffr_)=5;%PCE def


tmat0=zeros(N,NN);


out.pattern=pattern;
out.tmat0=tmat0;
out.tmat=tmat;

[irfsavem,irfsavec,irfsavecc,irfsave]=runfavarx_f_sign_new(out,1,spec);

save('results','irfsavem','irfsavec','irfsavecc','out','irfsave')

names=out.names;
figure(4)
id=[1 129 130 131 142 24 73 99 47 116 122 121 142 143 151 153 155 157];

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(3,8,j)
plotx3(HH',irfsavem(1:3,:,id(j))');
title(names{id(j)})
end




