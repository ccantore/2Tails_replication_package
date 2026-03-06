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

for j=1:5
    namesx{j}=strcat('$P_{',num2str(j),'}$');
end
tmp=5:5:95;
for j=1:19
    namesz{j}=strcat('$\le',num2str(tmp(j)),'$');
end

namez{1}='Less than high school';
namez{2}='High School';
namez{3}='Some college';
namez{4}='College';
namez{5}='Advanced';



fig = figure(40);

jj=151;
jjj=2;
for j=1:5
    subplot(2,3,j)
plotx99(1:19,squeeze(irfsavem(1:5,6,jj:2:jj+37))')
ylabel('percent','interpreter','latex')

title(namez{j},'interpreter','latex')
ax=gca
ax.XTick=1:19;
ax.XTickLabel=namesz;
ax.TickLabelInterpreter='latex';
jj=jj+38;
jjj=jjj+2;
end


% x0=50;
% y0=1000;
% width=1000;
% height=1000;
% set(gcf,'position',[x0,y0,width,height])
% 
% print('.\upload\hours_educ1','-dpdf','-bestfit')

export_with_margin(fig, fullfile(out_dir,'hours_educ1.pdf'));
