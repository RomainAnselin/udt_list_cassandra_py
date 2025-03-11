from cassandra.cluster import Cluster
from datetime import datetime
import pytz

# Configure timezone
tz = pytz.timezone('Europe/Paris')

# Connect to Cassandra cluster and set keyspace
ks = 'romaindc1'
hosts = '10.166.64.182'
cluster = Cluster([hosts])
session = cluster.connect()
session.set_keyspace(ks)

# Create UDT (User Defined Type) for history entries
session.execute("""CREATE TYPE IF NOT EXISTS romaindc1.history (
 approver text,
 approval_status text,
 approval_handled_at timestamp,
 approval_note text ); """)

# Create table with a list of history UDTs
session.execute("CREATE TABLE IF NOT EXISTS romaindc1.approvalhistories (id int PRIMARY KEY, approvalversion text, histories list<frozen<history>>);")

# Define Python class to represent the history UDT
class History(object):
    def __init__(self, approver, approval_status, approval_handled_at, approval_note):
        self.approver = approver
        self.approval_status = approval_status
        self.approval_handled_at = approval_handled_at
        self.approval_note = approval_note

# Register the UDT with the Cassandra driver
cluster.register_user_type('romaindc1', 'history', History)

# Prepare statements for database operations
insert_statement = session.prepare(f"INSERT INTO {ks}.approvalhistories (id, approvalversion, histories) VALUES (?, ?, ?);")
update_statement = session.prepare(f"UPDATE {ks}.approvalhistories SET histories = histories + ? WHERE id = ?;")
select_statement = session.prepare(f"SELECT id, approvalversion, histories FROM {ks}.approvalhistories WHERE id = ?;")

# Insert initial record with timestamp in milliseconds
current_time = round(datetime.now().timestamp() * 1000)
session.execute(insert_statement, [0, 'v1', [('romain', 'pending', current_time, 'Initial review pending')]])

# Function to build a history entry tuple
def build_history(value, status, note):
    current_time = round(datetime.now().timestamp() * 1000)
    history_item = (f'approver{value+1}@example.com', status, current_time, note)
    return history_item

# Create multiple records with IDs 1-6
for i in range(1, 7):
    try:
        # Create initial history entry with 'pending' status
        status = 'pending'
        history_item = build_history(i, status, 'Initial review pending')
        # Insert new record with the history entry
        insert_bind = insert_statement.bind((i, 'approval'+str(i), [history_item]))
        session.execute(insert_bind)
    except  Exception as e:
        print(f"Error inserting record {i}: {e}")

    # Update the second half of the records and add to the existing list
    if i >= 4:
        try:
            # Update the record by appending a new history entry with 'completed' status
            status = 'completed'
            history_updated_item = build_history(i, status, 'Review completed')
            update_bind = update_statement.bind(([history_updated_item], i))
            session.execute(update_bind)
        except Exception as e:
            print(f"Error updating record {i}: {e}")