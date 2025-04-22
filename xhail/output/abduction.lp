%ORIGINAL BACKGROUND%


%TEMPORARY NEGATIONS%

%EXAMPLES%

%ABDUCIBLES%
%#modeh p(a,$int,+int,-int,-int)
0 { abduced_p(a,V1,V2,V3,V4):int(V1), int(V2), int(V3), int(V4) } 1000000.
#minimize{1@1,V1, V2, V3, V4: abduced_p(a,V1,V2,V3,V4),int(V1), int(V2), int(V3), int(V4)}.
p(a,V1,V2,V3,V4) :- abduced_p(a,V1,V2,V3,V4),int(V1), int(V2), int(V3), int(V4).

