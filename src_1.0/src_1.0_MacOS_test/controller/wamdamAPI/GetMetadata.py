
from ..ConnectDB_ParseExcel import DB_Setup
from ..ConnectDB_ParseExcel import SqlAlchemy as sq


'''
This class is used to get data making sheets for meta data.
'''
class GetMetadata(object):
    def __init__(self):
        self.setup = DB_Setup()
        self.session = self.setup.get_session()
    def GetOrganizations(self):
        '''
        This method is used to get data making Organizations_table.
        :return: list of row (queried)
        '''
        result = self.session.query(sq.Organizations.OrganizationName, sq.Organizations.OrganizationType,
                                    sq.Organizations.OrganizationWebpage, sq.Organizations.Description).all()
        complete_result = list()
        nameResult = list()
        for row in result:
            isExisting = False
            for name in nameResult:
                if name == row.OrganizationName:
                    isExisting = True
                    break
            if not isExisting:
                nameResult.append(row.OrganizationName)
                complete_result.append([row.OrganizationName, row.OrganizationType, row.OrganizationWebpage,
                                        row.Description])
        return complete_result
    def GetPeople(self):
        '''
        This method is used to get data making People_table.
        :return: list of row (queried)
        '''
        result = self.session.query(sq.People.PersonName, sq.People.Address, sq.People.Email,
                                    sq.People.Phone, sq.People.PersonWebpage,sq.People.Position,
                                    sq.Organizations.OrganizationName).\
                    join(sq.Organizations,
                         sq.Organizations.OrganizationID == sq.People.OrganizationID).all()
        complete_result = list()
        nameResult = list()
        for row in result:
            isExisting = False
            for name in nameResult:
                if name == row.PersonName:
                    isExisting = True
                    break
            if not isExisting:
                nameResult.append(row.PersonName)
                complete_result.append([row.PersonName, row.Address, row.Email, row.Phone,
                                        row.PersonWebpage, row.Position, row.OrganizationName])
        return complete_result
    def GetSources(self):
        '''
        This method is used to get data making Sources_table.
        :return: list of row (queried)
        '''
        result = self.session.query(sq.Sources.SourceName, sq.Sources.SourceWebpage, sq.Sources.SourceCitation,
                                    sq.People.PersonName, sq.Sources.Description).\
                    join(sq.People,
                         sq.People.PersonID == sq.Sources.PersonID).all()
        complete_result = list()
        nameResult = list()
        ''' duplicate row check'''
        for row in result:
            isExisting = False
            for name in nameResult:
                if name == row.SourceName:
                    isExisting = True
                    break
            if not isExisting:
                nameResult.append(row.SourceName)
                complete_result.append([row.SourceName, row.SourceWebpage, row.SourceCitation,
                                        row.PersonName, row.Description])
        return complete_result
    def GetMethods(self):
        '''
        This method is used to get data making Methods_table.
        :return: list of row (queried)
        '''
        result = self.session.query(sq.Methods.MethodName, sq.Methods.MethodWebpage, sq.Methods.MethodCitation,
                                    sq.Methods.MethodTypeCV, sq.People.PersonName, sq.Methods.Description).\
                    join(sq.People,
                         sq.People.PersonID == sq.Methods.PersonID).all()
        complete_result = list()
        nameResult = list()
        ''' duplicate row check'''
        for row in result:
            isExisting = False
            for name in nameResult:
                if name == row.MethodName:
                    isExisting = True
                    break
            if not isExisting:
                nameResult.append(row.MethodName)
                complete_result.append([row.MethodName, row.MethodWebpage, row.MethodCitation,
                                        row.MethodTypeCV, row.PersonName, row.Description])
        return complete_result