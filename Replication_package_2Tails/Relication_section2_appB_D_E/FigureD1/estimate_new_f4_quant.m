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
fname=fullfile(this_dir,'..','data','Raw_data','DataEstimation','data_QUANT1_MPI.mat');
load(fname);
data_table=data_table(TR,:);
Z_table=Z_table(TR,:);
M_table=M_table(TR,:);
out.data1=data_table.Variables;
out.Z=Z_table.Variables;
out.m_t=M_table.Variables;
out.names=names_big;



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
spec.detrend_Z=0;
spec.over_write=[129 130 ];
spec.over_write_val=[0 0 ];



[irfsavem,irfsavec,irfsavecc,irfsave]=runfavarx_f_new(out,1,spec);

save('results','irfsavem','irfsavec','irfsavecc','out','irfsave','spec')

names=out.names;
figure(4)
id=[1 129 130 131 142 23 73 99 47 116 122 121 142 143 151 153 155 157 196];

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(3,8,j)
plotx3(HH',irfsavem(1:3,:,id(j))');
title(names{id(j)})
end




figure(5)
id=151:2:188;

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(4,5,j)
plotx3(HH',irfsavem(1:3,:,id(j))');
title(names{id(j)})
end

figure(6)
plotx99(1:19,squeeze(irfsavem(1:5,12,151:2:188))')
hold on
plotx99(1:19,squeeze(irfsavem(1:5,36,151:2:188))','b','b')



figure(7)
id=150:2:187;

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(4,5,j)
plotx3(HH',irfsavem(1:3,:,id(j))');
title(names{id(j)})
end


figure(8)
plot(squeeze(irfsavem(1:5,12,150:2:187))')



figure(40)
id=[129 130 131 24 77 82 85 64 48 99 77 79];

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(3,8,j)
plotx3(HH',irfsavem(1:5,:,id(j))');
title(names{id(j)})
end



figure(77)
id=[157 189:2:195];

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(4,5,j)
plotx3(HH',irfsavem(1:3,:,id(j))');
title(names{id(j)})
end
