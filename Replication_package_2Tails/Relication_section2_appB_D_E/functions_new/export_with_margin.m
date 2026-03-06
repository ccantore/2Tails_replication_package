function export_with_margin(fig_handle, file_name)
% Export a figure with slightly larger white margins around axes.
%
% Inputs:
%   fig_handle : figure handle (or [] to use gcf)
%   file_name  : output file path (PDF/PNG/etc. supported by exportgraphics)

if nargin < 1 || isempty(fig_handle)
    fig_handle = gcf;
end
if nargin < 2 || isempty(file_name)
    error('export_with_margin:MissingOutputPath', ...
        'An output file path must be provided.');
end

set(fig_handle, 'Color', 'w');

% For tiled layouts, loosen tile spacing/padding to increase edge whitespace.
tile_layouts = findall(fig_handle, '-isa', 'matlab.graphics.layout.TiledChartLayout');
for i = 1:numel(tile_layouts)
    tile_layouts(i).TileSpacing = 'loose';
    tile_layouts(i).Padding = 'loose';
end

% For classic axes/subplots, shrink each axes position slightly.
pad_x = 0.01;
pad_y = 0.015;
axes_handles = findall(fig_handle, 'Type', 'axes');
for i = 1:numel(axes_handles)
    try
        pos = axes_handles(i).Position;
        axes_handles(i).Position = [ ...
            pos(1) + pad_x, ...
            pos(2) + pad_y, ...
            max(0.01, pos(3) - 2*pad_x), ...
            max(0.01, pos(4) - 2*pad_y)];
    catch
        % Some layout-managed axes do not allow manual Position changes.
    end
end

exportgraphics(fig_handle, file_name, 'ContentType', 'vector', 'BackgroundColor', 'white');
end
