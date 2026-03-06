function [] = plotConfidenceBandsBlue(x,percentiles,colour)
%Plot Confidence Bands as fan charts from percentiles
%   Note: input must be odd number of percentiles where middle one is the
%   median
hold on
numberOfBands = (size(percentiles,2)-1)/2;

if isempty(x);
    x = (1:size(percentiles,1))';
end

for i = 1 : numberOfBands
    
    lowerbound = percentiles(:,numberOfBands+1) - percentiles(:,i);
    upperbound = percentiles(:,end-i+1) - percentiles(:,numberOfBands+1);
    %     boundedline(x, percentiles(:,numberOfBands+1), [lowerbound, upperbound],colour, 'alpha');
    
    if strcmp(colour,'b')
        switch i
            case 1
                
                colourBand = [1 1 1];
            case 2
                colourBand = [0 0 0];

%                 colourBand = [0.5142 0.8704 1];
            case 3
                colourBand = [0 0 0];
                
%                 colourBand = [0.2623 0.8033 1];
        end
        boundedlineBlue(x, percentiles(:,numberOfBands+1), [lowerbound, upperbound],colourBand,'alpha');
        
    elseif strcmp(colour,'r')
        %
        switch i
            case 1
                colourBand = [1 0.8 0.8];
            case 2
                colourBand = [1 0.65 0.65];
            case 3
                colourBand = [1 0.4 0.4];
        end
        
%         boundedlineBlue(x, percentiles(:,numberOfBands+1), [lowerbound, upperbound],colour,colourBand,'alpha');
        boundedlineBlue(x, percentiles(:,numberOfBands+1), [lowerbound, upperbound],colour,colourBand,'alpha');
    elseif strcmp(colour,'m')
        
        switch i
            case 1
                colourBand = [0.9 0.8 0.9];
            case 2
                colourBand = [0.8 0.5 0.8];
            case 3
                colourBand = [0.8 0.3 0.8];
        end
        
        boundedlineBlue(x, percentiles(:,numberOfBands+1), [lowerbound, upperbound],colour,colourBand,'alpha');
        
    elseif strcmp(colour,'g')
        
        switch i
            case 1
                colourBand = [0.7 0.9 0.7];
            case 2
                colourBand = [0.6 0.8 0.6];
            case 3
                colourBand = [0.6 0.8 0.6];
        end
        
        boundedlineBlue(x, percentiles(:,numberOfBands+1), [lowerbound, upperbound],colour,colourBand,'alpha');
        
    elseif strcmp(colour,'k')
        
        switch i
            case 1
                colourBand = [0.95 0.95 0.95];                
                colourBand = '#ededed';                
                %colorBand = '#adadad';
            case 2
                colourBand = [0.6 0.6 0.6];
            case 3
                colourBand = [0.4 0.4 0.4];
        end
        
        boundedlineBlue(x, percentiles(:,numberOfBands+1), [lowerbound, upperbound],colour,colourBand,'alpha');
        
    else
        boundedline(x, percentiles(:,numberOfBands+1), [lowerbound, upperbound],colour,'alpha');
    end
    hold on
end


hold off
end


