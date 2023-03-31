function [x,y]= Rulkovcoupled ()

    mu=0.01;
    alfa=4.3;
    sigmai=0.1;
    n=4000;
    w=0.5;
    
    cell=2;
    
    xi=ones(cell);
    yi=ones(cell);
    
    X=zeros(n,cell);
    Y=zeros(n,cell);
    
    for N=1:n
    for k=1:cell
    for j=1:cell-1
    sigma=sigmai*w*(xi(k)-xi(j));
    
    % chaotic Rulkov eq.
    
    X(N,k)=(alfa/(1+(xi(k)*xi(k))))+yi(k);
    Y(N,k)=yi(k)-(mu*(xi(k)+1))+mu*sigma;
    
    sigmai=sigma;
    xi(k)=X(N,k);
    yi(k)=Y(N,k);
    
    end
    end
    end
    
    F1=figure;
    
    plot(X(:,1),'r');
    hold on;
    plot(X(:,2),'b');
    hold off;
    
    F2=figure;
    plot(X(:,1),Y(:,1),'r');
    hold on;
    plot(X(:,2),Y(:,2),'b');
    hold off;
    
    end
    
    