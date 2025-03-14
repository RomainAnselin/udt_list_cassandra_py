# Object Mapping, UDT and list in python
The code shared here demonstrate how to leverage UDT in list in Cassandra.
The scenario involves
- creation of table containing a list of UDTs
- update/append of the UDT object in database

The repository contains 2 sample codes
- `udt_cql.py` shows how to do this using CQL
- `udt_objectmapper.py ` demonstrates the same operation done using the python Object Mapper

The documentation is available here
URL: https://docs.datastax.com/en/developer/python-driver/3.29/object_mapper/index.html

These scripts were tested on the following configuration
- python 3.11.2
- cassandra-driver 3.29.2
- DSE 6.8.50

## Sample output

### CQL code sample
```cqlsh> select * from romaindc1.approvalhistories;

@ Row 1
-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 id              | 5
 approvalversion | approval5
 histories       | [{approver: 'approver6@example.com', approval_status: 'pending', approval_handled_at: '2025-03-10 17:15:29.334000+0000', approval_note: 'Initial review pending'}, {approver: 'approver6@example.com', approval_status: 'completed', approval_handled_at: '2025-03-10 17:15:29.540000+0000', approval_note: 'Review completed'}]

@ Row 2
-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 id              | 1
 approvalversion | approval1
 histories       | [{approver: 'approver2@example.com', approval_status: 'pending', approval_handled_at: '2025-03-10 15:41:44.365000+0000', approval_note: 'Initial review pending'}]
```


### Object Mapper sample
```cqlsh> select * from romaindc1.omhistories ;


@ Row 1
-------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 id          | 10
 om_approval | approval v10
 om_history  | [{approver: 'approver11@example.com', approval_status: 'pending', approval_handled_at: '2025-03-11 13:20:23.866000+0000', approval_note: 'Initial review pending'}, {approver: 'approver11@example.com', approval_status: 'completed', approval_handled_at: '2025-03-11 13:20:24.278000+0000', approval_note: 'Review completed'}]

@ Row 3
-------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 id          | 8
 om_approval | approval v8
 om_history  | [{approver: 'approver9@example.com', approval_status: 'pending', approval_handled_at: '2025-03-11 13:20:22.538000+0000', approval_note: 'Initial review pending'}]
```
