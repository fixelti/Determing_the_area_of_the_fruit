% скрипт для выделения границ объектов

im_disk = imread('oranges.jpg');
figure(1)
imshow(im_disk);

im_disk_gray = rgb2gray(im_disk);
figure(2)
imshow(im_disk_gray);
bound = graythresh(im_disk_gray);

bound = 0.72;
im_disk_bw = im2bw(im_disk_gray, bound);
figure(3)
imshow(im_disk_bw);

% SE=strel('disk', 10);
% im_disk_bw2=imbothat(im_disk_bw, SE);
% figure(4)
% imshow(im_disk_bw);

% im_disk_bound=bwperim(im_disk_bw, 4);
% figure(5)
% imshow(im_disk_bound);

figure(6)
BWd=bwselect(im_disk_bw, 8);
BWd1=bwmorph(BWd,'majority',8);
BWd2=bwfill(BWd1, 8)
figure(7)
imshow(BWd2);
