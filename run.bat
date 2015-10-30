
set INPUT=C:\Users\MainUser\Downloads\Cloud.mail\povarenok.ru\1_1000\docs-000

type        %INPUT%.txt | python map_is2.py | sort > .\data\mapped.txt
type  .\data\mapped.txt | python red_is2.py | sort > .\data\output.txt

rem    type %INPUT%.txt | python map_is2.py | sort | python red_is2.py | sort > .\data\output_all.txt
