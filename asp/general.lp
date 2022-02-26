%Group members: Daniel Quintillán Quintillán, Sergio García Cascón.
%Emails: daniel.quintillan@udc.es, sergio.gcascon@udc.es
%To be specified in the instance file
row(1..N):- rows(N).
column(1..M):- columns(M).

%Hour adjacency and clock hours do not change depending on the characteristics of the instance
clock_hour(1..12).

consecutive(12,1).
consecutive(1,2).
consecutive(H,I):-consecutive(I,H).
consecutive(H+1,I+1) :- I<12, H<12, consecutive(H,I).

%Every cell must have a unique value
1 {cell_value(X,Y,H) : clock_hour(H) } 1 :- row(X), column(Y).

%For every hour, it must not be repeated a number of times different from N*M/12
:- {cell_value(X,Y,H)} != (N*M)/12, rows(N), columns(M), H=1..12.

%A situation in which two neighbouring cells have not been proven to have a wall between them
% and there is also no evidence of those two cells having consecutive values is not valid.
%Which means that if we don't have proof of the former, the latter is inferred.
:- cell_value(X,Y,H), cell_value(X,Y+1,I), not right_wall(X,Y), not consecutive(H,I).
:- cell_value(X,Y,H), cell_value(X+1,Y,I), not down_wall(X,Y), not consecutive(H,I).

#show cell_value/3.