
set INPUT=C:\data\povarenok.ru\1_1000\docs-000

type        %INPUT%.txt | python map_is2.py   | sort > .\data\mapped.txt
type  .\data\mapped.txt | python red_is2.py f | sort > .\data\output.txt

rem    type %INPUT%.txt | python map_is2.py   | sort | python red_is2.py s | sort > .\data\output_all.txt

type  C:\data\povarenok.ru\1_1000\docs-000.txt | python map_is2.py   | sort > .\data\mapped.txt

type  .\data\mapped.txt | python red_is2.py s | sort > .\data\reduced.txt
