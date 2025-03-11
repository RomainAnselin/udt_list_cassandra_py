from datetime import datetime
import pytz
from cassandra.cqlengine import columns, connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine.management import sync_table

### Connection and Settings for cluster connectivity and keyspace to leverage
tz = pytz.timezone('Europe/Paris')
ks = 'romaindc1'
ip = '10.166.64.182'

### Create UDT
class omhistory(UserType):
    approver = columns.Text(required=True)
    approval_status = columns.Text(required=True)
    approval_handled_at = columns.DateTime(required=True)
    approval_note = columns.Text()

class omhistories(Model):
    __keyspace__ = ks
    id = columns.Integer(primary_key=True)
    om_approval = columns.Text()
    om_history = columns.List(columns.UserDefinedType(omhistory))

### Create table with UDT defined above as object
###sync_type() - unnecessary as done as part of the sync table
### https://docs.datastax.com/en/developer/python-driver/3.29/object_mapper/index.html#getting-started
connection.setup([ip], ks)
sync_table(omhistories)

### Build the variables to insert in the objects
def build_history(value, status, note):
    current_time = datetime.now()
    approver, status, current_time, note = f'approver{i+1}@example.com', status, current_time, note
    return approver, status, current_time, note

for i in range(6,12):
    try:
        ### Create records with Object Mapper
        approver, status, current_time, note = build_history(i, 'pending', 'Initial review pending')
        print(f'Creating entry {i}')
        omhistories.create(id=i, om_approval=f'approval v{i}', om_history=[omhistory(approver=approver, approval_status=status, approval_handled_at=current_time, approval_note=note)])
        ### Update parts of the records
        if i >= 9:
            approver, status, current_time, note = build_history(i, 'completed', 'Review completed')
            # append items to a list
            # https://docs.datastax.com/en/developer/python-driver/3.29/api/cassandra/cqlengine/query/index.html
            # e.g.: Row.objects(row_id=5).update(list_column__append=[6, 7])
            print(f'Updating entry {i}')
            omhistories.objects(id=i).update(om_history__append=[omhistory(approver=approver, approval_status=status, approval_handled_at=current_time, approval_note=note)])
    except Exception as e:
        print(f"Error: {e}")
