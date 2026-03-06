clear
close all

this_dir = fileparts(mfilename('fullpath'));
addpath(fullfile(this_dir,'..','functions_new'), '-begin');
addpath(genpath(fullfile(this_dir,'..','data','functions')), '-end');

load(fullfile(this_dir,'priors_1.mat'))
load(fullfile(this_dir,'results.mat'))

out_dir = fullfile(this_dir,'..','Output');
if ~exist(out_dir,'dir')
    mkdir(out_dir);
end

tmp=5:5:95;
for j=1:19
    namesz{j}=strcat('$\le',num2str(tmp(j)),'$');
end

figure(40)

subplot(2,5,[1:5])
h1=plotx99(1:19,squeeze(irfsavem(1:5,6,151:2:188))')
hold on
h2=plotx99(1:19,squeeze(irfsavem(1:5,24,151:2:188))','b','b')
title('Response of Hours growth across the Distribution','interpreter','latex')
legend([h1(1) h2(1)],{'6 mths','2 years'})
ylabel('percent','interpreter','latex')

ax=gca
ax.XTick=1:19;
ax.XTickLabel=namesz;
ax.TickLabelInterpreter='latex';
%


subplot(2,5,[6:10])
h1=plotx99(1:19,squeeze(irfsavem(1:5,6,188:206))')
hold on
h2=plotx99(1:19,squeeze(irfsavem(1:5,24,188:206))','b','b')
title('Response of outflow from employment','interpreter','latex')
ylabel('percent','interpreter','latex')

ax=gca
ax.XTick=1:19;
ax.XTickLabel=namesz;
ax.TickLabelInterpreter='latex';

export_with_margin(gcf, fullfile(out_dir,'figure4_6.pdf'));

