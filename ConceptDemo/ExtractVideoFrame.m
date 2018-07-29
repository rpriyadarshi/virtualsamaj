function ExtractVideoFrame(filename)
%ExtractVideoFrame Summary of this function goes here
%   Detailed explanation goes here
    frame = 1;
    vidObj = VideoReader(filename);
    imgfile = strcat(filename, num2str(frame), '.png');
    b = read(vidObj, frame);
    imshow(b);
    imwrite(b, imgfile);
end

