% run_empirical_replication
% One-click empirical replication runner for Section 2 and Appendix D/E.
%
% This script:
% - Uses packaged datasets already stored in data/Raw_data/.
% - Writes all PDFs to Replication_files_section2_appB_D_E/Output/.
% - Covers Figures 1-5, D1, D2, D4, D7, D8, E1.
% - Excludes FigureA1_A2 and FigureA3 (external CEPR CSV prerequisites).
%
% At launch, you are asked to choose:
% 1) Full run: estimation + plots
% 2) Plot-only run: plots only, assuming estimation files already exist
%
% Optional non-interactive usage:
% - mode = 'full'; run('run_empirical_replication.m');
% - mode = 'plot'; run('run_empirical_replication.m');
% - mode = 'fast'; run('run_empirical_replication.m');   % alias for plot

close all

this_dir = fileparts(mfilename('fullpath'));
orig_dir = pwd;
cleanup_main = onCleanup(@() cd(orig_dir)); 
cd(this_dir);

out_dir = fullfile(this_dir,'Output');
if exist(out_dir,'dir') ~= 7
    mkdir(out_dir);
end

if exist('mode','var') && ~isempty(mode)
    mode = lower(strtrim(char(mode)));
else
    fprintf('\nSelect run mode:\n');
    fprintf('  1) Full replication (estimations + plots)\n');
    fprintf('  2) Plot only (use existing estimation files)\n');
    choice = strtrim(input('Enter 1 or 2 [1]: ', 's'));
    if isempty(choice)
        choice = '1';
    end
    if strcmp(choice,'1')
        mode = 'full';
    elseif strcmp(choice,'2')
        mode = 'plot';
    else
        error('run_empirical_replication:BadChoice', ...
            'Invalid choice "%s". Enter 1 or 2.', choice);
    end
end

if strcmp(mode,'fast')
    mode = 'plot';
end
if ~ismember(mode, {'full','plot'})
    error('run_empirical_replication:BadMode', ...
        'Unsupported mode "%s". Use "full", "plot", or "fast".', mode);
end

fprintf('\n[%s] Starting empirical replication (%s mode)\n', ...
    local_timestamp(), upper(mode));
fprintf('[%s] Output folder: %s\n\n', local_timestamp(), out_dir);

jobs = {
    'Figure1',  'estimate_new_f4_quant.m',      'plot_figure1.m',  {'results.mat','priors_1.mat'},                                      'figure1.pdf';
    'Figure2',  '',                              'plot_figure2.m',  {fullfile('..','Figure1','results.mat'),fullfile('..','Figure1','priors_1.mat')}, 'figure2_6.pdf';
    'Figure3',  'estimate_new_f4_quant.m',      'plot_figure3.m',  {'results.mat','priors_1.mat'},                                      'figure3.pdf';
    'Figure4',  'estimate_new_f4_quant_FT.m',   'plot_figure4.m',  {'results.mat','priors_1.mat'},                                      'figure_ft_2.pdf';
    'Figure5',  'estimate_new_f4GR.m',          'plot_Figure5.m',  {'results.mat','priors_1.mat'},                                      'figure4_6.pdf';
    'FigureD1', 'estimate_new_f4_quant.m',      'plot_figureD1.m', {'results.mat','priors_1.mat'},                                      'figure_mpi.pdf';
    'FigureD2', 'estimate_new_f4_quant_sign.m', 'plot_figureD2.m', {'results.mat'},                                                     'figure_sign.pdf';
    'FigureD4', 'estimate_new_f4_quant.m',      'plot_FigureD4.m', {'results.mat','priors_1.mat'},                                      'hours_ind.pdf';
    'FigureD7', 'estimate_new_f4_quant.m',      'plot_figureD7.m', {'results.mat','priors_1.mat'},                                      'hours_educ1.pdf';
    'FigureD8', '',                              'plot_figureD8.m', {fullfile('..','Figure1','results.mat'),fullfile('..','Figure1','priors_1.mat')}, 'figure_wages.pdf';
    'FigureE1', 'estimate_new_f4_quant.m',      'plot_FigureE1.m', {'results.mat','priors_1.mat'},                                      'figure_panel3M.pdf';
};

failed_jobs = {};
failed_msgs = {};

for i = 1:size(jobs,1)
    job_name = jobs{i,1};
    estimate_script = jobs{i,2};
    plot_script = jobs{i,3};
    fast_required = jobs{i,4};
    output_pdf = jobs{i,5};

    t_job = tic;
    job_dir = fullfile(this_dir, job_name);
    fprintf('[%s] START %s\n', local_timestamp(), job_name);

    cd(job_dir);
    try
        if strcmp(mode,'full')
            if ~isempty(estimate_script)
                fprintf('[%s]   estimate: %s\n', local_timestamp(), estimate_script);
                local_run_script(estimate_script);
            end
        else
            missing = {};
            for k = 1:numel(fast_required)
                if exist(fast_required{k},'file') ~= 2
                    missing{end+1} = fullfile(job_dir, fast_required{k}); 
                end
            end
            if ~isempty(missing)
                error('run_empirical_replication:MissingPrereqs', ...
                    'Plot-only mode missing files for %s:\n - %s', ...
                    job_name, strjoin(missing, sprintf('\n - ')));
            end
        end

        fprintf('[%s]   plot: %s\n', local_timestamp(), plot_script);
        local_run_script(plot_script);

        cd(this_dir);
        expected_pdf = fullfile(out_dir, output_pdf);
        if exist(expected_pdf,'file') ~= 2
            error('run_empirical_replication:MissingOutput', ...
                'Expected output file not found: %s', expected_pdf);
        end

        fprintf('[%s] SUCCESS %s (%.1fs)\n\n', ...
            local_timestamp(), job_name, toc(t_job));
    catch ME
        cd(this_dir);
        fprintf(2,'[%s] FAIL %s (%.1fs)\n', ...
            local_timestamp(), job_name, toc(t_job));
        fprintf(2,'[%s]   %s\n\n', local_timestamp(), ME.message);
        failed_jobs{end+1} = job_name; 
        failed_msgs{end+1} = ME.message; 
    end
end

fprintf('============================================================\n');
fprintf('[%s] Replication runner summary\n', local_timestamp());
fprintf('Mode: %s\n', mode);
fprintf('Total jobs: %d\n', size(jobs,1));
fprintf('Succeeded: %d\n', size(jobs,1) - numel(failed_jobs));
fprintf('Failed: %d\n', numel(failed_jobs));

if isempty(failed_jobs)
    fprintf('[%s] All jobs completed successfully.\n', local_timestamp());
else
    fprintf('\nFailed jobs:\n');
    for i = 1:numel(failed_jobs)
        fprintf(' - %s: %s\n', failed_jobs{i}, failed_msgs{i});
    end
    error('run_empirical_replication:JobFailures', ...
        '%d job(s) failed. See summary above.', numel(failed_jobs));
end

function local_run_script(script_name)
    run(script_name);
end

function out = local_timestamp()
    out = char(datetime('now','Format','yyyy-MM-dd HH:mm:ss'));
end
