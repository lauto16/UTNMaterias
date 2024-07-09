class Subject():
    """
    This class represents a Node of the Subjects tree.
    Note: At UTN FRC (Universidad Tecnologica Nacional, Facultad Regional Cordoba), there's plenty states that a student can obtain
    by studying any subject, but we only need 2 of them to build this app -> Regular and Approved

    Regular: The student has passed all of his exams but he still need's to pass the final exam.
    Approved: The student has passed all of his exams, including the final exam.

    Each subject established when a student is capable of registering, it can be either by being "regular" or "approved" on any
    other previous subject

    Attributes:
        self.sql_id: int -> Represents the sql database id
        self.name: str -> The subject's name
        self.is_approved: bool -> True if the user completely finished the subject
        self.is_regular: bool -> True if the user is regular at the subject
        self.is_enrollable: bool -> True if the user can register for the subject
        self.children = {'approved': [],'regular': []}: dict{list} -> Contains two lists:
            (approved) represents the children(Subject) whose connection to the father(current Subject) is the need to be approved
            (regular) represents the children(Subject) whose connection to the father(current Subject) is the need to be regular
    """

    def __init__(self, sql_id: int, name: str, is_approved: bool, is_regular: bool, is_enrollable: bool) -> None:
        self.sql_id = sql_id
        self.name = name
        self.is_approved = is_approved
        self.is_regular = is_regular
        self.is_enrollable = is_enrollable
        self.children = {
            'approved': [],
            'regular': []
        }

    def __str__(self) -> str:
        regular_children = [
            regular.name for regular in self.children['regular']]
        approved_children = [
            approved.name for approved in self.children['approved']]

        r = str(
            f'ID: {self.sql_id}\n' +
            f'NAME: {self.name}\n' +
            f'REGULAR_CHILDREN: {regular_children}\n' +
            f'APPROVED_CHILDREN: {approved_children}\n' +
            f'IS_APPROVED: {self.is_approved}\n' +
            f'IS_REGULAR: {self.is_regular}\n' +
            f'IS_ENROLLABLE: {self.is_enrollable}\n'
        )
        return r

    def newChild(self, subject, subject_conection: str) -> None:
        """
        Adds a new Subject child to the current Subject

        Args:
            subject (Subject): Subject object
            subject_conection (str): 'approved' or 'regular'
        """

        if subject_conection == 'approved':
            self.children['approved'].append(subject)
        elif subject_conection == 'regular':
            self.children['regular'].append(subject)


class Tree():
    """
    A Tree that containt Subject objects as nodes and 'approved' or 'regular' as connectors

    Attributes:
        self.root: Subject -> Represents the 'Ingreso' Subject, which is the father of all nodes.
    """

    def __init__(self) -> None:
        self.root = Subject(sql_id=1, name='Ingreso',
                            is_approved=False, is_regular=False, is_enrollable=True)

    def searchByConnection(self, father, sql_id: int, subject_connection: str):
        """
        Searches a subject on the Tree by passing: father, id and subject_connection with the father

        Args:
            sql_id (int): Represents the sql database id 
            subject_connection (str): 'approved', 'regular' or 'any', for more info read the class documentation

        Returns:
            Subject: if the subject has been found
            None: if the subject doesn't exist
        """

        if subject_connection == 'approved':
            return self._recursiveApprovedSearch(sql_id, father)
        elif subject_connection == 'regular':
            return self._recursiveRegularSearch(sql_id, father)
        elif subject_connection == 'any':
            approved_found = self._recursiveApprovedSearch(sql_id, father)
            if approved_found:
                return approved_found
            return self._recursiveRegularSearch(sql_id, father)

    def _recursiveApprovedSearch(self, sql_id: int, actualSubject: Subject):
        """
        Recursively searches for a subject whose connection to the current subject (father) is 'approved'.
        Starting from a given father Subject

        Args:
            sql_id (int): Represents the sql database id
            actualSubject (Subject): The subject object where the search is to start

        Returns:
            Subject: if the subject has been found
            None: if the subject doesn't exist as a children
        """
        if actualSubject.sql_id == sql_id:
            return actualSubject

        for child in actualSubject.children['approved']:
            found = self._recursiveApprovedSearch(sql_id, child)
            if found:
                return found

        return None

    def _recursiveRegularSearch(self, sql_id: int, actualSubject: Subject):
        """
        Recursively searches for a subject whose connection to the current subject (father) is 'regular'.
        Starting from a given father Subject

        Args:
            sql_id (int): Represents the sql database id
            actualSubject (Subject): The subject object where the search is to start

        Returns:
            Subject: if the subject has been found
            None: if the subject doesn't exist as a children
        """
        if actualSubject.sql_id == sql_id:
            return actualSubject

        for child in actualSubject.children['regular']:
            found = self._recursiveRegularSearch(sql_id, child)
            if found:
                return found

        return None

    def add(self, father_sql_id: int, child_subject: Subject, subject_conection: str) -> None:
        """
        Adds a new child subject to a given father subject

        Args:
            father_sql_id (int): Father's sql id
            child_subject (Subject): Child to add
            subject_conection (str): Connection between father and child, must be 'approved' or 'regular'
        """
        father_subject_approved = self.searchByConnection(
            self.root, father_sql_id, 'approved')
        father_subject_regular = self.searchByConnection(
            self.root, father_sql_id, 'regular')

        if father_subject_approved:
            father_subject_approved.newChild(child_subject, subject_conection)
        elif father_subject_regular:
            father_subject_regular.newChild(child_subject, subject_conection)
        else:
            print('Father doesnt exist')


t = Tree()

tree_subjects = [
    Subject(2, 'led', False, False, False),
    Subject(3, 'ami', False, False, False),
    Subject(4, 'fis', False, False, False),
    Subject(5, 'aga', False, False, False),
    Subject(6, 'spn', False, False, False),
    Subject(7, 'ing', False, False, False),
    Subject(8, 'aed', False, False, False),
    Subject(9, 'aco', False, False, False),
    Subject(10, 'iso', False, False, False)
]


for subject in tree_subjects:
    t.add(1, subject, 'approved')

t.add(10, Subject(11, 'legislacion', False, False, False), 'regular')

print(t.searchByConnection(t.root, 10, 'approved'))
