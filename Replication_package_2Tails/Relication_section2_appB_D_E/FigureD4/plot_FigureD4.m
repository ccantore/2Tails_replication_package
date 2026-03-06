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

namez{1}='Agriculture, forestry, fishing, and hunting';
namez{2}='Mining';
namez{3}='Construction';
namez{4}='Manufacturing';
namez{5}='Wholesale and retail trade';
namez{6}='Transportation and utilities';
namez{7}='Information';
namez{8}='Financial activities';
namez{9}='Professional and business services';
namez{10}='Educational and health services';
namez{11}='Leisure and hospitality';
namez{12}='Other services';
namez{13}='Public administration';


fig = figure(40);
tl = tiledlayout(fig,5,3,'TileSpacing','loose','Padding','loose');

jj=151;
for j=1:13
    nexttile(tl,j)
    plotx99(1:19,squeeze(irfsavem(1:5,6,jj:2:jj+37))')
    ylabel('percent','interpreter','latex')

    title(namez{j},'interpreter','latex')
    ax=gca;
    ax.XTick=1:19;
    ax.XTickLabel=namesz;
    ax.TickLabelInterpreter='latex';
    jj=jj+38;
end

% 
% x0=50;
% y0=1000;
% width=1000;
% height=1000;
% set(gcf,'position',[x0,y0,width,height])
% 
% print('.\upload\hours_ind','-dpdf','-bestfit')
% %savefigure_pdf('.\upload\hours_ind')

export_with_margin(fig, fullfile(out_dir,'hours_ind.pdf'));
