VALIDATIONS
===========

Most of the validations carried out so far is on the existence of foreign keys 
in its appropriate database tabke to as to retrieve them.

The validation is done using the python try-except clause where on failure and
Exception is raised to show the appropriate Error.



VALIDATION EXAMPLE
==================

try:
        method.MethodTypeID = self.__session.query(sq.MethodType).filter(
            sq.MethodType.MethodTypeCV == row[3].value
        ).first().MethodTypeCVID
except Exception as e:
    print e
    raise Exception('Error with sheet {}, could not find {} in MethodType Table'
                    .format(metadata_sheets_ordered[3], row[3].value))




OTHER VALIDATIONS
=================

- Testing if selected file are excel files else a message is sent to user
- Testing if selected excel file is valid (contains required sheets)
- Requesting confirmation from user upon exiting of the wizard



Validation TODO
===============

Next steps of the validation will require 
1) test for the availablity of non-Nullable fields
2) test for Uniqueness of unique fields.
3) try to handle sql integrity errors



Validate that the selected “existing SQLite file” conforms to WaMDaM structure and schema version'''
