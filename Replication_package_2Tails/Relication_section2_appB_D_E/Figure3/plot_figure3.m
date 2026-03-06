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



HH=0:size(irfsavem,2)-1;


% figure(1)
% temp1=irfsave(:,:,197)-irfsave(:,:,198);
% temp2=prctile(temp1,[50,16,84,5,95]);
% plotx3(HH',temp2(1:3,:)');
% title('Response of aggregate hours-response of the counterfactual')
namesx{1}='Hours $P_{1}$';
namesx{2}='Aggregate hours';
namesx{3}='Aggregate hours excluding $P_{1}$';

figure(2)
id=[157 197 198];

HH=0:size(irfsavem,2)-1;

for j=1:length(id)
    subplot(1,3,j)
plotx99(HH',irfsavem(1:5,:,id(j))','r','r');
title(namesx{j},'interpreter','latex','fontsize',14);

xlabel('months','interpreter','latex','fontsize',14);
if j==1
ylabel('percent','interpreter','latex','fontsize',14);
end
end


% x0=50;
% y0=1000;
% width=1000;
% height=1000;
% set(gcf,'position',[x0,y0,width,height])
% 
% %print('.\upload\figure3','-dpdf','-bestfit')
% savefigure_pdf('.\upload\figure3')

export_with_margin(gcf, fullfile(out_dir,'figure3.pdf'));
