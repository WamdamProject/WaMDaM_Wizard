Importing network’s spreadsheet data into WaMDaM SQLite is a complex task
in the Wizard which involve looking up and mapping foreign keys.
This document describes the logic of importing the data and explains
what the business rules are. The center of this data loading step
that maps tables together in WaMDaM is a table called “Mapping”.

This table is invisible to users. The Mapping table is populated
when users load networks, scenarios, then node and link “instances”
and relate them with Attributes, a source, and a method. In this step,

The user can define a new network which comprise node and links instances
but without populating data values for the attributes of instances.
This leaves the red tables in the ER diagram empty for now.



**Loading node Instances**
1.	Populate the Instances Table from the provided data in the Nodes spreadsheet
2.	Get the InstanceID, the SourceID, MethodID, AttributeID (through the provided ObjectName and the default dummy attribute for that Object which is called “ObjectTypeDummyAttribute”, and get the next available DataValueMapperID and populate all of them for one node instance into the Mapping Table.
3.	Get the MappingID from point (2) and the provided ScenarioID and create an entry in the ScenarioMapping table


After finishing point (3), a node instance would be connected to its objectType,
and network. Use a for-loop over each provided node entry in the spreadsheet
table to all of them.

# Revise this one
Implement this check: if the same node, with the same: source, method, Attribute
which is called “ObjectTypeDummyAttribute”,Type are provided again but with only
a different scenario name that is provided, then the Wizard will look up if the
these combinations exist in the Mapping Table. If so, then the Wizard only populates
the ScenarioMapping Table with the same MappingID but different scenarioID.

This concept is very important in WaMDaM which allows the reuse of data across scenarios.
It also allows users later to quickly query and compare if there is a difference
between two scenarios.



**Loading link instances**
Follow the same loading steps and checks for the node instances above. However, the
link spreadsheet contains additional data about the start and end nodes of each link.
These extra data will be populated in the Connections Table in a following step. The
start and end nodes are just foreign keys of other “node” instances while the LinkID is a
foreign key to the Link InstanceID. The Instances Table in WaMDaM works as a super
 class that shares the common metadata between nodes and links and the Connections
Table stores the special extra metadata for “link” instances. Later we will implement a
validation check that a link instance must have two different start and end node
instances. In other words, a link cannot exist without both a start and end nodes.


Revise this one
**Loading global attributes**
Besides the attributes for each ObjectType, there are attributes for the entire Dataset
that apply to the entire scenario. Example global attributes are like budget constraints or
objective function values for the whole scenario.


The global attributes are populated similar to the regular attributes except that they are
associated with the dummy ObjecType defined earlier called
“ScenarioDummyObjectType”. Users won’t see the ScenarioDummyObjectType.
Instead they will provide the Dataset name and the Wizard will look up the ID of the
ScenarioDummyObjectType based on the provided dataset name. In the Mapping
Table, you can use the ScenarioDummyInstance for all the global attributes.


**Validation**
The AttributeTypeCodeCV as defined for each Attribute will specify the data type for
each attribute which will be implemented to all instance of the same Object Type.
The Wizard needs to implement a software business rule that allows users to only
populate one of the eight data types as chosen in the Attribute table.
