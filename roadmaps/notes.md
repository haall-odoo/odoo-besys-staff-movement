# Staff Movements
A Module to track the on/offboarding and the change of positions instead of shitty sheet.
The purpose sof this module is to:
1. Keep data internally
2. Better track changes on record
3. Avoid use of shared sheet with complicated comments to communicate
4. Improve the users and access management
5. Improve communications between HR and SysAdmin
6. Reduce error by giving warning on weird action
7. 

Each record should propose:
- Guidance step by step to create / archive / change positions
- Chatter / Logger
- Log of each change
- Remark (based on description field) field for each
- List views for the different records
 - Group by entries/departures/change



## To change before prod
- For now base.group_user has all perm, need to manage these permissions more efficiently
- Link employee on not arrivals
- If hired, check if employee is not yet active
- Button departure → archive / reassign
- Smart button logs
  - WHEN / WHAT / WHO / OLD_DATA / NEW_DATA
- Access rights - (Think about onboarder BE)
- Add Chatter on every record
- Filter instead of tabs - except for review
  - No tab for movements (excpet main tab)
    - Filters for arrivals, departures and change of positions
  - Tab for review 
- Colors code
    - Red record if today or past
    - Green week before arrival
    - Gray either

data/ir.model.access → security/ir.model.access

## Workflow
### Hiring
- Quand recruitment stage == proposal → create employee archived + tag (or use state field in hr_employee)
- Ca créer une ligne dans hr.employee/Staff movements (record staff_movement)
- Run passwodoo to create user and others things


## Actual workflow



## Hiring in Odoo with staff.movement
1. When an employee record is created, it create the associate *staff.movement* record in *entry* mode
2. This record is available for sysadmin to determine action to take (use passwodoo to create the employee, give AR, etc)
3. These *staff.movement* records are available from two ways:
 - From each employee there is a smart button to redirect to the list view containing the staff movement related to them. (possibility to transform it in notebook page)
 - From the Empoyee app, there is a menu button allowing to view the whole staff movement
