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


fig = figure(40);
id=[1 129 130  24 132 131 99 73];
namesx{1}='1yr Rate';
namesx{2}='Industrial Production';
namesx{3}='CPI';
namesx{4}='Unemployment rate';
namesx{5}='Average Weekly hours';
namesx{6}='Excess Bond Premium';
namesx{7}='Dollar Pound Exchange rate';
namesx{8}='SP500';

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(2,4,j)
plotx99(HH',irfsavem(1:5,:,id(j))','r','r');
title(namesx{j},'interpreter','latex');
if j>4
xlabel('months','interpreter','latex')
end
if j==1 || j==5
ylabel('percent','interpreter','latex')
end
axis tight
end

% x0=50;
% y0=1000;
% width=1000;
% height=1000;
% set(gcf,'position',[x0,y0,width,height])
% 
% %print('.\upload\figure1','-dpdf','-bestfit')
% savefigure_pdf('.\upload\figure1')

export_with_margin(fig, fullfile(out_dir,'figure1.pdf'));
