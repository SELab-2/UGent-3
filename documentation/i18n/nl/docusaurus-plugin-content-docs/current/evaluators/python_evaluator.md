# Python evaluator
## Algemeen gebruik
Deze evaluator is verantwoordelijk voor het uitvoeren en testen van de Python-code van een student.

## Structuur
Bij het indienen van het project kan een leraar vereisten toevoegen via het bestand `req-manifest.txt`. Op deze manier zijn alleen de pakketten in het vereistenbestand bruikbaar op de evaluator.

Wanneer er geen manifest aanwezig is, kunnen studenten hun eigen paketten installeren met een `requirements.txt` en een `dev-requirements.txt`.
Of de leraar kan een `requirements.txt` toevoegen als ze paketten vooraf willen installeren die aanwezig moeten zijn voor het testen van het project.

## Tests uitvoeren
Als er een `run_tests.sh` aanwezig is in de projectopdrachtbestanden, wordt dit uitgevoerd wanneer de student zijn code indient.
Bij het uitvoeren van tests is het belangrijk op te merken dat de map van de inzending van de student `/submission` zal zijn.
