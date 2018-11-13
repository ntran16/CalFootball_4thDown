A = importdata('3rdDown1.csv');
data= A.data;
data_new = [];
for h = linspace(1,91,10)
    tot= data(h+1,3)+data(h,3);
    data(h+1,2)= data(h+1,2)*data(h+1,3)/tot + data(h,2)*data(h,3)/tot;
    data(h+1,3)=tot;
end
data(find(data(:,1)==0),:)=[];
for j = 1:10
    k=1+(j-1)*9;
    data_new=[data_new data((k:8+k),1:3)];
end
data_final = data_new;
b= [1 2 3 4 5 6 7 8 9];
for g =linspace(1,28,10)
    p = polyfit(data_new(:,g),data_new(:,g+1),3);
    a = polyval(p,b);
    data_final(:,g+1) = a;
end
%% 
B = importdata('4thDown1.csv');
data4= B.data;
data_new4 = [];
for h = linspace(1,91,10)
    tot4= data4(h+1,3)+data4(h,3);
    data4(h+1,2)= data4(h+1,2)*data4(h+1,3)/tot4 + data4(h,2)*data4(h,3)/tot4;
    data4(h+1,3)=tot4;
end
data4(find(data4(:,1)==0),:)=[];
for j = 1:10
    k=1+(j-1)*9;
    data_new4=[data_new4 data4((k:8+k),1:3)];
end
data_final4 = data_new4;
b= [1 2 3 4 5 6 7 8 9];
for g =linspace(1,28,10)
    p = polyfit(data_new4(:,g),data_new4(:,g+1),3);
    a = polyval(p,b);
    data_final4(:,g+1) = a;
end

%% 
data_result = data_final4;
for f = linspace(1,28,10)
    data_result(:,f+1) = data_final4(:,f+1)*0.6 +  data_final(:,f+1)*0.4;
end
data_result(:,linspace(1,28,10)+2)=[]
csvwrite('conv_pct_4060.csv',data_result)