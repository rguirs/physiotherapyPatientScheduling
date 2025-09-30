# physiotherapyPatientScheduling
A simple program to address a problem from a doctoral student of physiotherapy who needs to schedule sessions (considering several constraints) for a research


The greedy algorithm works and can handle English and Portugues as input/output.
Some characteristics of the problem are "hardcoded". It is expected that soon some of them are going to be set as parameters
I hope to implement a mathematical model later.

If you are researching a similar problem, feel free to send me a e-mail so we can share different formulations and methods

Thanks :)


About the example files:

Considering a scenario in which no patient is scheduled, we have a file eg.schedule.N.xlsx
After running the algorith, it is outputed a eg.schedule.N.ot.xlsx (the .ot means the file is an optimized output)
Then we have the rescheduling problem. In order to keep both the original output and the sheet with the blanck sessions
(that shows what sessions must be rescheduled), it was created a new file (based on the previous .ot) called eg.schedule.N.rs.xlsx.
Finally, the output of the rescheudling problem is provided in eg.schedule.N.rs.ot.xlsx (.ot because it is an output file
and .rs because it is from a rescheduling problem)


# Article (in Portuguese only)
Link: (ainda não publicado)
Como citar:

Errata:

1) Na seção 3.1, em conjuntos em variáveis de decisão, temos q, o qual na verdade é definido por:
   "q → Número de dias que durará o estudo. q ∈ R"
   "q" também poderia ter o domínio Z+

2) Na seção 3.2, em restrições, HC10.b deveria ser dada por:
   "x^{it}_{ds} = 0 ∀ i ∈ I, t ∈ T, d ∈ D, s ∈ S | d ≤ dr, H^{it}_{ds} = 0"
  Com essa mudança, assegura-se que não sejam marcadas consultas nos dias não permitidos. No código, essa restrição já era assegurada, porém, por motivos de processamento, alterando os conjuntos N^i_{ds} e N^p_{ds}. Assim, mesmo com a definição "livre" de HC10.b anterior, os resultados são equivalentes
