# Meeting avec BREM

## Change of position

- Bouton ok mais double action → automate employee
- Link vers ancien employé dans les move
 - Rehire = new employee (systeme de paie broken)

## Departures
- Fonctionalité double action kept
- Après pour eviter double action / oubli on ouvre un second wizard staff.movement après le wizard 'end of collaboration' (custo)
    - Le module ne doit pas en dépendre car relay on custo


# Hiring / Rehiring
Quand on envoit un contrat et que la personne signe, ca créer la fiche employé en archivé, payroll contre signe et la fiche se désarchive
- Problème si on créer uns taff movement quand on créer la ficher 
  - Comment différencier un hiring d'un change of company
  - Comment différencier un hiring d'un rehiring avec une nouvelle fiche
- Solution: double action RH créer le staff movment manuellement 
Mais ok pour double action vu que les infos sont reprises de la fiche employée et plus copié collées