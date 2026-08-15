@echo off
rem Ciclo de compilacion del paper. Cuatro pasadas de pdflatex, no tres:
rem cuando la paginacion cambia (una figura que entra o sale, una tabla
rem que crece), tres no bastan y el PDF sale SIN BIBLIOGRAFIA, con todas
rem las citas en interrogante y sin un solo error en pantalla. Ha pasado
rem tres veces el 2026-08-14.
rem
rem Al terminar conviene pasar el verificador, que revisa el .log:
rem   venv\Scripts\python.exe -X utf8 paper\verify_numbers.py
cd /d %~dp0
pdflatex -interaction=nonstopmode main.tex > nul
bibtex main > nul
pdflatex -interaction=nonstopmode main.tex > nul
pdflatex -interaction=nonstopmode main.tex > nul
pdflatex -interaction=nonstopmode main.tex > nul
findstr /C:"undefined" main.log > nul && echo AVISO: quedan referencias sin resolver
findstr /C:"Overfull \hbox" main.log > nul && echo AVISO: hay desbordes de caja
rem El Online Resource 1 se compila con el mismo ciclo
pdflatex -interaction=nonstopmode supplementary.tex > nul
bibtex supplementary > nul
pdflatex -interaction=nonstopmode supplementary.tex > nul
pdflatex -interaction=nonstopmode supplementary.tex > nul
pdflatex -interaction=nonstopmode supplementary.tex > nul
findstr /C:"undefined" supplementary.log > nul && echo AVISO: referencias sin resolver en el suplementario
echo Compilado.
