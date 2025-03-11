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