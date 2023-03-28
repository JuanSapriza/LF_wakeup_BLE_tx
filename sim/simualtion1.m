close all

# Get the values in 2 columns
file_name = 'values1.txt'

[A,B] = textread( file_name, '%s %s' );
dist_m = str2num(cell2mat(A));
B_T = str2num(cell2mat(B));

min_x_m = 0.01;
min_dist_idx = 100;

x = dist_m(min_dist_idx:end);
y = B_T(min_dist_idx:end);

lin = y .* (x.^3);

[p, s] = polyfit(x, lin, 1);



#{
[p, s] = polyfit(1 ./ x, y, 3);
yhat = polyval(p, 1 ./ (1:30));
figure;
hold on;
plot(y, 'o');
plot(yhat);
axis([0 1.5 4e-9 2e-4])

#plot(dist_cm(min_dist_idx:end),B_T(min_dist_idx:end))

}#